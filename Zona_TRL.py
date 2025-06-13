import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuração da página
st.set_page_config(
    page_title="Gestão de Portfolio por Zonas TRL",
    page_icon="🔬",
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

# Inicialização do estado da aplicação
if 'projects_df' not in st.session_state:
    st.session_state.projects_df = load_initial_projects()

# Interface principal
def main():
    # Tabs principais
    tab1, tab2 = st.tabs(["📊 Dashboard Interativo", "🎨 Visualização Original"])
    
    with tab1:
        show_interactive_dashboard()
    
    with tab2:
        show_original_html_view()

def show_interactive_dashboard():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔬 Gestão de Portfolio por Zonas TRL</h1>
        <p>Estruturação estratégica do portfolio de inovação baseada em níveis de maturidade tecnológica</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar para gestão de projetos
    with st.sidebar:
        st.header("🛠️ Gestão de Projetos")
        
        action = st.selectbox(
            "Escolha uma ação:",
            ["Visualizar Portfolio", "Adicionar Projeto", "Editar Projeto", "Excluir Projeto"]
        )
        
        if action == "Adicionar Projeto":
            add_project_form()
        elif action == "Editar Projeto":
            edit_project_form()
        elif action == "Excluir Projeto":
            delete_project_form()
    
    # Conteúdo principal
    if st.session_state.projects_df.empty:
        st.warning("Nenhum projeto cadastrado. Use o menu lateral para adicionar projetos.")
        return
    
    # Adicionar coluna de zona
    df = st.session_state.projects_df.copy()
    df['Zona'] = df['TRL'].apply(get_zone_from_trl)
    
    # Dashboard principal
    show_portfolio_dashboard(df)
    
    # Tabela detalhada de projetos
    show_projects_table(df)

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
    descoberta_pct = int((zone_stats.loc['Descoberta', 'Peso'] / total_peso * 100)) if 'Descoberta' in zone_stats.index else 0
    desenvolvimento_pct = int((zone_stats.loc['Desenvolvimento', 'Peso'] / total_peso * 100)) if 'Desenvolvimento' in zone_stats.index else 0
    transferencia_pct = int((zone_stats.loc['Transferência', 'Peso'] / total_peso * 100)) if 'Transferência' in zone_stats.index else 0
    
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
                height: {descoberta_pct * 2.5}px;
            }}

            .development-bar {{
                background: linear-gradient(135deg, #4834d4, #686de0);
                height: {desenvolvimento_pct * 2.5}px;
            }}

            .transfer-bar {{
                background: linear-gradient(135deg, #00d2d3, #54a0ff);
                height: {transferencia_pct * 2.5}px;
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

def add_project_form():
    st.subheader("➕ Adicionar Novo Projeto")
    
    with st.form("add_project"):
        nome = st.text_input("Nome do Projeto", placeholder="Digite o nome do projeto...")
        trl = st.selectbox("Nível TRL", options=list(range(1, 10)), format_func=lambda x: f"TRL {x}")
        peso = st.number_input("Peso do Projeto", min_value=0, max_value=10, value=1)
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Adicionar Projeto", type="primary")
        with col2:
            if st.form_submit_button("Limpar"):
                st.rerun()
        
        if submitted:
            if nome.strip():
                new_project = pd.DataFrame({
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
    
    project_names = st.session_state.projects_df['Nome'].tolist()
    selected_project = st.selectbox("Selecione o projeto para editar:", project_names)
    
    if selected_project:
        project_idx = st.session_state.projects_df[st.session_state.projects_df['Nome'] == selected_project].index[0]
        current_project = st.session_state.projects_df.loc[project_idx]
        
        with st.form("edit_project"):
            nome = st.text_input("Nome do Projeto", value=current_project['Nome'])
            trl = st.selectbox("Nível TRL", options=list(range(1, 10)), 
                             index=current_project['TRL']-1, format_func=lambda x: f"TRL {x}")
            peso = st.number_input("Peso do Projeto", min_value=0, max_value=10, value=int(current_project['Peso']))
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Salvar Alterações", type="primary")
            with col2:
                if st.form_submit_button("Cancelar"):
                    st.rerun()
            
            if submitted:
                if nome.strip():
                    st.session_state.projects_df.loc[project_idx, 'Nome'] = nome.strip()
                    st.session_state.projects_df.loc[project_idx, 'TRL'] = trl
                    st.session_state.projects_df.loc[project_idx, 'Peso'] = peso
                    st.success(f"Projeto '{nome}' atualizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Por favor, insira um nome para o projeto.")

def delete_project_form():
    st.subheader("🗑️ Excluir Projeto")
    
    if st.session_state.projects_df.empty:
        st.info("Nenhum projeto disponível para exclusão.")
        return
    
    project_names = st.session_state.projects_df['Nome'].tolist()
    selected_project = st.selectbox("Selecione o projeto para excluir:", project_names)
    
    if selected_project:
        st.warning(f"⚠️ Você está prestes a excluir o projeto: **{selected_project}**")
        st.write("Esta ação não pode ser desfeita.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirmar Exclusão", type="primary", key="delete_confirm"):
                st.session_state.projects_df = st.session_state.projects_df[
                    st.session_state.projects_df['Nome'] != selected_project
                ].reset_index(drop=True)
                st.success(f"Projeto '{selected_project}' excluído com sucesso!")
                st.rerun()
        with col2:
            if st.button("Cancelar", key="delete_cancel"):
                st.rerun()

def show_portfolio_dashboard(df):
    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Projetos", len(df))
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
                st.write(f"• **{project['Nome']}** (TRL {project['TRL']}, Peso {project['Peso']}) - {trl_desc}")

def show_projects_table(df):
    st.subheader("📋 Lista Completa de Projetos")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        zone_filter = st.multiselect(
            "Filtrar por Zona:",
            options=df['Zona'].unique(),
            default=df['Zona'].unique()
        )
    
    with col2:
        trl_filter = st.multiselect(
            "Filtrar por TRL:",
            options=sorted(df['TRL'].unique()),
            default=sorted(df['TRL'].unique())
        )
    
    with col3:
        search_term = st.text_input("Buscar projeto:", placeholder="Digite o nome do projeto...")
    
    # Aplicar filtros
    filtered_df = df[
        (df['Zona'].isin(zone_filter)) &
        (df['TRL'].isin(trl_filter))
    ]
    
    if search_term:
        filtered_df = filtered_df[
            filtered_df['Nome'].str.contains(search_term, case=False, na=False)
        ]
    
    # Adicionar descrição TRL
    filtered_df_display = filtered_df.copy()
    filtered_df_display['Descrição TRL'] = filtered_df_display['TRL'].apply(get_trl_description)
    
    # Ordenar por zona e TRL
    filtered_df_display = filtered_df_display.sort_values(['Zona', 'TRL', 'Nome'])
    
    # Exibir tabela
    st.dataframe(
        filtered_df_display[['Nome', 'TRL', 'Zona', 'Peso', 'Descrição TRL']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Nome": st.column_config.TextColumn("Nome do Projeto", width="large"),
            "TRL": st.column_config.NumberColumn("TRL", min_value=1, max_value=9),
            "Zona": st.column_config.TextColumn("Zona TRL"),
            "Peso": st.column_config.NumberColumn("Peso"),
            "Descrição TRL": st.column_config.TextColumn("Descrição do TRL", width="large")
        }
    )
    
    # Estatísticas dos projetos filtrados
    if len(filtered_df_display) > 0:
        st.info(f"Exibindo {len(filtered_df_display)} de {len(df)} projetos. Peso total: {filtered_df_display['Peso'].sum()}")
    else:
        st.warning("Nenhum projeto encontrado com os filtros aplicados.")

if __name__ == "__main__":
    main()