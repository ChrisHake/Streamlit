import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="TRL Portfolio Manager Integrado",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
    }
    
    .zone-card {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .discovery-zone {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
    }
    
    .development-zone {
        background: linear-gradient(135deg, #4834d4, #686de0);
        color: white;
    }
    
    .transfer-zone {
        background: linear-gradient(135deg, #00d2d3, #54a0ff);
        color: white;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stAlert > div {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
    }
    
    .matrix-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Dados iniciais dos projetos
@st.cache_data
def load_initial_projects():
    projects_data = [
        ("Inteligência Artificial", 1, 3),
        ("Banheiro WellNess (Feira ExpoRvestir 2025)", 5, 3),
        ("Óxido de Nióbio", 1, 2),
        ("Pesquisa Materiais - LabMat UFSC", 1, 9),
        ("Microbolhas Banheira", 4, 8),
        ("Microbolhas no Arejador", 5, 8),
        ("SunShower", 2, 2),
        ("Gerador de Ozônio - OEM", 5, 8),
        ("BacteriaFree para esmalte cerâmico", 5, 7),
        ("Futuro do sistema de descarga (VD)", 2, 2),
        ("Aplicação Grafeno", 1, 2),
        ("Central de Purificador de Água", 1, 2),
        ("Super Filtro (Água alcalina e antioxidante)", 3, 7),
        ("Nobreak DocolEletric", 2, 2),
        ("Acionamento Salvágua com Trava", 2, 2),
        ("Hydraloop (reciclagem de água)", 1, 2),
        ("WaterTrain (Neoperl)", 3, 7),
        ("Novo acionamento VD Sensor", 2, 2),
        ("Tóten de Hidratação (Água fresca e purificada, alcalina e Antiox)", 2, 2),
        ("Banheiro autolimpante", 1, 2),
        ("Esmalte cerâmico hidrofílico", 1, 2),
        ("Água em nanoescala", 1, 2),
        ("Ducha de Mão com Sabão", 2, 6),
        ("ZeroWaste - Composteira", 2, 2),
        ("Anti mancha no PVD", 2, 2),
        ("Cuba de Cozinha com Microbolhas (Bistro)", 3, 2),
        ("Gerador de Ozônio Docol", 3, 2),
        ("Sensor piezoelétrico (RNC)", 2, 2),
        ("Sensor com tecnologia ToF e Radar", 2, 2),
        ("Mictório Plug&Play (sensor embutido)", 3, 2),
        ("Filtro com fibras orgânicas (Comunidade Amazônia)", 1, 2),
        ("Barra de duchas com diferentes tipos de jatos", 3, 1),
        ("Dobradiça eletrônica sem engrenagem", 1, 1),
        ("Manutenção Ativa Inteligente Docol", 2, 0),
        ("Acabamentos NanoTech (Ciser)", 5, 5)
    ]
    
    df = pd.DataFrame(projects_data, columns=['Nome', 'TRL', 'Peso'])
    df['Index'] = range(1, len(df) + 1)
    return df

# Funções auxiliares
def get_zone_from_trl(trl):
    if 1 <= trl <= 3:
        return "Descoberta"
    elif 4 <= trl <= 6:
        return "Desenvolvimento"
    elif 7 <= trl <= 9:
        return "Transferência"
    else:
        return "Indefinido"

def get_zone_color(zone):
    colors = {
        "Descoberta": "#ee5a24",
        "Desenvolvimento": "#4834d4",
        "Transferência": "#00d2d3"
    }
    return colors.get(zone, "#7f8c8d")

def get_trl_description(trl):
    descriptions = {
        1: "Princípios básicos observados e reportados",
        2: "Conceito tecnológico e/ou aplicação formulados",
        3: "Prova de conceito analítica e experimental",
        4: "Validação de componentes em ambiente laboratorial",
        5: "Validação de componentes em ambiente relevante",
        6: "Demonstração de sistema em ambiente relevante",
        7: "Demonstração de protótipo em ambiente operacional",
        8: "Sistema completo e qualificado",
        9: "Sistema operacional comprovado"
    }
    return descriptions.get(trl, "Descrição não disponível")

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

def get_next_index(df):
    if not df.empty:
        return df['Index'].max() + 1
    return 1

# Inicialização do estado da aplicação
if 'projects_df' not in st.session_state:
    st.session_state.projects_df = load_initial_projects()

# Interface principal
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 TRL Portfolio Manager Integrado</h1>
        <p>Gestão estratégica completa de projetos por níveis de maturidade tecnológica e priorização</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard Interativo", 
        "📈 Matriz TRL vs Peso", 
        "🎨 Visualização Original",
        "📋 Gestão de Projetos"
    ])
    
    with tab1:
        show_interactive_dashboard()
    
    with tab2:
        show_trl_weight_matrix()
    
    with tab3:
        show_original_html_view()
    
    with tab4:
        show_project_management()

def show_interactive_dashboard():
    # Verificar se há projetos
    if st.session_state.projects_df.empty:
        st.warning("Nenhum projeto cadastrado. Use a aba 'Gestão de Projetos' para adicionar projetos.")
        return
    
    # Adicionar coluna de zona
    df = st.session_state.projects_df.copy()
    df['Zona'] = df['TRL'].apply(get_zone_from_trl)
    df['Prioridade'] = df['Peso'].apply(get_priority)
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("🔍 Buscar projeto:", placeholder="Digite o nome do projeto...")
    
    with col2:
        zone_filter = st.multiselect(
            "Filtrar por Zona:",
            options=df['Zona'].unique(),
            default=df['Zona'].unique()
        )
    
    with col3:
        priority_filter = st.multiselect(
            "Filtrar por Prioridade:",
            options=df['Prioridade'].unique(),
            default=df['Prioridade'].unique()
        )
    
    # Aplicar filtros
    filtered_df = df[
        (df['Zona'].isin(zone_filter)) &
        (df['Prioridade'].isin(priority_filter))
    ]
    
    if search_term:
        filtered_df = filtered_df[
            filtered_df['Nome'].str.contains(search_term, case=False, na=False)
        ]
    
    if filtered_df.empty:
        st.warning("Nenhum projeto encontrado com os filtros aplicados.")
        return
    
    # Dashboard principal
    show_portfolio_dashboard(filtered_df)
    
    # Tabela detalhada de projetos
    show_projects_table(filtered_df)

def show_trl_weight_matrix():
    st.header("📈 Matriz Estratégica TRL vs Peso")
    
    if st.session_state.projects_df.empty:
        st.warning("Nenhum projeto cadastrado. Use a aba 'Gestão de Projetos' para adicionar projetos.")
        return
    
    df = st.session_state.projects_df.copy()
    df['Zona'] = df['TRL'].apply(get_zone_from_trl)
    df['Prioridade'] = df['Peso'].apply(get_priority)
    df['Cor_Prioridade'] = df['Peso'].apply(get_priority_color)
    df['Tamanho'] = df['Peso'].apply(lambda x: max(15, x * 8))
    
    # Controles da matriz
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.subheader("🎛️ Controles")
        show_labels = st.checkbox("Mostrar índices dos projetos", value=True)
        show_zones = st.checkbox("Destacar zonas TRL", value=True)
        matrix_height = st.slider("Altura do gráfico", 500, 800, 650)
    
    with col1:
        # Criar gráfico de dispersão interativo
        fig = go.Figure()
        
        # Adicionar pontos por zona
        for zone in ["Descoberta", "Desenvolvimento", "Transferência"]:
            zone_data = df[df['Zona'] == zone]
            if not zone_data.empty:
                fig.add_trace(go.Scatter(
                    x=zone_data['TRL'],
                    y=zone_data['Peso'],
                    mode='markers+text' if show_labels else 'markers',
                    text=zone_data['Index'] if show_labels else None,
                    textposition='middle center',
                    textfont=dict(color='white', size=10, family="Arial Black"),
                    marker=dict(
                        size=zone_data['Tamanho'],
                        color=zone_data['Cor_Prioridade'],
                        line=dict(width=2, color='white'),
                        opacity=0.8
                    ),
                    hovertemplate='<b>%{customdata[0]}</b><br>' +
                                 'TRL: %{x}<br>' +
                                 'Peso: %{y}<br>' +
                                 'Zona: ' + zone + '<br>' +
                                 'Prioridade: %{customdata[1]}<br>' +
                                 '<extra></extra>',
                    customdata=list(zip(zone_data['Nome'], zone_data['Prioridade'])),
                    name=zone,
                    showlegend=True
                ))
        
        # Configurar layout do gráfico
        fig.update_layout(
            title={
                'text': "Matriz de Posicionamento Estratégico TRL vs Peso",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18}
            },
            xaxis_title="Nível TRL (Technology Readiness Level)",
            yaxis_title="Peso do Projeto (Impacto/Prioridade)",
            xaxis=dict(
                tickmode='linear', 
                tick0=1, 
                dtick=1, 
                range=[0.5, 9.5],
                gridcolor='lightgray',
                gridwidth=1
            ),
            yaxis=dict(
                tickmode='linear', 
                tick0=0, 
                dtick=1, 
                range=[-0.5, df['Peso'].max() + 0.5],
                gridcolor='lightgray',
                gridwidth=1
            ),
            height=matrix_height,
            hovermode='closest',
            plot_bgcolor='rgba(248,249,250,0.8)',
            paper_bgcolor='white',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Adicionar linhas de separação das zonas se habilitado
        if show_zones:
            fig.add_vline(
                x=3.5, 
                line_dash="dash", 
                line_color="#2196f3", 
                opacity=0.5, 
                line_width=2,
                annotation_text="Descoberta → Desenvolvimento",
                annotation_position="top"
            )
            fig.add_vline(
                x=6.5, 
                line_dash="dash", 
                line_color="#ff9800", 
                opacity=0.5, 
                line_width=2,
                annotation_text="Desenvolvimento → Transferência",
                annotation_position="top"
            )
            
            # Adicionar áreas de fundo para as zonas
            fig.add_vrect(
                x0=0.5, x1=3.5,
                fillcolor="#e3f2fd", opacity=0.2,
                layer="below", line_width=0
            )
            fig.add_vrect(
                x0=3.5, x1=6.5,
                fillcolor="#fff3e0", opacity=0.2,
                layer="below", line_width=0
            )
            fig.add_vrect(
                x0=6.5, x1=9.5,
                fillcolor="#e8f5e8", opacity=0.2,
                layer="below", line_width=0
            )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Análise da matriz
    st.subheader("💡 Análise Estratégica da Matriz")
    
    # Quadrantes estratégicos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Quadrantes Estratégicos")
        
        # Calcular projetos por quadrante
        q1 = df[(df['TRL'] >= 7) & (df['Peso'] >= 6)]  # Alto TRL, Alto Peso
        q2 = df[(df['TRL'] <= 3) & (df['Peso'] >= 6)]  # Baixo TRL, Alto Peso
        q3 = df[(df['TRL'] <= 3) & (df['Peso'] <= 3)]  # Baixo TRL, Baixo Peso
        q4 = df[(df['TRL'] >= 7) & (df['Peso'] <= 3)]  # Alto TRL, Baixo Peso
        
        st.info(f"""
        **🚀 Implementação (TRL 7-9, Peso Alto):** {len(q1)} projetos
        - Prioridade máxima para comercialização
        
        **💎 Oportunidades (TRL 1-3, Peso Alto):** {len(q2)} projetos  
        - Potencial disruptivo, requer investimento
        
        **🔬 Exploração (TRL 1-3, Peso Baixo):** {len(q3)} projetos
        - Pesquisa básica, monitoramento
        
        **⚡ Refinamento (TRL 7-9, Peso Baixo):** {len(q4)} projetos
        - Otimização ou descontinuação
        """)
    
    with col2:
        st.markdown("### 📊 Estatísticas da Matriz")
        
        # Métricas da matriz
        total_projetos = len(df)
        peso_medio = df['Peso'].mean()
        trl_medio = df['TRL'].mean()
        projetos_criticos = len(df[df['Peso'] >= 8])
        
        st.metric("Total de Projetos", total_projetos)
        st.metric("Peso Médio", f"{peso_medio:.1f}")
        st.metric("TRL Médio", f"{trl_medio:.1f}")
        st.metric("Projetos Críticos", projetos_criticos)
    
    # Legenda de prioridades
    show_priority_legend()

def show_original_html_view():
    # Recalcular estatísticas baseadas nos dados atuais
    df = st.session_state.projects_df.copy()
    df['Zona'] = df['TRL'].apply(get_zone_from_trl)
    
    # Calcular estatísticas por zona
    zone_stats = df.groupby('Zona').agg({
        'Nome': 'count',
        'Peso': 'sum'
    }).rename(columns={'Nome': 'Projetos'})
    
    total_peso = df['Peso'].sum()
    
    # Calcular percentuais
    descoberta_pct = int((zone_stats.loc['Descoberta', 'Peso'] / total_peso * 100)) if 'Descoberta' in zone_stats.index and total_peso > 0 else 0
    desenvolvimento_pct = int((zone_stats.loc['Desenvolvimento', 'Peso'] / total_peso * 100)) if 'Desenvolvimento' in zone_stats.index and total_peso > 0 else 0
    transferencia_pct = int((zone_stats.loc['Transferência', 'Peso'] / total_peso * 100)) if 'Transferência' in zone_stats.index and total_peso > 0 else 0
    
    # Contagem de projetos por zona
    descoberta_count = zone_stats.loc['Descoberta', 'Projetos'] if 'Descoberta' in zone_stats.index else 0
    desenvolvimento_count = zone_stats.loc['Desenvolvimento', 'Projetos'] if 'Desenvolvimento' in zone_stats.index else 0
    transferencia_count = zone_stats.loc['Transferência', 'Projetos'] if 'Transferência' in zone_stats.index else 0
    
    # HTML completo baseado no original
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                min-height: 100vh;
                padding: 20px;
                color: #333;
            }}

            .container {{
                max-width: 1400px;
                margin: 0 auto;
            }}

            .header {{
                text-align: center;
                margin-bottom: 40px;
                color: white;
            }}

            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 15px;
                font-weight: 700;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }}

            .header p {{
                font-size: 1.2em;
                opacity: 0.9;
                max-width: 800px;
                margin: 0 auto;
                line-height: 1.4;
            }}

            .zones-container {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 30px;
                margin: 50px 0;
            }}

            .zone {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                padding: 30px;
                backdrop-filter: blur(10px);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }}

            .zone:hover {{
                transform: translateY(-10px);
                box-shadow: 0 30px 60px rgba(0, 0, 0, 0.3);
            }}

            .zone::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 8px;
                border-radius: 20px 20px 0 0;
            }}

            .discovery-zone::before {{
                background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            }}

            .development-zone::before {{
                background: linear-gradient(135deg, #4834d4, #686de0);
            }}

            .transfer-zone::before {{
                background: linear-gradient(135deg, #00d2d3, #54a0ff);
            }}

            .zone-header {{
                display: flex;
                align-items: center;
                margin-bottom: 25px;
            }}

            .zone-icon {{
                font-size: 3em;
                margin-right: 20px;
                width: 80px;
                height: 80px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                color: white;
            }}

            .discovery-zone .zone-icon {{
                background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            }}

            .development-zone .zone-icon {{
                background: linear-gradient(135deg, #4834d4, #686de0);
            }}

            .transfer-zone .zone-icon {{
                background: linear-gradient(135deg, #00d2d3, #54a0ff);
            }}

            .zone-title {{
                flex: 1;
            }}

            .zone-title h2 {{
                font-size: 1.8em;
                margin-bottom: 5px;
                color: #2c3e50;
            }}

            .zone-title .trl-range {{
                color: #7f8c8d;
                font-weight: 600;
                font-size: 1.1em;
            }}

            .zone-stats {{
                display: flex;
                justify-content: space-between;
                margin: 20px 0;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 12px;
            }}

            .stat {{
                text-align: center;
                flex: 1;
            }}

            .stat-value {{
                font-size: 2em;
                font-weight: 700;
                margin-bottom: 5px;
            }}

            .discovery-zone .stat-value {{
                color: #ee5a24;
            }}

            .development-zone .stat-value {{
                color: #4834d4;
            }}

            .transfer-zone .stat-value {{
                color: #00d2d3;
            }}

            .stat-label {{
                font-size: 0.9em;
                color: #7f8c8d;
                font-weight: 600;
            }}

            .trl-levels {{
                margin: 25px 0;
            }}

            .trl-levels h3 {{
                margin-bottom: 15px;
                color: #2c3e50;
                font-size: 1.2em;
            }}

            .trl-level {{
                display: flex;
                align-items: center;
                padding: 12px;
                margin: 8px 0;
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                transition: all 0.2s ease;
            }}

            .trl-level:hover {{
                transform: translateX(10px);
                box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            }}

            .trl-number {{
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                color: white;
                margin-right: 15px;
                font-size: 1.1em;
            }}

            .discovery-zone .trl-number {{
                background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            }}

            .development-zone .trl-number {{
                background: linear-gradient(135deg, #4834d4, #686de0);
            }}

            .transfer-zone .trl-number {{
                background: linear-gradient(135deg, #00d2d3, #54a0ff);
            }}

            .trl-description {{
                flex: 1;
                font-size: 0.95em;
                line-height: 1.3;
                color: #2c3e50;
            }}

            .characteristics {{
                margin-top: 25px;
            }}

            .characteristics h3 {{
                margin-bottom: 15px;
                color: #2c3e50;
                font-size: 1.2em;
            }}

            .char-list {{
                list-style: none;
            }}

            .char-list li {{
                padding: 8px 0;
                border-bottom: 1px solid #ecf0f1;
                display: flex;
                align-items: center;
                font-size: 0.95em;
                line-height: 1.3;
            }}

            .char-list li::before {{
                content: '✓';
                margin-right: 10px;
                font-weight: 700;
                color: #27ae60;
                font-size: 1.1em;
            }}

            .portfolio-overview {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                padding: 40px;
                margin: 50px 0;
                backdrop-filter: blur(10px);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
            }}

            .portfolio-overview h2 {{
                text-align: center;
                margin-bottom: 30px;
                color: #2c3e50;
                font-size: 2em;
            }}

            .resource-allocation {{
                display: flex;
                justify-content: center;
                align-items: end;
                gap: 40px;
                margin: 40px 0;
                height: 300px;
            }}

            .allocation-bar {{
                width: 120px;
                background: #ecf0f1;
                border-radius: 10px;
                position: relative;
                display: flex;
                flex-direction: column;
                justify-content: end;
                padding: 10px;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            }}

            .bar-fill {{
                border-radius: 10px;
                transition: all 1s ease;
                display: flex;
                align-items: end;
                justify-content: center;
                color: white;
                font-weight: 700;
                font-size: 1.2em;
                padding: 10px;
            }}

            .discovery-bar {{
                background: linear-gradient(135deg, #ff6b6b, #ee5a24);
                height: {max(20, descoberta_pct * 2.5)}px;
            }}

            .development-bar {{
                background: linear-gradient(135deg, #4834d4, #686de0);
                height: {max(20, desenvolvimento_pct * 2.5)}px;
            }}

            .transfer-bar {{
                background: linear-gradient(135deg, #00d2d3, #54a0ff);
                height: {max(20, transferencia_pct * 2.5)}px;
            }}

            .bar-label {{
                text-align: center;
                margin-top: 15px;
                font-weight: 600;
                color: #2c3e50;
            }}

            .insights {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 25px;
                margin-top: 40px;
            }}

            .insight-card {{
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                border-left: 5px solid;
            }}

            .insight-card.discovery {{ border-left-color: #ee5a24; }}
            .insight-card.development {{ border-left-color: #4834d4; }}
            .insight-card.transfer {{ border-left-color: #00d2d3; }}

            .insight-card h4 {{
                margin-bottom: 15px;
                color: #2c3e50;
                font-size: 1.1em;
            }}

            .insight-card p {{
                color: #7f8c8d;
                line-height: 1.4;
                font-size: 0.95em;
            }}

            @media (max-width: 768px) {{
                .zones-container {{
                    grid-template-columns: 1fr;
                }}
                
                .resource-allocation {{
                    flex-direction: column;
                    height: auto;
                    gap: 20px;
                }}
                
                .allocation-bar {{
                    width: 100%;
                    height: 60px;
                    flex-direction: row;
                    align-items: center;
                }}
                
                .bar-fill {{
                    height: 100%;
                    align-items: center;
                }}
                
                .discovery-bar {{ width: {descoberta_pct}%; }}
                .development-bar {{ width: {desenvolvimento_pct}%; }}
                .transfer-bar {{ width: {transferencia_pct}%; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Gestão de Portfolio por Zonas TRL</h1>
                <p>Estruturação estratégica do portfolio de inovação baseada em níveis de maturidade tecnológica</p>
            </div>

            <div class="zones-container">
                <!-- Zona de Descoberta -->
                <div class="zone discovery-zone">
                    <div class="zone-header">
                        <div class="zone-icon">🔬</div>
                        <div class="zone-title">
                            <h2>Zona de Descoberta</h2>
                            <div class="trl-range">TRL 1 - 3</div>
                        </div>
                    </div>

                    <div class="zone-stats">
                        <div class="stat">
                            <div class="stat-value">{descoberta_pct}%</div>
                            <div class="stat-label">Recursos</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">{descoberta_count}</div>
                            <div class="stat-label">Projetos</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">Alta</div>
                            <div class="stat-label">Incerteza</div>
                        </div>
                    </div>

                    <div class="trl-levels">
                        <h3>Níveis TRL</h3>
                        <div class="trl-level">
                            <div class="trl-number">1</div>
                            <div class="trl-description">Princípios básicos observados e reportados</div>
                        </div>
                        <div class="trl-level">
                            <div class="trl-number">2</div>
                            <div class="trl-description">Conceito tecnológico e/ou aplicação formulados</div>
                        </div>
                        <div class="trl-level">
                            <div class="trl-number">3</div>
                            <div class="trl-description">Prova de conceito analítica e experimental</div>
                        </div>
                    </div>

                    <div class="characteristics">
                        <h3>Características</h3>
                        <ul class="char-list">
                            <li>Exploração de possibilidades científicas</li>
                            <li>Experimentos conceituais e simulações</li>
                            <li>Alto risco, alto potencial disruptivo</li>
                            <li>Ciclos de investigação de 2-4 semanas</li>
                            <li>Foco em validação de princípios básicos</li>
                            <li>Documentação científica fundamental</li>
                        </ul>
                    </div>
                </div>

                <!-- Zona de Desenvolvimento -->
                <div class="zone development-zone">
                    <div class="zone-header">
                        <div class="zone-icon">⚙️</div>
                        <div class="zone-title">
                            <h2>Zona de Desenvolvimento</h2>
                            <div class="trl-range">TRL 4 - 6</div>
                        </div>
                    </div>

                    <div class="zone-stats">
                        <div class="stat">
                            <div class="stat-value">{desenvolvimento_pct}%</div>
                            <div class="stat-label">Recursos</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">{desenvolvimento_count}</div>
                            <div class="stat-label">Projetos</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">Média</div>
                            <div class="stat-label">Incerteza</div>
                        </div>
                    </div>

                    <div class="trl-levels">
                        <h3>Níveis TRL</h3>
                        <div class="trl-level">
                            <div class="trl-number">4</div>
                            <div class="trl-description">Validação de componentes em ambiente laboratorial</div>
                        </div>
                        <div class="trl-level">
                            <div class="trl-number">5</div>
                            <div class="trl-description">Validação de componentes em ambiente relevante</div>
                        </div>
                        <div class="trl-level">
                            <div class="trl-number">6</div>
                            <div class="trl-description">Demonstração de sistema em ambiente relevante</div>
                        </div>
                    </div>

                    <div class="characteristics">
                        <h3>Características</h3>
                        <ul class="char-list">
                            <li>Validação e integração de componentes</li>
                            <li>Protótipos funcionais e testes sistêmicos</li>
                            <li>Risco moderado, foco em viabilidade</li>
                            <li>Ciclos de investigação de 6-8 semanas</li>
                            <li>Demonstrações em ambiente controlado</li>
                            <li>Especificações técnicas detalhadas</li>
                        </ul>
                    </div>
                </div>

                <!-- Zona de Transferência -->
                <div class="zone transfer-zone">
                    <div class="zone-header">
                        <div class="zone-icon">🚀</div>
                        <div class="zone-title">
                            <h2>Zona de Transferência</h2>
                            <div class="trl-range">TRL 7 - 9</div>
                        </div>
                    </div>

                    <div class="zone-stats">
                        <div class="stat">
                            <div class="stat-value">{transferencia_pct}%</div>
                            <div class="stat-label">Recursos</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">{transferencia_count}</div>
                            <div class="stat-label">Projetos</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">Baixa</div>
                            <div class="stat-label">Incerteza</div>
                        </div>
                    </div>

                    <div class="trl-levels">
                        <h3>Níveis TRL</h3>
                        <div class="trl-level">
                            <div class="trl-number">7</div>
                            <div class="trl-description">Demonstração de protótipo em ambiente operacional</div>
                        </div>
                        <div class="trl-level">
                            <div class="trl-number">8</div>
                            <div class="trl-description">Sistema completo e qualificado</div>
                        </div>
                        <div class="trl-level">
                            <div class="trl-number">9</div>
                            <div class="trl-description">Sistema operacional comprovado</div>
                        </div>
                    </div>

                    <div class="characteristics">
                        <h3>Características</h3>
                        <ul class="char-list">
                            <li>Preparação para implementação comercial</li>
                            <li>Validação em ambiente operacional real</li>
                            <li>Baixo risco, foco em confiabilidade</li>
                            <li>Processos de transferência estruturados</li>
                            <li>Certificações e qualificações</li>
                            <li>Documentação para produção</li>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="portfolio-overview">
                <h2>Distribuição Estratégica de Recursos</h2>
                
                <div class="resource-allocation">
                    <div class="allocation-bar">
                        <div class="bar-fill discovery-bar">{descoberta_pct}%</div>
                        <div class="bar-label">Descoberta</div>
                    </div>
                    <div class="allocation-bar">
                        <div class="bar-fill development-bar">{desenvolvimento_pct}%</div>
                        <div class="bar-label">Desenvolvimento</div>
                    </div>
                    <div class="allocation-bar">
                        <div class="bar-fill transfer-bar">{transferencia_pct}%</div>
                        <div class="bar-label">Transferência</div>
                    </div>
                </div>

                <div class="insights">
                    <div class="insight-card discovery">
                        <h4>🔬 Estratégia de Descoberta</h4>
                        <p>Maior alocação de recursos para exploração de territórios inexplorados. Aceita alta taxa de falha em troca do potencial de descobertas disruptivas que podem redefinir mercados.</p>
                    </div>
                    
                    <div class="insight-card development">
                        <h4>⚙️ Estratégia de Desenvolvimento</h4>
                        <p>Equilíbrio entre inovação e execução. Foco na transformação de conceitos promissores em soluções viáveis, com gestão ativa de riscos técnicos.</p>
                    </div>
                    
                    <div class="insight-card transfer">
                        <h4>🚀 Estratégia de Transferência</h4>
                        <p>Menor alocação, mas crítica para materializar o valor da inovação. Garante que descobertas se tornem produtos comercializáveis com qualidade e confiabilidade.</p>
                    </div>
                    
                    <div class="insight-card discovery">
                        <h4>📊 Gestão de Portfolio</h4>
                        <p>Portfolio balanceado garante fluxo contínuo de inovações. Projetos fluem naturalmente entre zonas conforme amadurecem, mantendo pipeline de oportunidades.</p>
                    </div>
                    
                    <div class="insight-card development">
                        <h4>⚡ Dinâmica de Transição</h4>
                        <p>Pontos de sincronização entre zonas permitem transferência eficiente de conhecimento e recursos. Evita gargalos e maximiza aproveitamento de descobertas.</p>
                    </div>
                    
                    <div class="insight-card transfer">
                        <h4>🎯 Métricas Diferenciadas</h4>
                        <p>Cada zona tem KPIs específicos: descoberta mede aprendizado, desenvolvimento mede viabilidade, transferência mede preparação comercial.</p>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Renderizar HTML
    st.components.v1.html(html_content, height=2000, scrolling=True)

def show_project_management():
    st.header("📋 Gestão Completa de Projetos")
    
    # Seções de gerenciamento
    management_option = st.selectbox(
        "Escolha uma ação:",
        ["Visualizar Todos", "Adicionar Projeto", "Editar Projeto", "Excluir Projeto", "Importar/Exportar"]
    )
    
    if management_option == "Adicionar Projeto":
        add_project_form()
    elif management_option == "Editar Projeto":
        edit_project_form()
    elif management_option == "Excluir Projeto":
        delete_project_form()
    elif management_option == "Importar/Exportar":
        import_export_section()
    else:
        show_all_projects_management()

def show_all_projects_management():
    if st.session_state.projects_df.empty:
        st.info("Nenhum projeto cadastrado. Use as opções acima para adicionar projetos.")
        return
    
    df = st.session_state.projects_df.copy()
    df['Zona'] = df['TRL'].apply(get_zone_from_trl)
    df['Prioridade'] = df['Peso'].apply(get_priority)
    df['Descrição TRL'] = df['TRL'].apply(get_trl_description)
    
    # Estatísticas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Projetos", len(df))
    with col2:
        st.metric("Peso Total", df['Peso'].sum())
    with col3:
        st.metric("TRL Médio", f"{df['TRL'].mean():.1f}")
    with col4:
        st.metric("Projetos Críticos", len(df[df['Peso'] >= 8]))
    
    # Tabela completa com todas as informações
    st.subheader("📊 Tabela Completa de Projetos")
    
    # Ordenar por prioridade e TRL
    df_display = df.sort_values(['Peso', 'TRL'], ascending=[False, True])
    
    st.dataframe(
        df_display[['Index', 'Nome', 'TRL', 'Peso', 'Zona', 'Prioridade', 'Descrição TRL']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Index": st.column_config.NumberColumn("ID", width="small"),
            "Nome": st.column_config.TextColumn("Nome do Projeto", width="large"),
            "TRL": st.column_config.NumberColumn("TRL", min_value=1, max_value=9, width="small"),
            "Peso": st.column_config.NumberColumn("Peso", width="small"),
            "Zona": st.column_config.TextColumn("Zona TRL", width="medium"),
            "Prioridade": st.column_config.TextColumn("Prioridade", width="medium"),
            "Descrição TRL": st.column_config.TextColumn("Descrição do TRL", width="large")
        }
    )

def add_project_form():
    st.subheader("➕ Adicionar Novo Projeto")
    
    with st.form("add_project"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome do Projeto", placeholder="Digite o nome do projeto...")
            trl = st.selectbox("Nível TRL", options=list(range(1, 10)), format_func=lambda x: f"TRL {x}")
        
        with col2:
            peso = st.number_input("Peso do Projeto", min_value=0, max_value=10, value=1)
            st.write(f"**Zona:** {get_zone_from_trl(trl)}")
            st.write(f"**Prioridade:** {get_priority(peso)}")
        
        # Descrição do TRL selecionado
        st.info(f"**TRL {trl}:** {get_trl_description(trl)}")
        
        submitted = st.form_submit_button("Adicionar Projeto", type="primary")
        
        if submitted:
            if nome.strip():
                new_index = get_next_index(st.session_state.projects_df)
                new_project = pd.DataFrame({
                    'Index': [new_index],
                    'Nome': [nome.strip()],
                    'TRL': [trl],
                    'Peso': [peso]
                })
                st.session_state.projects_df = pd.concat([st.session_state.projects_df, new_project], ignore_index=True)
                st.success(f"Projeto '{nome}' adicionado com sucesso!")
                st.rerun()
            else:
                st.error("Por favor, insira um nome para o projeto.")

def edit_project_form():
    st.subheader("✏️ Editar Projeto")
    
    if st.session_state.projects_df.empty:
        st.info("Nenhum projeto disponível para edição.")
        return
    
    df = st.session_state.projects_df.copy()
    project_options = {f"{row['Index']} - {row['Nome']}": row for _, row in df.iterrows()}
    selected_project_key = st.selectbox("Selecione o projeto para editar:", list(project_options.keys()))
    
    if selected_project_key:
        selected_project = project_options[selected_project_key]
        
        with st.form("edit_project"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome do Projeto", value=selected_project['Nome'])
                trl = st.selectbox("Nível TRL", options=list(range(1, 10)), 
                                 index=selected_project['TRL']-1, format_func=lambda x: f"TRL {x}")
            
            with col2:
                peso = st.number_input("Peso do Projeto", min_value=0, max_value=10, value=int(selected_project['Peso']))
                st.write(f"**Zona:** {get_zone_from_trl(trl)}")
                st.write(f"**Prioridade:** {get_priority(peso)}")
            
            # Descrição do TRL selecionado
            st.info(f"**TRL {trl}:** {get_trl_description(trl)}")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Salvar Alterações", type="primary")
            with col2:
                cancel = st.form_submit_button("Cancelar")
            
            if submitted:
                if nome.strip():
                    # Atualizar o projeto
                    mask = st.session_state.projects_df['Index'] == selected_project['Index']
                    st.session_state.projects_df.loc[mask, 'Nome'] = nome.strip()
                    st.session_state.projects_df.loc[mask, 'TRL'] = trl
                    st.session_state.projects_df.loc[mask, 'Peso'] = peso
                    st.success(f"Projeto '{nome}' atualizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Por favor, insira um nome para o projeto.")
            
            if cancel:
                st.rerun()

def delete_project_form():
    st.subheader("🗑️ Excluir Projeto")
    
    if st.session_state.projects_df.empty:
        st.info("Nenhum projeto disponível para exclusão.")
        return
    
    df = st.session_state.projects_df.copy()
    project_options = {f"{row['Index']} - {row['Nome']}": row for _, row in df.iterrows()}
    selected_project_key = st.selectbox("Selecione o projeto para excluir:", list(project_options.keys()))
    
    if selected_project_key:
        selected_project = project_options[selected_project_key]
        
        st.warning(f"⚠️ Você está prestes a excluir o projeto: **{selected_project['Nome']}**")
        st.write("Esta ação não pode ser desfeita.")
        
        # Mostrar informações do projeto
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("TRL", selected_project['TRL'])
        with col2:
            st.metric("Peso", selected_project['Peso'])
        with col3:
            st.metric("Zona", get_zone_from_trl(selected_project['TRL']))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirmar Exclusão", type="primary", key="delete_confirm"):
                st.session_state.projects_df = st.session_state.projects_df[
                    st.session_state.projects_df['Index'] != selected_project['Index']
                ].reset_index(drop=True)
                st.success(f"Projeto '{selected_project['Nome']}' excluído com sucesso!")
                st.rerun()
        with col2:
            if st.button("Cancelar", key="delete_cancel"):
                st.rerun()

def import_export_section():
    st.subheader("📁 Importação e Exportação de Projetos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📤 Exportar Projetos")
        
        if not st.session_state.projects_df.empty:
            # Preparar dados para exportação
            export_data = st.session_state.projects_df.to_dict('records')
            json_data = json.dumps(export_data, indent=2, ensure_ascii=False)
            
            st.download_button(
                label="💾 Download JSON",
                data=json_data,
                file_name=f"projetos_trl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                help="Baixar todos os projetos em formato JSON"
            )
            
            # Também disponibilizar CSV
            csv_data = st.session_state.projects_df.to_csv(index=False)
            st.download_button(
                label="💾 Download CSV",
                data=csv_data,
                file_name=f"projetos_trl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                help="Baixar todos os projetos em formato CSV"
            )
        else:
            st.info("Nenhum projeto para exportar.")
    
    with col2:
        st.markdown("### 📥 Importar Projetos")
        
        uploaded_file = st.file_uploader("Carregar arquivo", type=['json', 'csv'])
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.json'):
                    imported_data = json.load(uploaded_file)
                    if isinstance(imported_data, list):
                        df_imported = pd.DataFrame(imported_data)
                    else:
                        st.error("Formato JSON inválido. Esperado uma lista de projetos.")
                        return
                elif uploaded_file.name.endswith('.csv'):
                    df_imported = pd.read_csv(uploaded_file)
                
                # Verificar se as colunas necessárias existem
                required_columns = ['Nome', 'TRL', 'Peso']
                if all(col in df_imported.columns for col in required_columns):
                    st.success(f"Arquivo válido com {len(df_imported)} projetos encontrados.")
                    
                    # Mostrar preview
                    st.write("**Preview dos dados:**")
                    st.dataframe(df_imported.head(), use_container_width=True)
                    
                    # Opções de importação
                    import_option = st.radio(
                        "Como importar?",
                        ["Substituir todos os projetos", "Adicionar aos projetos existentes"]
                    )
                    
                    if st.button("Confirmar Importação", type="primary"):
                        if import_option == "Substituir todos os projetos":
                            # Recriar índices
                            df_imported['Index'] = range(1, len(df_imported) + 1)
                            st.session_state.projects_df = df_imported[['Index', 'Nome', 'TRL', 'Peso']]
                        else:
                            # Adicionar aos existentes
                            next_index = get_next_index(st.session_state.projects_df)
                            df_imported['Index'] = range(next_index, next_index + len(df_imported))
                            st.session_state.projects_df = pd.concat([
                                st.session_state.projects_df, 
                                df_imported[['Index', 'Nome', 'TRL', 'Peso']]
                            ], ignore_index=True)
                        
                        st.success(f"Importação concluída! {len(df_imported)} projetos processados.")
                        st.rerun()
                else:
                    missing_cols = [col for col in required_columns if col not in df_imported.columns]
                    st.error(f"Colunas obrigatórias ausentes: {missing_cols}")
            
            except Exception as e:
                st.error(f"Erro ao processar arquivo: {str(e)}")

def show_portfolio_dashboard(df):
    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Projetos Filtrados", len(df))
    with col2:
        st.metric("Peso Total", df['Peso'].sum())
    with col3:
        st.metric("TRL Médio", f"{df['TRL'].mean():.1f}")
    with col4:
        zones_count = df['Zona'].nunique()
        st.metric("Zonas Ativas", zones_count)
    
    st.divider()
    
    # Distribuição por zonas
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 Distribuição de Projetos por Zona")
        
        zone_stats = df.groupby('Zona').agg({
            'Nome': 'count',
            'Peso': 'sum'
        }).rename(columns={'Nome': 'Projetos'})
        
        # Gráfico de barras
        fig_bar = px.bar(
            zone_stats.reset_index(),
            x='Zona',
            y='Projetos',
            color='Zona',
            color_discrete_map={
                'Descoberta': '#ee5a24',
                'Desenvolvimento': '#4834d4',
                'Transferência': '#00d2d3'
            },
            title="Número de Projetos por Zona"
        )
        fig_bar.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Distribuição de Peso por Zona")
        
        # Gráfico de pizza
        fig_pie = px.pie(
            zone_stats.reset_index(),
            values='Peso',
            names='Zona',
            color='Zona',
            color_discrete_map={
                'Descoberta': '#ee5a24',
                'Desenvolvimento': '#4834d4',
                'Transferência': '#00d2d3'
            }
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Cards das zonas
    st.subheader("🔍 Visão Detalhada por Zona")
    
    for zone in ['Descoberta', 'Desenvolvimento', 'Transferência']:
        zone_projects = df[df['Zona'] == zone]
        if len(zone_projects) > 0:
            show_zone_card(zone, zone_projects)

def show_zone_card(zone, projects):
    # Definir informações da zona
    zone_info = {
        'Descoberta': {
            'icon': '🔬',
            'trl_range': 'TRL 1-3',
            'description': 'Exploração de possibilidades científicas e validação de conceitos',
            'characteristics': [
                'Experimentos conceituais e simulações',
                'Alto risco, alto potencial disruptivo',
                'Foco em validação de princípios básicos'
            ]
        },
        'Desenvolvimento': {
            'icon': '⚙️',
            'trl_range': 'TRL 4-6',
            'description': 'Validação e integração de componentes em ambiente controlado',
            'characteristics': [
                'Protótipos funcionais e testes sistêmicos',
                'Risco moderado, foco em viabilidade',
                'Demonstrações em ambiente relevante'
            ]
        },
        'Transferência': {
            'icon': '🚀',
            'trl_range': 'TRL 7-9',
            'description': 'Preparação para implementação comercial',
            'characteristics': [
                'Validação em ambiente operacional real',
                'Baixo risco, foco em confiabilidade',
                'Processos de transferência estruturados'
            ]
        }
    }
    
    info = zone_info[zone]
    
    with st.expander(f"{info['icon']} {zone} ({info['trl_range']}) - {len(projects)} projetos", expanded=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write(f"**Descrição:** {info['description']}")
            st.write("**Características:**")
            for char in info['characteristics']:
                st.write(f"• {char}")
        
        with col2:
            st.metric("Projetos", len(projects))
            st.metric("Peso Total", projects['Peso'].sum())
            st.metric("TRL Médio", f"{projects['TRL'].mean():.1f}")
        
        # Projetos na zona
        if len(projects) > 0:
            st.write("**Projetos nesta zona:**")
            for _, project in projects.iterrows():
                trl_desc = get_trl_description(project['TRL'])
                priority = get_priority(project['Peso'])
                st.write(f"• **{project['Nome']}** (TRL {project['TRL']}, Peso {project['Peso']}, {priority}) - {trl_desc}")

def show_projects_table(df):
    st.subheader("📋 Lista Completa de Projetos")
    
    # Adicionar descrição TRL
    df_display = df.copy()
    df_display['Descrição TRL'] = df_display['TRL'].apply(get_trl_description)
    
    # Ordenar por zona e TRL
    df_display = df_display.sort_values(['Zona', 'TRL', 'Nome'])
    
    # Exibir tabela
    st.dataframe(
        df_display[['Index', 'Nome', 'TRL', 'Zona', 'Peso', 'Prioridade', 'Descrição TRL']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Index": st.column_config.NumberColumn("ID", width="small"),
            "Nome": st.column_config.TextColumn("Nome do Projeto", width="large"),
            "TRL": st.column_config.NumberColumn("TRL", min_value=1, max_value=9, width="small"),
            "Zona": st.column_config.TextColumn("Zona TRL", width="medium"),
            "Peso": st.column_config.NumberColumn("Peso", width="small"),
            "Prioridade": st.column_config.TextColumn("Prioridade", width="medium"),
            "Descrição TRL": st.column_config.TextColumn("Descrição do TRL", width="large")
        }
    )
    
    # Estatísticas dos projetos filtrados
    if len(df_display) > 0:
        st.info(f"Exibindo {len(df_display)} projetos. Peso total: {df_display['Peso'].sum()}")
    else:
        st.warning("Nenhum projeto encontrado com os filtros aplicados.")

def show_priority_legend():
    st.subheader("🎨 Legenda de Prioridades")
    
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

# Executar aplicação principal
if __name__ == "__main__":
    main()

# Rodapé
st.markdown("---")
st.markdown("**🚀 TRL Portfolio Manager Integrado** - Desenvolvido para gestão estratégica completa de projetos de inovação")
st.markdown(f"*Última atualização: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}*")