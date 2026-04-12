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
        return pd.read_csv("data/processed/transaction_features.csv", parse_dates=['InvoiceDate'])

    @st.cache_resource
    def load_model():
        return joblib.load("models/anomaly_model.pkl")

    tx    = load_data()
    model = load_model()

    X              = tx[['LogRevenue','LogQuantity','LogPrice']]
    tx['Label']    = model.predict(X)
    tx['Score']    = model.decision_function(X)
    tx['Status']   = tx['Label'].map({1: 'Normal', -1: 'Suspicious'})

    total       = len(tx)
    suspicious  = (tx['Status'] == 'Suspicious').sum()
    normal      = (tx['Status'] == 'Normal').sum()

    st.title("Suspicious Transactions")
    st.caption("Transactions that look unusual based on revenue, quantity and price.")
    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Transactions",   f"{total:,}")
    c2.metric("Suspicious",           f"{suspicious:,}")
    c3.metric("Normal",               f"{normal:,}")
    style_metric_cards(background_color="#1a1d27", border_color="#2a2d3a", border_left_color="#e74c3c")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Transaction Overview")
        counts = tx['Status'].value_counts().reset_index()
        counts.columns = ['Status', 'Count']
        fig = px.pie(counts, names='Status', values='Count',
                     hole=0.5, color='Status',
                     color_discrete_map={'Suspicious':'#e74c3c','Normal':'#4a9eff'})
        fig.update_traces(textinfo='percent+label', textfont_size=14)
        fig.update_layout(showlegend=False, margin=dict(t=0, b=0))
        st.plotly_chart(fig, width='stretch')

    with col2:
        st.subheader("What This Means")
        st.markdown(f"""
        <div style='background:#1a1d27;padding:16px;border-radius:10px;border-left:4px solid #e74c3c;margin-bottom:12px;'>
            <b style='color:#e74c3c;'>🔴 Suspicious — {suspicious:,} transactions</b><br>
            <span style='color:#ccc;'>These transactions have unusually high revenue, quantity or price compared to the rest.</span><br>
            <span style='color:#8b8fa8;font-size:13px;'>Worth investigating to check for errors or fraud.</span>
        </div>
        <div style='background:#1a1d27;padding:16px;border-radius:10px;border-left:4px solid #4a9eff;'>
            <b style='color:#4a9eff;'>🔵 Normal — {normal:,} transactions</b><br>
            <span style='color:#ccc;'>These transactions follow the expected pattern of purchasing behaviour.</span><br>
            <span style='color:#8b8fa8;font-size:13px;'>No action needed.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Suspicious transactions table
    st.subheader("Suspicious Transactions")
    st.caption("The most unusual transactions — sorted by how suspicious they are.")

    suspicious_tx = tx[tx['Status'] == 'Suspicious'].copy()
    suspicious_tx = suspicious_tx.sort_values('Score')

    display = suspicious_tx[['Invoice','Customer ID','InvoiceDate','Quantity','Price','Revenue']].copy()
    display['InvoiceDate'] = display['InvoiceDate'].dt.strftime('%Y-%m-%d')
    display['Revenue']     = display['Revenue'].round(2)
    display['Price']       = display['Price'].round(2)
    display.columns        = ['Invoice','Customer ID','Date','Quantity','Price (£)','Revenue (£)']

    st.dataframe(display.head(100), hide_index=True)

    st.markdown("---")

    # Revenue comparison chart
    st.subheader("Revenue: Suspicious vs Normal")
    st.caption("Suspicious transactions have significantly higher revenue than normal ones.")

    avg = tx.groupby('Status')['Revenue'].mean().reset_index()
    avg.columns = ['Status', 'Avg Revenue (£)']
    fig2 = px.bar(avg, x='Status', y='Avg Revenue (£)', color='Status',
                  color_discrete_map={'Suspicious':'#e74c3c','Normal':'#4a9eff'})
    fig2.update_layout(yaxis_tickprefix='£', showlegend=False)
    st.plotly_chart(fig2, width='stretch')