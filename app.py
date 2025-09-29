import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="SMART EXPENSE TRACKER", layout="wide")

st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background: white;
            font-family: 'Poppins', sans-serif;
        }
        [data-testid="stSidebar"] {
            background: #065f46;
            border-right: 1px solid #e5e7eb;
            font-family: 'Poppins', sans-serif;
        }
        [data-testid="stSidebar"] * {
            color: white !important;
            font-size: 18px !important;
            font-weight: 700 !important;
            font-family: 'Poppins', sans-serif !important;
        }
        .title {
            text-align: center;
            font-size: 42px;
            color: #065f46;
            font-weight: bold;
            margin-bottom: 20px;
        }
        /* 🔥 Make ALL buttons same as sidebar */
        .stButton>button, .stDownloadButton>button, .stFormSubmitButton>button {
            background-color: #065f46 !important;
            color: white !important;
            border-radius: 10px;
            padding: 0.6rem 1.2rem;
            border: none;
            font-weight: bold;
            transition: all 0.2s ease;
        }
        .stButton>button:hover, .stDownloadButton>button:hover, .stFormSubmitButton>button:hover {
            background-color: #047857 !important;
            transform: scale(1.05);
        }
        .dataframe {
            border: 2px solid #10b981;
            border-radius: 10px;
        }
    
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">SMART EXPENSE TRACKER</div>', unsafe_allow_html=True)

if "expenses" not in st.session_state:
    st.session_state["expenses"] = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

st.sidebar.markdown("<h2 style='color:white; font-weight:800; font-size:22px;'>📌 NAVIGATION</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio("", ["Add Expense", "View Expenses", "Edit Expenses", "Summary"])

if menu == "Add Expense":
    with st.form("expense_form", clear_on_submit=True):
        date = st.date_input("📅 Date")
        category = st.selectbox("📂 Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
        amount = st.number_input("💵 Amount", min_value=0, step=1)  
        description = st.text_area("📝 Description")
        submitted = st.form_submit_button("➕ Add Expense")

        if submitted:
            new_expense = pd.DataFrame([[date, category, amount, description]],
                                       columns=["Date", "Category", "Amount", "Description"])
            st.session_state["expenses"] = pd.concat([st.session_state["expenses"], new_expense], ignore_index=True)
            st.success("✅ Expense added successfully!")


elif menu == "View Expenses":
    if st.session_state["expenses"].empty:
        st.warning("⚠ No expenses recorded yet!")
    else:
        st.subheader("📊 All Expenses")
        st.data_editor(st.session_state["expenses"], use_container_width=True, num_rows="dynamic")


        csv = st.session_state["expenses"].to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download as CSV", data=csv, file_name="expenses.csv", mime="text/csv")

        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            st.session_state["expenses"].to_excel(writer, index=False, sheet_name="Expenses")
        excel_data = output.getvalue()

        st.download_button(
            "⬇ Download as Excel",
            data=excel_data,
            file_name="expenses.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

elif menu == "Summary":
    if st.session_state["expenses"].empty:
        st.warning("⚠ No expenses available for summary.")
    else:
        st.subheader("📈 Expense Summary")

        st.session_state["expenses"]["Month"] = pd.to_datetime(
            st.session_state["expenses"]["Date"].astype(str)
        ).dt.to_period("M")

        category_summary = st.session_state["expenses"].groupby("Category")["Amount"].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(category_summary, labels=category_summary.index, autopct="%1.1f%%", startangle=90)
        ax1.axis("equal")
        st.pyplot(fig1)

        monthly_summary = st.session_state["expenses"].groupby("Month")["Amount"].sum()
        fig2, ax2 = plt.subplots()
        monthly_summary.plot(kind="bar", ax=ax2, color="#10b981")
        ax2.set_ylabel("Amount")
        ax2.set_title("Monthly Expense Trend")
        st.pyplot(fig2)

elif menu == "Edit Expenses":
    if st.session_state["expenses"].empty:
        st.warning("⚠ No expenses available to edit.")
    else:
        st.subheader("✏ Edit or Delete Expense")

        selected_index = st.selectbox("Select expense to edit/delete", st.session_state["expenses"].index)
        expense = st.session_state["expenses"].loc[selected_index]

        # Editable fields
        new_date = st.date_input("📅 Date", value=pd.to_datetime(expense["Date"]))
        new_category = st.selectbox(
            "📂 Category",
            ["Food", "Transport", "Shopping", "Bills", "Other"],
            index=["Food", "Transport", "Shopping", "Bills", "Other"].index(expense["Category"])
        )
        new_amount = st.number_input("💵 Amount", value=int(expense["Amount"]), min_value=0, step=1)
        new_description = st.text_area("📝 Description", value=expense["Description"])

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑 Delete Expense", key=f"del{selected_index}"):
                st.session_state["expenses"] = st.session_state["expenses"].drop(selected_index).reset_index(drop=True)
                st.success("✅ Expense deleted successfully!")

        with col2:
            if st.button("💾 Update Expense", key=f"upd{selected_index}"):
                st.session_state["expenses"].at[selected_index, "Date"] = new_date
                st.session_state["expenses"].at[selected_index, "Category"] = new_category
                st.session_state["expenses"].at[selected_index, "Amount"] = new_amount
                st.session_state["expenses"].at[selected_index, "Description"] = new_description
                st.success("✅ Expense updated successfully!")
