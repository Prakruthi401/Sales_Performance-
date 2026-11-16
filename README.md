# Superstore Sales Performance Analysis

A sales-analysis learning project with SQL queries, a Power BI report, and a Streamlit dashboard. The dashboard uses the Excel dataset included in this repository; it is not connected to a business database.

## Run the dashboard

Use Python 3.11 or 3.12. From this repository:

```sh
python -m venv .venv
# Activate .venv for your operating system, then:
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

No API keys or database setup are needed. Filter orders by year, region, category, and customer segment. The charts cover sales, profit, shipping modes, products, discounts, and monthly trends. An empty filter selection shows a message instead of blank charts. Amounts are shown in dollars as in the source dashboard.

## Files

- `app.py`: interactive dashboard.
- `DataSet/Superstore_Orders_Data.xlsx`: input data.
- `Superstore_Sales_Analysis.sql`: SQL Server analysis queries, separate from the Streamlit app.
- `Superstore_Sales_Data_Analysis.pbix`: editable Power BI report; open with Power BI Desktop.
- `Superstore_Sales_Data_Analysis.png`: saved dashboard image.

The SQL and Power BI files are separate analysis artifacts, not services required by the Python dashboard. This repository does not yet include a verified hosted dashboard link. The data and findings are for practice, not forecasts or business advice.
