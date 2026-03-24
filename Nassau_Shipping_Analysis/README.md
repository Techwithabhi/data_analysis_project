# 🍬 Nassau Candy Distributor — Shipping Route Efficiency Analysis

A data analytics project that analyzes factory-to-customer shipping routes to identify performance bottlenecks, delay patterns, and optimization opportunities.

---

## 📌 Project Overview

Nassau Candy Distributor ships confectionery products from **5 factories** to customers across multiple US regions. This project uses historical order and shipment data to answer:

- Which routes are the **fastest and slowest**?
- Which US states have the **most delays**?
- Does **Expedited shipping** actually perform better than Standard?
- Where are the **geographic bottlenecks**?

---

## 🗂️ Project Structure

```
Nassau_Shipping_Analysis/
│
├── data/
│   └── processed/
│       ├── clean_shipping_data.csv
│       ├── route_efficiency_data.csv
│       ├── geographic_bottleneck_analysis.csv
│       ├── ship_mode_performance.csv
│       ├── shipping_delay_patterns.csv
│       ├── logistics_kpi_dataset.csv
│       └── Nassau Candy Distributor.csv       ← raw data
│
├── notebook/
│   ├── 01_data_cleaning_validation.ipynb
│   ├── 02_route_efficiency_analysis.ipynb
│   ├── 03_geographic_bottleneck_analysis.ipynb
│   ├── 04_ship_mode_performance_analysis.ipynb
│   ├── 05_shipping_delay_pattern_analysis.ipynb
│   ├── 06_logistics_kpi_analysis.ipynb
│   └── 07_business_summary_report.ipynb
│
├── streamlit_app/
│   └── app.py                                 ← interactive dashboard
│
├── src/                                       ← helper functions
├── README.md
└── requirements.txt
```

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|------|---------|
| Python | Main programming language |
| Pandas | Data cleaning and analysis |
| NumPy | Numerical calculations |
| Matplotlib | Charts and plots |
| Seaborn | Heatmaps, box plots, visual EDA |
| Jupyter Notebook | Step-by-step analysis workflow |
| Streamlit | Interactive web dashboard |
| Git / GitHub | Version control |

---

## 📊 Dataset

**File:** `Nassau Candy Distributor.csv`

**Key columns:**

| Column | Description |
|--------|-------------|
| Order Date | When the order was placed |
| Ship Date | When it was shipped |
| Ship Mode | Standard or Expedited |
| State / Region | Customer location |
| Division | Chocolate, Sugar, or Other |
| Sales / Cost / Gross Profit | Financial data |

**Engineered Feature:**
> `Shipping Lead Time (days) = Ship Date − Order Date`

---

## 📓 Notebooks Breakdown

| # | Notebook | What it does |
|---|----------|-------------|
| 01 | Data Cleaning | Removes invalid records, fixes dates, standardizes columns |
| 02 | Route Efficiency | Calculates lead times, ranks routes fastest → slowest |
| 03 | Geographic Bottlenecks | Finds delay-heavy US states and regions |
| 04 | Ship Mode Analysis | Compares Standard vs Expedited performance |
| 05 | Delay Patterns | Measures delay rates by route, region, product |
| 06 | Logistics KPIs | Consolidates all key metrics |
| 07 | Business Summary | Final findings and recommendations |

---

## 📈 Key Metrics (KPIs)

- **Shipping Lead Time** — days from order to shipment
- **Average Lead Time** — mean lead time per route
- **Route Volume** — number of orders per route
- **Delay Frequency** — % of shipments exceeding the delay threshold
- **Route Efficiency Score** — normalized score for cross-route comparison

---

## 🏭 Factories

| Factory | Location | Division |
|---------|----------|---------|
| Lot's O' Nuts | Arizona | Chocolate |
| Wicked Choccy's | Georgia | Chocolate |
| Sugar Shack | Minnesota | Sugar + Other |
| Secret Factory | Illinois | Sugar + Other |
| The Other Factory | Tennessee | Sugar + Other |

---

## 🚀 Running the Streamlit Dashboard

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app/app.py
```

The dashboard includes:
- 📍 Route Efficiency Overview
- 🗺️ US Geographic Heatmap
- 🚚 Ship Mode Comparison
- 🔍 Route Drill-Down (state & order level)

---

## 🔑 Key Findings

- Lead time varies significantly across routes — distance alone doesn't explain it
- Certain US states are consistent bottleneck zones with high delay rates
- Expedited shipping is faster on average, but the advantage shrinks in high-congestion corridors
- Sugar Shack → East Coast routes have the longest average lead times
- Delay rates are route-specific, not random — meaning they can be fixed

---

## 📁 Output Files

All cleaned and processed data is saved to `data/processed/`:

```
clean_shipping_data.csv          ← cleaned master dataset
route_efficiency_data.csv        ← route-level metrics
geographic_bottleneck_analysis.csv
ship_mode_performance.csv
shipping_delay_patterns.csv
logistics_kpi_dataset.csv
```

---

## 👤 Author

**Abhishek** — Entry-Level Data Analyst
🔗 [github.com/Techwithabhi](https://github.com/Techwithabhi)

---

## 📄 License

This project is for educational and portfolio purposes.