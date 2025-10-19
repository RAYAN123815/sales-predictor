import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="📊 Sales & Profit Predictor", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-image: linear-gradient(to bottom, #87CEEB, #A9A9A9); /* Light Gray Background */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h1 style='text-align:center; color:#2c3e50;'>📊 Advanced Sales & Profit Predictor</h1>
    <p style='text-align:center; font-size:18px; color:#FFFFFF;'>
        Enter last 6 months of sales & profit and predict the next 6 months with AI-powered forecasting
    </p>
    """, unsafe_allow_html=True
)
# --- Dummy Data ---
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
dummy_revenue = [120000, 115000, 118000, 122000, 125000, 130000]
dummy_profit = [40000, 38000, 39000, 41000, 42000, 45000]

# --- User Inputs ---
st.subheader("Enter Last 6 Months Data")
st.markdown(
    """
    <div style='background-color:#f0f8ff; padding:10px; border-radius:10px;'>
        <b>💡 Data Entry Guidelines:</b><br>
        • Enter realistic numbers (e.g., in the range of 10,000 – 200,000).<br>
        • Keep the scale consistent across months (avoid sudden jumps like 50,000 → 5,000,000).<br>
        • Use numeric values only — no commas or symbols.<br>
        • The app adjusts for minor input differences but extreme values may reduce prediction accuracy.
    </div>
    """,
    unsafe_allow_html=True
)

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
    try:
        # Convert safely
        revenue = [float(r) for r in revenue]
        profit = [float(p) for p in profit]

        # Linear growth calculation
        rev_growth = (revenue[-1] - revenue[0]) / (len(revenue) - 1)
        prof_growth = (profit[-1] - profit[0]) / (len(profit) - 1)

        # Future values
        future_months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        future_revenue = [round(revenue[-1] + (i + 1) * rev_growth) for i in range(6)]
        future_profit = [round(profit[-1] + (i + 1) * prof_growth) for i in range(6)]

        # Prevent negative values
        future_revenue = [max(0, r) for r in future_revenue]
        future_profit = [max(0, p) for p in future_profit]

        # Data display
        df_hist = pd.DataFrame({"Month": months, "Revenue": revenue, "Profit": profit})
        df_pred = pd.DataFrame({"Month": future_months, "Revenue": future_revenue, "Profit": future_profit})

        st.subheader("📌 Historical Data")
        st.dataframe(df_hist, use_container_width=True)

        st.subheader("📌 Predicted Data (Next 6 Months)")
        st.dataframe(df_pred, use_container_width=True)

        # Combine
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
            plt.close(fig)

        # Bar Chart
        with col2:
            fig, ax = plt.subplots()
            ax.bar(all_months, all_revenue, color="#3498db", alpha=0.7, label="Revenue")
            ax.bar(all_months, all_profit, color="#2ecc71", alpha=0.7, label="Profit")
            ax.set_title("Sales & Profit (Bar Chart)")
            ax.legend()
            st.pyplot(fig)
            plt.close(fig)

        col3, col4 = st.columns(2)

        # Pie Chart (Revenue)
        with col3:
            fig, ax = plt.subplots()
            safe_rev = [max(1, r) for r in future_revenue]  # avoid zero wedge sizes
            ax.pie(safe_rev, labels=future_months, autopct="%1.1f%%", colors=plt.cm.Paired.colors)
            ax.set_title("Future Revenue Share")
            st.pyplot(fig)
            plt.close(fig)

        # Doughnut Chart (Profit)
        with col4:
            if sum(future_profit) == 0:
                st.warning("⚠️ Predicted profits are zero or negative — chart skipped.")
            else:
                fig, ax = plt.subplots()
                safe_prof = [max(1, p) for p in future_profit]
                wedges, texts, autotexts = ax.pie(
                    safe_prof,
                    labels=future_months,
                    autopct="%1.1f%%",
                    colors=plt.cm.Set3.colors,
                    wedgeprops=dict(width=0.4)
                )
                ax.set_title("Future Profit Share (Doughnut)")
                st.pyplot(fig)
                plt.close(fig)

    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")
