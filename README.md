# SmartExpenseTracker


A simple and interactive expense tracking application built with **Streamlit**, **Pandas**, and **Matplotlib**.  
This tool helps you **add, view, edit, delete, and analyze expenses** with options to download reports in CSV or Excel format.

---

## 🚀 Features
- 📌 **Add Expense** → Quickly log new expenses (date, category, amount, description)  
- 📊 **View Expenses** → View all expenses in a clean, editable table  
- ✏ **Edit/Delete Expenses** → Update or remove any entry easily  
- 📈 **Summary** → Visualize category distribution (Pie Chart) and monthly trends (Bar Chart)  
- 💾 **Download Reports** → Export your data as CSV or Excel  

---

## 🛠️ Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/expense-tracker.git
   cd expense-tracker
````

2. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```

3. Install the required dependencies manually:

   ```bash
   pip install streamlit pandas matplotlib xlsxwriter
   ```

---

## ▶️ Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

This will start a local server and open the app in your browser (default: `http://localhost:8501`).

---

## 📂 Project Structure

```
expense-tracker/
│── app.py            # Main Streamlit app
│── README.md         # Documentation
```

---

## 📊 Tech Stack

* [Streamlit](https://streamlit.io/) – UI framework
* [Pandas](https://pandas.pydata.org/) – Data handling
* [Matplotlib](https://matplotlib.org/) – Data visualization
* [XlsxWriter](https://xlsxwriter.readthedocs.io/) – Excel export

---



```
