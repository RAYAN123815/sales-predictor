import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="📊 Sales & Profit Predictor", layout="wide")

st.title("📊 Sales & Profit Predictor")
st.write("Enter last 6 months data and get prediction for next 6 months with charts.")

# --- Dummy Data ---
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
dummy_revenue = [120000, 115000, 118000, 122000, 125000, 130000]
dummy_profit = [40000, 38000, 39000, 41000, 42000, 45000]

# --- User Inputs ---
st.subheader("Enter Last 6 Months Data")
cols = st.columns(2)
revenue, profit = [], []

for i, m in enumerate(months):
    with cols[0]:
        r = st.number_input(f"{m} Revenue", min_value=0, value=dummy_revenue[i])
        revenue.append(r)
    with cols[1]:
        p = st.number_input(f"{m} Profit", min_value=0, value=dummy_profit[i])
        profit.append(p)

if st.button("Run Prediction"):
    # --- Linear Growth ---
    rev_growth = (revenue[-1] - revenue[0]) / (len(revenue) - 1)
    prof_growth = (profit[-1] - profit[0]) / (len(profit) - 1)

    future_months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    future_revenue = [round(revenue[-1] + (i+1)*rev_growth) for i in range(6)]
    future_profit = [round(profit[-1] + (i+1)*prof_growth) for i in range(6)]

    # --- DataFrames ---
    df_hist = pd.DataFrame({"Month": months, "Revenue": revenue, "Profit": profit})
    df_pred = pd.DataFrame({"Month": future_months, "Revenue": future_revenue, "Profit": future_profit})

    st.subheader("📌 Historical Data")
    st.dataframe(df_hist, use_container_width=True)

    st.subheader("📌 Predicted Data (Next 6 Months)")
    st.dataframe(df_pred, use_container_width=True)

    all_months = months + future_months
    all_revenue = revenue + future_revenue
    all_profit = profit + future_profit

    # --- Charts ---
    st.subheader("📈 Charts")

    col1, col2 = st.columns(2)

    # Line Chart
    with col1:
        fig, ax = plt.subplots()
        ax.plot(all_months, all_revenue, marker="o", label="Revenue", color="#3498db")
        ax.plot(all_months, all_profit, marker="o", label="Profit", color="#2ecc71")
        ax.axvline(x=months[-1], linestyle="--", color="gray", alpha=0.7, label="Prediction Start")
        ax.set_title("Sales & Profit (Line Chart)")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.6)
        st.pyplot(fig)

    # Bar Chart
    with col2:
        fig, ax = plt.subplots()
        ax.bar(all_months, all_revenue, color="#3498db", alpha=0.7, label="Revenue")
        ax.bar(all_months, all_profit, color="#2ecc71", alpha=0.7, label="Profit")
        ax.set_title("Sales & Profit (Bar Chart)")
        ax.legend()
        st.pyplot(fig)

    col3, col4 = st.columns(2)

    # Pie Chart (Revenue Distribution Future)
    with col3:
        fig, ax = plt.subplots()
        ax.pie(future_revenue, labels=future_months, autopct="%1.1f%%", colors=plt.cm.Paired.colors)
        ax.set_title("Future Revenue Share")
        st.pyplot(fig)

    # Doughnut Chart (Profit Distribution Future)
    with col4:
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(
            future_profit, labels=future_months, autopct="%1.1f%%",
            colors=plt.cm.Set3.colors, wedgeprops=dict(width=0.4)
        )
        ax.set_title("Future Profit Share (Doughnut)")
        st.pyplot(fig)
