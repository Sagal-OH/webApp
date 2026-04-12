# Analytiq

A customer analytics platform that helps retail businesses make smarter decisions through automated customer segmentation, churn prediction and suspicious transaction detection.

---

## Requirements

- Python 3.12
- Conda (recommended)

---

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/Sagal-OH/webApp.git
cd webApp
```

**2. Activate your environment**
```bash
conda activate base
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Download the dataset**

Download the UCI Online Retail II dataset from:
https://archive.ics.uci.edu/dataset/502/online-retail-ii

Place it in: data/raw/online_retail_II.xlsx

**5. Generate the processed data and models**

Run the notebooks in order:
notebooks/01_data_understanding.ipynb
notebooks/02_data_testing.ipynb
notebooks/03_data_cleaning.ipynb
notebooks/04_post_clean_validation.ipynb
notebooks/05_eda.ipynb
notebooks/06_feature_engineering.ipynb
notebooks/07_model_selection.ipynb

**6. Run the app**
```bash
streamlit run app.py
```

> The user database will be created automatically when the app runs for the first time. No manual setup is required.

---

## Features

- **Dashboard** - Real-time overview of revenue, customers and sales trends
- **Customer Segments** - Automatically groups customers by purchasing behaviour
- **Churn Prediction** - Identifies customers at risk of leaving
- **Suspicious Transactions** -  Flags unusual orders for review

---

## Security

All user accounts are password protected with encrypted credentials stored locally.