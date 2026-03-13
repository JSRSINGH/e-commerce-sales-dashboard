# E-Commerce Sales Analytics Dashboard

## Project Overview
This is an end-to-end Data Analytics project analyzing an E-commerce sales dataset. It covers data preparation, exploratory data analysis, SQL-based metric calculations, and a complete interactive dashboard built with Streamlit. The goal is to provide actionable insights into revenue, product performance, and customer behavior.

## Dataset Description
The dataset used contains E-commerce sales data (2024-2025). It holds information regarding order categories, sales, profit, regions, and customer names.

**Important:** Note that you need to place the dataset (`Ecommerce_Sales_Data_2024_2025.csv`) into the `data/raw/` directory.

## Tools Used
- **Python**: Core programming language.
- **Pandas / NumPy**: Data manipulation and cleaning.
- **Matplotlib / Seaborn**: Static visualizations in notebooks.
- **SQLite**: Local database for SQL analysis.
- **Streamlit**: Interactive dashboard generation.
- **Plotly**: Dynamic charts within Streamlit.

## Project Structure
```
e-commerce-sales-dashboard/
├── data/
│   ├── raw/             
│   │   └── Ecommerce_Sales_Data_2024_2025.csv
│   └── processed/       # Cleaned data and SQLite DB
├── notebooks/           # Jupyter notebooks for EDA
│   ├── 01_data_cleaning.ipynb
│   └── 02_eda.ipynb
├── sql/                 # SQL queries
│   └── queries.sql
├── dashboard/           # Streamlit app
│   └── app.py
├── src/                 # Source code
│   ├── data_prep.py
│   └── sql_analysis.py
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Instructions to Run the Project

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download Data:**
   Place the `.csv` file into `data/raw/`.

3. **Data Preparation:**
   Run the data preparation script to clean the data and extract features.
   ```bash
   python src/data_prep.py
   ```

4. **SQL Analysis:**
   Load the cleaned data into the SQLite database and run sample queries.
   ```bash
   python src/sql_analysis.py
   ```

5. **Run Dashboard:**
   Start the Streamlit dashboard to explore the visual insights interactively.
   ```bash
   streamlit run dashboard/app.py
   ```

## Key Insights
*(To be populated after analysis)*
- Monthly revenue trends show...
- The top-selling product categories are...
- Most sales are concentrated in the region...
- Average customer purchase frequency is...
