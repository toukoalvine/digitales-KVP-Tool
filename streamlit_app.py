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

# CSS für besseres Design
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
        st.session_state.user_role = 'Admin'  # Vereinfacht für Demo
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

# PDCA Fortschrittsanzeige
def show_pdca_progress(current_phase):
    phases = ['Plan', 'Do', 'Check', 'Act']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    cols = st.columns(4)
    for i, (phase, color) in enumerate(zip(phases, colors)):
        with cols[i]:
            if phase.lower() == current_phase:
                st.markdown(f"""
                <div style="background-color: {color}; color: white; padding: 10px; 
                           border-radius: 5px; text-align: center; font-weight: bold;">
                    {phase} ✓
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color: #f0f0f0; color: #666; padding: 10px; 
                           border-radius: 5px; text-align: center;">
                    {phase}
                </div>
                """, unsafe_allow_html=True)

# Hauptanwendung
def main():
    init_session_state()
    
    # Header
    st.markdown('<div class="pdca-header">🔄 Digitales KVP-Tool</div>', unsafe_allow_html=True)
    
    # Sidebar für Projektauswahl
    with st.sidebar:
        st.header("Projektauswahl")
        
        # Neues Projekt erstellen
        if st.button("➕ Neues Projekt"):
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
        if st.button("📝 Beispielprojekt laden"):
            sample = create_sample_project()
            st.session_state.projects[sample['id']] = sample
            st.session_state.current_project = sample['id']
            st.rerun()
        
        # Projektliste
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
        
        # Benutzerrolle
        st.selectbox("Benutzerrolle:", ['Admin', 'Bearbeiter', 'Leser'], 
                    index=['Admin', 'Bearbeiter', 'Leser'].index(st.session_state.user_role),
                    key='user_role')
    
    # Hauptinhalt
    if not st.session_state.projects:
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
    
    # Projekt-Header mit Fortschritt
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.header(current_proj['name'])
        if st.session_state.user_role in ['Admin', 'Bearbeiter']:
            new_name = st.text_input("Projektname:", current_proj['name'], key="proj_name")
            if new_name != current_proj['name']:
                current_proj['name'] = new_name
    
    with col2:
        progress = calculate_progress(current_proj)
        st.metric("Fortschritt", f"{progress:.0f}%")
    
    with col3:
        status_options = ['draft', 'in_progress', 'completed', 'on_hold']
        status_labels = {'draft': '📝 Entwurf', 'in_progress': '🔄 In Bearbeitung', 
                        'completed': '✅ Abgeschlossen', 'on_hold': '⏸️ Pausiert'}
        if st.session_state.user_role in ['Admin', 'Bearbeiter']:
            new_status = st.selectbox("Status:", status_options, 
                                    index=status_options.index(current_proj.get('status', 'draft')),
                                    format_func=lambda x: status_labels[x])
            current_proj['status'] = new_status
    
    # Tabs für PDCA-Phasen
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Plan", "🔨 Do", "📊 Check", "🎯 Act", "📈 Dashboard"])
    
    with tab1:  # PLAN
        st.markdown('<div class="phase-card plan-card"><h3>📋 Plan - Planen</h3></div>', unsafe_allow_html=True)
        show_pdca_progress('plan')
        
        if st.session_state.user_role in ['Admin', 'Bearbeiter']:
            # Problemdefinition
            st.subheader("🎯 Problemdefinition")
            problem = st.text_area("Was ist das Problem?", 
                                 current_proj.get('plan', {}).get('problem', ''),
                                 help="Beschreiben Sie das Problem konkret und messbar")
            
            # Zielsetzung
            st.subheader("🎯 Zielsetzung")
            goal = st.text_area("Was ist das Ziel?", 
                              current_proj.get('plan', {}).get('goal', ''),
                              help="SMART-Ziele: Spezifisch, Messbar, Erreichbar, Relevant, Terminiert")
            
            # Ursachenanalyse
            st.subheader("🔍 Ursachenanalyse")
            root_cause = st.text_area("Was sind die Hauptursachen?", 
                                    current_proj.get('plan', {}).get('root_cause', ''),
                                    help="Nutzen Sie 5-Why, Ishikawa-Diagramm oder andere Analysemethoden")
            
            # Maßnahmenplanung
            st.subheader("📝 Maßnahmenplanung")
            measures_text = st.text_area("Geplante Maßnahmen (eine pro Zeile):", 
                                       '\n'.join(current_proj.get('plan', {}).get('measures', [])))
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
                st.write("**Problem:**", plan_data['problem'])
            if plan_data.get('goal'):
                st.write("**Ziel:**", plan_data['goal'])
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
