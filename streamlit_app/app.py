import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Early Warning Dashboard",
    page_icon="data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%230B409C' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M3 3v18h18'/><path d='M7 14l3-3 3 2 4-5'/></svg>",
    layout="wide",
)

PRIMARY_BLUE = "#0B409C"
DEEP_NAVY = "#10316B"
ACCENT_YELLOW = "#FFE867"
WHITE = "#FFFFFF"
LIGHT_BG = "#F7F9FC"
BORDER = "#E6ECF5"
TEXT = "#1F2937"
MUTED = "#6B7280"


def icon_bar_chart():
    return """
    <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
      <path stroke-linecap="round" stroke-linejoin="round" d="M3 3v18h18" />
      <path stroke-linecap="round" stroke-linejoin="round" d="M7 16v-4m5 4V8m5 8V11" />
    </svg>
    """


def icon_users():
    return """
    <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
      <path stroke-linecap="round" stroke-linejoin="round" d="M15 19a4 4 0 0 0-8 0" />
      <path stroke-linecap="round" stroke-linejoin="round" d="M11 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z" />
      <path stroke-linecap="round" stroke-linejoin="round" d="M20 19a4 4 0 0 0-3-3.87" />
      <path stroke-linecap="round" stroke-linejoin="round" d="M15.5 3.13a4 4 0 0 1 0 7.75" />
    </svg>
    """


def icon_warning():
    return """
    <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
      <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v4m0 4h.01" />
      <path stroke-linecap="round" stroke-linejoin="round" d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0Z" />
    </svg>
    """


def icon_academic():
    return """
    <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
      <path stroke-linecap="round" stroke-linejoin="round" d="M12 14 3 9l9-5 9 5-9 5Z" />
      <path stroke-linecap="round" stroke-linejoin="round" d="M7 12v4c0 1.5 2.24 3 5 3s5-1.5 5-3v-4" />
    </svg>
    """


st.markdown(
    f"""
    <style>
    :root {{
        --primary-blue: {PRIMARY_BLUE};
        --deep-navy: {DEEP_NAVY};
        --accent-yellow: {ACCENT_YELLOW};
        --white: {WHITE};
        --light-bg: {LIGHT_BG};
        --border: {BORDER};
        --text: {TEXT};
        --muted: {MUTED};
    }}

    .stApp {{
        background-color: var(--light-bg);
        color: var(--text);
    }}

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1280px;
    }}

    .hero {{
        background: linear-gradient(135deg, var(--deep-navy) 0%, var(--primary-blue) 100%);
        border-radius: 20px;
        padding: 28px 30px;
        color: white;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 10px 30px rgba(16,49,107,0.18);
        margin-bottom: 1.25rem;
    }}

    .hero-top {{
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 12px;
    }}

    .hero h1 {{
        margin: 0;
        font-size: 2rem;
        line-height: 1.15;
        font-weight: 800;
    }}

    .hero p {{
        margin: 0;
        color: rgba(255,255,255,0.9);
        font-size: 0.98rem;
        line-height: 1.6;
    }}

    .badge {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255,255,255,0.12);
        color: white;
        border: 1px solid rgba(255,255,255,0.18);
        padding: 8px 12px;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 14px;
    }}

    .section-title {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 0.25rem;
        margin-bottom: 0.9rem;
        color: var(--deep-navy);
    }}

    .section-title h3 {{
        margin: 0;
        font-size: 1.15rem;
        font-weight: 800;
    }}

    .card {{
        background: var(--white);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 18px 18px 14px 18px;
        box-shadow: 0 8px 22px rgba(15,23,42,0.04);
        margin-bottom: 1rem;
    }}

    .metric-card {{
        background: var(--white);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 16px;
        box-shadow: 0 8px 22px rgba(15,23,42,0.04);
        min-height: 126px;
    }}

    .metric-top {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
    }}

    .metric-label {{
        color: var(--muted);
        font-size: 0.9rem;
        font-weight: 600;
    }}

    .metric-value {{
        color: var(--deep-navy);
        font-size: 1.75rem;
        font-weight: 800;
        line-height: 1.1;
    }}

    .metric-foot {{
        margin-top: 8px;
        color: var(--muted);
        font-size: 0.82rem;
    }}

    .icon-wrap {{
        width: 38px;
        height: 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        background: rgba(11,64,156,0.08);
        color: var(--primary-blue);
        flex-shrink: 0;
    }}

    .hero-icon {{
        width: 46px;
        height: 46px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        background: rgba(255,232,103,0.18);
        color: var(--accent-yellow);
    }}

    .icon {{
        width: 22px;
        height: 22px;
    }}

    .hero-icon .icon {{
        width: 26px;
        height: 26px;
    }}

    div[data-testid="stDataFrame"] {{
        border: 1px solid var(--border);
        border-radius: 16px;
        overflow: hidden;
    }}

    div[data-testid="stMetric"] {{
        background: transparent;
    }}

    .small-note {{
        color: var(--muted);
        font-size: 0.88rem;
        line-height: 1.6;
    }}

    .highlight {{
        display: inline-block;
        background: rgba(255,232,103,0.45);
        color: var(--deep-navy);
        padding: 2px 8px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.82rem;
    }}

    hr {{
        border: none;
        border-top: 1px solid var(--border);
        margin: 1rem 0 1.25rem 0;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__)) if "__file__" in globals() else os.getcwd()
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed", "merged_processed_oulad.csv")
MODEL_PATH = os.path.join(BASE_DIR, "data", "output", "model_comparison.csv")
FEATURE_PATH = os.path.join(BASE_DIR, "data", "output", "feature_importance_dt.csv")
RISK_PATH = os.path.join(BASE_DIR, "data", "output", "at_risk_students.csv")


@st.cache_data
def load_csv(path: str):
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


merged_data = load_csv(PROCESSED_PATH)
model_comparison = load_csv(MODEL_PATH)
feature_importance_dt = load_csv(FEATURE_PATH)
at_risk_students = load_csv(RISK_PATH)

if merged_data is None:
    st.error(
        "File data utama tidak ditemukan. Pastikan file 'data/processed/merged_processed_oulad.csv' tersedia."
    )
    st.stop()

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-top">
            <div class="hero-icon">
                {icon_bar_chart()}
            </div>
            <div>
                <h1>Early Warning Dashboard</h1>
            </div>
        </div>
        <p>
            Dashboard ini menampilkan ringkasan akademik, pola keterlibatan mahasiswa,
            performa asesmen, dan hasil model prediktif untuk mendukung deteksi dini mahasiswa
            berisiko gagal atau withdrawal pada pembelajaran daring.
        </p>
        <div class="badge">The Open University &nbsp;|&nbsp; Learning Analytics Dashboard</div>
    </div>
    """,
    unsafe_allow_html=True,
)

total_students = len(merged_data)
withdrawal_rate = (
    merged_data["final_result"].isin(["Withdrawn", "Withdrawal"]).mean() * 100
    if "final_result" in merged_data.columns
    else 0
)
fail_rate = (
    merged_data["final_result"].eq("Fail").mean() * 100
    if "final_result" in merged_data.columns
    else 0
)
engagement_rate = (
    merged_data["low_engagement"].eq(0).mean() * 100
    if "low_engagement" in merged_data.columns
    else None
)
completion_rate = (
    merged_data["assessment_completion_rate"].mean() * 100
    if "assessment_completion_rate" in merged_data.columns
    else None
)
at_risk_rate = (
    merged_data["risk_label"].eq(1).mean() * 100
    if "risk_label" in merged_data.columns
    else None
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

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-top">
                <div class="metric-label">Total Students</div>
                <div class="icon-wrap">{icon_users()}</div>
            </div>
            <div class="metric-value">{total_students:,}</div>
            <div class="metric-foot">Total record mahasiswa pada dataset terintegrasi</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-top">
                <div class="metric-label">Withdrawal Rate</div>
                <div class="icon-wrap">{icon_warning()}</div>
            </div>
            <div class="metric-value">{withdrawal_rate:.2f}%</div>
            <div class="metric-foot">Persentase mahasiswa yang withdrawal</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-top">
                <div class="metric-label">Fail Rate</div>
                <div class="icon-wrap">{icon_academic()}</div>
            </div>
            <div class="metric-value">{fail_rate:.2f}%</div>
            <div class="metric-foot">Persentase mahasiswa yang tidak lulus</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-top">
                <div class="metric-label">Engagement Rate</div>
                <div class="icon-wrap">{icon_bar_chart()}</div>
            </div>
            <div class="metric-value">{engagement_rate:.2f}%</div>
            <div class="metric-foot">Mahasiswa dengan engagement tidak rendah</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c5:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-top">
                <div class="metric-label">At-Risk Rate</div>
                <div class="icon-wrap">{icon_warning()}</div>
            </div>
            <div class="metric-value">{at_risk_rate:.2f}%</div>
            <div class="metric-foot">Mahasiswa yang masuk kategori berisiko</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr>", unsafe_allow_html=True)

left, right = st.columns([1.1, 1])

with left:
    st.markdown(
        f"""
        <div class="section-title">
            <div class="icon-wrap">{icon_bar_chart()}</div>
            <h3>Distribusi Hasil Akhir Mahasiswa</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    final_result_count = (
        merged_data["final_result"].value_counts()
        if "final_result" in merged_data.columns
        else pd.Series(dtype=int)
    )

    if not final_result_count.empty:
        fig, ax = plt.subplots(figsize=(7, 4.5))
        final_result_count.plot(kind="bar", ax=ax)
        ax.set_title("Distribusi Final Result")
        ax.set_xlabel("Final Result")
        ax.set_ylabel("Jumlah Mahasiswa")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        st.pyplot(fig)
        st.dataframe(
            final_result_count.reset_index().rename(
                columns={"index": "final_result", "final_result": "jumlah_mahasiswa"}
            ),
            use_container_width=True,
        )
    else:
        st.info("Kolom final_result tidak tersedia.")

with right:
    st.markdown(
        f"""
        <div class="section-title">
            <div class="icon-wrap">{icon_academic()}</div>
            <h3>Ringkasan Assessment Completion</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if "assessment_completion_rate" in merged_data.columns:
        summary_completion = merged_data["assessment_completion_rate"].describe().round(4)
        st.dataframe(summary_completion.to_frame("value"), use_container_width=True)

        fig, ax = plt.subplots(figsize=(7, 4.5))
        merged_data.groupby("final_result")["assessment_completion_rate"].mean().plot(kind="bar", ax=ax)
        ax.set_title("Assessment Completion Rate per Final Result")
        ax.set_xlabel("Final Result")
        ax.set_ylabel("Completion Rate")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        st.pyplot(fig)
    else:
        st.info("Kolom assessment_completion_rate tidak tersedia.")

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="section-title">
        <div class="icon-wrap">{icon_warning()}</div>
        <h3>Persentase Final Result per Modul</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

if {"code_module", "final_result"}.issubset(merged_data.columns):
    module_result_pct = pd.crosstab(
        merged_data["code_module"],
        merged_data["final_result"],
        normalize="index",
    ) * 100

    st.dataframe(module_result_pct.round(2), use_container_width=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    module_result_pct.plot(kind="bar", stacked=True, ax=ax)
    ax.set_title("Persentase Final Result per Modul")
    ax.set_xlabel("Code Module")
    ax.set_ylabel("Persentase (%)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    st.pyplot(fig)
else:
    st.info("Kolom code_module/final_result tidak tersedia.")

st.markdown("<hr>", unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    st.markdown(
        f"""
        <div class="section-title">
            <div class="icon-wrap">{icon_bar_chart()}</div>
            <h3>Aktivitas VLE</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    vle_cols = [c for c in ["total_clicks", "active_days"] if c in merged_data.columns]
    if "final_result" in merged_data.columns and vle_cols:
        vle_summary = merged_data.groupby("final_result")[vle_cols].mean().round(2)
        st.dataframe(vle_summary, use_container_width=True)

        if "total_clicks" in merged_data.columns:
            fig, ax = plt.subplots(figsize=(7, 4.5))
            merged_data.groupby("final_result")["total_clicks"].mean().plot(kind="bar", ax=ax)
            ax.set_title("Rata-rata Total Clicks")
            ax.set_xlabel("Final Result")
            ax.set_ylabel("Rata-rata Total Clicks")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            st.pyplot(fig)
    else:
        st.info("Kolom aktivitas VLE tidak lengkap.")

with col_b:
    st.markdown(
        f"""
        <div class="section-title">
            <div class="icon-wrap">{icon_academic()}</div>
            <h3>Performa Asesmen</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    assessment_cols = [c for c in ["avg_score", "assessment_completion_rate"] if c in merged_data.columns]
    if "final_result" in merged_data.columns and assessment_cols:
        assessment_summary = merged_data.groupby("final_result")[assessment_cols].mean().round(2)
        st.dataframe(assessment_summary, use_container_width=True)

        if "avg_score" in merged_data.columns:
            fig, ax = plt.subplots(figsize=(7, 4.5))
            merged_data.groupby("final_result")["avg_score"].mean().plot(kind="bar", ax=ax)
            ax.set_title("Rata-rata Avg Score")
            ax.set_xlabel("Final Result")
            ax.set_ylabel("Rata-rata Avg Score")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            st.pyplot(fig)
    else:
        st.info("Kolom asesmen tidak lengkap.")

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="section-title">
        <div class="icon-wrap">{icon_warning()}</div>
        <h3>Model Performance</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

if model_comparison is not None:
    st.markdown(
        '<div class="small-note">Tabel berikut menampilkan perbandingan performa model prediktif yang digunakan untuk mendukung sistem early warning.</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(model_comparison, use_container_width=True)

    numeric_plot_col = None
    for candidate in ["F1-Score", "F1_Score", "Recall", "Accuracy"]:
        if candidate in model_comparison.columns:
            numeric_plot_col = candidate
            break

    if numeric_plot_col is not None and "Model" in model_comparison.columns:
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.bar(model_comparison["Model"], model_comparison[numeric_plot_col])
        ax.set_title(f"Perbandingan {numeric_plot_col}")
        ax.set_xlabel("Model")
        ax.set_ylabel(numeric_plot_col)
        ax.set_ylim(0, 1)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        st.pyplot(fig)
else:
    st.info("File model_comparison.csv belum tersedia di folder data/output.")

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="section-title">
        <div class="icon-wrap">{icon_bar_chart()}</div>
        <h3>Feature Importance Decision Tree</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

if feature_importance_dt is not None and {"feature", "importance"}.issubset(feature_importance_dt.columns):
    top_features = feature_importance_dt.head(10)
    st.dataframe(top_features, use_container_width=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top_features["feature"][::-1], top_features["importance"][::-1])
    ax.set_title("Top 10 Feature Importance")
    ax.set_xlabel("Importance")
    ax.set_ylabel("Feature")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    st.pyplot(fig)
else:
    st.info("File feature_importance_dt.csv belum tersedia atau formatnya belum sesuai.")

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="section-title">
        <div class="icon-wrap">{icon_users()}</div>
        <h3>Daftar Mahasiswa Berisiko</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

if at_risk_students is not None:
    st.markdown(
        '<div class="small-note">Bagian ini menampilkan sampel mahasiswa yang masuk kategori berisiko dan dapat diprioritaskan untuk intervensi.</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(at_risk_students.head(20), use_container_width=True)
else:
    if "risk_label" in merged_data.columns:
        risk_cols = [
            c for c in [
                "id_student",
                "code_module",
                "code_presentation",
                "final_result",
                "risk_label",
                "total_clicks",
                "avg_score",
                "assessment_completion_rate",
            ]
            if c in merged_data.columns
        ]
        st.dataframe(
            merged_data[merged_data["risk_label"] == 1][risk_cols].head(20),
            use_container_width=True,
        )
    else:
        st.info("Data mahasiswa berisiko belum tersedia.")

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="card">
        <div class="section-title" style="margin-top:0;">
            <div class="icon-wrap">{icon_warning()}</div>
            <h3>Interpretasi Singkat</h3>
        </div>
        <div class="small-note">
            Dashboard ini memperlihatkan bahwa pola <span class="highlight">aktivitas VLE</span>,
            <span class="highlight">performa asesmen</span>, dan <span class="highlight">hasil model prediktif</span>
            dapat digunakan bersama untuk mendukung proses deteksi dini mahasiswa berisiko.
            Modul dengan persentase fail atau withdrawal yang lebih tinggi perlu mendapat perhatian lebih awal,
            sementara daftar mahasiswa berisiko dapat dipakai sebagai dasar intervensi akademik.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)