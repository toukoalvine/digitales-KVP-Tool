import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any
import uuid

# Konfiguration der Seite
st.set_page_config(
    page_title="Digitales KVP-Tool",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS Design inspired by cloud storage interfaces
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 32px;
        margin: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(145deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 20px;
        padding: 24px;
        color: white;
    }
    
    .kvp-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 32px;
        border-radius: 20px;
        text-align: center;
        color: white;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 32px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .kvp-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
        pointer-events: none;
    }
    
    .phase-card {
        background: white;
        padding: 24px;
        border-radius: 16px;
        margin: 16px 0;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .phase-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
    }
    
    .phase-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        transition: width 0.3s ease;
    }
    
    .phase-card:hover::before {
        width: 8px;
    }
    
    .plan-card::before { background: linear-gradient(135deg, #ff6b6b, #ff8e8e); }
    .do-card::before { background: linear-gradient(135deg, #4ecdc4, #44a08d); }
    .check-card::before { background: linear-gradient(135deg, #45b7d1, #96c93d); }
    .act-card::before { background: linear-gradient(135deg, #96ceb4, #ffecd2); }
    
    .progress-indicator {
        display: flex;
        justify-content: space-between;
        margin: 24px 0;
        padding: 0;
    }
    
    .progress-step {
        flex: 1;
        text-align: center;
        padding: 16px 12px;
        margin: 0 4px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .progress-step.active {
        color: white;
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
    
    .progress-step.inactive {
        background: rgba(0, 0, 0, 0.05);
        color: #666;
    }
    
    .progress-step.plan.active { background: linear-gradient(135deg, #ff6b6b, #ff8e8e); }
    .progress-step.do.active { background: linear-gradient(135deg, #4ecdc4, #44a08d); }
    .progress-step.check.active { background: linear-gradient(135deg, #45b7d1, #96c93d); }
    .progress-step.act.active { background: linear-gradient(135deg, #96ceb4, #ffecd2); }
    
    .metric-card {
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        text-align: center;
        border: 1px solid rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .task-item {
        background: white;
        padding: 20px;
        border-radius: 12px;
        margin: 12px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .task-item:hover {
        transform: translateX(4px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    }
    
    .task-completed {
        opacity: 0.6;
        background: rgba(76, 175, 80, 0.1);
        border-left: 4px solid #4CAF50;
    }
    
    .task-completed .task-text {
        text-decoration: line-through;
    }
    
    .priority-high { border-left: 4px solid #FF4444; }
    .priority-medium { border-left: 4px solid #FFA500; }
    .priority-low { border-left: 4px solid #4CAF50; }
    
    .floating-button {
        position: fixed;
        bottom: 24px;
        right: 24px;
        width: 64px;
        height: 64px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border: none;
        color: white;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        z-index: 1000;
    }
    
    .floating-button:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.4);
    }
    
    .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 24px 0;
    }
    
    .category-item {
        background: white;
        padding: 24px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .category-item:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
    }
    
    .category-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 100%;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .category-item:hover::before {
        opacity: 0.1;
    }
    
    .category-plan::before { background: linear-gradient(135deg, #ff6b6b, #ff8e8e); }
    .category-do::before { background: linear-gradient(135deg, #4ecdc4, #44a08d); }
    .category-check::before { background: linear-gradient(135deg, #45b7d1, #96c93d); }
    .category-act::before { background: linear-gradient(135deg, #96ceb4, #ffecd2); }
    
    .category-icon {
        font-size: 32px;
        margin-bottom: 12px;
        display: block;
    }
    
    .category-title {
        font-size: 16px;
        font-weight: 600;
        color: #333;
        margin-bottom: 8px;
    }
    
    .category-count {
        font-size: 14px;
        color: #666;
    }
    
    .welcome-screen {
        text-align: center;
        padding: 80px 40px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        margin: 40px 0;
    }
    
    .welcome-icon {
        font-size: 64px;
        margin-bottom: 24px;
        opacity: 0.8;
    }
    
    .welcome-title {
        font-size: 32px;
        font-weight: 700;
        color: #333;
        margin-bottom: 16px;
    }
    
    .welcome-subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 32px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 1px solid rgba(0, 0, 0, 0.1);
        padding: 12px 16px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(0, 0, 0, 0.02);
        padding: 8px;
        border-radius: 16px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 12px 20px;
        font-weight: 600;
        border: none;
        background: transparent;
        color: #666;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: #667eea;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(145deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 0 20px 20px 0;
    }
    
    .css-1d391kg .stButton > button {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        width: 100%;
        margin-bottom: 8px;
    }
    
    .css-1d391kg .stButton > button:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(4px);
    }
    
    .css-1d391kg .stSelectbox label,
    .css-1d391kg .stHeader {
        color: white;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialisierung der Session State
def init_session_state():
    if 'projects' not in st.session_state:
        st.session_state.projects = {}
    if 'current_project' not in st.session_state:
        st.session_state.current_project = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = 'Admin'
    if 'tasks' not in st.session_state:
        st.session_state.tasks = {}
    if 'comments' not in st.session_state:
        st.session_state.comments = {}

# Beispieldaten erstellen
def create_sample_project():
    sample_id = str(uuid.uuid4())
    return {
        'id': sample_id,
        'name': 'Beispiel: Reduzierung der Wartezeiten',
        'description': 'Wartezeiten in der Produktion um 30% reduzieren',
        'created_date': datetime.now().strftime('%Y-%m-%d'),
        'status': 'in_progress',
        'plan': {
            'problem': 'Lange Wartezeiten zwischen Produktionsschritten',
            'goal': 'Wartezeiten um 30% reduzieren',
            'root_cause': 'Unausgewogene Maschinenkapazitäten',
            'measures': ['Maschinenanalyse', 'Prozessoptimierung', 'Schulung']
        },
        'do': {
            'implementation_steps': [
                {'task': 'Maschinenauslastung analysieren', 'responsible': 'Max Mustermann', 'due_date': '2024-07-15', 'status': 'completed'},
                {'task': 'Engpässe identifizieren', 'responsible': 'Anna Schmidt', 'due_date': '2024-07-20', 'status': 'in_progress'},
                {'task': 'Optimierungsmaßnahmen implementieren', 'responsible': 'Tom Weber', 'due_date': '2024-07-30', 'status': 'open'}
            ]
        },
        'check': {
            'metrics': {'wartezeit_vorher': 45, 'wartezeit_nachher': 32, 'verbesserung_prozent': 28.9},
            'results': 'Wartezeiten konnten um 28.9% reduziert werden'
        },
        'act': {
            'standardization': 'Neue Arbeitsanweisungen erstellt',
            'lessons_learned': 'Regelmäßige Kapazitätsanalyse ist essentiell',
            'next_steps': 'Ausweitung auf andere Produktionslinien'
        }
    }

# Fortschrittsberechnung
def calculate_progress(project_data):
    phases = ['plan', 'do', 'check', 'act']
    completed_phases = 0
    
    if project_data.get('plan', {}).get('problem'):
        completed_phases += 0.25
    if project_data.get('do', {}).get('implementation_steps'):
        completed_phases += 0.25
    if project_data.get('check', {}).get('results'):
        completed_phases += 0.25
    if project_data.get('act', {}).get('standardization'):
        completed_phases += 0.25
    
    return min(completed_phases * 100, 100)

# Moderne PDCA Fortschrittsanzeige
def show_modern_pdca_progress(current_phase):
    phases = [
        {'name': 'Plan', 'icon': '📋', 'class': 'plan'},
        {'name': 'Do', 'icon': '🔨', 'class': 'do'},
        {'name': 'Check', 'icon': '📊', 'class': 'check'},
        {'name': 'Act', 'icon': '🎯', 'class': 'act'}
    ]
    
    progress_html = '<div class="progress-indicator">'
    for phase in phases:
        active_class = 'active' if phase['name'].lower() == current_phase else 'inactive'
        progress_html += f'''
        <div class="progress-step {phase['class']} {active_class}">
            <div style="font-size: 20px; margin-bottom: 4px;">{phase['icon']}</div>
            <div>{phase['name']}</div>
        </div>
        '''
    progress_html += '</div>'
    
    st.markdown(progress_html, unsafe_allow_html=True)

# Welcome Screen
def show_welcome_screen():
    st.markdown("""
    <div class="welcome-screen">
        <div class="welcome-icon">🚀</div>
        <div class="welcome-title">Willkommen im KVP-Tool</div>
        <div class="welcome-subtitle">
            Optimieren Sie Ihre Prozesse mit dem bewährten PDCA-Zyklus. 
            Strukturiert, effizient und nachvollziehbar zu besseren Ergebnissen.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Category Grid
    st.markdown('<div class="category-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="category-item category-plan">
            <span class="category-icon">📋</span>
            <div class="category-title">Plan</div>
            <div class="category-count">Probleme definieren</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="category-item category-do">
            <span class="category-icon">🔨</span>
            <div class="category-title">Do</div>
            <div class="category-count">Maßnahmen umsetzen</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="category-item category-check">
            <span class="category-icon">📊</span>
            <div class="category-title">Check</div>
            <div class="category-count">Ergebnisse prüfen</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="category-item category-act">
            <span class="category-icon">🎯</span>
            <div class="category-title">Act</div>
            <div class="category-count">Standardisieren</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📝 Beispielprojekt laden", key="welcome_sample"):
            sample = create_sample_project()
            st.session_state.projects[sample['id']] = sample
            st.session_state.current_project = sample['id']
            st.rerun()

# Hauptanwendung
def main():
    init_session_state()
    
    # Header
    st.markdown('<div class="kvp-header">🔄 Digitales KVP-Tool</div>', unsafe_allow_html=True)
    
    # Sidebar für Projektauswahl
    with st.sidebar:
        st.markdown("### 🎯 Projektauswahl")
        
        # Neues Projekt erstellen
        if st.button("✨ Neues Projekt", help="Erstellen Sie ein neues KVP-Projekt"):
            new_project = {
                'id': str(uuid.uuid4()),
                'name': 'Neues KVP-Projekt',
                'description': '',
                'created_date': datetime.now().strftime('%Y-%m-%d'),
                'status': 'draft',
                'plan': {}, 'do': {}, 'check': {}, 'act': {}
            }
            st.session_state.projects[new_project['id']] = new_project
            st.session_state.current_project = new_project['id']
            st.rerun()
        
        # Beispielprojekt hinzufügen
        if st.button("🚀 Beispielprojekt", help="Laden Sie ein vorgefertigtes Beispielprojekt"):
            sample = create_sample_project()
            st.session_state.projects[sample['id']] = sample
            st.session_state.current_project = sample['id']
            st.rerun()
        
        st.markdown("---")
        
        # Projektliste
        if st.session_state.projects:
            st.markdown("### 📂 Meine Projekte")
            project_names = {pid: proj['name'] for pid, proj in st.session_state.projects.items()}
            selected_project = st.selectbox(
                "Aktives Projekt:",
                options=list(project_names.keys()),
                format_func=lambda x: project_names[x],
                index=0 if st.session_state.current_project is None else 
                      list(project_names.keys()).index(st.session_state.current_project) 
                      if st.session_state.current_project in project_names else 0,
                label_visibility="collapsed"
            )
            st.session_state.current_project = selected_project
        
        st.markdown("---")
        
        # Benutzerrolle
        st.markdown("### 👤 Benutzerrolle")
        st.selectbox("Rolle:", ['Admin', 'Bearbeiter', 'Leser'], 
                    index=['Admin', 'Bearbeiter', 'Leser'].index(st.session_state.user_role),
                    key='user_role',
                    label_visibility="collapsed")
    
    # Hauptinhalt
    if not st.session_state.projects:
        show_welcome_screen()
        return
    
    # Aktuelles Projekt anzeigen
    current_proj = st.session_state.projects[st.session_state.current_project]
    
    # Projekt-Header mit modernen Metriken
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        st.markdown(f"## {current_proj['name']}")
        if st.session_state.user_role in ['Admin', 'Bearbeiter']:
            new_name = st.text_input("Projektname bearbeiten:", current_proj['name'], key="proj_name", label_visibility="collapsed")
            if new_name != current_proj['name']:
                current_proj['name'] = new_name
    
    with col2:
        progress = calculate_progress(current_proj)
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 24px; font-weight: 700; color: #667eea;">{progress:.0f}%</div>
            <div style="color: #666; font-size: 14px;">Fortschritt</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        tasks = current_proj.get('do', {}).get('implementation_steps', [])
        completed_tasks = len([t for t in tasks if t['status'] == 'completed'])
        total_tasks = len(tasks)
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 24px; font-weight: 700; color: #4ecdc4;">{completed_tasks}/{total_tasks}</div>
            <div style="color: #666; font-size: 14px;">Aufgaben</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        status_options = ['draft', 'in_progress', 'completed', 'on_hold']
        status_labels = {'draft': '📝 Entwurf', 'in_progress': '🔄 Aktiv', 
                        'completed': '✅ Fertig', 'on_hold': '⏸️ Pausiert'}
        if st.session_state.user_role in ['Admin', 'Bearbeiter']:
            new_status = st.selectbox("Status:", status_options, 
                                    index=status_options.index(current_proj.get('status', 'draft')),
                                    format_func=lambda x: status_labels[x],
                                    label_visibility="collapsed")
            current_proj['status'] = new_status
        else:
            current_status = current_proj.get('status', 'draft')
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 16px; font-weight: 600;">{status_labels[current_status]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabs für PDCA-Phasen
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Plan", "🔨 Do", "📊 Check", "🎯 Act", "📈 Dashboard"])
    
    with tab1:  # PLAN
        st.markdown('<div class="phase-card plan-card"><h3>📋 Plan - Planen</h3></div>', unsafe_allow_html=True)
        show_modern_pdca_progress('plan')
        
        if st.session_state.user_role in ['Admin', 'Bearbeiter']:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🎯 Problemdefinition")
                problem = st.text_area("Was ist das Problem?", 
                                     current_proj.get('plan', {}).get('problem', ''),
                                     help="Beschreiben Sie das Problem konkret und messbar",
                                     key="problem_input")
                
                st.markdown("#### 🔍 Ursachenanalyse")
                root_cause = st.text_area("Was sind die Hauptursachen?", 
                                        current_proj.get('plan', {}).get('root_cause', ''),
                                        help="Nutzen Sie 5-Why, Ishikawa-Diagramm oder andere Analysemethoden",
                                        key="root_cause_input")
            
            with col2:
                st.markdown("#### 🎯 Zielsetzung")
                goal = st.text_area("Was ist das Ziel?", 
                                  current_proj.get('plan', {}).get('goal', ''),
                                  help="SMART-Ziele: Spezifisch, Messbar, Erreichbar, Relevant, Terminiert",
                                  key="goal_input")
                
                st.markdown("#### 📝 Maßnahmenplanung")
                measures_text = st.text_area("Geplante Maßnahmen (eine pro Zeile):", 
                                           '\n'.join(current_proj.get('plan', {}).get('measures', [])),
                                           key="measures_input")
                measures = [m.strip() for m in measures_text.split('\n') if m.strip()]
            
            # Automatisches Speichern
            if 'plan' not in current_proj:
                current_proj['plan'] = {}
            current_proj['plan'].update({
                'problem': problem,
                'goal': goal,
                'root_cause': root_cause,
                'measures': measures
            })
        else:
            # Nur anzeigen für Leser
            plan_data = current_proj.get('plan', {})
            if plan_data:
                col1, col2 = st.columns(2)
                with col1:
                    if plan_data.get('problem'):
                        st.markdown("**Problem:**")
                        st.info(plan_data['problem'])
                    if plan_data.get('root_cause'):
                        st.write("**Ursachen:**", plan_data['root_cause'])
            if plan_data.get('measures'):
                st.write("**Maßnahmen:**")
                for measure in plan_data['measures']:
                    st.write(f"• {measure}")
    
    with tab2:  # DO
        st.markdown('<div class="phase-card do-card"><h3>🔨 Do - Umsetzen</h3></div>', unsafe_allow_html=True)
        show_pdca_progress('do')
        
        # Aufgaben-Management
        st.subheader("📋 Aufgaben-Tracking")
        
        if st.session_state.user_role in ['Admin', 'Bearbeiter']:
            # Neue Aufgabe hinzufügen
            with st.expander("➕ Neue Aufgabe hinzufügen"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_task = st.text_input("Aufgabe:")
                with col2:
                    new_responsible = st.text_input("Verantwortlich:")
                with col3:
                    new_date = st.date_input("Fälligkeitsdatum:")
                
                if st.button("Aufgabe hinzufügen") and new_task:
                    if 'do' not in current_proj:
                        current_proj['do'] = {'implementation_steps': []}
                    if 'implementation_steps' not in current_proj['do']:
                        current_proj['do']['implementation_steps'] = []
                    
                    current_proj['do']['implementation_steps'].append({
                        'task': new_task,
                        'responsible': new_responsible,
                        'due_date': new_date.strftime('%Y-%m-%d'),
                        'status': 'open',
                        'priority': 'medium'
                    })
                    st.rerun()
        
        # Aufgabenliste anzeigen
        tasks = current_proj.get('do', {}).get('implementation_steps', [])
        if tasks:
            for i, task in enumerate(tasks):
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])
                    
                    with col1:
                        task_class = "task-completed" if task['status'] == 'completed' else ""
                        st.markdown(f'<div class="{task_class}">{task["task"]}</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.write(f"👤 {task['responsible']}")
                    
                    with col3:
                        st.write(f"📅 {task['due_date']}")
                    
                    with col4:
                        if st.session_state.user_role in ['Admin', 'Bearbeiter']:
                            new_status = st.selectbox("", ['open', 'in_progress', 'completed'], 
                                                    index=['open', 'in_progress', 'completed'].index(task['status']),
                                                    key=f"status_{i}")
                            task['status'] = new_status
                    
                    with col5:
                        if st.session_state.user_role == 'Admin':
                            if st.button("🗑️", key=f"delete_{i}"):
                                tasks.pop(i)
                                st.rerun()
                    
                    st.divider()
        else:
            st.info("Noch keine Aufgaben definiert.")
    
    with tab3:  # CHECK
        st.markdown('<div class="phase-card check-card"><h3>📊 Check - Überprüfen</h3></div>', unsafe_allow_html=True)
        show_pdca_progress('check')
        
        if st.session_state.user_role in ['Admin', 'Bearbeiter']:
            st.subheader("📈 Kennzahlen & Ergebnisse")
            
            # Metriken eingeben
            col1, col2, col3 = st.columns(3)
            with col1:
                metric1 = st.number_input("Vorher-Wert:", 
                                        value=current_proj.get('check', {}).get('metrics', {}).get('wartezeit_vorher', 0.0))
            with col2:
                metric2 = st.number_input("Nachher-Wert:", 
                                        value=current_proj.get('check', {}).get('metrics', {}).get('wartezeit_nachher', 0.0))
            with col3:
                if metric1 > 0:
                    improvement = ((metric1 - metric2) / metric1) * 100
                    st.metric("Verbesserung", f"{improvement:.1f}%")
            
            # Ergebnisbewertung
            results = st.text_area("Ergebnisbewertung:", 
                                 current_proj.get('check', {}).get('results', ''))
            
            # Speichern
            if 'check' not in current_proj:
                current_proj['check'] = {}
            current_proj['check'].update({
                'metrics': {
                    'wartezeit_vorher': metric1,
                    'wartezeit_nachher': metric2,
                    'verbesserung_prozent': improvement if metric1 > 0 else 0
                },
                'results': results
            })
        else:
            # Nur anzeigen
            check_data = current_proj.get('check', {})
            if check_data.get('metrics'):
                metrics = check_data['metrics']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Vorher", metrics.get('wartezeit_vorher', 0))
                with col2:
                    st.metric("Nachher", metrics.get('wartezeit_nachher', 0))
                with col3:
                    st.metric("Verbesserung", f"{metrics.get('verbesserung_prozent', 0):.1f}%")
            
            if check_data.get('results'):
                st.write("**Ergebnisse:**", check_data['results'])
    
    with tab4:  # ACT
        st.markdown('<div class="phase-card act-card"><h3>🎯 Act - Handeln</h3></div>', unsafe_allow_html=True)
        show_pdca_progress('act')
        
        if st.session_state.user_role in ['Admin', 'Bearbeiter']:
            st.subheader("📋 Standardisierung & Nächste Schritte")
            
            # Standardisierung
            standardization = st.text_area("Standardisierung:", 
                                         current_proj.get('act', {}).get('standardization', ''),
                                         help="Wie werden die Verbesserungen dauerhaft verankert?")
            
            # Lessons Learned
            lessons = st.text_area("Lessons Learned:", 
                                 current_proj.get('act', {}).get('lessons_learned', ''),
                                 help="Was haben Sie gelernt? Was würden Sie anders machen?")
            
            # Nächste Schritte
            next_steps = st.text_area("Nächste Schritte:", 
                                    current_proj.get('act', {}).get('next_steps', ''),
                                    help="Welche Folgemaßnahmen sind geplant?")
            
            # Speichern
            if 'act' not in current_proj:
                current_proj['act'] = {}
            current_proj['act'].update({
                'standardization': standardization,
                'lessons_learned': lessons,
                'next_steps': next_steps
            })
        else:
            # Nur anzeigen
            act_data = current_proj.get('act', {})
            if act_data.get('standardization'):
                st.write("**Standardisierung:**", act_data['standardization'])
            if act_data.get('lessons_learned'):
                st.write("**Lessons Learned:**", act_data['lessons_learned'])
            if act_data.get('next_steps'):
                st.write("**Nächste Schritte:**", act_data['next_steps'])
    
    with tab5:  # DASHBOARD
        st.header("📈 Projekt-Dashboard")
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        tasks = current_proj.get('do', {}).get('implementation_steps', [])
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t['status'] == 'completed'])
        in_progress_tasks = len([t for t in tasks if t['status'] == 'in_progress'])
        overdue_tasks = len([t for t in tasks if t['status'] != 'completed' and 
                           datetime.strptime(t['due_date'], '%Y-%m-%d') < datetime.now()])
        
        with col1:
            st.metric("Gesamt Aufgaben", total_tasks)
        with col2:
            st.metric("Abgeschlossen", completed_tasks, f"{completed_tasks}/{total_tasks}")
        with col3:
            st.metric("In Bearbeitung", in_progress_tasks)
        with col4:
            st.metric("Überfällig", overdue_tasks, delta=f"-{overdue_tasks}" if overdue_tasks > 0 else None)
        
        # Aufgaben-Status Diagramm
        if tasks:
            status_counts = {}
            for task in tasks:
                status = task['status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            fig = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                title="Aufgaben-Status Verteilung",
                color_discrete_map={
                    'completed': '#4CAF50',
                    'in_progress': '#FFA500',
                    'open': '#FF4444'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Zeitlicher Verlauf (falls Metriken vorhanden)
        check_data = current_proj.get('check', {}).get('metrics', {})
        if check_data:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['Vorher', 'Nachher'],
                y=[check_data.get('wartezeit_vorher', 0), check_data.get('wartezeit_nachher', 0)],
                marker_color=['#FF6B6B', '#4CAF50']
            ))
            fig.update_layout(title="Verbesserung im Vergleich", yaxis_title="Wert")
            st.plotly_chart(fig, use_container_width=True)
    
    # Export-Funktionen
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔄 Aktionen")
    
    if st.sidebar.button("📥 Projekt exportieren"):
        project_json = json.dumps(current_proj, indent=2, ensure_ascii=False, default=str)
        st.sidebar.download_button(
            label="💾 JSON herunterladen",
            data=project_json,
            file_name=f"kvp_projekt_{current_proj['name'].replace(' ', '_')}.json",
            mime="application/json"
        )
    
    if st.sidebar.button("🗑️ Projekt löschen") and st.session_state.user_role == 'Admin':
        if len(st.session_state.projects) > 1:
            del st.session_state.projects[st.session_state.current_project]
            st.session_state.current_project = list(st.session_state.projects.keys())[0]
            st.rerun()
        else:
            st.sidebar.error("Das letzte Projekt kann nicht gelöscht werden.")

if __name__ == "__main__":
    main()
