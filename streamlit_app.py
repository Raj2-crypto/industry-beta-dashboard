import streamlit as st
import pandas as pd
from main import run_industry_analysis
import time

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(
    page_title="Industry Beta Calculator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Custom CSS for Modern Design
# -----------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide tabs - we'll control navigation programmatically */
    .stTabs [data-baseweb="tab-list"] {
        display: none !important;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0 1.5rem 0;
        margin-bottom: 2rem;
    }
    
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1.25rem;
        background: rgba(6, 182, 212, 0.1);
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
        color: #67e8f9;
        margin-bottom: 1rem;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(to right, #ffffff, #67e8f9, #93c5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .sub-title {
        font-size: 2rem;
        color: #94a3b8;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .description {
        font-size: 1.1rem;
        color: #94a3b8;
        max-width: 50rem;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Progress indicator */
    .progress-indicator {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        margin: 1rem 0 2rem 0;
        padding: 1rem;
        background: rgba(15, 23, 42, 0.5);
        border-radius: 0.75rem;
        border: 1px solid rgba(148, 163, 184, 0.2);
    }
    
    .progress-step {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #64748b;
        font-size: 0.875rem;
        font-weight: 600;
    }
    
    .progress-step.completed {
        color: #86efac;
    }
    
    .progress-step.active {
        color: #67e8f9;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .progress-dot {
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 50%;
        background: rgba(100, 116, 139, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1rem;
        border: 2px solid transparent;
    }
    
    .progress-step.completed .progress-dot {
        background: rgba(34, 197, 94, 0.3);
        border-color: #86efac;
    }
    
    .progress-step.active .progress-dot {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.4), rgba(59, 130, 246, 0.4));
        border-color: #67e8f9;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
    }
    
    .progress-arrow {
        color: #64748b;
        font-size: 1.5rem;
    }
    
    .progress-arrow.active {
        color: #67e8f9;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    /* Section Cards */
    .section-card {
        background: rgba(15, 23, 42, 0.5);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 1rem;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
    }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
    }
    
    /* Search box */
    .stTextInput > div > div > input {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 0.75rem;
        color: white;
        padding: 1rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(6, 182, 212, 0.5);
        box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1);
    }
    
    /* Text area */
    .stTextArea > div > div > textarea {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 0.75rem;
        color: white;
        padding: 1rem;
        font-size: 1rem;
        font-family: 'Courier New', monospace;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(6, 182, 212, 0.5);
        box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1);
    }
    
    /* DataFrame styling */
    .stDataFrame {
        background: rgba(15, 23, 42, 0.3);
        border-radius: 0.75rem;
        overflow: hidden;
    }
    
    /* Table styling */
    table {
        color: #e2e8f0 !important;
    }
    
    thead tr th {
        background: rgba(30, 41, 59, 0.5) !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
        padding: 1rem !important;
        border-bottom: 1px solid rgba(100, 116, 139, 0.3) !important;
    }
    
    tbody tr {
        border-bottom: 1px solid rgba(100, 116, 139, 0.2) !important;
    }
    
    tbody tr:hover {
        background: rgba(30, 41, 59, 0.3) !important;
    }
    
    tbody tr td {
        padding: 1rem !important;
        color: #e2e8f0 !important;
    }
    
    /* Ticker badges */
    .ticker-badge {
        display: inline-block;
        background: rgba(6, 182, 212, 0.1);
        border: 1px solid rgba(6, 182, 212, 0.3);
        color: #67e8f9;
        padding: 0.375rem 0.75rem;
        border-radius: 0.5rem;
        font-family: 'Courier New', monospace;
        font-size: 0.875rem;
        margin: 0.25rem;
    }
    
    /* Alert boxes */
    .info-box {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 0.75rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .info-title {
        font-weight: 600;
        color: #60a5fa;
        margin-bottom: 0.5rem;
        font-size: 0.875rem;
    }
    
    .info-text {
        color: #94a3b8;
        font-size: 0.875rem;
        line-height: 1.5;
    }
    
    .code-block {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 0.5rem;
        font-family: 'Courier New', monospace;
        font-size: 0.875rem;
        color: #67e8f9;
        overflow-x: auto;
    }
    
    /* Success box */
    .success-box {
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 0.75rem;
        padding: 1rem;
        margin: 1rem 0;
        color: #86efac;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(59, 130, 246, 0.1));
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 0.75rem;
        padding: 1.5rem;
        text-align: center;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.25rem;
    }
    
    .metric-description {
        font-size: 0.75rem;
        color: #67e8f9;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(to right, #06b6d4, #3b82f6);
        color: white;
        border: none;
        border-radius: 0.75rem;
        padding: 1rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(6, 182, 212, 0.3);
    }
    
    .stButton > button:hover {
        box-shadow: 0 10px 15px -3px rgba(6, 182, 212, 0.4);
        transform: scale(1.02);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #06b6d4 !important;
    }
    
    /* Back button */
    .back-button {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: rgba(100, 116, 139, 0.2);
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 0.5rem;
        color: #94a3b8;
        font-size: 0.875rem;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
    }
    
    .back-button:hover {
        background: rgba(100, 116, 139, 0.3);
        border-color: rgba(100, 116, 139, 0.5);
        color: #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Initialize Session State
# -----------------------------
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1  # 1=Industry, 2=Tickers, 3=Review, 4=Results
if 'selected_industry' not in st.session_state:
    st.session_state.selected_industry = None
if 'industry_df' not in st.session_state:
    st.session_state.industry_df = None
if 'ticker_input' not in st.session_state:
    st.session_state.ticker_input = ""
if 'tickers' not in st.session_state:
    st.session_state.tickers = []
if 'results' not in st.session_state:
    st.session_state.results = None

# -----------------------------
# Load Industry CSV
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/Companies_list_industry_wise.csv")

# -----------------------------
# Helper Functions
# -----------------------------
def go_to_step(step):
    """Navigate to a specific step"""
    st.session_state.current_step = step

def select_industry(industry):
    """Select an industry and move to next step"""
    df = load_data()
    st.session_state.selected_industry = industry
    st.session_state.industry_df = df[df["Industry Group"] == industry]
    st.session_state.current_step = 2  # Move to ticker input
    st.session_state.results = None  # Reset results

def process_tickers():
    """Process tickers and move to review step"""
    if st.session_state.ticker_input.strip():
        tickers = [t.strip().upper() for t in st.session_state.ticker_input.strip().split('\n') if t.strip()]
        # Remove duplicates
        seen = set()
        unique_tickers = []
        for ticker in tickers:
            if ticker not in seen:
                seen.add(ticker)
                unique_tickers.append(ticker)
        st.session_state.tickers = unique_tickers
        st.session_state.current_step = 3  # Move to review
    else:
        st.error("Please enter at least one ticker symbol")

def run_analysis():
    """Run analysis and move to results step"""
    if st.session_state.tickers:
        try:
            with st.spinner("🔄 Running financial analysis..."):
                df_result, summary = run_industry_analysis(st.session_state.tickers)
                st.session_state.results = {
                    'df': df_result,
                    'summary': summary
                }
                st.session_state.current_step = 4  # Move to results
                time.sleep(0.5)
        except Exception as e:
            st.error(f"❌ Error running analysis: {str(e)}")
    else:
        st.error("No tickers to analyze")

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="main-header">
    <div class="badge">
        📊 INDUSTRY BETA CALCULATOR
    </div>
    <h1 class="main-title">Industry's Beta Dashboard</h1>
    <p class="description">
        Calculate industry-specific beta coefficients and capital structure metrics across global markets
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Progress Indicator
# -----------------------------
step1_class = "completed" if st.session_state.current_step > 1 else "active"
step1_icon = "✓" if st.session_state.current_step > 1 else "1"

step2_class = "completed" if st.session_state.current_step > 2 else ("active" if st.session_state.current_step == 2 else "")
step2_icon = "✓" if st.session_state.current_step > 2 else "2"

step3_class = "completed" if st.session_state.current_step > 3 else ("active" if st.session_state.current_step == 3 else "")
step3_icon = "✓" if st.session_state.current_step > 3 else "3"

step4_class = "active" if st.session_state.current_step == 4 else ""
step4_icon = "4"

arrow1_class = "active" if st.session_state.current_step >= 2 else ""
arrow2_class = "active" if st.session_state.current_step >= 3 else ""
arrow3_class = "active" if st.session_state.current_step >= 4 else ""

progress_html = f"""
<div class="progress-indicator">
    <div class="progress-step {step1_class}">
        <div class="progress-dot">{step1_icon}</div>
        <span>Industry</span>
    </div>
    <div class="progress-arrow {arrow1_class}">→</div>
    <div class="progress-step {step2_class}">
        <div class="progress-dot">{step2_icon}</div>
        <span>Tickers</span>
    </div>
    <div class="progress-arrow {arrow2_class}">→</div>
    <div class="progress-step {step3_class}">
        <div class="progress-dot">{step3_icon}</div>
        <span>Review</span>
    </div>
    <div class="progress-arrow {arrow3_class}">→</div>
    <div class="progress-step {step4_class}">
        <div class="progress-dot">{step4_icon}</div>
        <span>Results</span>
    </div>
</div>
"""

st.markdown(progress_html, unsafe_allow_html=True)

# -----------------------------
# STEP 1: Industry Selection
# -----------------------------
if st.session_state.current_step == 1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <h2 class="section-title">Select Industry</h2>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_data()
    industries = sorted(df["Industry Group"].dropna().unique())
    
    search_term = st.text_input("🔍 Search industries...", "", key="search_industry")
    
    if search_term:
        filtered_industries = [ind for ind in industries if search_term.lower() in ind.lower()]
    else:
        filtered_industries = industries
    
    cols_per_row = 3
    rows = [filtered_industries[i:i + cols_per_row] for i in range(0, len(filtered_industries), cols_per_row)]
    
    for row in rows:
        cols = st.columns(len(row))
        for idx, industry in enumerate(row):
            with cols[idx]:
                company_count = len(df[df["Industry Group"] == industry])
                primary_sector = df[df["Industry Group"] == industry]["Primary Sector"].mode()
                sector_name = primary_sector.iloc[0] if len(primary_sector) > 0 else "N/A"
                
                is_selected = st.session_state.selected_industry == industry
                
                if st.button(
                    f"{'✓ ' if is_selected else ''}{industry}",
                    key=f"ind_{industry}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    select_industry(industry)
                    st.rerun()
                
                st.caption(f"📂 {sector_name}")
                st.caption(f"🏢 {company_count} companies")
    
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# STEP 2: Ticker Input
# -----------------------------
elif st.session_state.current_step == 2:
    # Back button
    if st.button("← Back to Industry Selection", key="back_to_step1"):
        go_to_step(1)
        st.rerun()
    
    st.markdown(f"""
    <div class="success-box">
        ✅ Selected: <strong>{st.session_state.selected_industry}</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # Display companies
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="section-header">
        <h2 class="section-title">Companies in {st.session_state.selected_industry}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    display_df = st.session_state.industry_df[["Company Name", "Country", "Broad Group"]].copy()
    display_df.columns = ["Company", "Country", "Market"]
    st.dataframe(display_df, use_container_width=True, height=300)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Ticker Input
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <h2 class="section-title">Provide Yahoo Finance Tickers</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <div class="info-title">📝 How to Enter Tickers</div>
        <div class="info-text">
            Enter Yahoo Finance ticker symbols for the companies above, one per line.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.ticker_input = st.text_area(
        "Enter tickers (one per line)",
        value=st.session_state.ticker_input,
        height=200,
        placeholder="AAPL\nMSFT\nGOOGL\nBARC.L\nTCS.BO",
        key="ticker_text_area"
    )
    
    st.markdown("""
    <div class="info-box">
        <div class="info-title">📖 Ticker Format Examples</div>
        <div class="code-block">
<span style="color: #64748b;"># US: AAPL, MSFT | UK: BARC.L | India: RELIANCE.NS | Canada: TD.TO</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Continue →", use_container_width=True, type="primary"):
            process_tickers()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# STEP 3: Review Tickers
# -----------------------------
elif st.session_state.current_step == 3:
    # Back button
    if st.button("← Back to Edit Tickers", key="back_to_step2"):
        go_to_step(2)
        st.rerun()
    
    st.markdown(f"""
    <div class="success-box">
        ✅ Industry: <strong>{st.session_state.selected_industry}</strong> | 
        Tickers: <strong>{len(st.session_state.tickers)}</strong>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <h2 class="section-title">Review Tickers</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Tickers", len(st.session_state.tickers))
    with col2:
        st.metric("Companies in Industry", len(st.session_state.industry_df))
    
    st.markdown(f"### 🏷️ Tickers Ready for Analysis")
    ticker_html = "<div style='display: flex; flex-wrap: wrap; gap: 0.5rem;'>"
    for ticker in st.session_state.tickers:
        ticker_html += f'<span class="ticker-badge">{ticker}</span>'
    ticker_html += "</div>"
    st.markdown(ticker_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Run Industry Analysis", use_container_width=True, type="primary"):
            run_analysis()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# STEP 4: Results
# -----------------------------
elif st.session_state.current_step == 4:
    # Start over button
    if st.button("← Start New Analysis", key="start_over"):
        st.session_state.current_step = 1
        st.session_state.selected_industry = None
        st.session_state.ticker_input = ""
        st.session_state.tickers = []
        st.session_state.results = None
        st.rerun()
    
    st.markdown(f"""
    <div class="success-box">
        ✅ Successfully analyzed {st.session_state.results['summary'].get('Successful Analyses', 0)} companies in {st.session_state.selected_industry}
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Key Metrics")
    
    summary = st.session_state.results['summary']
    
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        ("Average Beta", summary.get("Average Beta", "N/A"), "Industry average"),
        ("Median Beta", summary.get("Median Beta", "N/A"), "50th percentile"),
        ("D/E Ratio", summary.get("Average D/E Ratio", "N/A"), "Debt to equity"),
        ("Unlevered Beta", summary.get("Unlevered Beta", "N/A"), "Asset beta")
    ]
    
    for col, (label, value, desc) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-description">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed Data
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📈 Detailed Financial Data")
    st.dataframe(st.session_state.results['df'], use_container_width=True, height=400)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Complete Summary
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Complete Summary")
    
    col1, col2 = st.columns(2)
    summary_items = list(summary.items())
    mid_point = len(summary_items) // 2
    
    with col1:
        for key, value in summary_items[:mid_point]:
            st.metric(label=key, value=value)
    
    with col2:
        for key, value in summary_items[mid_point:]:
            st.metric(label=key, value=value)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Export
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 💾 Export Results")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        csv = st.session_state.results['df'].to_csv(index=False)
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name=f"{st.session_state.selected_industry.replace(' ', '_')}_beta_analysis.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
