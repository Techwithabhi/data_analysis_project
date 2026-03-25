import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

# ─────────────────────────────────────────────────────────────
# PATH RESOLUTION
# Expected layout:
#   nassau_shipping_analysis/
#     data/processed/   <- CSVs live here
#     streamlit_app/    <- app.py lives here
# ─────────────────────────────────────────────────────────────
_BASE = os.path.dirname(os.path.abspath(__file__))
_CANDIDATES = [
    os.path.join(_BASE, "..", "data", "processed"),
    os.path.join(_BASE, "..", "data"),
    _BASE,
    os.path.join(_BASE, "data", "processed"),
    os.path.join(_BASE, "data"),
    os.path.join(_BASE, ".."),
]
_DATA_DIR = None
for _c in _CANDIDATES:
    if os.path.isfile(os.path.join(_c, "clean_shipping_data.csv")):
        _DATA_DIR = os.path.realpath(_c)
        break

if _DATA_DIR is None:
    st.error(
        "**Data files not found.**\n\n"
        f"app.py location: `{_BASE}`\n\n"
        "Expected CSVs at `../data/processed/` relative to app.py.\n\n"
        "Files needed: clean_shipping_data.csv, route_efficiency_data.csv, "
        "geographic_bottleneck_analysis.csv, ship_mode_performance.csv, "
        "shipping_delay_patterns.csv, logistics_kpi_dataset.csv"
    )
    st.stop()

def data_path(filename: str) -> str:
    return os.path.join(_DATA_DIR, filename)

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nassau Logistics Dashboard",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CSS — Only static styles, zero dynamic HTML injection
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:      #0c0f1a;
    --surface: #131726;
    --surface2:#1b2035;
    --border:  #252d45;
    --accent:  #3d85ff;
    --text:    #e2e8f5;
    --muted:   #7a86a1;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

[data-testid="stAppViewContainer"] > .main { background: var(--bg) !important; }
[data-testid="block-container"] { padding: 1.5rem 2rem !important; }

[data-testid="metric-container"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1.2rem 1.4rem !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.08em !important;
    color: var(--muted) !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 1.9rem !important;
    color: var(--accent) !important;
}

hr { border-color: var(--border) !important; }

[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

[data-testid="stTabs"] button {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.05em !important;
    color: var(--muted) !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}

[data-testid="stSelectbox"] label,
[data-testid="stMultiSelect"] label,
[data-testid="stSlider"] label,
[data-testid="stDateInput"] label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.68rem !important;
    color: var(--muted) !important;
    text-transform: uppercase !important;
}

h1, h2, h3 { color: var(--text) !important; }
h1 { font-family: 'Space Mono', monospace !important; font-size: 1.4rem !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(19,23,38,0)",
    plot_bgcolor="rgba(19,23,38,0)",
    font=dict(family="DM Sans, sans-serif", color="#e2e8f5", size=12),
    title_font=dict(family="Space Mono, monospace", size=13, color="#e2e8f5"),
    xaxis=dict(gridcolor="#252d45", linecolor="#252d45", tickfont=dict(color="#7a86a1")),
    yaxis=dict(gridcolor="#252d45", linecolor="#252d45", tickfont=dict(color="#7a86a1")),
    margin=dict(l=20, r=20, t=45, b=20),
    hoverlabel=dict(bgcolor="#1b2035", bordercolor="#3d85ff",
                    font=dict(family="DM Sans", color="#e2e8f5")),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#252d45"),
    colorway=["#3d85ff", "#00d4aa", "#ffb547", "#ff5c5c", "#a78bfa", "#38bdf8"],
)

def apply_theme(fig, height=380):
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    return fig

# ─────────────────────────────────────────────────────────────
# SECTION HEADER — 100% native Streamlit, zero unsafe HTML
# ─────────────────────────────────────────────────────────────
def section(title, subtitle=""):
    st.markdown(f"#### {title}")
    if subtitle:
        st.caption(subtitle)
    st.divider()

# ─────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    clean      = pd.read_csv(data_path("clean_shipping_data.csv"),
                             parse_dates=["Order Date", "Ship Date"])
    route      = pd.read_csv(data_path("route_efficiency_data.csv"),
                             parse_dates=["Order Date", "Ship Date"])
    bottleneck = pd.read_csv(data_path("geographic_bottleneck_analysis.csv"))
    ship_mode  = pd.read_csv(data_path("ship_mode_performance.csv"))
    delay      = pd.read_csv(data_path("shipping_delay_patterns.csv"))
    kpi        = pd.read_csv(data_path("logistics_kpi_dataset.csv"),
                             parse_dates=["Order Date", "Ship Date"])
    return clean, route, bottleneck, ship_mode, delay, kpi

clean_data, route_data, bottlenecks, ship_mode_perf, delay_patterns, kpi_data = load_data()

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
st.sidebar.title("Nassau Logistics")
st.sidebar.caption("Shipping Intelligence Platform")

page = st.sidebar.radio(
    "NAVIGATION",
    ["Overview", "Route Efficiency", "Geographic Analysis",
     "Ship Mode Comparison", "Route Drill-Down"],
)

st.sidebar.divider()
st.sidebar.caption("FILTERS")

min_date   = clean_data["Order Date"].min().date()
max_date   = clean_data["Order Date"].max().date()
date_range = st.sidebar.date_input(
    "Date Range", value=(min_date, max_date),
    min_value=min_date, max_value=max_date
)

all_regions = sorted(clean_data["Region"].dropna().unique().tolist())
sel_regions = st.sidebar.multiselect("Region", all_regions, default=all_regions)

all_states = sorted(clean_data["State/Province"].dropna().unique().tolist())
sel_states  = st.sidebar.multiselect("State / Province", all_states,
                                     placeholder="All States")

all_modes  = sorted(clean_data["Ship Mode"].dropna().unique().tolist())
sel_modes  = st.sidebar.multiselect("Ship Mode", all_modes, default=all_modes)

max_lt = int(clean_data["lead_time"].max())
min_lt = int(clean_data["lead_time"].min())
lt_threshold = st.sidebar.slider(
    "Lead-Time Threshold (days)", min_lt, max_lt, (min_lt, max_lt), step=10
)

st.sidebar.divider()
st.sidebar.caption("Nassau Candy Distributor | 2024-2025")

st.sidebar.markdown(
    "<div style='margin-top:4px; padding:12px 14px; background:#131726; border-radius:10px; border:1px solid #252d45;'>"
    "<p style='margin:0 0 10px 0; font-size:0.6rem; letter-spacing:0.12em; color:#3d85ff; text-transform:uppercase; font-family:monospace; border-bottom:1px solid #252d45; padding-bottom:8px;'>Project Info</p>"
    "<p style='margin:0 0 2px 0; font-size:0.58rem; color:#7a86a1; text-transform:uppercase; letter-spacing:0.08em;'>Organization</p>"
    "<p style='margin:0 0 10px 0;'><a href='https://unifiedmentor.com/' target='_blank' style='color:#e2e8f5; font-size:0.8rem; font-weight:600; text-decoration:none;'>Unified Mentor &#8599;</a></p>"
    "<p style='margin:0 0 2px 0; font-size:0.58rem; color:#7a86a1; text-transform:uppercase; letter-spacing:0.08em;'>Instructor</p>"
    "<p style='margin:0 0 10px 0;'><a href='https://saikagne.github.io/' target='_blank' style='color:#e2e8f5; font-size:0.8rem; font-weight:600; text-decoration:none;'>Saiprasad Kagne &#8599;</a></p>"
    "<p style='margin:0 0 2px 0; font-size:0.58rem; color:#7a86a1; text-transform:uppercase; letter-spacing:0.08em;'>Analyst</p>"
    "<p style='margin:0;'><a href='https://techwithabhi.github.io/' target='_blank' style='color:#3d85ff; font-size:0.8rem; font-weight:600; text-decoration:none;'>Abhi Sarkar &#8599;</a></p>"
    "</div>",
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────────────────────
# FILTER LOGIC
# ─────────────────────────────────────────────────────────────
def apply_filters(df):
    d = df.copy()
    if len(date_range) == 2:
        d = d[(d["Order Date"].dt.date >= date_range[0]) &
              (d["Order Date"].dt.date <= date_range[1])]
    if sel_regions:
        d = d[d["Region"].isin(sel_regions)]
    if sel_states:
        d = d[d["State/Province"].isin(sel_states)]
    if sel_modes:
        d = d[d["Ship Mode"].isin(sel_modes)]
    d = d[(d["lead_time"] >= lt_threshold[0]) &
          (d["lead_time"] <= lt_threshold[1])]
    return d

df_clean = apply_filters(clean_data)
df_kpi   = apply_filters(kpi_data)
df_route = apply_filters(route_data)

COLORS = {
    "Standard Class": "#3d85ff",
    "First Class":    "#00d4aa",
    "Second Class":   "#ffb547",
    "Same Day":       "#ff5c5c",
}

# ═══════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════════
if page == "Overview":

    st.title("Overview Dashboard")

    if df_clean.empty:
        st.warning("No data matches current filters.")
        st.stop()

    # KPI row
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Shipments",   f"{len(df_clean):,}")
    c2.metric("Avg Lead Time",     f"{df_clean['lead_time'].mean():.0f} days")
    c3.metric("Active Routes",
              str(df_route["Route"].nunique()) if "Route" in df_route.columns else "N/A")
    delay_rate = (df_kpi["Delayed"].sum() / len(df_kpi) * 100) if len(df_kpi) else 0
    c4.metric("Delay Rate",        f"{delay_rate:.1f}%")
    c5.metric("Total Sales",       f"${df_clean['Sales'].sum():,.0f}")

    st.write("")

    # Row 1
    col1, col2 = st.columns([1.2, 1])

    with col1:
        section("Shipments by Ship Mode",
                "Volume distribution across shipping methods")
        mode_counts = df_clean["Ship Mode"].value_counts().reset_index()
        mode_counts.columns = ["Ship Mode", "Count"]
        fig = px.bar(
            mode_counts, x="Ship Mode", y="Count", color="Ship Mode",
            color_discrete_map=COLORS, text="Count"
        )
        fig.update_traces(texttemplate="%{text:,}", textposition="outside",
                          marker_line_width=0)
        apply_theme(fig, 340)
        fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Shipments")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("Shipments by Division", "Candy product category breakdown")
        div_counts = df_clean["Division"].value_counts().reset_index()
        div_counts.columns = ["Division", "Count"]
        fig2 = px.pie(
            div_counts, names="Division", values="Count",
            color_discrete_sequence=["#3d85ff", "#00d4aa", "#ffb547"],
            hole=0.55
        )
        fig2.update_traces(
            textfont=dict(family="DM Sans", size=12),
            marker=dict(line=dict(color="#0c0f1a", width=2))
        )
        apply_theme(fig2, 340)
        fig2.update_layout(
            legend=dict(orientation="v", x=1.02, y=0.5),
            annotations=[dict(text="Division<br>Split", x=0.5, y=0.5,
                              font=dict(size=11, family="Space Mono",
                                        color="#7a86a1"),
                              showarrow=False)]
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Row 2
    col3, col4 = st.columns([1.5, 1])

    with col3:
        section("Monthly Shipment Volume and Avg Lead Time",
                "Trend over the order date period")
        df_tmp = df_clean.copy()
        df_tmp["YearMonth"] = df_tmp["Order Date"].dt.to_period("M").astype(str)
        monthly = df_tmp.groupby("YearMonth").agg(
            Shipments=("lead_time", "count"),
            Avg_Lead_Time=("lead_time", "mean")
        ).reset_index()

        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        fig3.add_trace(
            go.Bar(x=monthly["YearMonth"], y=monthly["Shipments"],
                   name="Shipments", marker_color="#3d85ff", opacity=0.75),
            secondary_y=False
        )
        fig3.add_trace(
            go.Scatter(x=monthly["YearMonth"], y=monthly["Avg_Lead_Time"],
                       name="Avg Lead Time",
                       line=dict(color="#ffb547", width=2.5),
                       mode="lines+markers", marker=dict(size=5)),
            secondary_y=True
        )
        apply_theme(fig3, 340)
        fig3.update_layout(
            yaxis=dict(title="Shipments", gridcolor="#252d45"),
            yaxis2=dict(title="Avg Lead Time (days)", gridcolor="rgba(0,0,0,0)"),
            xaxis_tickangle=-45,
            legend=dict(orientation="h", y=1.1, x=0),
            hovermode="x unified"
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        section("Shipments by Region")
        reg_counts = df_clean["Region"].value_counts().reset_index()
        reg_counts.columns = ["Region", "Count"]
        fig4 = px.bar(
            reg_counts, y="Region", x="Count", orientation="h",
            color="Count",
            color_continuous_scale=["#1b2035", "#3d85ff"],
            text="Count"
        )
        fig4.update_traces(texttemplate="%{text:,}", textposition="outside",
                           marker_line_width=0)
        apply_theme(fig4, 340)
        fig4.update_layout(showlegend=False, coloraxis_showscale=False,
                           xaxis_title="Shipments", yaxis_title="")
        st.plotly_chart(fig4, use_container_width=True)

    # Delayed vs On-time
    if not df_kpi.empty and "Delayed" in df_kpi.columns:
        st.divider()
        section("Delayed vs On-Time Shipments by Ship Mode")
        delay_mode = (df_kpi.groupby(["Ship Mode", "Delayed"])
                      .size().reset_index(name="Count"))
        delay_mode["Status"] = delay_mode["Delayed"].map(
            {True: "Delayed", False: "On-Time"})
        fig5 = px.bar(
            delay_mode, x="Ship Mode", y="Count", color="Status",
            color_discrete_map={"Delayed": "#ff5c5c", "On-Time": "#00d4aa"},
            barmode="group", text="Count"
        )
        fig5.update_traces(texttemplate="%{text:,}", textposition="outside",
                           marker_line_width=0)
        apply_theme(fig5, 340)
        fig5.update_layout(xaxis_title="", yaxis_title="Shipments",
                           legend_title="Status")
        st.plotly_chart(fig5, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# PAGE 2 — ROUTE EFFICIENCY
# ═══════════════════════════════════════════════════════════════
elif page == "Route Efficiency":

    st.title("Route Efficiency Analysis")

    if df_route.empty or "Route" not in df_route.columns:
        st.warning("No route data matches current filters.")
        st.stop()

    route_agg = df_route.groupby("Route").agg(
        Avg_Lead_Time=("lead_time", "mean"),
        Volume=("lead_time", "count"),
        Total_Sales=("Sales", "sum"),
    ).reset_index()

    if "Delayed" in df_kpi.columns and "Route" in df_kpi.columns:
        delay_agg = df_kpi.groupby("Route").agg(
            Delay_Rate=("Delayed",
                        lambda x: round(x.sum() / len(x) * 100, 1)),
            Avg_Efficiency=("Route_Efficiency_Score", "mean")
        ).reset_index()
        route_agg = route_agg.merge(delay_agg, on="Route", how="left")

    route_agg["Avg_Lead_Time"] = route_agg["Avg_Lead_Time"].round(1)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Routes",      f"{len(route_agg):,}")
    c2.metric("Fastest Route Avg", f"{route_agg['Avg_Lead_Time'].min():.0f} days")
    c3.metric("Slowest Route Avg", f"{route_agg['Avg_Lead_Time'].max():.0f} days")
    c4.metric("Overall Avg",       f"{route_agg['Avg_Lead_Time'].mean():.0f} days")

    st.write("")

    tab1, tab2, tab3 = st.tabs(
        ["Leaderboard", "Fastest Routes", "Slowest Routes"]
    )

    with tab1:
        section("Route Performance Leaderboard",
                "All routes sorted by average lead time")
        leaderboard = route_agg.sort_values("Avg_Lead_Time").reset_index(drop=True)
        leaderboard.index = leaderboard.index + 1
        leaderboard.columns = ["Route", "Avg Lead Time (days)", "Volume",
                                "Total Sales ($)", "Delay Rate (%)",
                                "Avg Efficiency"]

        def color_lead_time(val):
            if val < 1100:   return "color: #00d4aa"
            elif val < 1300: return "color: #ffb547"
            else:            return "color: #ff5c5c"

        styled = leaderboard.style.map(color_lead_time,
                                       subset=["Avg Lead Time (days)"])
        st.dataframe(styled, use_container_width=True, height=500)

    with tab2:
        section("Top 15 Fastest Routes",
                "Routes with the lowest average lead times")
        fastest = route_agg.nsmallest(15, "Avg_Lead_Time")
        fig = px.bar(
            fastest.sort_values("Avg_Lead_Time"),
            y="Route", x="Avg_Lead_Time", orientation="h",
            color="Avg_Lead_Time",
            color_continuous_scale=["#00d4aa", "#3d85ff"],
            text="Avg_Lead_Time",
            hover_data=["Volume"]
        )
        fig.update_traces(texttemplate="%{text:.0f}d",
                          textposition="outside", marker_line_width=0)
        apply_theme(fig, 520)
        fig.update_layout(coloraxis_showscale=False,
                          xaxis_title="Avg Lead Time (days)", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        section("Top 15 Slowest Routes",
                "Routes requiring operational attention")
        slowest = route_agg.nlargest(15, "Avg_Lead_Time")
        fig2 = px.bar(
            slowest.sort_values("Avg_Lead_Time", ascending=False),
            y="Route", x="Avg_Lead_Time", orientation="h",
            color="Avg_Lead_Time",
            color_continuous_scale=["#ffb547", "#ff5c5c"],
            text="Avg_Lead_Time",
            hover_data=["Volume"]
        )
        fig2.update_traces(texttemplate="%{text:.0f}d",
                           textposition="outside", marker_line_width=0)
        apply_theme(fig2, 520)
        fig2.update_layout(coloraxis_showscale=False,
                           xaxis_title="Avg Lead Time (days)", yaxis_title="")
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    section("Volume vs. Lead Time Scatter",
            "Identify high-risk, high-volume routes")
    fig3 = px.scatter(
        route_agg, x="Avg_Lead_Time", y="Volume",
        hover_name="Route",
        size="Volume", size_max=30,
        color="Avg_Lead_Time",
        color_continuous_scale=["#00d4aa", "#3d85ff", "#ff5c5c"],
        labels={"Avg_Lead_Time": "Avg Lead Time (days)",
                "Volume": "Shipment Volume"}
    )
    avg_lt_all = route_agg["Avg_Lead_Time"].mean()
    fig3.add_vline(
        x=avg_lt_all, line_dash="dash", line_color="#ffb547",
        annotation_text=f"Avg: {avg_lt_all:.0f}d",
        annotation_font_color="#ffb547"
    )
    apply_theme(fig3, 420)
    fig3.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# PAGE 3 — GEOGRAPHIC ANALYSIS
# ═══════════════════════════════════════════════════════════════
elif page == "Geographic Analysis":

    st.title("Geographic Shipping Analysis")

    geo_data = bottlenecks.copy()
    if sel_states:
        geo_data = geo_data[geo_data["State/Province"].isin(sel_states)]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("States Analyzed", len(geo_data))
    c2.metric("Highest Risk State",
              geo_data.nlargest(1, "Risk_Score")["State/Province"].values[0]
              if len(geo_data) > 0 else "N/A")
    c3.metric("Peak Avg Lead Time",
              f"{geo_data['Avg_Lead_Time'].max():.0f} days"
              if len(geo_data) > 0 else "N/A")
    c4.metric("Total Shipments", f"{geo_data['Total_Shipments'].sum():,}")

    st.write("")

    tab1, tab2, tab3 = st.tabs(
        ["US Shipping Map", "Bottleneck Analysis", "State Rankings"]
    )

    with tab1:
        section("US Shipping Efficiency Heatmap",
                "Average lead time by state")

        state_agg = df_clean.groupby("State/Province").agg(
            Avg_Lead_Time=("lead_time", "mean"),
            Shipments=("lead_time", "count"),
            Total_Sales=("Sales", "sum")
        ).reset_index()

        state_abbrev = {
            "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ",
            "Arkansas": "AR", "California": "CA", "Colorado": "CO",
            "Connecticut": "CT", "Delaware": "DE", "Florida": "FL",
            "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
            "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
            "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
            "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
            "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
            "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
            "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
            "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
            "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
            "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
            "South Carolina": "SC", "South Dakota": "SD",
            "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
            "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
            "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
            "District of Columbia": "DC",
        }
        state_agg["State_Code"] = state_agg["State/Province"].map(state_abbrev)
        us_data = state_agg.dropna(subset=["State_Code"])

        fig_map = px.choropleth(
            us_data,
            locations="State_Code",
            locationmode="USA-states",
            color="Avg_Lead_Time",
            hover_name="State/Province",
            hover_data={"Shipments": True, "Total_Sales": ":.0f",
                        "State_Code": False},
            color_continuous_scale=["#00d4aa", "#3d85ff", "#ffb547", "#ff5c5c"],
            labels={"Avg_Lead_Time": "Avg Lead Time (days)"},
            scope="usa",
            title="Average Shipping Lead Time by State"
        )
        fig_map.update_layout(
            **PLOTLY_LAYOUT,
            height=480,
            geo=dict(
                bgcolor="rgba(0,0,0,0)", lakecolor="rgba(0,0,0,0)",
                landcolor="#1b2035", showlakes=True,
                showcoastlines=True, coastlinecolor="#252d45"
            ),
            coloraxis_colorbar=dict(
                title="Lead Time<br>(days)",
                tickfont=dict(color="#7a86a1"),
                title_font=dict(color="#7a86a1")
            )
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with tab2:
        section("Regional Bottleneck Visualization",
                "Risk score = shipment volume x avg lead time")

        top_n = st.slider("Show Top N States by Risk", 5, 30, 15)
        top_bottlenecks = geo_data.nlargest(top_n, "Risk_Score")

        c1, c2 = st.columns(2)

        with c1:
            sorted_bt = top_bottlenecks.sort_values("Risk_Score")
            fig_b1 = px.bar(
                sorted_bt,
                y="State/Province", x="Risk_Score", orientation="h",
                color="Risk_Score",
                color_continuous_scale=["#ffb547", "#ff5c5c"],
                text=sorted_bt["Risk_Score"].apply(
                    lambda x: f"{x/1e6:.1f}M"),
                title="Risk Score by State"
            )
            fig_b1.update_traces(textposition="outside",
                                 marker_line_width=0)
            apply_theme(fig_b1, 420)
            fig_b1.update_layout(coloraxis_showscale=False,
                                 xaxis_title="Risk Score", yaxis_title="")
            st.plotly_chart(fig_b1, use_container_width=True)

        with c2:
            fig_b2 = px.scatter(
                top_bottlenecks,
                x="Total_Shipments", y="Avg_Lead_Time",
                size="Risk_Score", size_max=40,
                color="Risk_Score",
                color_continuous_scale=["#ffb547", "#ff5c5c"],
                hover_name="State/Province",
                title="Shipment Volume vs Lead Time",
                labels={"Total_Shipments": "Total Shipments",
                        "Avg_Lead_Time": "Avg Lead Time (days)"}
            )
            apply_theme(fig_b2, 420)
            fig_b2.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig_b2, use_container_width=True)

        st.divider()
        section("State Delay Patterns",
                "Avg lead time by state — delay analysis")
        top_delay = delay_patterns.copy()
        if sel_states:
            top_delay = top_delay[
                top_delay["State/Province"].isin(sel_states)]
        top_delay = top_delay.sort_values(
            "lead_time", ascending=False).head(20)
        fig_d = px.bar(
            top_delay, y="State/Province", x="lead_time",
            orientation="h",
            color="lead_time",
            color_continuous_scale=["#3d85ff", "#ff5c5c"],
            text=top_delay["lead_time"].apply(lambda x: f"{x:.0f}d"),
            title="Top 20 States by Avg Lead Time"
        )
        fig_d.update_traces(textposition="outside", marker_line_width=0)
        apply_theme(fig_d, 520)
        fig_d.update_layout(coloraxis_showscale=False,
                            xaxis_title="Avg Lead Time (days)",
                            yaxis_title="")
        st.plotly_chart(fig_d, use_container_width=True)

    with tab3:
        section("State-Level Performance Rankings", "Full ranking table")
        state_full = df_clean.groupby("State/Province").agg(
            Avg_Lead_Time=("lead_time", "mean"),
            Shipments=("lead_time", "count"),
            Total_Sales=("Sales", "sum"),
            Avg_Profit_Margin=("Profit_Margin", "mean")
        ).round(2).reset_index().sort_values("Avg_Lead_Time")
        state_full["Rank"] = range(1, len(state_full) + 1)
        state_full = state_full[[
            "Rank", "State/Province", "Avg_Lead_Time",
            "Shipments", "Total_Sales", "Avg_Profit_Margin"
        ]]
        state_full.columns = [
            "Rank", "State/Province", "Avg Lead Time (days)",
            "Shipments", "Total Sales ($)", "Avg Profit Margin"
        ]
        st.dataframe(state_full, use_container_width=True, height=500)


# ═══════════════════════════════════════════════════════════════
# PAGE 4 — SHIP MODE COMPARISON
# ═══════════════════════════════════════════════════════════════
elif page == "Ship Mode Comparison":

    st.title("Ship Mode Performance")

    if df_clean.empty:
        st.warning("No data matches current filters.")
        st.stop()

    mode_agg = df_clean.groupby("Ship Mode").agg(
        Avg_Lead_Time=("lead_time", "mean"),
        Total_Shipments=("lead_time", "count"),
        Avg_Sales=("Sales", "mean"),
        Total_Sales=("Sales", "sum"),
        Avg_Profit_Margin=("Profit_Margin", "mean"),
    ).reset_index()

    if "Delayed" in df_kpi.columns:
        delay_mode = (
            df_kpi.groupby("Ship Mode")["Delayed"]
            .agg(lambda x: round(x.sum() / len(x) * 100, 1))
            .reset_index()
        )
        delay_mode.columns = ["Ship Mode", "Delay_Rate"]
        mode_agg = mode_agg.merge(delay_mode, on="Ship Mode", how="left")

    cols = st.columns(len(mode_agg))
    for col, row in zip(cols, mode_agg.itertuples()):
        col.metric(row._1,
                   f"{row.Avg_Lead_Time:.0f}d avg",
                   f"{row.Total_Shipments:,} shipments")

    st.write("")

    c1, c2 = st.columns(2)

    with c1:
        section("Average Lead Time by Ship Mode")
        fig1 = px.bar(
            mode_agg.sort_values("Avg_Lead_Time"),
            x="Ship Mode", y="Avg_Lead_Time",
            color="Ship Mode", color_discrete_map=COLORS,
            text="Avg_Lead_Time",
            title="Avg Lead Time Comparison"
        )
        fig1.update_traces(texttemplate="%{text:.0f}d",
                           textposition="outside", marker_line_width=0)
        apply_theme(fig1, 360)
        fig1.update_layout(showlegend=False, xaxis_title="",
                           yaxis_title="Avg Lead Time (days)")
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        section("Shipment Volume by Ship Mode")
        fig2 = px.pie(
            mode_agg, names="Ship Mode", values="Total_Shipments",
            color="Ship Mode", color_discrete_map=COLORS, hole=0.5,
            title="Volume Distribution"
        )
        fig2.update_traces(
            marker=dict(line=dict(color="#0c0f1a", width=2)))
        apply_theme(fig2, 360)
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        section("Lead Time Distribution by Ship Mode")
        fig3 = px.box(
            df_clean, x="Ship Mode", y="lead_time",
            color="Ship Mode", color_discrete_map=COLORS,
            points=False, title="Lead Time Box Plot"
        )
        apply_theme(fig3, 380)
        fig3.update_layout(showlegend=False, xaxis_title="",
                           yaxis_title="Lead Time (days)")
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        if "Delay_Rate" in mode_agg.columns:
            section("Delay Rate by Ship Mode")
            fig4 = px.bar(
                mode_agg.sort_values("Delay_Rate", ascending=False),
                x="Ship Mode", y="Delay_Rate",
                color="Delay_Rate",
                color_continuous_scale=["#00d4aa", "#ff5c5c"],
                text="Delay_Rate",
                title="% Delayed Shipments"
            )
            fig4.update_traces(texttemplate="%{text:.1f}%",
                               textposition="outside",
                               marker_line_width=0)
            apply_theme(fig4, 380)
            fig4.update_layout(coloraxis_showscale=False,
                               xaxis_title="",
                               yaxis_title="Delay Rate (%)")
            st.plotly_chart(fig4, use_container_width=True)

    st.divider()
    section("Ship Mode Performance Summary Table")
    summary = mode_agg.copy()
    summary["Avg_Lead_Time"]     = summary["Avg_Lead_Time"].round(1)
    summary["Avg_Sales"]         = summary["Avg_Sales"].round(2)
    summary["Total_Sales"]       = summary["Total_Sales"].round(2)
    summary["Avg_Profit_Margin"] = (summary["Avg_Profit_Margin"] * 100).round(1)
    if "Delay_Rate" in summary.columns:
        summary["Delay_Rate"] = summary["Delay_Rate"].round(1)
    summary.columns = [c.replace("_", " ") for c in summary.columns]
    st.dataframe(summary, use_container_width=True)

    st.divider()
    section("Ship Mode Lead Time Trend Over Time")
    df_tmp2 = df_clean.copy()
    df_tmp2["YearMonth"] = (df_tmp2["Order Date"]
                            .dt.to_period("M").astype(str))
    trend = (df_tmp2.groupby(["YearMonth", "Ship Mode"])["lead_time"]
             .mean().reset_index())
    fig5 = px.line(
        trend, x="YearMonth", y="lead_time", color="Ship Mode",
        color_discrete_map=COLORS, markers=True,
        labels={"lead_time": "Avg Lead Time (days)", "YearMonth": "Month"}
    )
    apply_theme(fig5, 380)
    fig5.update_layout(xaxis_tickangle=-45, hovermode="x unified",
                       yaxis_title="Avg Lead Time (days)", xaxis_title="")
    st.plotly_chart(fig5, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# PAGE 5 — ROUTE DRILL-DOWN
# ═══════════════════════════════════════════════════════════════
elif page == "Route Drill-Down":

    st.title("Route Drill-Down")

    if "Route" not in df_kpi.columns or df_kpi.empty:
        st.warning("No data matches current filters.")
        st.stop()

    available_routes = sorted(df_kpi["Route"].dropna().unique())
    selected_route   = st.selectbox("Select Route", available_routes, index=0)

    route_df = df_kpi[df_kpi["Route"] == selected_route].copy()

    if route_df.empty:
        st.warning("No shipments found for this route.")
        st.stop()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Shipments",   f"{len(route_df):,}")
    c2.metric("Avg Lead Time",     f"{route_df['lead_time'].mean():.0f} days")
    c3.metric("Min Lead Time",     f"{route_df['lead_time'].min():.0f} days")
    c4.metric("Max Lead Time",     f"{route_df['lead_time'].max():.0f} days")
    delayed_pct = route_df["Delayed"].sum() / len(route_df) * 100
    c5.metric("Delay Rate",        f"{delayed_pct:.1f}%")

    st.write("")
    avg_eff = route_df["Route_Efficiency_Score"].mean()
    st.info(
        f"Showing **{len(route_df):,}** shipments for route "
        f"**{selected_route}** | "
        f"Avg efficiency score: **{avg_eff:.3f}**"
    )

    tab1, tab2, tab3 = st.tabs(
        ["State Insights", "Order Timeline", "KPI Trends"]
    )

    with tab1:
        section("State-Level Performance Insights")

        state_perf = df_kpi.groupby("State/Province").agg(
            Avg_Lead_Time=("lead_time", "mean"),
            Shipments=("lead_time", "count"),
            Delay_Rate=("Delayed",
                        lambda x: round(x.sum() / len(x) * 100, 1)),
            Avg_Efficiency=("Route_Efficiency_Score", "mean"),
            Total_Sales=("Sales", "sum")
        ).reset_index().sort_values("Avg_Lead_Time")

        c1, c2 = st.columns(2)

        with c1:
            top15 = state_perf.head(15)
            fig1 = px.bar(
                top15, y="State/Province", x="Avg_Lead_Time",
                orientation="h",
                color="Avg_Lead_Time",
                color_continuous_scale=["#00d4aa", "#3d85ff", "#ff5c5c"],
                text=top15["Avg_Lead_Time"].apply(lambda x: f"{x:.0f}d"),
                title="Avg Lead Time — All States"
            )
            fig1.update_traces(textposition="outside",
                               marker_line_width=0)
            apply_theme(fig1, 460)
            fig1.update_layout(coloraxis_showscale=False,
                               xaxis_title="Avg Lead Time (days)",
                               yaxis_title="")
            st.plotly_chart(fig1, use_container_width=True)

        with c2:
            fig2 = px.scatter(
                state_perf,
                x="Shipments", y="Avg_Lead_Time",
                size="Shipments", size_max=35,
                color="Delay_Rate",
                color_continuous_scale=["#00d4aa", "#ffb547", "#ff5c5c"],
                hover_name="State/Province",
                title="State Volume vs Lead Time (colour = delay %)",
                labels={"Avg_Lead_Time": "Avg Lead Time (days)"}
            )
            apply_theme(fig2, 460)
            fig2.update_layout(
                coloraxis_colorbar=dict(
                    title="Delay %",
                    tickfont=dict(color="#7a86a1")
                )
            )
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        section("Order-Level Shipment Timelines",
                f"Individual orders — route: {selected_route}")

        cols_show  = ["Order ID", "Order Date", "Ship Date", "lead_time",
                      "Ship Mode", "State/Province", "City", "Sales",
                      "Delayed"]
        cols_avail = [c for c in cols_show if c in route_df.columns]
        timeline_df = (route_df[cols_avail]
                       .sort_values("Order Date", ascending=False))
        timeline_df["lead_time"] = (timeline_df["lead_time"]
                                    .round(0).astype(int))
        timeline_df["Sales"] = timeline_df["Sales"].round(2)

        st.dataframe(
            timeline_df.reset_index(drop=True),
            use_container_width=True,
            height=500,
            column_config={
                "lead_time": st.column_config.NumberColumn(
                    "Lead Time (days)", format="%d"),
                "Sales": st.column_config.NumberColumn(
                    "Sales ($)", format="$%.2f"),
                "Delayed": st.column_config.CheckboxColumn("Delayed?"),
                "Order Date": st.column_config.DateColumn("Order Date"),
                "Ship Date":  st.column_config.DateColumn("Ship Date"),
            }
        )

    with tab3:
        section("KPI Trends for Selected Route")

        route_df2 = route_df.copy()
        route_df2["YearMonth"] = (route_df2["Order Date"]
                                  .dt.to_period("M").astype(str))
        trend = route_df2.groupby("YearMonth").agg(
            Avg_Lead_Time=("lead_time", "mean"),
            Shipments=("lead_time", "count"),
            Delay_Rate=("Delayed",
                        lambda x: x.sum() / len(x) * 100)
        ).reset_index()

        fig_t = make_subplots(
            rows=2, cols=1, shared_xaxes=True,
            row_heights=[0.6, 0.4], vertical_spacing=0.08
        )
        fig_t.add_trace(
            go.Scatter(
                x=trend["YearMonth"], y=trend["Avg_Lead_Time"],
                name="Avg Lead Time",
                line=dict(color="#3d85ff", width=2.5),
                mode="lines+markers", marker=dict(size=6)
            ), row=1, col=1
        )
        fig_t.add_trace(
            go.Bar(
                x=trend["YearMonth"], y=trend["Shipments"],
                name="Shipments", marker_color="#00d4aa", opacity=0.7
            ), row=2, col=1
        )
        apply_theme(fig_t, 460)
        fig_t.update_layout(
            yaxis=dict(title="Avg Lead Time (days)", gridcolor="#252d45"),
            yaxis2=dict(title="Shipments", gridcolor="#252d45"),
            xaxis2_tickangle=-45,
            hovermode="x unified",
            showlegend=True
        )
        st.plotly_chart(fig_t, use_container_width=True)

        st.divider()
        section("Route Efficiency Score Distribution")
        fig_eff = px.histogram(
            route_df, x="Route_Efficiency_Score", nbins=30,
            color_discrete_sequence=["#3d85ff"],
            title="Distribution of Route Efficiency Scores",
            labels={"Route_Efficiency_Score": "Efficiency Score"}
        )
        apply_theme(fig_eff, 300)
        fig_eff.update_layout(yaxis_title="Count",
                              xaxis_title="Efficiency Score")
        st.plotly_chart(fig_eff, use_container_width=True)