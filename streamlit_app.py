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

# CSS für modernes Design
st.markdown("""
<style>
    .pdca-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    .phase-card {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid;
    }
    
    .plan-card { border-left-color: #FF6B6B; background-color: #FFE5E5; }
    .do-card { border-left-color: #4ECDC4; background-color: #E5F9F6; }
    .check-card { border-left-color: #45B7D1; background-color: #E5F3FF; }
    .act-card { border-left-color: #96CEB4; background-color: #E5F5E5; }
    
    .task-completed { text-decoration: line-through; opacity: 0.6; }
    .priority-high { border-left: 3px solid #FF4444; }
    .priority-medium { border-left: 3px solid #FFA500; }
    .priority-low { border-left: 3px solid #4CAF50; }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
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

# Hauptanwendung
def main():
    init_session_state()
    
    # Header
    st.markdown('<div class="header">Digitales KVP-Tool</div>', unsafe_allow_html=True)
    
    # Sidebar für Projektauswahl
    with st.sidebar:
        st.markdown("### Projektverwaltung")
        
        # File browser inspired project selection
        st.markdown("#### Kategorien")
        
        # Project status categories
        status_counts = {
            'all': len(st.session_state.projects),
            'in_progress': len([p for p in st.session_state.projects.values() if p.get('status') == 'in_progress']),
            'completed': len([p for p in st.session_state.projects.values() if p.get('status') == 'completed']),
            'draft': len([p for p in st.session_state.projects.values() if p.get('status') == 'draft'])
        }
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown('<div class="file-browser-item"><span class="file-browser-item-icon">📁</span></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="file-browser-item-text">Alle Projekte</div><div class="file-browser-item-count">{status_counts["all"]}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown('<div class="file-browser-item"><span class="file-browser-item-icon">🔄</span></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="file-browser-item-text">In Bearbeitung</div><div class="file-browser-item-count">{status_counts["in_progress"]}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown('<div class="file-browser-item"><span class="file-browser-item-icon">✅</span></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="file-browser-item-text">Abgeschlossen</div><div class="file-browser-item-count">{status_counts["completed"]}</div>', unsafe_allow_html=True)
        
        # Buttons for new projects
        st.markdown("---")
        if st.button("➕ Neues Projekt", use_container_width=True):
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
        
        if st.button("📝 Beispielprojekt laden", use_container_width=True):
            sample = create_sample_project()
            st.session_state.projects[sample['id']] = sample
            st.session_state.current_project = sample['id']
            st.rerun()
        
        # Project list
        if st.session_state.projects:
            project_names = {pid: proj['name'] for pid, proj in st.session_state.projects.items()}
            selected_project = st.selectbox(
                "Aktives Projekt:",
                options=list(project_names.keys()),
                format_func=lambda x: project_names[x],
                index=0 if st.session_state.current_project is None else 
                      list(project_names.keys()).index(st.session_state.current_project) 
                      if st.session_state.current_project in project_names else 0
            )
            st.session_state.current_project = selected_project
        
        # User role
        st.selectbox("Benutzerrolle:", ['Admin', 'Bearbeiter', 'Leser'], 
                    index=['Admin', 'Bearbeiter', 'Leser'].index(st.session_state.user_role),
                    key='user_role')
        
        # Recent actions
        st.markdown("---")
        st.markdown("### Letzte Aktionen")
        st.markdown('<div class="file-browser-item"><span class="file-browser-item-icon">📝</span><div class="file-browser-item-text">Projekt aktualisiert</div><div class="file-browser-item-count">heute</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="file-browser-item"><span class="file-browser-item-icon">✅</span><div class="file-browser-item-text">Aufgabe erledigt</div><div class="file-browser-item-count">gestern</div></div>', unsafe_allow_html=True)
    
    # Hauptinhalt
    if not st.session_state.projects:
        with st.container():
            st.info("👋 Willkommen! Erstellen Sie ein neues Projekt oder laden Sie das Beispielprojekt.")
            
            # Onboarding Info
            with st.expander("🎯 Tool-Tour: So funktioniert das KVP-Tool"):
                st.markdown("""
                **1. PDCA-Zyklus:** Arbeiten Sie strukturiert durch die vier Phasen
                - **Plan:** Problem definieren und Maßnahmen planen
                - **Do:** Maßnahmen umsetzen und verfolgen
                - **Check:** Ergebnisse prüfen und bewerten
                - **Act:** Standardisieren und nächste Schritte festlegen
                
                **2. Aufgaben-Tracking:** Verwalten Sie To-dos mit Zuständigkeiten und Fristen
                **3. Visualisierung:** Dashboards und Fortschrittsverfolgung
                **4. Teamarbeit:** Kommentare und Zusammenarbeit
                """)
        return
    
    # Aktuelles Projekt anzeigen
    current_proj = st.session_state.projects[st.session_state.current_project]
    
    # Project header with progress
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.session_state.user_role in ['Admin', 'Bearbeiter']:
                new_name = st.text_input("Projektname:", current_proj['name'], key="proj_name")
                if new_name != current_proj['name']:
                    current_proj['name'] = new_name
            else:
                st.markdown(f'<div class="card-title">{current_proj["name"]}</div>', unsafe_allow_html=True)
        
        with col2:
            progress = calculate_progress(current_proj)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{progress:.0f}%</div>
                <div class="metric-label">Fortschritt</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Tabs für PDCA-Phasen
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Plan", "🔨 Do", "📊 Check", "🎯 Act", "📈 Dashboard"])
    
    with tab1:  # PLAN
        with st.container():
            st.markdown('<div class="card-title">📋 Plan - Planen</div>', unsafe_allow_html=True)
            
            if st.session_state.user_role in ['Admin', 'Bearbeiter']:
                # Problemdefinition
                with st.container():
                    st.subheader("Problemdefinition")
                    problem = st.text_area("Was ist das Problem?", 
                                         current_proj.get('plan', {}).get('problem', ''),
                                         help="Beschreiben Sie das Problem konkret und messbar",
                                         label_visibility="collapsed")
                
                # Zielsetzung
                with st.container():
                    st.subheader("Zielsetzung")
                    goal = st.text_area("Was ist das Ziel?", 
                                      current_proj.get('plan', {}).get('goal', ''),
                                      help="SMART-Ziele: Spezifisch, Messbar, Erreichbar, Relevant, Terminiert",
                                      label_visibility="collapsed")
                
                # Ursachenanalyse
                with st.container():
                    st.subheader("Ursachenanalyse")
                    root_cause = st.text_area("Was sind die Hauptursachen?", 
                                            current_proj.get('plan', {}).get('root_cause', ''),
                                            help="Nutzen Sie 5-Why, Ishikawa-Diagramm oder andere Analysemethoden",
                                            label_visibility="collapsed")
                
                # Maßnahmenplanung
                with st.container():
                    st.subheader("Maßnahmenplanung")
                    measures_text = st.text_area("Geplante Maßnahmen (eine pro Zeile):", 
                                               '\n'.join(current_proj.get('plan', {}).get('measures', [])),
                                               label_visibility="collapsed")
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
                if plan_data.get('problem'):
                    with st.container():
                        st.markdown("**Problem:**")
                        st.markdown(f'<div class="card">{plan_data["problem"]}</div>', unsafe_allow_html=True)
                if plan_data.get('goal'):
                    with st.container():
                        st.markdown("**Ziel:**")
                        st.markdown(f'<div class="card">{plan_data["goal"]}</div>', unsafe_allow_html=True)
                if plan_data.get('root_cause'):
                    with st.container():
                        st.markdown("**Ursachen:**")
                        st.markdown(f'<div class="card">{plan_data["root_cause"]}</div>', unsafe_allow_html=True)
                if plan_data.get('measures'):
                    with st.container():
                        st.markdown("**Maßnahmen:**")
                        measures_html = '<div class="card">' + ''.join([f'<div class="file-browser-item"><span class="file-browser-item-icon">•</span><div class="file-browser-item-text">{measure}</div></div>' for measure in plan_data['measures']]) + '</div>'
                        st.markdown(measures_html, unsafe_allow_html=True)
    
    with tab2:  # DO
        with st.container():
            st.markdown('<div class="card-title">🔨 Do - Umsetzen</div>', unsafe_allow_html=True)
            
            # Aufgaben-Management
            st.subheader("Aufgaben-Tracking")
            
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
                    status_class = f"status-{task['status']}"
                    task_class = "task-completed" if task['status'] == 'completed' else ""
                    
                    with st.container():
                        st.markdown(f"""
                        <div class="task-item">
                            <span class="{status_class} status-indicator"></span>
                            <div class="file-browser-item-text {task_class}" style="flex-grow:1">{task["task"]}</div>
                            <div style="margin-right:15px;">👤 {task['responsible']}</div>
                            <div style="margin-right:15px;">📅 {task['due_date']}</div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2 = st.columns([5, 1])
                        with col1:
                            if st.session_state.user_role in ['Admin', 'Bearbeiter']:
                                new_status = st.selectbox("Status", ['open', 'in_progress', 'completed'], 
                                                        index=['open', 'in_progress', 'completed'].index(task['status']),
                                                        key=f"status_{i}",
                                                        label_visibility="collapsed")
                                task['status'] = new_status
                        
                        with col2:
                            if st.session_state.user_role == 'Admin':
                                if st.button("🗑️", key=f"delete_{i}"):
                                    tasks.pop(i)
                                    st.rerun()
            else:
                st.info("Noch keine Aufgaben definiert.")
    
    with tab3:  # CHECK
        with st.container():
            st.markdown('<div class="card-title">📊 Check - Überprüfen</div>', unsafe_allow_html=True)
            
            if st.session_state.user_role in ['Admin', 'Bearbeiter']:
                st.subheader("Kennzahlen & Ergebnisse")
                
                # Metriken eingeben
                col1, col2, col3 = st.columns(3)
                with col1:
                    metric1 = st.number_input("Vorher-Wert:", 
                                            value=current_proj.get('check', {}).get('metrics', {}).get('wartezeit_vorher', 0.0),
                                            label_visibility="collapsed")
                with col2:
                    metric2 = st.number_input("Nachher-Wert:", 
                                            value=current_proj.get('check', {}).get('metrics', {}).get('wartezeit_nachher', 0.0),
                                            label_visibility="collapsed")
                with col3:
                    if metric1 > 0:
                        improvement = ((metric1 - metric2) / metric1) * 100
                        st.metric("Verbesserung", f"{improvement:.1f}%")
                
                # Ergebnisbewertung
                st.subheader("Ergebnisbewertung")
                results = st.text_area("Ergebnisbewertung:", 
                                     current_proj.get('check', {}).get('results', ''),
                                     label_visibility="collapsed")
                
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
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{metrics.get('wartezeit_vorher', 0)}</div>
                            <div class="metric-label">Vorher</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{metrics.get('wartezeit_nachher', 0)}</div>
                            <div class="metric-label">Nachher</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{metrics.get('verbesserung_prozent', 0):.1f}%</div>
                            <div class="metric-label">Verbesserung</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                if check_data.get('results'):
                    with st.container():
                        st.markdown("**Ergebnisse:**")
                        st.markdown(f'<div class="card">{check_data["results"]}</div>', unsafe_allow_html=True)
    
    with tab4:  # ACT
        with st.container():
            st.markdown('<div class="card-title">🎯 Act - Handeln</div>', unsafe_allow_html=True)
            
            if st.session_state.user_role in ['Admin', 'Bearbeiter']:
                st.subheader("Standardisierung & Nächste Schritte")
                
                # Standardisierung
                standardization = st.text_area("Standardisierung:", 
                                             current_proj.get('act', {}).get('standardization', ''),
                                             help="Wie werden die Verbesserungen dauerhaft verankert?",
                                             label_visibility="collapsed")
                
                # Lessons Learned
                lessons = st.text_area("Lessons Learned:", 
                                     current_proj.get('act', {}).get('lessons_learned', ''),
                                     help="Was haben Sie gelernt? Was würden Sie anders machen?",
                                     label_visibility="collapsed")
                
                # Nächste Schritte
                next_steps = st.text_area("Nächste Schritte:", 
                                        current_proj.get('act', {}).get('next_steps', ''),
                                        help="Welche Folgemaßnahmen sind geplant?",
                                        label_visibility="collapsed")
                
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
                    with st.container():
                        st.markdown("**Standardisierung:**")
                        st.markdown(f'<div class="card">{act_data["standardization"]}</div>', unsafe_allow_html=True)
                if act_data.get('lessons_learned'):
                    with st.container():
                        st.markdown("**Lessons Learned:**")
                        st.markdown(f'<div class="card">{act_data["lessons_learned"]}</div>', unsafe_allow_html=True)
                if act_data.get('next_steps'):
                    with st.container():
                        st.markdown("**Nächste Schritte:**")
                        st.markdown(f'<div class="card">{act_data["next_steps"]}</div>', unsafe_allow_html=True)
    
    with tab5:  # DASHBOARD
        with st.container():
            st.markdown('<div class="card-title">📈 Projekt-Dashboard</div>', unsafe_allow_html=True)
            
            # KPIs
            col1, col2, col3, col4 = st.columns(4)
            
            tasks = current_proj.get('do', {}).get('implementation_steps', [])
            total_tasks = len(tasks)
            completed_tasks = len([t for t in tasks if t['status'] == 'completed'])
            in_progress_tasks = len([t for t in tasks if t['status'] == 'in_progress'])
            overdue_tasks = len([t for t in tasks if t['status'] != 'completed' and 
                               datetime.strptime(t['due_date'], '%Y-%m-%d') < datetime.now()])
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{total_tasks}</div>
                    <div class="metric-label">Gesamt Aufgaben</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{completed_tasks}</div>
                    <div class="metric-label">Abgeschlossen</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{in_progress_tasks}</div>
                    <div class="metric-label">In Bearbeitung</div>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{overdue_tasks}</div>
                    <div class="metric-label">Überfällig</div>
                </div>
                """, unsafe_allow_html=True)
            
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
                        'completed': '#2ecc71',
                        'in_progress': '#f39c12',
                        'open': '#e74c3c'
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
                    marker_color=['#e74c3c', '#2ecc71']
                ))
                fig.update_layout(title="Verbesserung im Vergleich", yaxis_title="Wert")
                st.plotly_chart(fig, use_container_width=True)
    
    # Export-Funktionen in der Sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Aktionen")
    
    if st.sidebar.button("📥 Projekt exportieren", use_container_width=True):
        project_json = json.dumps(current_proj, indent=2, ensure_ascii=False, default=str)
        st.sidebar.download_button(
            label="💾 JSON herunterladen",
            data=project_json,
            file_name=f"kvp_projekt_{current_proj['name'].replace(' ', '_')}.json",
            mime="application/json"
        )
    
    if st.sidebar.button("🗑️ Projekt löschen", use_container_width=True) and st.session_state.user_role == 'Admin':
        if len(st.session_state.projects) > 1:
            del st.session_state.projects[st.session_state.current_project]
            st.session_state.current_project = list(st.session_state.projects.keys())[0]
            st.rerun()
        else:
            st.sidebar.error("Das letzte Projekt kann nicht gelöscht werden.")

if __name__ == "__main__":
    main()
