import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
from streamlit_extras.metric_cards import style_metric_cards

pio.templates.default = "plotly_dark"


def show():
    if not st.session_state.get("authentication_status"):
        st.warning("Please log in to access this page.")
        st.stop()

    @st.cache_data
    def load_data():
        df = pd.read_csv("data/processed/cleaned_data.csv", parse_dates=['InvoiceDate'])
        df_cancelled = pd.read_csv("data/processed/cancelled_data.csv")
        return df, df_cancelled

    df, df_cancelled = load_data()

    df['Month'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    df['Day']   = df['InvoiceDate'].dt.day_name()
    df['Hour']  = df['InvoiceDate'].dt.hour

    total_revenue    = df['Revenue'].sum()
    total_orders     = df['Invoice'].nunique()
    unique_customers = df['Customer ID'].nunique()
    avg_order        = df.groupby('Invoice')['Revenue'].sum().mean()
    avg_lifetime     = df.groupby('Customer ID')['Revenue'].sum().mean()
    total_raw        = len(df) + len(df_cancelled)
    cancel_rate      = round(len(df_cancelled) / total_raw * 100, 1)
    cancel_revenue   = abs(df_cancelled['Quantity'] * df_cancelled['Price']).sum()

    st.title("Dashboard")
    st.caption("Business performance overview — Dec 2009 to Dec 2011")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue",     f"£{total_revenue/1e6:.1f}M",  f"Avg £{avg_order:,.0f} per order")
    c2.metric("Total Orders",      f"{total_orders:,}",            "Unique invoices")
    c3.metric("Unique Customers",  f"{unique_customers:,}",        f"Avg £{avg_lifetime:,.0f} lifetime")
    c4.metric("Cancellation Rate", f"{cancel_rate}%",              f"£{cancel_revenue/1e6:.1f}M lost")
    style_metric_cards(background_color="#1a1d27", border_color="#2a2d3a", border_left_color="#4a9eff")

    st.markdown("---")

    st.subheader("Monthly Revenue")
    monthly = df.groupby('Month')['Revenue'].sum().reset_index()
    fig1 = px.line(monthly, x='Month', y='Revenue',
                   markers=True, color_discrete_sequence=['#4a9eff'])
    fig1.update_layout(xaxis_tickangle=-45, yaxis_tickprefix='£')
    st.plotly_chart(fig1, width='stretch')

    st.markdown("---")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("Top 10 Products by Revenue")
        top_products = df.groupby('Description')['Revenue'].sum().sort_values().tail(10).reset_index()
        fig2 = px.bar(top_products, x='Revenue', y='Description',
                      orientation='h', color_discrete_sequence=['#00c896'])
        fig2.update_layout(xaxis_tickprefix='£')
        st.plotly_chart(fig2, width='stretch')

    with col2:
        st.subheader("Top Countries")
        top_countries = (
            df[df['Country'] != 'United Kingdom']
            .groupby('Country')['Revenue'].sum()
            .sort_values().tail(10).reset_index()
        )
        fig3 = px.bar(top_countries, x='Revenue', y='Country',
                      orientation='h', color_discrete_sequence=['#7b61ff'])
        fig3.update_layout(xaxis_tickprefix='£')
        st.plotly_chart(fig3, width='stretch')

    st.markdown("---")

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Revenue by Day of Week")
        day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        day_rev   = df.groupby('Day')['Revenue'].sum().reindex(day_order).reset_index()
        fig4 = px.bar(day_rev, x='Day', y='Revenue',
                      color_discrete_sequence=['#f5a623'])
        fig4.update_layout(yaxis_tickprefix='£')
        st.plotly_chart(fig4, width='stretch')

    with col4:
        st.subheader("Revenue by Hour of Day")
        hour_rev = df.groupby('Hour')['Revenue'].sum().reset_index()
        fig5 = px.bar(hour_rev, x='Hour', y='Revenue',
                      color_discrete_sequence=['#f5a623'])
        fig5.update_layout(yaxis_tickprefix='£')
        st.plotly_chart(fig5, width='stretch')