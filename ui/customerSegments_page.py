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
        rfm        = pd.read_csv("data/processed/rfm_features.csv")
        rfm_scaled = pd.read_csv("data/processed/rfm_scaled.csv")
        return rfm, rfm_scaled

    @st.cache_resource
    def load_model():
        return joblib.load("models/kmeans_model.pkl")

    rfm, rfm_scaled = load_data()
    kmeans = load_model()

    X = rfm_scaled[['Recency','Frequency','Monetary','AvgOrderValue','TotalItems']]
    rfm['Cluster'] = kmeans.predict(X)
    rfm['Segment'] = rfm['Cluster'].map({0: 'Inactive', 1: 'Active'})

    active   = rfm[rfm['Segment'] == 'Active']
    inactive = rfm[rfm['Segment'] == 'Inactive']
    total    = len(rfm)

    st.title("Customer Segments")
    st.caption("Your customers grouped by how they shop.")
    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Customers",    f"{total:,}")
    c2.metric("Active Customers",   f"{len(active):,}")
    c3.metric("Inactive Customers", f"{len(inactive):,}")
    style_metric_cards(background_color="#1a1d27", border_color="#2a2d3a", border_left_color="#4a9eff")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Customer Split")
        counts = rfm['Segment'].value_counts().reset_index()
        counts.columns = ['Segment', 'Customers']
        fig = px.pie(counts, names='Segment', values='Customers',
                     hole=0.5, color='Segment',
                     color_discrete_map={'Active':'#4a9eff','Inactive':'#f5a623'})
        fig.update_traces(textinfo='percent+label', textfont_size=14)
        fig.update_layout(showlegend=False, margin=dict(t=0, b=0))
        st.plotly_chart(fig, width='stretch')

    with col2:
        st.subheader("What Each Group Looks Like")
        st.markdown(f"""
        <div style='background:#1a1d27;padding:16px;border-radius:10px;border-left:4px solid #4a9eff;margin-bottom:12px;'>
            <b style='color:#4a9eff;'>🟢 Active — {len(active):,} customers</b><br>
            <span style='color:#ccc;'>Last bought <b>{int(active['Recency'].mean())} days ago</b> · {round(active['Frequency'].mean(),1)} orders · £{active['Monetary'].mean():,.0f} spent</span><br>
            <span style='color:#8b8fa8;font-size:13px;'>Your most valuable customers. Buy regularly and spend more.</span>
        </div>
        <div style='background:#1a1d27;padding:16px;border-radius:10px;border-left:4px solid #f5a623;'>
            <b style='color:#f5a623;'>🟠 Inactive — {len(inactive):,} customers</b><br>
            <span style='color:#ccc;'>Last bought <b>{int(inactive['Recency'].mean())} days ago</b> · {round(inactive['Frequency'].mean(),1)} orders · £{inactive['Monetary'].mean():,.0f} spent</span><br>
            <span style='color:#8b8fa8;font-size:13px;'>Have not purchased recently. May need a nudge to come back.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("Look Up a Customer")
    st.caption("Select a Customer ID to see which segment they belong to.")

    customer_ids = sorted(rfm['Customer ID'].astype(int).unique().tolist())
    selected_id  = st.selectbox("Select Customer ID", customer_ids)

    if selected_id:
        row     = rfm[rfm['Customer ID'] == selected_id].iloc[0]
        segment = row['Segment']
        emoji   = "🟢" if segment == "Active" else "🟠"

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Segment",             f"{emoji} {segment}")
        c2.metric("Days Since Purchase", f"{int(row['Recency'])} days")
        c3.metric("Total Orders",        int(row['Frequency']))
        c4.metric("Total Spend",         f"£{row['Monetary']:,.2f}")

        if segment == 'Active':
            st.success("This customer is active. Keep them engaged with loyalty offers.")
        else:
            st.warning("This customer has gone quiet. Consider reaching out with a special offer.")

    st.markdown("---")

    st.subheader("All Customers")
    st.caption("Browse and filter all customers and their segments.")

    seg_filter = st.selectbox("Filter by Segment", ["All", "Active", "Inactive"])

    display = rfm[['Customer ID','Segment','Recency','Frequency','Monetary']].copy()
    display.columns = ['Customer ID','Segment','Days Since Purchase','Total Orders','Total Spend (£)']
    display['Total Spend (£)'] = display['Total Spend (£)'].round(2)

    if seg_filter != "All":
        display = display[display['Segment'] == seg_filter]

    st.dataframe(display, hide_index=True)