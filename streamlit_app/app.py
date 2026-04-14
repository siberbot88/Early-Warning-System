import os
import pandas as pd
import streamlit as st
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Early Warning Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# THEME COLORS
# =========================================================
PRIMARY_BLUE = "#0B409C"
DEEP_NAVY = "#10316B"
ACCENT_YELLOW = "#FFE867"
DANGER_RED = "#D62828"
WHITE = "#FFFFFF"
LIGHT_BG = "#F7F9FC"
BORDER = "#E5EAF2"
TEXT = "#1F2937"
MUTED = "#6B7280"

FINAL_RESULT_COLORS = {
    "Distinction": PRIMARY_BLUE,
    "Fail": ACCENT_YELLOW,
    "Pass": DEEP_NAVY,
    "Withdrawn": DANGER_RED,
    "Withdrawal": DANGER_RED,
}

# =========================================================
# SVG ICONS
# =========================================================
def icon_chart():
    return """
    <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24"
         stroke="currentColor" stroke-width="1.8">
      <path stroke-linecap="round" stroke-linejoin="round" d="M3 3v18h18"/>
      <path stroke-linecap="round" stroke-linejoin="round" d="M7 15v-3m5 3V8m5 7v-5"/>
    </svg>
    """

def icon_users():
    return """
    <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24"
         stroke="currentColor" stroke-width="1.8">
      <path stroke-linecap="round" stroke-linejoin="round" d="M15 19a4 4 0 0 0-8 0"/>
      <path stroke-linecap="round" stroke-linejoin="round" d="M11 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z"/>
      <path stroke-linecap="round" stroke-linejoin="round" d="M20 19a4 4 0 0 0-3-3.87"/>
      <path stroke-linecap="round" stroke-linejoin="round" d="M15.5 3.13a4 4 0 0 1 0 7.75"/>
    </svg>
    """

def icon_warning():
    return """
    <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24"
         stroke="currentColor" stroke-width="1.8">
      <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v4m0 4h.01"/>
      <path stroke-linecap="round" stroke-linejoin="round" d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0Z"/>
    </svg>
    """

def icon_academic():
    return """
    <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24"
         stroke="currentColor" stroke-width="1.8">
      <path stroke-linecap="round" stroke-linejoin="round" d="M12 14 3 9l9-5 9 5-9 5Z"/>
      <path stroke-linecap="round" stroke-linejoin="round" d="M7 12v4c0 1.5 2.24 3 5 3s5-1.5 5-3v-4"/>
    </svg>
    """

# =========================================================
# GLOBAL CSS
# =========================================================
st.markdown(
    f"""
    <style>
    .stApp {{
        background: {LIGHT_BG};
        color: {TEXT};
    }}

    .block-container {{
        max-width: 1360px;
        padding-top: 1.25rem;
        padding-bottom: 2rem;
    }}

    .hero {{
        width: 100%;
        background: linear-gradient(135deg, {DEEP_NAVY} 0%, {PRIMARY_BLUE} 100%);
        border-radius: 24px;
        padding: 30px 32px;
        color: white;
        box-shadow: 0 14px 34px rgba(16,49,107,0.18);
        margin-bottom: 1.5rem;
    }}

    .hero-top {{
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 14px;
    }}

    .hero h1 {{
        margin: 0;
        font-size: 2rem;
        line-height: 1.1;
        font-weight: 800;
        color: white;
    }}

    .hero p {{
        margin: 0;
        color: rgba(255,255,255,0.92);
        font-size: 1rem;
        line-height: 1.7;
        max-width: 950px;
    }}

    .badge {{
        display: inline-flex;
        align-items: center;
        padding: 9px 14px;
        margin-top: 18px;
        border-radius: 999px;
        background: rgba(255,255,255,0.14);
        color: white;
        font-size: 0.85rem;
        font-weight: 700;
    }}

    .hero-icon {{
        width: 48px;
        height: 48px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: {ACCENT_YELLOW};
        background: rgba(255,232,103,0.15);
        flex-shrink: 0;
    }}

    .icon-wrap {{
        width: 40px;
        height: 40px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(11,64,156,0.08);
        color: {PRIMARY_BLUE};
        flex-shrink: 0;
    }}

    .icon {{
        width: 22px;
        height: 22px;
    }}

    .hero-icon .icon {{
        width: 26px;
        height: 26px;
    }}

    .section-title {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 0 0 14px 0;
    }}

    .section-title h3 {{
        margin: 0;
        color: {DEEP_NAVY};
        font-size: 1.18rem;
        font-weight: 800;
    }}

    .metric-card {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 20px;
        padding: 18px;
        min-height: 132px;
        box-shadow: 0 10px 24px rgba(15,23,42,0.04);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}

    .metric-top {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        margin-bottom: 10px;
    }}

    .metric-label {{
        color: {MUTED};
        font-size: 0.92rem;
        font-weight: 700;
    }}

    .metric-value {{
        color: {DEEP_NAVY};
        font-size: 1.9rem;
        font-weight: 800;
        line-height: 1.1;
    }}

    .metric-foot {{
        color: {MUTED};
        font-size: 0.84rem;
        line-height: 1.5;
        margin-top: 6px;
    }}

    .card {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 20px;
        padding: 18px;
        box-shadow: 0 10px 24px rgba(15,23,42,0.04);
        margin-bottom: 1rem;
    }}

    .small-note {{
        color: {MUTED};
        font-size: 0.88rem;
        line-height: 1.6;
    }}

    .highlight {{
        display: inline-block;
        padding: 2px 8px;
        border-radius: 999px;
        background: rgba(255,232,103,0.45);
        color: {DEEP_NAVY};
        font-weight: 700;
        font-size: 0.82rem;
    }}

    div[data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 16px;
        overflow: hidden;
    }}

    [data-testid="stSidebar"] {{
        background: {WHITE};
        border-right: 1px solid {BORDER};
    }}

    hr {{
        border: none;
        border-top: 1px solid {BORDER};
        margin: 1.15rem 0 1.15rem 0;
    }}

    /* TABLET RESPONSIVE (576px - 1024px) */
    @media screen and (min-width: 576px) and (max-width: 1024px) {{
        div[data-testid="stHorizontalBlock"] {{
            flex-wrap: wrap !important;
            gap: 1rem !important;
        }}
        div[data-testid="column"] {{
            min-width: calc(45% - 1rem) !important;
            flex-grow: 1 !important;
        }}
        .metric-value {{
            font-size: 1.6rem !important;
        }}
        .hero h1 {{
            font-size: 1.6rem !important;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# HELPERS
# =========================================================
def style_plotly(fig):
    fig.update_layout(
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        font=dict(color=TEXT, family="Arial", size=14),
        title_font=dict(color=DEEP_NAVY, size=18),
        legend_title_font=dict(color=DEEP_NAVY, size=13),
        legend_font=dict(color=TEXT, size=13),
        margin=dict(l=20, r=20, t=60, b=20),
        hoverlabel=dict(bgcolor="white", font_color=TEXT, font_size=13),
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor=BORDER,
        tickfont=dict(color=TEXT, size=13),
        title_font=dict(color=DEEP_NAVY, size=14),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E8EEF7",
        linecolor=BORDER,
        tickfont=dict(color=TEXT, size=13),
        title_font=dict(color=DEEP_NAVY, size=14),
    )
    return fig


def normalize_final_result(df: pd.DataFrame) -> pd.DataFrame:
    if "final_result" in df.columns:
        df = df.copy()
        df["final_result"] = df["final_result"].replace({"Withdrawal": "Withdrawn"})
    return df


@st.cache_data
def load_csv(path: str):
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


def metric_card(label: str, value: str, foot: str, icon_svg: str):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-top">
                <div class="metric-label">{label}</div>
                <div class="icon-wrap">{icon_svg}</div>
            </div>
            <div class="metric-value">{value}</div>
            <div class="metric-foot">{foot}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# PATHS
# =========================================================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed", "merged_processed_oulad.csv")
MODEL_PATH = os.path.join(BASE_DIR, "data", "output", "model_comparison.csv")
FEATURE_PATH = os.path.join(BASE_DIR, "data", "output", "feature_importance_dt.csv")
RISK_PATH = os.path.join(BASE_DIR, "data", "output", "at_risk_students.csv")

# =========================================================
# LOAD DATA
# =========================================================
merged_data = load_csv(PROCESSED_PATH)
model_comparison = load_csv(MODEL_PATH)
feature_importance_dt = load_csv(FEATURE_PATH)
at_risk_students = load_csv(RISK_PATH)

if merged_data is None:
    st.error("File data utama tidak ditemukan. Pastikan file data/processed/merged_processed_oulad.csv tersedia.")
    st.stop()

merged_data = normalize_final_result(merged_data)
if at_risk_students is not None:
    at_risk_students = normalize_final_result(at_risk_students)

# =========================================================
# HERO
# =========================================================
st.markdown(
    f"""
    <div class="hero">
        <div class="hero-top">
            <div class="hero-icon">{icon_chart()}</div>
            <div><h1>Early Warning Dashboard</h1></div>
        </div>
        <p>
            Dashboard ini menampilkan ringkasan akademik, pola keterlibatan mahasiswa,
            performa asesmen, dan hasil model prediktif untuk mendukung deteksi dini mahasiswa
            berisiko gagal atau withdrawal pada pembelajaran daring.
        </p>
        <div class="badge">The Open University | Learning Analytics Dashboard</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SIDEBAR FILTER
# =========================================================
st.sidebar.markdown("## Filter Dashboard")

filtered_data = merged_data.copy()

if "code_module" in filtered_data.columns:
    module_options = ["All"] + sorted(filtered_data["code_module"].dropna().astype(str).unique().tolist())
    selected_module = st.sidebar.selectbox("Code Module", module_options, index=0)
    if selected_module != "All":
        filtered_data = filtered_data[filtered_data["code_module"].astype(str) == selected_module]

if "code_presentation" in filtered_data.columns:
    presentation_options = ["All"] + sorted(filtered_data["code_presentation"].dropna().astype(str).unique().tolist())
    selected_presentation = st.sidebar.selectbox("Code Presentation", presentation_options, index=0)
    if selected_presentation != "All":
        filtered_data = filtered_data[filtered_data["code_presentation"].astype(str) == selected_presentation]

if "final_result" in filtered_data.columns:
    result_options = ["All"] + sorted(filtered_data["final_result"].dropna().astype(str).unique().tolist())
    selected_result = st.sidebar.selectbox("Final Result", result_options, index=0)
    if selected_result != "All":
        filtered_data = filtered_data[filtered_data["final_result"].astype(str) == selected_result]

st.sidebar.markdown("---")
st.sidebar.markdown("### Data Summary")
st.sidebar.write(f"Rows after filter: **{len(filtered_data):,}**")

# =========================================================
# KPI SUMMARY
# =========================================================
total_students = len(filtered_data)

withdrawal_rate = (
    filtered_data["final_result"].eq("Withdrawn").mean() * 100
    if "final_result" in filtered_data.columns and len(filtered_data) > 0
    else 0
)

fail_rate = (
    filtered_data["final_result"].eq("Fail").mean() * 100
    if "final_result" in filtered_data.columns and len(filtered_data) > 0
    else 0
)

engagement_rate = (
    filtered_data["low_engagement"].eq(0).mean() * 100
    if "low_engagement" in filtered_data.columns and len(filtered_data) > 0
    else 0
)

completion_rate = (
    filtered_data["assessment_completion_rate"].mean() * 100
    if "assessment_completion_rate" in filtered_data.columns and len(filtered_data) > 0
    else 0
)

at_risk_rate = (
    filtered_data["risk_label"].eq(1).mean() * 100
    if "risk_label" in filtered_data.columns and len(filtered_data) > 0
    else 0
)

st.markdown(
    f"""
    <div class="section-title">
        <div class="icon-wrap">{icon_users()}</div>
        <h3>Executive Summary</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4, m5 = st.columns(5, gap="medium")
with m1:
    metric_card("Total Students", f"{total_students:,}", "Total record mahasiswa pada data terfilter", icon_users())
with m2:
    metric_card("Withdrawal Rate", f"{withdrawal_rate:.2f}%", "Persentase mahasiswa yang withdrawal", icon_warning())
with m3:
    metric_card("Fail Rate", f"{fail_rate:.2f}%", "Persentase mahasiswa yang tidak lulus", icon_academic())
with m4:
    metric_card("Engagement Rate", f"{engagement_rate:.2f}%", "Mahasiswa dengan engagement tidak rendah", icon_chart())
with m5:
    metric_card("At-Risk Rate", f"{at_risk_rate:.2f}%", "Mahasiswa yang masuk kategori berisiko", icon_warning())

st.markdown("<hr>", unsafe_allow_html=True)

# =========================================================
# ROW 1
# =========================================================
col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="section-title">
            <div class="icon-wrap">{icon_chart()}</div>
            <h3>Distribusi Hasil Akhir Mahasiswa</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "final_result" in filtered_data.columns and len(filtered_data) > 0:
        final_result_count = filtered_data["final_result"].value_counts().reset_index()
        final_result_count.columns = ["final_result", "jumlah_mahasiswa"]

        fig = px.bar(
            final_result_count,
            x="final_result",
            y="jumlah_mahasiswa",
            color="final_result",
            color_discrete_map=FINAL_RESULT_COLORS,
            text="jumlah_mahasiswa",
            title="Distribusi Final Result",
        )
        fig = style_plotly(fig)
        fig.update_layout(showlegend=False, xaxis_title="Final Result", yaxis_title="Jumlah Mahasiswa")
        fig.update_traces(textposition="outside", textfont=dict(color=DEEP_NAVY, size=13))
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(final_result_count, use_container_width=True)
    else:
        st.info("Kolom final_result tidak tersedia.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="section-title">
            <div class="icon-wrap">{icon_academic()}</div>
            <h3>Assessment Completion Summary</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "assessment_completion_rate" in filtered_data.columns and len(filtered_data) > 0:
        summary_completion = filtered_data["assessment_completion_rate"].describe().round(4).reset_index()
        summary_completion.columns = ["statistic", "value"]
        st.dataframe(summary_completion, use_container_width=True)

        if "final_result" in filtered_data.columns:
            completion_by_result = (
                filtered_data.groupby("final_result")["assessment_completion_rate"]
                .mean()
                .round(4)
                .reset_index()
            )

            fig = px.bar(
                completion_by_result,
                x="final_result",
                y="assessment_completion_rate",
                color="final_result",
                color_discrete_map=FINAL_RESULT_COLORS,
                text="assessment_completion_rate",
                title="Assessment Completion Rate per Final Result",
            )
            fig = style_plotly(fig)
            fig.update_layout(showlegend=False, xaxis_title="Final Result", yaxis_title="Completion Rate")
            fig.update_traces(textposition="outside", textfont=dict(color=DEEP_NAVY, size=13))
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Kolom assessment_completion_rate tidak tersedia.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# =========================================================
# ROW 2 - MODULE RESULT
# =========================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="section-title">
        <div class="icon-wrap">{icon_warning()}</div>
        <h3>Persentase Final Result per Modul</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

if {"code_module", "final_result"}.issubset(filtered_data.columns) and len(filtered_data) > 0:
    module_result_pct = pd.crosstab(
        filtered_data["code_module"],
        filtered_data["final_result"],
        normalize="index"
    ).reset_index()

    module_result_long = module_result_pct.melt(
        id_vars="code_module",
        var_name="final_result",
        value_name="percentage"
    )
    module_result_long["percentage"] = module_result_long["percentage"] * 100

    fig = px.bar(
        module_result_long,
        x="code_module",
        y="percentage",
        color="final_result",
        color_discrete_map=FINAL_RESULT_COLORS,
        barmode="stack",
        title="Persentase Final Result per Modul",
    )
    fig = style_plotly(fig)
    fig.update_layout(xaxis_title="Code Module", yaxis_title="Persentase (%)")
    st.plotly_chart(fig, use_container_width=True)

    module_table = pd.crosstab(
        filtered_data["code_module"],
        filtered_data["final_result"],
        normalize="index"
    ) * 100
    st.dataframe(module_table.round(2), use_container_width=True)
else:
    st.info("Kolom code_module/final_result tidak tersedia.")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# =========================================================
# ROW 3
# =========================================================
col_a, col_b = st.columns(2, gap="large")

with col_a:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="section-title">
            <div class="icon-wrap">{icon_chart()}</div>
            <h3>Aktivitas VLE</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if {"final_result", "total_clicks", "active_days"}.issubset(filtered_data.columns) and len(filtered_data) > 0:
        vle_summary = (
            filtered_data.groupby("final_result")[["total_clicks", "active_days"]]
            .mean()
            .round(2)
            .reset_index()
        )

        st.dataframe(vle_summary, use_container_width=True)

        fig_clicks = px.bar(
            vle_summary,
            x="final_result",
            y="total_clicks",
            color="final_result",
            color_discrete_map=FINAL_RESULT_COLORS,
            text="total_clicks",
            title="Rata-rata Total Clicks",
        )
        fig_clicks = style_plotly(fig_clicks)
        fig_clicks.update_layout(showlegend=False, xaxis_title="Final Result", yaxis_title="Rata-rata Total Clicks")
        fig_clicks.update_traces(textposition="outside", textfont=dict(color=DEEP_NAVY, size=13))
        st.plotly_chart(fig_clicks, use_container_width=True)

        fig_days = px.bar(
            vle_summary,
            x="final_result",
            y="active_days",
            color="final_result",
            color_discrete_map=FINAL_RESULT_COLORS,
            text="active_days",
            title="Rata-rata Active Days",
        )
        fig_days = style_plotly(fig_days)
        fig_days.update_layout(showlegend=False, xaxis_title="Final Result", yaxis_title="Rata-rata Active Days")
        fig_days.update_traces(textposition="outside", textfont=dict(color=DEEP_NAVY, size=13))
        st.plotly_chart(fig_days, use_container_width=True)
    else:
        st.info("Kolom aktivitas VLE tidak lengkap.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="section-title">
            <div class="icon-wrap">{icon_academic()}</div>
            <h3>Performa Asesmen</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    needed = {"final_result", "avg_score", "assessment_completion_rate"}
    if needed.issubset(filtered_data.columns) and len(filtered_data) > 0:
        assessment_summary = (
            filtered_data.groupby("final_result")[["avg_score", "assessment_completion_rate"]]
            .mean()
            .round(4)
            .reset_index()
        )

        st.dataframe(assessment_summary, use_container_width=True)

        fig_score = px.bar(
            assessment_summary,
            x="final_result",
            y="avg_score",
            color="final_result",
            color_discrete_map=FINAL_RESULT_COLORS,
            text="avg_score",
            title="Rata-rata Avg Score",
        )
        fig_score = style_plotly(fig_score)
        fig_score.update_layout(showlegend=False, xaxis_title="Final Result", yaxis_title="Rata-rata Avg Score")
        fig_score.update_traces(textposition="outside", textfont=dict(color=DEEP_NAVY, size=13))
        st.plotly_chart(fig_score, use_container_width=True)

        fig_comp = px.bar(
            assessment_summary,
            x="final_result",
            y="assessment_completion_rate",
            color="final_result",
            color_discrete_map=FINAL_RESULT_COLORS,
            text="assessment_completion_rate",
            title="Rata-rata Assessment Completion Rate",
        )
        fig_comp = style_plotly(fig_comp)
        fig_comp.update_layout(showlegend=False, xaxis_title="Final Result", yaxis_title="Completion Rate")
        fig_comp.update_traces(textposition="outside", textfont=dict(color=DEEP_NAVY, size=13))
        st.plotly_chart(fig_comp, use_container_width=True)
    else:
        st.info("Kolom asesmen tidak lengkap.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# =========================================================
# ROW 4 - LOW ENGAGEMENT / LOW SCORE
# =========================================================
col_c, col_d = st.columns(2, gap="large")

with col_c:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="section-title">
            <div class="icon-wrap">{icon_warning()}</div>
            <h3>Low Engagement Analysis</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if {"low_engagement", "final_result"}.issubset(filtered_data.columns) and len(filtered_data) > 0:
        le = pd.crosstab(
            filtered_data["low_engagement"],
            filtered_data["final_result"],
            normalize="index"
        ).reset_index()

        le_long = le.melt(
            id_vars="low_engagement",
            var_name="final_result",
            value_name="percentage"
        )
        le_long["percentage"] = le_long["percentage"] * 100

        fig = px.bar(
            le_long,
            x="low_engagement",
            y="percentage",
            color="final_result",
            color_discrete_map=FINAL_RESULT_COLORS,
            barmode="stack",
            title="Distribusi Final Result berdasarkan Low Engagement",
        )
        fig = style_plotly(fig)
        fig.update_layout(
            xaxis_title="Low Engagement (0 = tidak rendah, 1 = rendah)",
            yaxis_title="Persentase (%)"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Kolom low_engagement/final_result tidak tersedia.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_d:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="section-title">
            <div class="icon-wrap">{icon_warning()}</div>
            <h3>Low Score Analysis</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if {"low_score", "final_result"}.issubset(filtered_data.columns) and len(filtered_data) > 0:
        ls = pd.crosstab(
            filtered_data["low_score"],
            filtered_data["final_result"],
            normalize="index"
        ).reset_index()

        ls_long = ls.melt(
            id_vars="low_score",
            var_name="final_result",
            value_name="percentage"
        )
        ls_long["percentage"] = ls_long["percentage"] * 100

        fig = px.bar(
            ls_long,
            x="low_score",
            y="percentage",
            color="final_result",
            color_discrete_map=FINAL_RESULT_COLORS,
            barmode="stack",
            title="Distribusi Final Result berdasarkan Low Score",
        )
        fig = style_plotly(fig)
        fig.update_layout(
            xaxis_title="Low Score (0 = tidak rendah, 1 = rendah)",
            yaxis_title="Persentase (%)"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Kolom low_score/final_result tidak tersedia.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# =========================================================
# ROW 5 - MODEL PERFORMANCE
# =========================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="section-title">
        <div class="icon-wrap">{icon_chart()}</div>
        <h3>Model Performance</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

if model_comparison is not None and len(model_comparison) > 0:
    st.dataframe(model_comparison, use_container_width=True)

    metric_cols = [c for c in ["Accuracy", "Precision", "Recall", "F1-Score"] if c in model_comparison.columns]
    if "Model" in model_comparison.columns and metric_cols:
        compare_long = model_comparison.melt(
            id_vars="Model",
            value_vars=metric_cols,
            var_name="Metric",
            value_name="Score"
        )

        fig = px.bar(
            compare_long,
            x="Model",
            y="Score",
            color="Metric",
            barmode="group",
            color_discrete_sequence=[PRIMARY_BLUE, DEEP_NAVY, ACCENT_YELLOW, DANGER_RED],
            title="Perbandingan Kinerja Model",
        )
        fig = style_plotly(fig)
        fig.update_yaxes(range=[0, 1])
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("File model_comparison.csv belum tersedia.")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# =========================================================
# ROW 6 - FEATURE IMPORTANCE + AT RISK
# =========================================================
col_e, col_f = st.columns(2, gap="large")

with col_e:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="section-title">
            <div class="icon-wrap">{icon_chart()}</div>
            <h3>Feature Importance Decision Tree</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if feature_importance_dt is not None and {"feature", "importance"}.issubset(feature_importance_dt.columns):
        top_features = feature_importance_dt.head(10)
        st.dataframe(top_features, use_container_width=True)

        fig = px.bar(
            top_features.sort_values("importance"),
            x="importance",
            y="feature",
            orientation="h",
            color="importance",
            color_continuous_scale=[[0, PRIMARY_BLUE], [1, ACCENT_YELLOW]],
            title="Top 10 Feature Importance",
        )
        fig = style_plotly(fig)
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("File feature_importance_dt.csv belum tersedia.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_f:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="section-title">
            <div class="icon-wrap">{icon_users()}</div>
            <h3>Daftar Mahasiswa Berisiko</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if at_risk_students is not None and len(at_risk_students) > 0:
        risk_df = at_risk_students.copy()
    else:
        if "risk_label" in filtered_data.columns:
            risk_df = filtered_data[filtered_data["risk_label"] == 1].copy()
        else:
            risk_df = pd.DataFrame()

    if len(risk_df) > 0:
        preferred_cols = [
            "id_student",
            "code_module",
            "code_presentation",
            "final_result",
            "risk_label",
            "total_clicks",
            "avg_score",
            "assessment_completion_rate",
        ]
        show_cols = [c for c in preferred_cols if c in risk_df.columns]
        st.dataframe(risk_df[show_cols].head(20), use_container_width=True)
    else:
        st.info("Data mahasiswa berisiko belum tersedia.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# =========================================================
# FOOTNOTE
# =========================================================
st.markdown(
    f"""
    <div class="card">
        <div class="section-title" style="margin-top:0;">
            <div class="icon-wrap">{icon_warning()}</div>
            <h3>Interpretasi Singkat</h3>
        </div>
        <div class="small-note">
            Dashboard ini menunjukkan bahwa <span class="highlight">aktivitas VLE</span>,
            <span class="highlight">performa asesmen</span>, dan
            <span class="highlight">hasil model prediktif</span> dapat digunakan bersama
            untuk mendukung proses deteksi dini mahasiswa berisiko gagal atau withdrawal.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)