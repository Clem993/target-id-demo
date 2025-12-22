"""
Excelra Novel Target Identification Demo
Interactive demonstration of WGCNA + Bayesian Network target discovery
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import json
import time
import base64
from pathlib import Path

# Get asset paths
ASSETS_DIR = Path(__file__).parent / "assets"

def get_base64_image(image_path):
    """Convert image to base64 for embedding"""
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

# Load favicon
favicon_path = ASSETS_DIR / "Target.png"

# Page configuration
st.set_page_config(
    page_title="Excelra | Novel Target Identification",
    page_icon=str(favicon_path) if favicon_path.exists() else None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Brand assets
logo_b64 = get_base64_image(ASSETS_DIR / "Logo.png")
slogan_b64 = get_base64_image(ASSETS_DIR / "Slogan.png")

# Page icons
icon_helix = get_base64_image(ASSETS_DIR / "Helix.png")
icon_analysis = get_base64_image(ASSETS_DIR / "Analysis.png")
icon_network = get_base64_image(ASSETS_DIR / "Network.png")
icon_stats = get_base64_image(ASSETS_DIR / "Stats.png")

# Workflow icons
icon_gene = get_base64_image(ASSETS_DIR / "Gene.png")
icon_genetic = get_base64_image(ASSETS_DIR / "genetic.png")
icon_expression = get_base64_image(ASSETS_DIR / "expression.png")
icon_bar_chart = get_base64_image(ASSETS_DIR / "Bar_chart.png")
icon_pie_chart = get_base64_image(ASSETS_DIR / "Pie_chart.png")
icon_clinical = get_base64_image(ASSETS_DIR / "Clinical.png")

# Additional icons
icon_controls = get_base64_image(ASSETS_DIR / "Controls.png")
icon_configure = get_base64_image(ASSETS_DIR / "Configure.png")
icon_input = get_base64_image(ASSETS_DIR / "Input.png")
icon_novel = get_base64_image(ASSETS_DIR / "Novel.png")
icon_prioritised = get_base64_image(ASSETS_DIR / "Prioritised.png")
icon_start = get_base64_image(ASSETS_DIR / "Start.png")
icon_e_logo = get_base64_image(ASSETS_DIR / "e logo.png")
icon_target = get_base64_image(ASSETS_DIR / "Target.png")
icon_data_acquisition = get_base64_image(ASSETS_DIR / "Data acquisition.png")

# Wave backgrounds
wave_b64 = get_base64_image(ASSETS_DIR / "Wave.png")
wave2_b64 = get_base64_image(ASSETS_DIR / "Wave2.png")

# EXCELRA BRAND COLOURS
NAVY = "#0A1E4A"
TEAL = "#00A6A6"
MAGENTA = "#E04F8A"
PURPLE = "#A24DBE"
MINT = "#B8FEEF"
LIGHT_BLUE = "#CFE3F9"
LAVENDER = "#C4BFDF"
LIGHT_PINK = "#F7D6E6"

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Force Poppins everywhere */
    *, *::before, *::after { 
        font-family: 'Poppins', sans-serif !important; 
    }
    
    html, body, div, span, p, h1, h2, h3, h4, h5, h6, label, input, button, select, textarea {
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* White background */
    .stApp { background: #FFFFFF; }
    
    /* Sidebar - OFF-WHITE */
    section[data-testid="stSidebar"] { 
        background: #F8F9FA;
        border-right: 1px solid #E8E8E8;
    }
    section[data-testid="stSidebar"] > div { 
        color: #0A1E4A !important; 
        font-family: 'Poppins', sans-serif !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label { 
        color: #0A1E4A !important; 
    }
    section[data-testid="stSidebar"] hr { border-color: rgba(10,30,74,0.1); }
    section[data-testid="stSidebar"] .stButton > button {
        background: #0A1E4A !important;
        color: white !important;
        font-family: 'Poppins', sans-serif !important;
        border: none !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #E04F8A !important;
        color: white !important;
    }
    section[data-testid="stSidebar"] .stButton > button p,
    section[data-testid="stSidebar"] .stButton > button span {
        color: white !important;
    }
    
    /* Metric cards - MAGENTA accent, uniform size */
    .metric-card {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 1.5rem;
        border: 1px solid #E8E8E8;
        border-left: 5px solid #E04F8A;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-sizing: border-box;
    }
    .metric-card h3 {
        color: #0A1E4A !important;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
    }
    .metric-card .value {
        color: #00A6A6 !important;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }
    
    /* Section headers with MAGENTA underline */
    .section-header {
        color: #0A1E4A !important;
        font-size: 1.2rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #E04F8A;
        display: inline-flex;
        align-items: center;
        gap: 14px;
    }
    .section-header img {
        width: 44px;
        height: 44px;
    }
    
    /* Step cards - uniform size */
    .step-card {
        text-align: center;
        padding: 1.5rem 0.6rem;
        background: #FFFFFF;
        border-radius: 10px;
        border: 1px solid #E8E8E8;
        border-top: 4px solid #00A6A6;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-sizing: border-box;
    }
    .step-card:hover { 
        box-shadow: 0 6px 16px rgba(224,79,138,0.15);
        border-top-color: #E04F8A;
    }
    .step-icon { margin-bottom: 0.6rem; }
    .step-icon img { width: 60px; height: 60px; }
    .step-number { font-size: 1.4rem; color: #00A6A6; font-weight: 700; }
    .step-name { font-size: 0.75rem; color: #0A1E4A; font-weight: 500; line-height: 1.3; margin-top: 0.35rem; }
    
    /* Hub gene badge - MAGENTA gradient */
    .hub-gene {
        background: linear-gradient(90deg, #E04F8A 0%, #A24DBE 100%);
        color: #FFFFFF !important;
        padding: 0.3rem 0.8rem;
        border-radius: 14px;
        font-weight: 600;
        font-size: 0.8rem;
        display: inline-block;
        margin: 0.15rem;
    }
    
    /* Info box - uniform styling */
    .info-box {
        background: #FFF9FB;
        border-radius: 10px;
        padding: 1.25rem;
        border-left: 5px solid #E04F8A;
        margin: 1rem 0;
        min-height: 80px;
        box-sizing: border-box;
    }
    .info-box h4 { color: #0A1E4A !important; margin: 0 0 0.5rem 0; font-weight: 600; font-size: 0.95rem; }
    .info-box p { color: #0A1E4A !important; margin: 0; font-size: 0.88rem; }
    
    /* Success box - uniform styling */
    .success-box {
        background: #F5FFFE;
        border-radius: 10px;
        padding: 1.25rem;
        border-left: 5px solid #00A6A6;
        margin: 1rem 0;
        min-height: 80px;
        box-sizing: border-box;
    }
    .success-box p { color: #0A1E4A !important; margin: 0; font-size: 0.88rem; line-height: 1.8; }
    
    /* Text colours */
    .stMarkdown, .stMarkdown p, .stMarkdown li { color: #0A1E4A !important; font-family: 'Poppins', sans-serif !important; }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 { color: #0A1E4A !important; font-family: 'Poppins', sans-serif !important; }
    
    /* Force Poppins on Streamlit elements */
    [data-testid="stMarkdownContainer"] * { font-family: 'Poppins', sans-serif !important; }
    .stSelectbox, .stSlider, .stTextInput { font-family: 'Poppins', sans-serif !important; }
    
    /* Slider thumb (circle) - gradient */
    div[data-baseweb="slider"] div[role="slider"] {
        background: linear-gradient(135deg, #E04F8A 0%, #00A6A6 100%) !important;
        border: 2px solid white !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
    }
    /* Slider track fill (left of thumb) - magenta */
    div[data-baseweb="slider"] > div > div:nth-child(3),
    div[data-baseweb="slider"] > div > div > div:first-child {
        background: #E04F8A !important;
    }
    /* Slider value text */
    .stSlider [data-testid="stThumbValue"] {
        color: #00A6A6 !important;
    }
    .stDataFrame { font-family: 'Poppins', sans-serif !important; }
    .stExpander { font-family: 'Poppins', sans-serif !important; }
    .stCaption { font-family: 'Poppins', sans-serif !important; }
    
    /* Tabs - BETTER SPACING */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 12px; 
        background: #F5F5F5; 
        padding: 8px; 
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] { 
        background: transparent; 
        border-radius: 8px; 
        color: #0A1E4A; 
        font-weight: 500;
        font-family: 'Poppins', sans-serif !important;
        padding: 10px 20px;
        white-space: nowrap;
    }
    .stTabs [aria-selected="true"] { 
        background: #E04F8A; 
        color: #FFFFFF !important; 
    }
    
    /* Buttons - Gradient magenta to turquoise */
    .stButton > button {
        background: linear-gradient(90deg, #E04F8A 0%, #00A6A6 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px;
        font-weight: 600;
        font-family: 'Poppins', sans-serif !important;
        padding: 0.6rem 1.5rem;
    }
    .stButton > button:hover { 
        background: linear-gradient(90deg, #C93D75 0%, #008A8A 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(224,79,138,0.3);
    }
    
    /* Progress bar - gradient */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #E04F8A 0%, #A24DBE 50%, #0A1E4A 100%);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] { color: #00A6A6 !important; font-weight: 600; font-family: 'Poppins', sans-serif !important; }
    [data-testid="stMetricLabel"] { color: #0A1E4A !important; font-family: 'Poppins', sans-serif !important; }
    
    /* Uniform metric container height */
    [data-testid="metric-container"] {
        background: #FFFFFF;
        border: 1px solid #E8E8E8;
        border-radius: 10px;
        padding: 1rem;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* Hide Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Sidebar logo - NO white box */
    .sidebar-logo {
        padding: 1.25rem 0.5rem;
        text-align: center;
        margin-bottom: 0.75rem;
    }
    .sidebar-logo img { max-width: 170px; }
    
    /* Sidebar slogan */
    .sidebar-slogan { text-align: center; padding: 0.75rem; margin-top: 0.5rem; }
    .sidebar-slogan img { max-width: 140px; }
    
    /* Footer slogan - centered at bottom */
    .footer-slogan {
        text-align: center;
        padding: 3rem 1rem 2rem 1rem;
        margin-top: 3rem;
    }
    .footer-slogan img {
        max-width: 280px;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load the analysis data"""
    data_path = Path(__file__).parent / "data" / "pruritus_data.json"
    with open(data_path, 'r') as f:
        return json.load(f)


def icon_img(icon_b64, size=44):
    """Generate inline icon HTML"""
    if icon_b64:
        return f'<img src="data:image/png;base64,{icon_b64}" width="{size}" height="{size}" style="vertical-align: middle;">'
    return ""


def create_network_graph(data, highlight_hub=None):
    """Create an interactive network visualisation"""
    G = nx.Graph()
    
    genes_df = pd.DataFrame(data['module_genes'])
    for _, row in genes_df.iterrows():
        G.add_node(row['gene'], 
                   connections=row['connections'],
                   is_hub=row['is_hub'],
                   category=row['category'],
                   kme=row['kme'])
    
    for edge in data['network_edges']:
        if edge['source'] in G.nodes() and edge['target'] in G.nodes():
            G.add_edge(edge['source'], edge['target'])
    
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.5, color=LAVENDER),
        hoverinfo='none',
        mode='lines',
        opacity=0.5
    )
    
    node_x, node_y, node_text, node_color, node_size = [], [], [], [], []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        node_data = G.nodes[node]
        text = f"<b>{node}</b><br>Category: {node_data['category']}<br>Connections: {node_data['connections']}<br>kME: {node_data['kme']:.2f}"
        if node_data['is_hub']:
            text += "<br><b>HUB GENE</b>"
        node_text.append(text)
        
        if highlight_hub and node == highlight_hub:
            node_color.append(MAGENTA)
            node_size.append(50)
        elif node_data['is_hub']:
            node_color.append(TEAL)
            node_size.append(40)
        else:
            node_color.append(NAVY)
            node_size.append(18 + node_data['connections'] * 1.5)
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=[n for n in G.nodes()],
        textposition="top center",
        textfont=dict(size=9, color=NAVY, family='Poppins'),
        hovertext=node_text,
        marker=dict(size=node_size, color=node_color, line=dict(width=2, color='white'))
    )
    
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=10, l=10, r=10, t=10),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        plot_bgcolor='#FAFAFA',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=420,
                        font=dict(family='Poppins')
                    ))
    return fig


def create_module_heatmap(data):
    """Create module-trait correlation heatmap"""
    modules = [f"Module {i}" for i in range(1, 13)]
    traits = ['Disease Status', 'Severity Score', 'Itch Intensity', 'Inflammation']
    
    import numpy as np
    np.random.seed(42)
    correlations = np.random.uniform(-0.3, 0.3, (12, 4))
    correlations[4, 0] = 0.78
    correlations[4, 1] = 0.65
    correlations[4, 2] = 0.72
    correlations[4, 3] = 0.58
    
    fig = go.Figure(data=go.Heatmap(
        z=correlations, x=traits, y=modules,
        colorscale=[[0, NAVY], [0.5, '#FFFFFF'], [1, TEAL]],
        zmid=0,
        text=[[f"{v:.2f}" for v in row] for row in correlations],
        texttemplate="%{text}",
        textfont={"size": 9, "family": "Poppins"},
        hovertemplate="Module: %{y}<br>Trait: %{x}<br>Correlation: %{z:.2f}<extra></extra>"
    ))
    
    fig.update_layout(
        height=380,
        margin=dict(l=90, r=20, t=20, b=40),
        font=dict(family='Poppins', color=NAVY)
    )
    return fig


def create_clinical_pipeline_chart(data):
    """Create clinical pipeline visualisation"""
    clinical_df = pd.DataFrame(data['clinical_validation'])
    
    phase_order = {'Phase I': 1, 'Phase II': 2, 'Phase III': 3, 'Approved': 4}
    clinical_df['phase_num'] = clinical_df['phase'].map(phase_order)
    
    phase_colors = {'Phase I': LIGHT_PINK, 'Phase II': MAGENTA, 'Phase III': TEAL, 'Approved': NAVY}
    clinical_df['color'] = clinical_df['phase'].map(phase_colors)
    
    fig = go.Figure()
    
    for i, row in clinical_df.iterrows():
        text_color = 'white' if row['phase'] in ['Phase II', 'Phase III', 'Approved'] else NAVY
        fig.add_trace(go.Bar(
            x=[row['phase_num']], y=[row['drug']],
            orientation='h',
            marker_color=row['color'],
            text=f"{row['gene']} | {row['company']}",
            textposition='inside',
            textfont=dict(family='Poppins', size=9, color=text_color),
            hovertemplate=f"<b>{row['drug']}</b><br>Target: {row['gene']}<br>Phase: {row['phase']}<br>Company: {row['company']}<extra></extra>",
            showlegend=False
        ))
    
    fig.update_layout(
        xaxis=dict(
            tickmode='array', tickvals=[1, 2, 3, 4],
            ticktext=['Phase I', 'Phase II', 'Phase III', 'Approved'],
            title=dict(text='Development Stage', font=dict(family='Poppins', color=NAVY, size=11)),
            tickfont=dict(family='Poppins', color=NAVY)
        ),
        yaxis=dict(title='', tickfont=dict(family='Poppins', color=NAVY)),
        height=380,
        margin=dict(l=140, r=20, t=20, b=40),
        barmode='stack',
        font=dict(family='Poppins')
    )
    return fig


def run_analysis_simulation(data):
    """Simulate the analysis workflow"""
    steps = data['workflow_steps']
    
    st.markdown(f"<p class='section-header'>{icon_img(icon_bar_chart)} Analysis Progress</p>", unsafe_allow_html=True)
    progress_bar = st.progress(0)
    status_text = st.empty()
    metrics_cols = st.columns(4)
    
    metric_placeholders = {
        'genes': metrics_cols[0].empty(),
        'modules': metrics_cols[1].empty(),
        'hub_genes': metrics_cols[2].empty(),
        'targets': metrics_cols[3].empty()
    }
    
    step_container = st.empty()
    total_steps = len(steps)
    
    for i, step in enumerate(steps):
        progress = (i + 1) / total_steps
        progress_bar.progress(progress)
        status_text.markdown(f"**Step {step['step']}/{total_steps}:** {step['name']}")
        
        with step_container.container():
            st.info(step['description'])
            
            if 'genes_after_qc' in step['metrics']:
                metric_placeholders['genes'].metric("Genes Analysed", f"{step['metrics']['genes_after_qc']:,}")
            if 'modules_identified' in step['metrics']:
                metric_placeholders['modules'].metric("Modules Found", step['metrics']['modules_identified'])
            if 'hub_genes' in step['metrics']:
                metric_placeholders['hub_genes'].metric("Hub Genes", step['metrics']['hub_genes'])
            if 'total_prioritised' in step['metrics']:
                metric_placeholders['targets'].metric("Targets Prioritised", step['metrics']['total_prioritised'])
        
        time.sleep(1.5)
    
    status_text.markdown("**Analysis Complete**")
    metric_placeholders['genes'].metric("Genes Analysed", "25,000")
    metric_placeholders['modules'].metric("Modules Found", "12")
    metric_placeholders['hub_genes'].metric("Hub Genes", "4")
    metric_placeholders['targets'].metric("Targets Prioritised", "7")
    return True


def render_header(icon_b64, title, subtitle):
    """Render page header with wave background"""
    wave_bg = ""
    if wave_b64:
        wave_bg = f"""
            background-image: url('data:image/png;base64,{wave_b64}');
            background-position: center;
            background-repeat: no-repeat;
            background-size: 100% auto;
        """
    
    if icon_b64:
        st.markdown(f"""
        <div style="background-color:#F8F9FA;padding:2.5rem;border-radius:12px;margin-bottom:1.5rem;display:flex;align-items:center;border:1px solid #E8E8E8;position:relative;overflow:hidden;">
            <div style="position:absolute;top:0;left:0;right:0;bottom:0;{wave_bg}opacity:0.4;"></div>
            <div style="background:white;border:4px solid #0A1E4A;padding:16px;border-radius:14px;display:flex;align-items:center;justify-content:center;margin-right:24px;position:relative;z-index:1;">
                <img src="data:image/png;base64,{icon_b64}" width="64" height="64">
            </div>
            <div style="position:relative;z-index:1;">
                <div style="color:#0A1E4A;font-size:1.85rem;font-weight:600;margin:0;font-family:Poppins,sans-serif;">{title}</div>
                <div style="color:#00A6A6;font-size:1.05rem;margin-top:0.5rem;font-family:Poppins,sans-serif;">{subtitle}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background-color:#F8F9FA;padding:2.5rem;border-radius:12px;margin-bottom:1.5rem;border:1px solid #E8E8E8;position:relative;overflow:hidden;">
            <div style="position:absolute;top:0;left:0;right:0;bottom:0;{wave_bg}opacity:0.4;"></div>
            <div style="position:relative;z-index:1;">
                <div style="color:#0A1E4A;font-size:1.85rem;font-weight:600;margin:0;font-family:Poppins,sans-serif;">{title}</div>
                <div style="color:#00A6A6;font-size:1.05rem;margin-top:0.5rem;font-family:Poppins,sans-serif;">{subtitle}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_footer():
    """Render footer with slogan centered at bottom of page"""
    if slogan_b64:
        st.markdown(f"""
        <div class='footer-slogan'>
            <img src='data:image/png;base64,{slogan_b64}' alt='Where data means more'>
        </div>
        """, unsafe_allow_html=True)


def main():
    data = load_data()
    
    # Sidebar
    with st.sidebar:
        if logo_b64:
            st.markdown(f"<div class='sidebar-logo'><img src='data:image/png;base64,{logo_b64}' alt='Excelra'></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("**Navigation**")
        
        nav_options = ["Overview", "Run Analysis", "Network Explorer", "Results Dashboard"]
        
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Overview"
        
        for nav_name in nav_options:
            if st.button(nav_name, key=f"nav_{nav_name}", use_container_width=True):
                st.session_state.current_page = nav_name
                st.rerun()
        
        st.markdown("---")
        st.markdown("**Demo Settings**")
        st.selectbox("Disease Area", ["Atopic Dermatitis / Pruritus", "Alzheimer's Disease (Coming Soon)"], index=0, label_visibility="collapsed")
        
        st.markdown("---")
        st.caption("Demo Version 1.0")
    
    # Main content
    page = st.session_state.current_page
    
    if page == "Overview":
        show_overview_page(data)
    elif page == "Run Analysis":
        show_analysis_page(data)
    elif page == "Network Explorer":
        show_network_page(data)
    elif page == "Results Dashboard":
        show_results_page(data)


def show_overview_page(data):
    """Overview page"""
    render_header(icon_target, "Novel Target Identification", "Data-driven, unbiased target discovery using WGCNA & Bayesian Networks")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='metric-card'><h3>Delivery Time</h3><p class='value'>8-10 Weeks</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'><h3>Methodology</h3><p class='value'>WGCNA + Bayesian</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'><h3>Data Assets</h3><p class='value'>GOSTAR + GoBiom</p></div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='metric-card'><h3>Expert Team</h3><p class='value'>SME + Data + Tech</p></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Workflow - LARGER ICONS
    st.markdown(f"<p class='section-header'>{icon_img(icon_e_logo)} Our Approach</p>", unsafe_allow_html=True)
    
    workflow_cols = st.columns(7)
    step_data = [
        (icon_data_acquisition, "Data Acquisition"),
        (icon_pie_chart, "WGCNA Modules"),
        (icon_bar_chart, "Module-Trait Correlation"),
        (icon_gene, "Hub Gene ID"),
        (icon_network, "Bayesian Network"),
        (icon_genetic, "Knock-Out Simulation"),
        (icon_clinical, "Clinical Validation")
    ]
    
    for i, (col, (step_icon, name)) in enumerate(zip(workflow_cols, step_data), 1):
        with col:
            icon_html = f'<img src="data:image/png;base64,{step_icon}" width="60" height="60">' if step_icon else ""
            st.markdown(f"""
            <div class='step-card'>
                <div class='step-icon'>{icon_html}</div>
                <div class='step-number'>{i}</div>
                <div class='step-name'>{name}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Case study
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"<p class='section-header'>{icon_img(icon_clinical)} Demo Case Study: Atopic Dermatitis</p>", unsafe_allow_html=True)
        
        st.markdown(f"""
**Disease:** {data['disease']['name']}

**Therapeutic Area:** {data['disease']['therapeutic_area']}

**Description:** {data['disease']['description']}

**Unmet Need:** {data['disease']['unmet_need']}
        """)
        
        st.markdown(f"""
        <div class='success-box'>
            <p>
            <strong>{data['analysis_metadata']['total_genes_analysed']:,}</strong> genes analysed<br>
            <strong>{data['analysis_metadata']['modules_identified']}</strong> co-expression modules identified<br>
            <strong>{data['analysis_metadata']['hub_genes_identified']}</strong> hub genes validated against approved drugs<br>
            <strong>3</strong> novel targets identified for preclinical pursuit
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<p class='section-header'>{icon_img(icon_start)} Quick Start</p>", unsafe_allow_html=True)
        
        if st.button("Run Demo Analysis", type="primary", use_container_width=True):
            st.session_state.current_page = "Run Analysis"
            st.rerun()
        
        st.markdown("")
        
        if st.button("Explore Network", use_container_width=True):
            st.session_state.current_page = "Network Explorer"
            st.rerun()
        
        st.markdown("")
        
        if st.button("View Results", use_container_width=True):
            st.session_state.current_page = "Results Dashboard"
            st.rerun()
    
    render_footer()


def show_analysis_page(data):
    """Analysis page"""
    render_header(icon_analysis, "Run Target Identification Analysis", "Simulated workflow demonstration")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"<p class='section-header'>{icon_img(icon_configure)} Input Configuration</p>", unsafe_allow_html=True)
        
        st.selectbox("Disease Area", ["Atopic Dermatitis / Pruritus"])
        st.selectbox("Data Source", ["GEO: GSE32924 (64 samples)", "Client Proprietary Data"])
        st.slider("Minimum Module Size", 20, 100, 30)
        st.slider("Hub Gene Threshold (kME)", 0.5, 0.9, 0.7)
        
        st.markdown("---")
        run_button = st.button("Start Analysis", type="primary", use_container_width=True)
    
    with col2:
        if run_button:
            with st.spinner("Initialising analysis pipeline..."):
                time.sleep(1)
            run_analysis_simulation(data)
            st.success("Analysis complete! Navigate to Results Dashboard to explore findings.")
        else:
            st.markdown(f"""
            <div class='info-box'>
                <h4>Configure and Run</h4>
                <p>Set your parameters and click 'Start Analysis' to begin the demonstration workflow.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<p class='section-header'>{icon_img(icon_input)} Sample Input Data Preview</p>", unsafe_allow_html=True)
            
            import numpy as np
            np.random.seed(42)
            sample_genes = ['JAK1', 'IL4R', 'IL13', 'IL22', 'NTRK1', 'STAT3', 'STAT6', 'GRB2']
            sample_ids = [f"GSM{800000+i}" for i in range(8)]
            expression_data = np.random.lognormal(mean=5, sigma=1, size=(8, 8))
            
            sample_df = pd.DataFrame(expression_data, index=sample_genes, columns=sample_ids).round(2)
            st.dataframe(sample_df, use_container_width=True)
            st.caption("Sample gene expression matrix (log2 normalised)")
    
    render_footer()


def show_network_page(data):
    """Network explorer page"""
    render_header(icon_network, "Gene Network Explorer", "Interactive visualisation of disease-relevant gene module")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.markdown(f"<p class='section-header'>{icon_img(icon_controls)} Controls</p>", unsafe_allow_html=True)
        
        genes_df = pd.DataFrame(data['module_genes'])
        hub_genes = genes_df[genes_df['is_hub']]['gene'].tolist()
        
        selected_gene = st.selectbox("Highlight Gene", ["None"] + genes_df['gene'].tolist())
        
        st.markdown("---")
        st.markdown("**Module Statistics**")
        st.metric("Total Genes", len(genes_df))
        st.metric("Hub Genes", len(hub_genes))
        st.metric("Network Edges", len(data['network_edges']))
        
        st.markdown("---")
        st.markdown("**Hub Genes**")
        for gene in hub_genes:
            st.markdown(f"<span class='hub-gene'>{gene}</span>", unsafe_allow_html=True)
    
    with col1:
        highlight = selected_gene if selected_gene != "None" else None
        fig = create_network_graph(data, highlight_hub=highlight)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown(f"<p class='section-header'>{icon_img(icon_gene)} Gene Details</p>", unsafe_allow_html=True)
        
        if selected_gene and selected_gene != "None":
            gene_data = genes_df[genes_df['gene'] == selected_gene].iloc[0]
            
            detail_cols = st.columns(4)
            detail_cols[0].metric("Gene", gene_data['gene'])
            detail_cols[1].metric("Connections", gene_data['connections'])
            detail_cols[2].metric("kME Score", f"{gene_data['kme']:.2f}")
            detail_cols[3].metric("Category", gene_data['category'])
            
            clinical_df = pd.DataFrame(data['clinical_validation'])
            gene_drugs = clinical_df[clinical_df['gene'] == selected_gene]
            
            if not gene_drugs.empty:
                st.markdown("**Drugs Targeting This Gene**")
                st.dataframe(gene_drugs[['drug', 'phase', 'company', 'indication']], use_container_width=True, hide_index=True)
        else:
            st.dataframe(genes_df[['gene', 'connections', 'kme', 'category', 'is_hub']], use_container_width=True, hide_index=True)
    
    render_footer()


def show_results_page(data):
    """Results dashboard page"""
    render_header(icon_stats, "Results Dashboard", "Target prioritisation and clinical validation")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Genes Analysed", f"{data['analysis_metadata']['total_genes_analysed']:,}")
    col2.metric("Disease Modules", data['analysis_metadata']['modules_identified'])
    col3.metric("Validated Targets", "4")
    col4.metric("Novel Targets", "3")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Prioritised Targets", "Module Analysis", "Clinical Pipeline", "Novel Targets"])
    
    with tab1:
        st.markdown(f"<p class='section-header'>{icon_img(icon_prioritised)} Prioritised Target List</p>", unsafe_allow_html=True)
        
        genes_df = pd.DataFrame(data['module_genes'])
        hub_df = genes_df[genes_df['is_hub']].copy()
        hub_df['Priority'] = ['High', 'High', 'High', 'High']
        hub_df['Validation'] = ['4 approved drugs', '1 approved drug', '2 approved drugs', '1 Phase II']
        
        st.dataframe(
            hub_df[['gene', 'connections', 'kme', 'category', 'Priority', 'Validation']].rename(
                columns={'gene': 'Gene', 'connections': 'Network Connections', 'kme': 'Module Membership (kME)', 'category': 'Functional Category'}
            ),
            use_container_width=True, hide_index=True
        )
        
        st.markdown("---")
        st.markdown(f"<p class='section-header'>{icon_img(icon_bar_chart)} Gene Connectivity Ranking</p>", unsafe_allow_html=True)
        
        top_genes = genes_df.nlargest(15, 'connections')
        fig = px.bar(top_genes, x='connections', y='gene', orientation='h', color='is_hub',
                     color_discrete_map={True: MAGENTA, False: NAVY},
                     labels={'connections': 'Network Connections', 'gene': 'Gene', 'is_hub': 'Hub Gene'})
        fig.update_layout(showlegend=True, height=320, yaxis={'categoryorder': 'total ascending'},
                         font=dict(family='Poppins', color=NAVY), margin=dict(l=70, r=20, t=20, b=40))
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown(f"<p class='section-header'>{icon_img(icon_pie_chart)} Module-Trait Correlation Analysis</p>", unsafe_allow_html=True)
        st.markdown("""
WGCNA identified **12 co-expression modules**. Module 5 shows the strongest 
correlation with disease status (r = 0.78, p < 2.3×10⁻⁸) and was selected 
for hub gene identification.
        """)
        
        fig = create_module_heatmap(data)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div class='info-box'>
            <h4>Module 5 Selected</h4>
            <p>Disease-relevant module based on highest correlation with disease phenotype.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown(f"<p class='section-header'>{icon_img(icon_clinical)} Clinical Validation</p>", unsafe_allow_html=True)
        st.markdown("""
Hub genes identified through WGCNA analysis were validated against 
the clinical landscape. **4 of 4 hub genes** have approved drugs 
or drugs in clinical development, confirming methodology accuracy.
        """)
        
        fig = create_clinical_pipeline_chart(data)
        st.plotly_chart(fig, use_container_width=True)
        
        clinical_df = pd.DataFrame(data['clinical_validation'])
        st.markdown("**Drug Details**")
        st.dataframe(clinical_df, use_container_width=True, hide_index=True)
    
    with tab4:
        st.markdown(f"<p class='section-header'>{icon_img(icon_novel)} Novel Target Opportunities</p>", unsafe_allow_html=True)
        st.markdown("""
In addition to validating known targets, the analysis identified 
**3 novel targets** for potential preclinical pursuit.
        """)
        
        novel_df = pd.DataFrame(data['novel_targets'])
        
        for _, row in novel_df.iterrows():
            st.markdown(f"""
            <div style="background:#F8F9FA;border-radius:10px;padding:1.25rem;margin-bottom:1rem;border-left:5px solid #E04F8A;">
                <div style="color:#0A1E4A;font-size:1.1rem;font-weight:600;margin-bottom:1rem;font-family:Poppins,sans-serif;">{row['gene']} <span style="color:#00A6A6;font-weight:500;">Novelty Score: {row['novelty_score']:.0%}</span></div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            col1.metric("Druggability", row['druggability'])
            col2.metric("Novelty Score", f"{row['novelty_score']:.0%}")
            st.markdown(f"**Rationale:** {row['rationale']}")
            st.markdown("---")
        
        st.markdown("---")
        st.markdown(f"<p class='section-header'>Export Options</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        col1.download_button("Download Target List (CSV)", data=pd.DataFrame(data['module_genes']).to_csv(index=False),
                            file_name="excelra_target_list.csv", mime="text/csv")
        col2.download_button("Download Clinical Data (CSV)", data=pd.DataFrame(data['clinical_validation']).to_csv(index=False),
                            file_name="excelra_clinical_validation.csv", mime="text/csv")
    
    render_footer()


if __name__ == "__main__":
    main()
