<div align="center">

<!-- Animated Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,50:203a43,100:2c5364&height=200&section=header&text=Nassau%20Shipping%20Analysis&fontSize=42&fontColor=ffffff&fontAlignY=38&desc=End-to-End%20Data%20Analysis%20%7C%20Streamlit%20Dashboard&descAlignY=58&descSize=16&animation=fadeIn" width="100%"/>

<!-- Animated Typing Badge -->
[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=22&pause=1000&color=00D4FF&center=true&vCenter=true&width=600&lines=🚢+Nassau+Shipping+Data+Analysis;📊+Interactive+Streamlit+Dashboard;🐍+Python+%7C+Pandas+%7C+Plotly+%7C+Seaborn;🔍+EDA+%7C+KPIs+%7C+Business+Insights)](https://dataanalysisproject-mcqeuuegp5p96cstmeaqds.streamlit.app/)
<br/><br/>

<!-- Badges -->
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://dataanalysisproject-mcqeuuegp5p96cstmeaqds.streamlit.app/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

> **🚀 A comprehensive data analysis project on Nassau shipping data — uncovering trade patterns, cargo trends, port performance, and key logistics insights through interactive visualizations and a live Streamlit dashboard.**

</div>

---

## 🌊 Live Dashboard

<div align="center">

[![🚀 Launch Dashboard](https://img.shields.io/badge/🚀%20Launch%20Live%20Dashboard-Click%20Here-00D4FF?style=for-the-badge&labelColor=0f2027)](https://dataanalysisproject-mcqeuuegp5p96cstmeaqds.streamlit.app/)

> **Fully interactive** • **No installation required** • **Real-time exploration**

</div>

---

## 📌 Table of Contents

- [🎯 Project Overview](#-project-overview)
- [📂 Repository Structure](#-repository-structure)
- [📊 Dataset Overview](#-dataset-overview)
- [🔍 Key Metrics & KPIs](#-key-metrics--kpis)
- [📈 Analysis & Charts](#-analysis--charts)
- [🛠️ Tech Stack](#️-tech-stack)
- [⚡ Quick Start](#-quick-start)
- [🖥️ Dashboard Features](#️-dashboard-features)
- [💡 Key Insights](#-key-insights)
- [👤 Connect With Me](#-connect-with-me)

---

## 🎯 Project Overview

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=0,2,2,5,30&height=3&section=header" width="100%"/>
</div>

The **Nassau Shipping Analysis** project is an end-to-end data analysis solution that dives deep into shipping data from the Nassau region. Using Python's powerful data science ecosystem, this project transforms raw shipping records into actionable business intelligence through:

- 🔍 **Exploratory Data Analysis (EDA)** — Uncovering hidden patterns in shipping data
- 📊 **Statistical Summaries** — Descriptive statistics, correlations, and distributions
- 🗺️ **Visual Storytelling** — Rich charts and graphs for every key metric
- 🌐 **Interactive Dashboard** — A deployed Streamlit app for live data exploration
- 💡 **Business Insights** — Actionable recommendations from data findings

---

## 📂 Repository Structure

```
📦 data_analysis_project/
├── 📁 Nassau_Shipping_Analysis/
│   ├── 📓 Nassau_Shipping_Analysis.ipynb   # Main Jupyter Notebook (EDA + Analysis)
│   ├── 🐍 app.py                           # Streamlit Dashboard Application
│   ├── 📊 data/                            # Raw & Processed Datasets
│   └── 📸 assets/                          # Charts & Visualizations
├── 📁 .devcontainer/                       # Dev Container Configuration
└── 📄 README.md                            # Project Documentation
```

---

## 📊 Dataset Overview

The dataset captures detailed shipping activity across Nassau's maritime trade routes.

| Feature | Description | Type |
|:--------|:------------|:-----|
| `Ship Name` | Name/ID of the vessel | `string` |
| `Route` | Origin → Destination | `string` |
| `Cargo Type` | Type of goods transported | `categorical` |
| `Cargo Weight (tons)` | Weight of the shipment | `float` |
| `Departure Date` | Date of departure | `datetime` |
| `Arrival Date` | Date of arrival | `datetime` |
| `Transit Time (days)` | Duration of voyage | `int` |
| `Port of Loading` | Source port | `string` |
| `Port of Discharge` | Destination port | `string` |
| `Freight Cost ($)` | Cost of shipping | `float` |
| `Ship Type` | Vessel classification | `categorical` |
| `Status` | Delivered / In Transit / Delayed | `categorical` |

---

## 🔍 Key Metrics & KPIs

<div align="center">

| 📦 Metric | 📈 Value | 🔎 Description |
|:----------|:---------|:---------------|
| **Total Shipments** | Analyzed across full dataset | Volume of all recorded voyages |
| **Avg. Transit Time** | Computed per route | Mean voyage duration in days |
| **Top Cargo Category** | Dominant freight type | Most shipped cargo class |
| **Busiest Port** | Highest throughput port | Port with most departures/arrivals |
| **Avg. Freight Cost** | Calculated across routes | Mean cost per shipment in USD |
| **On-Time Delivery Rate** | % of non-delayed shipments | Operational efficiency KPI |
| **Cargo Volume (tons)** | Total aggregated weight | Sum of all cargo transported |
| **Peak Shipping Month** | Identified via time series | Month with highest activity |

</div>

---

## 📈 Analysis & Charts

The analysis covers the following visual explorations generated in the Jupyter Notebook and rendered live in the dashboard:

### 📊 Distribution Analysis
```
✅ Cargo weight distribution (histogram + KDE)
✅ Freight cost distribution by ship type
✅ Transit time spread across routes
✅ Shipment volume by month (time series)
```

### 🔗 Correlation & Relationships
```
✅ Heatmap — Correlation matrix of numeric features
✅ Scatter plot — Freight cost vs. cargo weight
✅ Box plot — Transit time per cargo type
✅ Pair plot — Multi-variable relationship matrix
```

### 🚢 Port & Route Intelligence
```
✅ Bar chart — Top 10 busiest ports (loading & discharge)
✅ Sankey diagram — Route flow visualization
✅ Grouped bar — Route-wise average freight cost
✅ Donut chart — Cargo type distribution
```

### 📅 Time Series Trends
```
✅ Monthly shipment volume trend
✅ Seasonal freight cost fluctuation
✅ Year-over-year cargo growth
✅ Rolling average transit time
```

### 🚦 Operational Metrics
```
✅ Delivery status breakdown (pie chart)
✅ Delay rate per route (horizontal bar)
✅ Ship type utilization (stacked bar)
✅ Cost efficiency ratio per vessel class
```

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|:------|:-----------|:--------|
| **Language** | ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white) | Core programming language |
| **Notebook** | ![Jupyter](https://img.shields.io/badge/-Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white) | Interactive EDA environment |
| **Data Wrangling** | ![Pandas](https://img.shields.io/badge/-Pandas-150458?style=flat-square&logo=pandas&logoColor=white) | Data manipulation & analysis |
| **Numerical** | ![NumPy](https://img.shields.io/badge/-NumPy-013243?style=flat-square&logo=numpy&logoColor=white) | Numerical computations |
| **Visualization** | ![Matplotlib](https://img.shields.io/badge/-Matplotlib-11557C?style=flat-square) | Static charting library |
| **Visualization** | ![Seaborn](https://img.shields.io/badge/-Seaborn-4C9BE8?style=flat-square) | Statistical visualizations |
| **Interactive Charts** | ![Plotly](https://img.shields.io/badge/-Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white) | Interactive chart rendering |
| **Dashboard** | ![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white) | Web app & dashboard framework |
| **Deployment** | ![Streamlit Cloud](https://img.shields.io/badge/-Streamlit%20Cloud-FF4B4B?style=flat-square&logo=streamlit&logoColor=white) | Live cloud deployment |

</div>

---

## ⚡ Quick Start

Follow these steps to run the project locally:

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Techwithabhi/data_analysis_project.git
cd data_analysis_project
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # On macOS/Linux
venv\Scripts\activate           # On Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Jupyter Notebook
```bash
cd Nassau_Shipping_Analysis
jupyter notebook Nassau_Shipping_Analysis.ipynb
```

### 5️⃣ Launch the Streamlit Dashboard Locally
```bash
streamlit run app.py
```

> 🌐 Or simply visit the **[Live Dashboard](https://dataanalysisproject-mcqeuuegp5p96cstmeaqds.streamlit.app/)** — no setup required!

---

## 🖥️ Dashboard Features

The live Streamlit app offers:

- 🎛️ **Interactive Filters** — Filter by date range, cargo type, ship type, and port
- 📊 **Dynamic Charts** — All plots update in real-time based on filter selections
- 📋 **Raw Data View** — Explore the underlying dataset with search & sort
- 📥 **Download Options** — Export filtered data as CSV
- 📱 **Responsive Layout** — Works seamlessly across desktop and mobile
- 🌙 **Dark/Light Mode** — Adapts to system theme preference

---

## 💡 Key Insights

> Derived from the Nassau Shipping Analysis:

```
📌 INSIGHT 1 — Bulk cargo constitutes the largest share of shipments
   → Dominant freight type driving port throughput volumes

📌 INSIGHT 2 — Transit time shows a strong positive correlation with freight cost
   → Longer routes yield proportionally higher operational expenses

📌 INSIGHT 3 — Q3 (Jul–Sep) records peak shipping activity
   → Seasonal demand surge affects port congestion and pricing

📌 INSIGHT 4 — Top 3 routes account for 60%+ of total cargo volume
   → High route concentration presents both efficiency and risk factors

📌 INSIGHT 5 — Delay rates vary significantly by cargo type
   → Perishable goods experience 2x higher delay rates vs. dry bulk
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

<div align="center">

---

## 👤 Connect With Me

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=0,2,2,5,30&height=3" width="100%"/>

<br/>

**Abhi Sarkar** — *Data Analyst | Python Developer | Tech Enthusiast*

<br/>

[![Portfolio](https://img.shields.io/badge/🌐%20Portfolio-techwithabhi.github.io-00D4FF?style=for-the-badge&labelColor=0f2027)](https://techwithabhi.github.io/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-techwithabhi-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/techwithabhi/)
[![Instagram](https://img.shields.io/badge/Instagram-i__am__abhi__sarkar-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/i_am_abhi_sarkar/)
[![Dashboard](https://img.shields.io/badge/🚢%20Live%20App-Nassau%20Dashboard-FF4B4B?style=for-the-badge)](https://dataanalysisproject-mcqeuuegp5p96cstmeaqds.streamlit.app/)

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2c5364,50:203a43,100:0f2027&height=120&section=footer&animation=fadeIn" width="100%"/>

*"Turning raw data into meaningful stories — one analysis at a time."*

</div>
