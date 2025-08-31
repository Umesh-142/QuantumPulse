import streamlit as st
import requests
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import warnings

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Page config
st.set_page_config(
    page_title="Quantum Data Generator",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    try:
        with open("static/style.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found. Using default styling.")

# Load custom JavaScript
def load_js():
    try:
        with open("static/script.js", "r") as f:
            st.components.v1.html(f"<script>{f.read()}</script>", height=0)
    except FileNotFoundError:
        pass  # JS is optional

# API base URL
API_BASE = "http://localhost:8000"

def main():
    load_css()
    load_js()
    
    # Header
    st.markdown("""
    <div class="header-container">
        <h1 class="main-title">⚛️ Quantum Data Generator</h1>
        <p class="subtitle">AI-Generated Experimental Quantum Data (Synthetic)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-header">Experiment Configuration</div>', unsafe_allow_html=True)
        
        experiment_type = st.selectbox(
            "🔬 Select Experiment Type",
            ["Rabi Oscillations", "T1/T2 Decay", "Bell State Measurements"],
            help="Choose the type of quantum experiment to simulate"
        )
        
        st.markdown("---")
        
        # Common parameters
        shots = st.slider("📊 Number of Shots", 100, 10000, 1000, step=100)
        noise_rate = st.slider("🔊 Noise Level", 0.0, 0.5, 0.1, step=0.01)
        seed = st.number_input("🎲 Random Seed (optional)", value=None, placeholder="Leave empty for random")
        
        st.markdown("---")
        
        # Experiment-specific parameters
        params = {}
        if experiment_type == "Rabi Oscillations":
            st.markdown('<div class="param-section">Rabi Parameters</div>', unsafe_allow_html=True)
            omega = st.slider("⚡ Drive Frequency (Ω)", 0.5, 3.0, 1.0, step=0.1)
            time_max = st.slider("⏱️ Maximum Time", 5.0, 20.0, 10.0, step=1.0)
            time_steps = st.slider("📈 Time Steps", 50, 200, 100, step=10)
            
            params = {
                "omega": omega,
                "time_max": time_max,
                "time_steps": time_steps,
                "noise_rate": noise_rate,
                "shots": shots,
                "seed": seed
            }
            
        elif experiment_type == "T1/T2 Decay":
            st.markdown('<div class="param-section">Decay Parameters</div>', unsafe_allow_html=True)
            t1 = st.slider("T₁ Decay Time", 1.0, 10.0, 5.0, step=0.5)
            t2 = st.slider("T₂ Coherence Time", 1.0, 8.0, 3.0, step=0.5)
            time_max = st.slider("⏱️ Maximum Time", 10.0, 25.0, 15.0, step=1.0)
            time_steps = st.slider("📈 Time Steps", 50, 200, 100, step=10)
            
            params = {
                "t1": t1,
                "t2": t2,
                "time_max": time_max,
                "time_steps": time_steps,
                "noise_rate": noise_rate,
                "shots": shots,
                "seed": seed
            }
            
        elif experiment_type == "Bell State Measurements":
            st.markdown('<div class="param-section">Bell State Parameters</div>', unsafe_allow_html=True)
            theta = st.slider("θ Bell Parameter", 0.0, 2*np.pi, 0.0, step=0.1)
            
            params = {
                "noise_rate": noise_rate,
                "shots": shots,
                "theta": theta,
                "seed": seed
            }
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.markdown('<div class="control-panel">', unsafe_allow_html=True)
        
        if st.button("🚀 Generate Data", type="primary", width='stretch'):
            generate_data(experiment_type, params)
        
        if st.button("💾 Download Example", width='stretch'):
            show_example_data()
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col1:
        # Display results if available
        if 'data' in st.session_state:
            display_results(st.session_state.data, experiment_type)

def generate_data(experiment_type, params):
    """Generate synthetic quantum data"""
    with st.spinner("Generating synthetic quantum data..."):
        try:
            # Map experiment type to API endpoint
            endpoint_map = {
                "Rabi Oscillations": "rabi",
                "T1/T2 Decay": "decay", 
                "Bell State Measurements": "bell"
            }
            
            endpoint = endpoint_map[experiment_type]
            response = requests.post(f"{API_BASE}/generate/{endpoint}", json=params)
            
            if response.status_code == 200:
                data = response.json()['data']
                st.session_state.data = data
                st.success("✅ Data generated successfully!")
            else:
                st.error(f"❌ Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API server. Make sure the backend is running!")
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")

def display_results(data, experiment_type):
    """Display generated data with visualizations"""
    
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    
    # Results header
    st.markdown(f"""
    <div class="results-header">
        <h2>📊 Results: {experiment_type}</h2>
        <div class="experiment-badge">{data['experiment_type'].replace('_', ' ').title()}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create visualizations based on experiment type
    if experiment_type == "Rabi Oscillations":
        display_rabi_results(data)
    elif experiment_type == "T1/T2 Decay":
        display_decay_results(data)
    elif experiment_type == "Bell State Measurements":
        display_bell_results(data)
    
    # Statistics and download section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="stats-panel">', unsafe_allow_html=True)
        st.markdown("### 📈 Statistics")
        
        stats_df = pd.DataFrame(list(data['statistics'].items()), columns=['Metric', 'Value'])
        st.dataframe(stats_df, width='stretch', hide_index=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="download-panel">', unsafe_allow_html=True)
        st.markdown("### 💾 Download Data")
        
        # JSON download
        json_data = json.dumps(data, indent=2)
        st.download_button(
            "📄 Download JSON",
            json_data,
            f"{data['experiment_type']}_data.json",
            "application/json",
            width='stretch'
        )
        
        # CSV download
        if experiment_type == "Rabi Oscillations":
            csv_data = pd.DataFrame(data['measurements']).to_csv(index=False)
        elif experiment_type == "T1/T2 Decay":
            if isinstance(data['measurements'], dict):
                t1_df = pd.DataFrame(data['measurements']['t1_decay'])
                t2_df = pd.DataFrame(data['measurements']['t2_coherence'])
                csv_data = pd.concat([t1_df.add_prefix('t1_'), t2_df.add_prefix('t2_')], axis=1).to_csv(index=False)
            else:
                csv_data = pd.DataFrame(data['measurements']).to_csv(index=False)
        else:  # Bell State
            bell_data = []
            for basis, meas in data['measurements'].items():
                bell_data.append({
                    'basis': basis,
                    **meas
                })
            csv_data = pd.DataFrame(bell_data).to_csv(index=False)
        
        st.download_button(
            "📊 Download CSV",
            csv_data,
            f"{data['experiment_type']}_data.csv",
            "text/csv",
            width='stretch'
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_rabi_results(data):
    """Display Rabi oscillation results with error handling"""
    try:
        measurements = data['measurements']
        
        if not isinstance(measurements, list):
            st.error("❌ Expected Rabi measurements to be a list")
            st.json(measurements)
            return
            
        df = pd.DataFrame(measurements)
        
        # Check for required columns
        required_cols = ['time', 'theory_prob', 'measured_prob', 'ones_count']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.error(f"❌ Missing columns: {missing_cols}")
            st.write("Available columns:", list(df.columns))
            return
        
        # Create subplot
        fig = make_subplots(rows=2, cols=1, 
                           subplot_titles=('Rabi Oscillation', 'Measurement Counts'),
                           vertical_spacing=0.1)
        
        # Probability plot
        fig.add_trace(
            go.Scatter(x=df['time'], y=df['theory_prob'], 
                      name='Theoretical', line=dict(color='blue', dash='dash')),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['time'], y=df['measured_prob'], 
                      name='Measured', line=dict(color='red'), 
                      mode='lines+markers'),
            row=1, col=1
        )
        
        # Counts histogram
        fig.add_trace(
            go.Bar(x=df['time'], y=df['ones_count'], 
                   name='|1⟩ counts', marker_color='orange'),
            row=2, col=1
        )
        
        fig.update_layout(height=600, title_text="Rabi Oscillation Analysis")
        fig.update_xaxes(title_text="Time", row=2, col=1)
        fig.update_yaxes(title_text="Probability", row=1, col=1)
        fig.update_yaxes(title_text="Counts", row=2, col=1)
        
        st.plotly_chart(fig, width='stretch')
        
    except Exception as e:
        st.error(f"❌ Error displaying Rabi results: {str(e)}")
        st.json(data)

def display_decay_results(data):
    """Display T1/T2 decay results with comprehensive error handling"""
    try:
        measurements = data['measurements']
        
        if isinstance(measurements, dict):
            # Expected structure: dict with 't1_decay' and 't2_coherence' keys
            if 't1_decay' in measurements and 't2_coherence' in measurements:
                t1_data = pd.DataFrame(measurements['t1_decay'])
                t2_data = pd.DataFrame(measurements['t2_coherence'])
                
                # Create two subplots for T1 and T2
                fig = make_subplots(rows=1, cols=2,
                                   subplot_titles=('T₁ Amplitude Decay', 'T₂ Coherence Decay'))
                
                # T1 decay
                fig.add_trace(
                    go.Scatter(x=t1_data['time'], y=t1_data['theory_signal'],
                              name='T₁ Theory', line=dict(color='blue', dash='dash')),
                    row=1, col=1
                )
                fig.add_trace(
                    go.Scatter(x=t1_data['time'], y=t1_data['measured_signal'],
                              name='T₁ Measured', line=dict(color='red'), mode='lines+markers'),
                    row=1, col=1
                )
                
                # T2 coherence
                fig.add_trace(
                    go.Scatter(x=t2_data['time'], y=t2_data['theory_signal'],
                              name='T₂ Theory', line=dict(color='green', dash='dash')),
                    row=1, col=2
                )
                fig.add_trace(
                    go.Scatter(x=t2_data['time'], y=t2_data['measured_signal'],
                              name='T₂ Measured', line=dict(color='orange'), mode='lines+markers'),
                    row=1, col=2
                )
                
                fig.update_layout(height=500, title_text="T₁/T₂ Decay Analysis")
                fig.update_xaxes(title_text="Time")
                fig.update_yaxes(title_text="Signal")
                
            else:
                st.error("❌ Expected 't1_decay' and 't2_coherence' keys in measurements dict")
                st.write("Available keys:", list(measurements.keys()))
                return
                
        elif isinstance(measurements, list):
            # If measurements is a list, treat as single decay
            st.warning("⚠️ Measurements is a list. Creating single decay plot.")
            df = pd.DataFrame(measurements)
            
            fig = go.Figure()
            
            if 'theory_signal' in df.columns and 'measured_signal' in df.columns:
                fig.add_trace(
                    go.Scatter(x=df['time'], y=df['theory_signal'],
                              name='Theory', line=dict(color='blue', dash='dash'))
                )
                fig.add_trace(
                    go.Scatter(x=df['time'], y=df['measured_signal'],
                              name='Measured', line=dict(color='red'), mode='lines+markers')
                )
            else:
                st.error("❌ Expected 'theory_signal' and 'measured_signal' columns")
                st.write("Available columns:", list(df.columns))
                return
            
            fig.update_layout(
                height=500, 
                title_text="Decay Analysis",
                xaxis_title="Time",
                yaxis_title="Signal"
            )
        else:
            st.error("❌ Unexpected measurements data type")
            st.json(measurements)
            return
        
        st.plotly_chart(fig, width='stretch')
        
    except Exception as e:
        st.error(f"❌ Error displaying decay results: {str(e)}")
        st.json(data)

def display_bell_results(data):
    """Display Bell state measurement results"""
    try:
        measurements = data['measurements']
        
        if not isinstance(measurements, dict):
            st.error("❌ Expected Bell measurements to be a dictionary")
            st.json(measurements)
            return
        
        # Correlation plot
        bases = list(measurements.keys())
        theory_corr = [measurements[b]['theory_correlation'] for b in bases]
        measured_corr = [measurements[b]['measured_correlation'] for b in bases]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=bases, y=theory_corr, name='Theory', marker_color='blue', opacity=0.7))
        fig.add_trace(go.Bar(x=bases, y=measured_corr, name='Measured', marker_color='red', opacity=0.7))
        
        fig.update_layout(
            title="Bell State Correlations",
            xaxis_title="Measurement Basis",
            yaxis_title="Correlation",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, width='stretch')
        
        # CHSH violation indicator
        chsh_value = data['statistics']['chsh_value']
        violation = data['statistics']['violation']
        
        st.markdown(f"""
        <div class="chsh-indicator {'violation' if violation else 'no-violation'}">
            <h3>CHSH Value: {chsh_value:.3f}</h3>
            <p>{'🎉 Bell Inequality Violation!' if violation else '❌ No Bell Violation'}</p>
            <small>Classical limit: ≤ 2.0 | Quantum maximum: ~2.83</small>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ Error displaying Bell results: {str(e)}")
        st.json(data)

def show_example_data():
    """Show example datasets"""
    st.info("💡 Example datasets would be pre-generated and shown here for quick access!")

if __name__ == "__main__":
    main()
