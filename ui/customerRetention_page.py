import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import joblib
from streamlit_extras.metric_cards import style_metric_cards

pio.templates.default = "plotly_dark"


def show():
    if not st.session_state.get("authentication_status"):
        st.warning("Please log in to access this page.")
        st.stop()

    @st.cache_data
    def load_data():
        return pd.read_csv("data/processed/rfm_features.csv")

    @st.cache_resource
    def load_model():
        return joblib.load("models/churn_model.pkl")

    rfm   = load_data()
    model = load_model()

    X = rfm[['Frequency','Monetary','AvgOrderValue','TotalItems']]
    rfm['ChurnProbability'] = model.predict_proba(X)[:, 1]
    rfm['ChurnPrediction']  = model.predict(X)
    rfm['Status']           = rfm['ChurnPrediction'].map({1: 'At Risk', 0: 'Likely to Stay'})

    total     = len(rfm)
    at_risk   = (rfm['Status'] == 'At Risk').sum()
    staying   = (rfm['Status'] == 'Likely to Stay').sum()

    st.title("Customer Retention")
    st.caption("Identify customers who are likely to stop purchasing soon.")
    st.markdown("---")

    # Metric cards
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Customers",   f"{total:,}")
    c2.metric("At Risk",           f"{at_risk:,}")
    c3.metric("Likely to Stay",    f"{staying:,}")
    style_metric_cards(background_color="#1a1d27", border_color="#2a2d3a", border_left_color="#e74c3c")

    st.markdown("---")

    # Split chart + explanation
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Retention Overview")
        counts = rfm['Status'].value_counts().reset_index()
        counts.columns = ['Status', 'Customers']
        fig = px.pie(counts, names='Status', values='Customers',
                     hole=0.5, color='Status',
                     color_discrete_map={'At Risk':'#e74c3c','Likely to Stay':'#4a9eff'})
        fig.update_traces(textinfo='percent+label', textfont_size=14)
        fig.update_layout(showlegend=False, margin=dict(t=0, b=0))
        st.plotly_chart(fig, width='stretch')

    with col2:
        st.subheader("What This Means")
        st.markdown(f"""
        <div style='background:#1a1d27;padding:16px;border-radius:10px;border-left:4px solid #e74c3c;margin-bottom:12px;'>
            <b style='color:#e74c3c;'>🔴 At Risk — {at_risk:,} customers</b><br>
            <span style='color:#ccc;'>These customers show signs of leaving. They are buying less frequently and spending less.</span><br>
            <span style='color:#8b8fa8;font-size:13px;'>Consider reaching out with a special offer or discount.</span>
        </div>
        <div style='background:#1a1d27;padding:16px;border-radius:10px;border-left:4px solid #4a9eff;'>
            <b style='color:#4a9eff;'>🔵 Likely to Stay — {staying:,} customers</b><br>
            <span style='color:#ccc;'>These customers are engaged and continue to purchase regularly.</span><br>
            <span style='color:#8b8fa8;font-size:13px;'>Keep them happy with loyalty rewards and good service.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Customer lookup
    st.subheader("Look Up a Customer")
    st.caption("Select a Customer ID to see their churn risk.")

    customer_ids = sorted(rfm['Customer ID'].astype(int).unique().tolist())
    selected_id  = st.selectbox("Select Customer ID", customer_ids)

    if selected_id:
        row    = rfm[rfm['Customer ID'] == selected_id].iloc[0]
        status = row['Status']
        prob   = round(row['ChurnProbability'] * 100, 1)
        color  = "#e74c3c" if status == "At Risk" else "#4a9eff"
        emoji  = "🔴" if status == "At Risk" else "🔵"

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Status",          f"{emoji} {status}")
        c2.metric("Churn Risk",      f"{prob}%")
        c3.metric("Total Orders",    int(row['Frequency']))
        c4.metric("Total Spend",     f"£{row['Monetary']:,.2f}")

        if status == 'At Risk':
            st.error("This customer is at risk of leaving. Act now to retain them.")
        else:
            st.success("This customer is likely to stay. Keep up the good work.")

    st.markdown("---")

    # At risk customers table
    st.subheader("Customers Most at Risk")
    st.caption("Sorted by churn probability — highest risk at the top.")

    display = rfm[['Customer ID','Status','ChurnProbability','Frequency','Monetary']].copy()
    display.columns = ['Customer ID','Status','Churn Risk (%)','Total Orders','Total Spend (£)']
    display['Churn Risk (%)']  = (display['Churn Risk (%)'] * 100).round(1)
    display['Total Spend (£)'] = display['Total Spend (£)'].round(2)
    display = display.sort_values('Churn Risk (%)', ascending=False)

    status_filter = st.selectbox("Filter by Status", ["All", "At Risk", "Likely to Stay"])
    if status_filter != "All":
        display = display[display['Status'] == status_filter]

    st.dataframe(display, hide_index=True)