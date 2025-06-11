import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json

# Configuração da página
st.set_page_config(
    page_title="TRL Portfolio Manager",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .zone-descoberta {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .zone-desenvolvimento {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .zone-transferencia {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Dados iniciais dos projetos
if 'projects' not in st.session_state:
    st.session_state.projects = [
        {"index": 1, "name": "Inteligência Artificial", "trl": 1, "weight": 3},
        {"index": 2, "name": "Banheiro WellNess (Feira ExpoRvestir 2025)", "trl": 5, "weight": 3},
        {"index": 3, "name": "Óxido de Nióbio", "trl": 1, "weight": 2},
        {"index": 4, "name": "Pesquisa Materiais - LabMat UFSC", "trl": 1, "weight": 9},
        {"index": 5, "name": "Microbolhas Banheira", "trl": 4, "weight": 8},
        {"index": 6, "name": "Microbolhas no Arejador", "trl": 5, "weight": 8},
        {"index": 7, "name": "SunShower", "trl": 2, "weight": 2},
        {"index": 8, "name": "Gerador de Ozônio - OEM", "trl": 5, "weight": 8},
        {"index": 9, "name": "BacteriaFree para esmalte cerâmico", "trl": 5, "weight": 7},
        {"index": 10, "name": "Futuro do sistema de descarga (VD)", "trl": 2, "weight": 2},
        {"index": 11, "name": "Aplicação Grafeno", "trl": 1, "weight": 2},
        {"index": 12, "name": "Central de Purificador de Água", "trl": 1, "weight": 2},
        {"index": 13, "name": "Super Filtro (Água alcalina e antioxidante)", "trl": 3, "weight": 7},
        {"index": 14, "name": "Nobreak DocolEletric", "trl": 2, "weight": 2},
        {"index": 15, "name": "Acionamento Salvágua com Trava", "trl": 2, "weight": 2},
        {"index": 16, "name": "Hydraloop (reciclagem de água)", "trl": 1, "weight": 2},
        {"index": 17, "name": "WaterTrain (Neoperl)", "trl": 3, "weight": 7},
        {"index": 18, "name": "Novo acionamento VD Sensor", "trl": 2, "weight": 2},
        {"index": 19, "name": "Tóten de Hidratação (Água fresca e purificada, alcalina e Antiox)", "trl": 2, "weight": 2},
        {"index": 20, "name": "Banheiro autolimpante", "trl": 1, "weight": 2},
        {"index": 21, "name": "Esmalte cerâmico hidrofílico", "trl": 1, "weight": 2},
        {"index": 22, "name": "Água em nanoescala", "trl": 1, "weight": 2},
        {"index": 23, "name": "Ducha de Mão com Sabão", "trl": 2, "weight": 6},
        {"index": 24, "name": "ZeroWaste - Composteira", "trl": 2, "weight": 2},
        {"index": 25, "name": "Anti mancha no PVD", "trl": 2, "weight": 2},
        {"index": 26, "name": "Cuba de Cozinha com Microbolhas (Bistro)", "trl": 3, "weight": 2},
        {"index": 27, "name": "Gerador de Ozônio Docol", "trl": 3, "weight": 2},
        {"index": 28, "name": "Sensor piezoelétrico (RNC)", "trl": 2, "weight": 2},
        {"index": 29, "name": "Sensor com tecnologia ToF e Radar", "trl": 2, "weight": 2},
        {"index": 30, "name": "Mictório Plug&Play (sensor embutido)", "trl": 3, "weight": 2},
        {"index": 31, "name": "Filtro com fibras orgânicas (Comunidade Amazônia)", "trl": 1, "weight": 2},
        {"index": 32, "name": "Barra de duchas com diferentes tipos de jatos", "trl": 3, "weight": 1},
        {"index": 33, "name": "Dobradiça eletrônica sem engrenagem", "trl": 1, "weight": 1},
        {"index": 34, "name": "Manutenção Ativa Inteligente Docol", "trl": 2, "weight": 0},
        {"index": 35, "name": "Acabamentos NanoTech (Ciser)", "trl": 5, "weight": 5},
        {"index": 36, "name": "Teste", "trl": 7, "weight": 5}
    ]

# Funções auxiliares
def get_zone(trl):
    if trl <= 3:
        return {"name": "Descoberta", "color": "#2196f3", "range": "TRL 1-3"}
    elif trl <= 6:
        return {"name": "Desenvolvimento", "color": "#ff9800", "range": "TRL 4-6"}
    else:
        return {"name": "Transferência", "color": "#4caf50", "range": "TRL 7-9"}

def get_priority(weight):
    if weight >= 8:
        return "Crítica"
    elif weight >= 6:
        return "Alta"
    elif weight >= 3:
        return "Média"
    elif weight >= 1:
        return "Baixa"
    else:
        return "Mínima"

def get_priority_color(weight):
    if weight >= 8:
        return "#f44336"
    elif weight >= 6:
        return "#ff9800"
    elif weight >= 3:
        return "#ffeb3b"
    elif weight >= 1:
        return "#2196f3"
    else:
        return "#9e9e9e"

def get_next_index():
    if st.session_state.projects:
        return max([p["index"] for p in st.session_state.projects]) + 1
    return 1

# Título principal
st.title("🚀 TRL Portfolio Manager")
st.markdown("**Gestão Interativa de Projetos por Nível TRL e Peso**")

# Sidebar para gerenciamento de projetos
st.sidebar.header("📋 Gerenciamento de Projetos")

# Seção de adicionar novo projeto
with st.sidebar.expander("➕ Adicionar Novo Projeto", expanded=False):
    with st.form("add_project"):
        new_name = st.text_input("Nome do Projeto", placeholder="Digite o nome do projeto...")
        new_trl = st.selectbox("Nível TRL", options=list(range(1, 10)), index=0)
        new_weight = st.number_input("Peso", min_value=0, max_value=10, value=1, step=1)
        
        if st.form_submit_button("Adicionar Projeto"):
            if new_name.strip():
                new_project = {
                    "index": get_next_index(),
                    "name": new_name.strip(),
                    "trl": new_trl,
                    "weight": new_weight
                }
                st.session_state.projects.append(new_project)
                st.success(f"Projeto '{new_name}' adicionado com sucesso!")
                st.rerun()
            else:
                st.error("Por favor, digite um nome para o projeto.")

# Seção de editar/excluir projetos
with st.sidebar.expander("✏️ Editar/Excluir Projetos", expanded=False):
    if st.session_state.projects:
        # Seleção do projeto para editar
        project_options = {f"{p['index']} - {p['name'][:30]}...": p for p in st.session_state.projects}
        selected_project_key = st.selectbox("Selecionar Projeto", options=list(project_options.keys()))
        selected_project = project_options[selected_project_key]
        
        # Formulário de edição
        with st.form("edit_project"):
            st.write(f"**Editando:** {selected_project['name']}")
            edit_name = st.text_input("Nome", value=selected_project['name'])
            edit_trl = st.selectbox("TRL", options=list(range(1, 10)), index=selected_project['trl']-1)
            edit_weight = st.number_input("Peso", min_value=0, max_value=10, value=selected_project['weight'], step=1)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("💾 Salvar"):
                    # Encontrar e atualizar o projeto
                    for i, p in enumerate(st.session_state.projects):
                        if p['index'] == selected_project['index']:
                            st.session_state.projects[i] = {
                                "index": selected_project['index'],
                                "name": edit_name.strip(),
                                "trl": edit_trl,
                                "weight": edit_weight
                            }
                            break
                    st.success("Projeto atualizado com sucesso!")
                    st.rerun()
            
            with col2:
                if st.form_submit_button("🗑️ Excluir"):
                    st.session_state.projects = [p for p in st.session_state.projects if p['index'] != selected_project['index']]
                    st.success("Projeto excluído com sucesso!")
                    st.rerun()
    else:
        st.info("Nenhum projeto disponível para editar.")

# Seção de importar/exportar
with st.sidebar.expander("📁 Importar/Exportar", expanded=False):
    # Exportar projetos
    if st.button("📤 Exportar Projetos (JSON)"):
        json_data = json.dumps(st.session_state.projects, indent=2, ensure_ascii=False)
        st.download_button(
            label="💾 Download JSON",
            data=json_data,
            file_name=f"projetos_trl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    # Importar projetos
    uploaded_file = st.file_uploader("📥 Importar Projetos", type=['json'])
    if uploaded_file is not None:
        try:
            imported_data = json.load(uploaded_file)
            if isinstance(imported_data, list) and all(isinstance(item, dict) for item in imported_data):
                if st.button("Confirmar Importação"):
                    st.session_state.projects = imported_data
                    st.success(f"Importados {len(imported_data)} projetos com sucesso!")
                    st.rerun()
            else:
                st.error("Formato de arquivo inválido.")
        except Exception as e:
            st.error(f"Erro ao importar arquivo: {str(e)}")

# Área principal
df = pd.DataFrame(st.session_state.projects)

if df.empty:
    st.warning("Nenhum projeto cadastrado. Adicione projetos usando a barra lateral.")
else:
    # Filtros
    st.header("🔍 Filtros e Análise")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("🔍 Buscar projetos", placeholder="Digite para buscar...")
    
    with col2:
        zone_filter = st.selectbox("🎯 Filtrar por Zona", 
                                 options=["Todas", "Descoberta", "Desenvolvimento", "Transferência"])
    
    with col3:
        priority_filter = st.selectbox("⚡ Filtrar por Prioridade",
                                     options=["Todas", "Crítica", "Alta", "Média", "Baixa", "Mínima"])
    
    # Aplicar filtros
    filtered_df = df.copy()
    
    if search_term:
        filtered_df = filtered_df[filtered_df['name'].str.contains(search_term, case=False, na=False)]
    
    if zone_filter != "Todas":
        filtered_df = filtered_df[filtered_df['trl'].apply(lambda x: get_zone(x)['name']) == zone_filter]
    
    if priority_filter != "Todas":
        filtered_df = filtered_df[filtered_df['weight'].apply(get_priority) == priority_filter]
    
    # Estatísticas das zonas
    st.header("📊 Estatísticas por Zona")
    
    # Calcular estatísticas
    zones_stats = []
    for zone_name in ["Descoberta", "Desenvolvimento", "Transferência"]:
        if zone_name == "Descoberta":
            zone_projects = df[df['trl'] <= 3]
        elif zone_name == "Desenvolvimento":
            zone_projects = df[(df['trl'] >= 4) & (df['trl'] <= 6)]
        else:
            zone_projects = df[df['trl'] >= 7]
        
        zones_stats.append({
            "Zona": zone_name,
            "Projetos": len(zone_projects),
            "Peso Total": zone_projects['weight'].sum(),
            "Peso Médio": round(zone_projects['weight'].mean(), 1) if len(zone_projects) > 0 else 0,
            "Percentual": round(len(zone_projects) / len(df) * 100, 1)
        })
    
    # Exibir cards das zonas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="zone-descoberta">', unsafe_allow_html=True)
        st.metric("🔬 Descoberta (TRL 1-3)", 
                 f"{zones_stats[0]['Projetos']} projetos",
                 f"{zones_stats[0]['Percentual']}% do total")
        st.write(f"**Peso Total:** {zones_stats[0]['Peso Total']} | **Peso Médio:** {zones_stats[0]['Peso Médio']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="zone-desenvolvimento">', unsafe_allow_html=True)
        st.metric("⚙️ Desenvolvimento (TRL 4-6)", 
                 f"{zones_stats[1]['Projetos']} projetos",
                 f"{zones_stats[1]['Percentual']}% do total")
        st.write(f"**Peso Total:** {zones_stats[1]['Peso Total']} | **Peso Médio:** {zones_stats[1]['Peso Médio']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="zone-transferencia">', unsafe_allow_html=True)
        st.metric("🚀 Transferência (TRL 7-9)", 
                 f"{zones_stats[2]['Projetos']} projetos",
                 f"{zones_stats[2]['Percentual']}% do total")
        st.write(f"**Peso Total:** {zones_stats[2]['Peso Total']} | **Peso Médio:** {zones_stats[2]['Peso Médio']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Matriz de Dispersão TRL vs Peso
    st.header("📈 Matriz TRL vs Peso")
    
    # Preparar dados para o gráfico
    filtered_df['zone'] = filtered_df['trl'].apply(lambda x: get_zone(x)['name'])
    filtered_df['priority'] = filtered_df['weight'].apply(get_priority)
    filtered_df['color'] = filtered_df['weight'].apply(get_priority_color)
    filtered_df['size'] = filtered_df['weight'].apply(lambda x: max(10, x * 5))
    
    # Criar gráfico de dispersão
    fig = go.Figure()
    
    # Adicionar pontos por zona
    for zone in ["Descoberta", "Desenvolvimento", "Transferência"]:
        zone_data = filtered_df[filtered_df['zone'] == zone]
        if not zone_data.empty:
            fig.add_trace(go.Scatter(
                x=zone_data['trl'],
                y=zone_data['weight'],
                mode='markers+text',
                text=zone_data['index'],
                textposition='middle center',
                textfont=dict(color='white', size=10),
                marker=dict(
                    size=zone_data['size'],
                    color=zone_data['color'],
                    line=dict(width=2, color='white'),
                    opacity=0.8
                ),
                hovertemplate='<b>%{customdata[0]}</b><br>' +
                             'TRL: %{x}<br>' +
                             'Peso: %{y}<br>' +
                             'Zona: ' + zone + '<br>' +
                             'Prioridade: %{customdata[1]}<extra></extra>',
                customdata=list(zip(zone_data['name'], zone_data['priority'])),
                name=zone,
                showlegend=True
            ))
    
    # Configurar layout do gráfico
    fig.update_layout(
        title="Matriz de Posicionamento TRL de Projetos",
        xaxis_title="Nível TRL (Technology Readiness Level)",
        yaxis_title="Peso do Projeto",
        xaxis=dict(tickmode='linear', tick0=1, dtick=1, range=[0.5, 9.5]),
        yaxis=dict(tickmode='linear', tick0=0, dtick=1, range=[-0.5, df['weight'].max() + 0.5]),
        height=600,
        hovermode='closest',
        plot_bgcolor='rgba(240,240,240,0.8)',
        paper_bgcolor='white'
    )
    
    # Adicionar linhas de grade para as zonas
    fig.add_vline(x=3.5, line_dash="dash", line_color="blue", opacity=0.3, annotation_text="Descoberta → Desenvolvimento")
    fig.add_vline(x=6.5, line_dash="dash", line_color="orange", opacity=0.3, annotation_text="Desenvolvimento → Transferência")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela de projetos
    st.header("📋 Lista de Projetos")
    
    # Preparar dados para exibição
    display_df = filtered_df.copy()
    display_df['Zona'] = display_df['zone']
    display_df['Prioridade'] = display_df['priority']
    display_df = display_df[['index', 'name', 'trl', 'weight', 'Zona', 'Prioridade']]
    display_df.columns = ['Índice', 'Nome do Projeto', 'TRL', 'Peso', 'Zona', 'Prioridade']
    
    # Ordenar por peso (decrescente) e depois por TRL (crescente)
    display_df = display_df.sort_values(['Peso', 'TRL'], ascending=[False, True])
    
    # Exibir tabela
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Índice": st.column_config.NumberColumn("Índice", width="small"),
            "Nome do Projeto": st.column_config.TextColumn("Nome do Projeto", width="large"),
            "TRL": st.column_config.NumberColumn("TRL", width="small"),
            "Peso": st.column_config.NumberColumn("Peso", width="small"),
            "Zona": st.column_config.TextColumn("Zona", width="medium"),
            "Prioridade": st.column_config.TextColumn("Prioridade", width="medium")
        }
    )
    
    # Gráficos adicionais
    st.header("📊 Análises Adicionais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição por TRL
        trl_counts = df['trl'].value_counts().sort_index()
        fig_trl = px.bar(
            x=trl_counts.index,
            y=trl_counts.values,
            title="Distribuição de Projetos por TRL",
            labels={'x': 'Nível TRL', 'y': 'Número de Projetos'},
            color=trl_counts.values,
            color_continuous_scale='viridis'
        )
        fig_trl.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_trl, use_container_width=True)
    
    with col2:
        # Distribuição por Peso
        weight_counts = df['weight'].value_counts().sort_index()
        fig_weight = px.bar(
            x=weight_counts.index,
            y=weight_counts.values,
            title="Distribuição de Projetos por Peso",
            labels={'x': 'Peso', 'y': 'Número de Projetos'},
            color=weight_counts.values,
            color_continuous_scale='plasma'
        )
        fig_weight.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_weight, use_container_width=True)
    
    # Insights do Portfolio
    st.header("💡 Insights do Portfolio")
    
    # Calcular insights
    total_projects = len(df)
    critical_projects = len(df[df['weight'] >= 8])
    high_priority_projects = len(df[(df['weight'] >= 6) & (df['weight'] < 8)])
    trl5_projects = len(df[df['trl'] == 5])
    
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        st.info(f"""
        **🎯 Distribuição Estratégica:**
        - **Descoberta:** {zones_stats[0]['Projetos']} projetos ({zones_stats[0]['Percentual']}%)
        - **Desenvolvimento:** {zones_stats[1]['Projetos']} projetos ({zones_stats[1]['Percentual']}%)
        - **Transferência:** {zones_stats[2]['Projetos']} projetos ({zones_stats[2]['Percentual']}%)
        
        **📈 Recomendação:** Manter equilíbrio entre as zonas conforme estratégia organizacional.
        """)
    
    with insight_col2:
        st.warning(f"""
        **⚡ Projetos Prioritários:**
        - **Críticos (≥8):** {critical_projects} projetos
        - **Alta prioridade (6-7):** {high_priority_projects} projetos
        - **Prontos para TRL 6:** {trl5_projects} projetos
        
        **🎯 Foco:** Projetos críticos demandam atenção imediata.
        """)
    
    # Legenda de prioridades
    st.header("🎨 Legenda de Prioridades")
    
    priority_info = [
        ("Crítica (≥8)", "#f44336", "Máximo impacto - Requer atenção imediata"),
        ("Alta (6-7)", "#ff9800", "Alto impacto - Prioridade elevada"),
        ("Média (3-5)", "#ffeb3b", "Impacto moderado - Acompanhamento regular"),
        ("Baixa (1-2)", "#2196f3", "Impacto limitado - Monitoramento"),
        ("Mínima (0)", "#9e9e9e", "Sem impacto atual - Revisão necessária")
    ]
    
    legend_cols = st.columns(5)
    for i, (priority, color, description) in enumerate(priority_info):
        with legend_cols[i]:
            st.markdown(f"""
            <div style="background-color: {color}; color: white; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 5px;">
                <strong>{priority}</strong>
            </div>
            <small>{description}</small>
            """, unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.markdown("**📊 TRL Portfolio Manager** - Desenvolvido para gestão estratégica de projetos de inovação")
st.markdown(f"*Última atualização: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}*")