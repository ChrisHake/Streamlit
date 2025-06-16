import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from typing import Dict, List, Tuple
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Sistema de Priorização TRL",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

class TRLMatrixSystem:
    def __init__(self):
        self.inicializar_dados()
    
    def inicializar_dados(self):
        """Inicializa os dados dos projetos"""
        if 'projetos' not in st.session_state:
            st.session_state.projetos = self.carregar_projetos_iniciais()
    
    def carregar_projetos_iniciais(self) -> List[Dict]:
        """Carrega a lista inicial de projetos fornecida"""
        projetos_iniciais = [
            {"nome": "Inteligência Artificial", "trl": 1, "impacto": "Alto", "dificuldade": "Difícil", "peso": 3},
            {"nome": "Banheiro WellNess (Feira ExpoRvestir 2025)", "trl": 5, "impacto": "Alto", "dificuldade": "Moderada", "peso": 3},
            {"nome": "Óxido de Nióbio", "trl": 1, "impacto": "Médio", "dificuldade": "Difícil", "peso": 2},
            {"nome": "Pesquisa Materiais - LabMat UFSC", "trl": 1, "impacto": "Alto", "dificuldade": "Difícil", "peso": 9},
            {"nome": "Microbolhas Banheira", "trl": 4, "impacto": "Médio", "dificuldade": "Moderada", "peso": 8},
            {"nome": "Microbolhas no Arejador", "trl": 5, "impacto": "Médio", "dificuldade": "Moderada", "peso": 8},
            {"nome": "SunShower", "trl": 2, "impacto": "Baixo", "dificuldade": "Difícil", "peso": 2},
            {"nome": "Gerador de Ozônio - OEM", "trl": 5, "impacto": "Médio", "dificuldade": "Moderada", "peso": 8},
            {"nome": "BacteriaFree para esmalte cerâmico", "trl": 5, "impacto": "Médio", "dificuldade": "Fácil", "peso": 7},
            {"nome": "Futuro do sistema de descarga (VD)", "trl": 2, "impacto": "Baixo", "dificuldade": "Difícil", "peso": 2},
            {"nome": "Aplicação Grafeno", "trl": 1, "impacto": "Alto", "dificuldade": "Difícil", "peso": 2},
            {"nome": "Central de Purificador de Água", "trl": 1, "impacto": "Médio", "dificuldade": "Difícil", "peso": 2},
            {"nome": "Super Filtro (Água alcalina e antioxidante)", "trl": 3, "impacto": "Médio", "dificuldade": "Fácil", "peso": 7},
            {"nome": "Nobreak DocolEletric", "trl": 2, "impacto": "Baixo", "dificuldade": "Difícil", "peso": 2},
            {"nome": "Acionamento Salvágua com Trava", "trl": 2, "impacto": "Baixo", "dificuldade": "Difícil", "peso": 2},
            {"nome": "Hydraloop (reciclagem de água)", "trl": 1, "impacto": "Alto", "dificuldade": "Difícil", "peso": 2},
            {"nome": "WaterTrain (Neoperl)", "trl": 3, "impacto": "Médio", "dificuldade": "Fácil", "peso": 7},
            {"nome": "Novo acionamento VD Sensor", "trl": 2, "impacto": "Baixo", "dificuldade": "Difícil", "peso": 2},
            {"nome": "Tóten de Hidratação (Água fresca e purificada, alcalina e Antiox)", "trl": 2, "impacto": "Baixo", "dificuldade": "Difícil", "peso": 2},
            {"nome": "Banheiro autolimpante", "trl": 1, "impacto": "Alto", "dificuldade": "Difícil", "peso": 2},
            {"nome": "Esmalte cerâmico hidrofílico", "trl": 1, "impacto": "Médio", "dificuldade": "Difícil", "peso": 2},
            {"nome": "Água em nanoescala", "trl": 1, "impacto": "Alto", "dificuldade": "Difícil", "peso": 2},
            {"nome": "Ducha de Mão com Sabão", "trl": 2, "impacto": "Baixo", "dificuldade": "Moderada", "peso": 6},
            {"nome": "ZeroWaste - Composteira", "trl": 2, "impacto": "Baixo", "dificuldade": "Difícil", "peso": 2},
            {"nome": "Anti mancha no PVD", "trl": 2, "impacto": "Baixo", "dificuldade": "Difícil", "peso": 2},
            {"nome": "Cuba de Cozinha com Microbolhas (Bistro)", "trl": 3, "impacto": "Baixo", "dificuldade": "Moderada", "peso": 2},
            {"nome": "Gerador de Ozônio Docol", "trl": 3, "impacto": "Baixo", "dificuldade": "Moderada", "peso": 2},
            {"nome": "Sensor piezoelétrico (RNC)", "trl": 2, "impacto": "Baixo", "dificuldade": "Difícil", "peso": 2},
            {"nome": "Sensor com tecnologia ToF e Radar", "trl": 2, "impacto": "Baixo", "dificuldade": "Difícil", "peso": 2},
            {"nome": "Mictório Plug&Play (sensor embutido)", "trl": 3, "impacto": "Baixo", "dificuldade": "Moderada", "peso": 2},
            {"nome": "Filtro com fibras orgânicas (Comunidade Amazônia)", "trl": 1, "impacto": "Médio", "dificuldade": "Difícil", "peso": 2},
            {"nome": "Barra de duchas com diferentes tipos de jatos", "trl": 3, "impacto": "Baixo", "dificuldade": "Fácil", "peso": 1},
            {"nome": "Dobradiça eletrônica sem engrenagem", "trl": 1, "impacto": "Baixo", "dificuldade": "Fácil", "peso": 1},
            {"nome": "Manutenção Ativa Inteligente Docol", "trl": 2, "impacto": "Baixo", "dificuldade": "Fácil", "peso": 0},
            {"nome": "Acabamentos NanoTech (Ciser)", "trl": 5, "impacto": "Médio", "dificuldade": "Fácil", "peso": 5}
        ]
        return projetos_iniciais
    
    def calcular_prioridade(self, impacto: str, dificuldade: str) -> int:
        """Calcula a prioridade baseada no impacto e dificuldade"""
        matriz_prioridade = {
            ('Alto', 'Fácil'): 1,
            ('Alto', 'Moderada'): 2,
            ('Alto', 'Difícil'): 3,
            ('Médio', 'Fácil'): 4,
            ('Médio', 'Moderada'): 5,
            ('Médio', 'Difícil'): 6,
            ('Baixo', 'Fácil'): 7,
            ('Baixo', 'Moderada'): 8,
            ('Baixo', 'Difícil'): 9
        }
        return matriz_prioridade.get((impacto, dificuldade), 9)
    
    def criar_dataframe(self, projetos_filtrados=None):
        """Cria DataFrame dos projetos"""
        if projetos_filtrados is None:
            projetos = st.session_state.projetos
        else:
            projetos = projetos_filtrados
            
        df = pd.DataFrame(projetos)
        if not df.empty:
            df['prioridade'] = df.apply(lambda x: self.calcular_prioridade(x['impacto'], x['dificuldade']), axis=1)
            df = df.sort_values(['prioridade', 'peso'], ascending=[True, False])
        return df
    
    def criar_matriz_visual(self, df):
        """Cria a matriz visual de priorização"""
        # Preparar dados para a matriz - ordenar impactos de baixo para alto
        impactos = ['Baixo', 'Médio', 'Alto']  # Invertido para ter Alto no topo
        dificuldades = ['Difícil', 'Moderada', 'Fácil']  # Invertido: Difícil próximo à origem, Fácil no extremo
        
        # Contar projetos por categoria
        matriz_contagem = np.zeros((3, 3))
        matriz_labels = []
        
        for i, impacto in enumerate(impactos):
            row_labels = []
            for j, dificuldade in enumerate(dificuldades):
                count = len(df[(df['impacto'] == impacto) & (df['dificuldade'] == dificuldade)])
                matriz_contagem[i][j] = count
                prioridade = self.calcular_prioridade(impacto, dificuldade)
                row_labels.append(f"P{prioridade}<br>{count} projetos")
            matriz_labels.append(row_labels)
        
        # Criar heatmap
        fig = go.Figure(data=go.Heatmap(
            z=matriz_contagem,
            x=dificuldades,
            y=impactos,
            text=matriz_labels,
            texttemplate="%{text}",
            textfont={"size": 12, "color": "white"},
            colorscale=[[0, '#95a5a6'], [0.3, '#f1c40f'], [0.6, '#f39c12'], [1, '#e74c3c']],
            showscale=False,
            hoverongaps=False
        ))
        
        fig.update_layout(
            title={
                'text': "Matriz de Priorização TRL<br><sub>Impacto vs Dificuldade da Próxima Transição</sub>",
                'x': 0.5,
                'font': {'size': 16, 'color': '#2c3e50'}
            },
            xaxis_title="Dificuldade da Próxima Transição TRL",
            yaxis_title="Impacto Potencial",
            font=dict(size=12),
            height=400,
            plot_bgcolor='white'
        )
        
        return fig
    
    def criar_dashboard_analytics(self, df):
        """Cria gráficos de análise dos dados"""
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de distribuição por prioridade
            prioridade_counts = df['prioridade'].value_counts().sort_index()
            fig_prioridade = px.bar(
                x=[f"P{p}" for p in prioridade_counts.index],
                y=prioridade_counts.values,
                title="Distribuição por Prioridade",
                color=prioridade_counts.values,
                color_continuous_scale=['#95a5a6', '#f1c40f', '#f39c12', '#e74c3c']
            )
            fig_prioridade.update_layout(showlegend=False, xaxis_title="Prioridade", yaxis_title="Quantidade")
            st.plotly_chart(fig_prioridade, use_container_width=True)
        
        with col2:
            # Gráfico de distribuição por TRL
            trl_counts = df['trl'].value_counts().sort_index()
            fig_trl = px.bar(
                x=[f"TRL {t}" for t in trl_counts.index],
                y=trl_counts.values,
                title="Distribuição por TRL",
                color=trl_counts.values,
                color_continuous_scale="Blues"
            )
            fig_trl.update_layout(showlegend=False, xaxis_title="TRL", yaxis_title="Quantidade")
            st.plotly_chart(fig_trl, use_container_width=True)
        
        # Scatter plot: Peso vs TRL colorido por prioridade
        fig_scatter = px.scatter(
            df, x='trl', y='peso', color='prioridade',
            hover_data=['nome', 'impacto', 'dificuldade'],
            title="Relação TRL vs Peso (Colorido por Prioridade)",
            color_continuous_scale=['#95a5a6', '#f1c40f', '#f39c12', '#e74c3c']
        )
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    def exportar_dados(self, df):
        """Funcionalidades de exportação"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Exportar CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Exportar CSV",
                data=csv,
                file_name="projetos_trl.csv",
                mime="text/csv"
            )
        
        with col2:
            # Exportar JSON
            json_data = df.to_json(orient='records', indent=2)
            st.download_button(
                label="📥 Exportar JSON",
                data=json_data,
                file_name="projetos_trl.json",
                mime="application/json"
            )
        
        with col3:
            # Salvar no session_state
            if st.button("💾 Salvar Alterações"):
                st.session_state.projetos = df.drop('prioridade', axis=1).to_dict('records')
                st.success("Dados salvos!")

def main():
    # Header
    st.title("🎯 Sistema de Priorização TRL")
    st.markdown("**Sistema estratégico para priorização de projetos de inovação considerando impacto potencial e dificuldade de transição TRL**")
    st.divider()
    
    # Inicializar sistema
    sistema = TRLMatrixSystem()
    
    # Sidebar - Filtros e Gestão
    with st.sidebar:
        st.header("🔧 Controles")
        
        # Filtros
        st.subheader("🔍 Filtros")
        filtro_trl = st.selectbox("TRL:", ['Todos'] + [str(i) for i in range(1, 10)])
        filtro_impacto = st.selectbox("Impacto:", ['Todos', 'Alto', 'Médio', 'Baixo'])
        filtro_dificuldade = st.selectbox("Dificuldade:", ['Todos', 'Fácil', 'Moderada', 'Difícil'])
        
        # Gestão de Projetos
        st.subheader("➕ Adicionar Projeto")
        with st.form("novo_projeto"):
            nome = st.text_input("Nome do Projeto:")
            col1, col2 = st.columns(2)
            with col1:
                trl = st.selectbox("TRL:", range(1, 10), key="new_trl")
                impacto = st.selectbox("Impacto:", ['Alto', 'Médio', 'Baixo'], key="new_impacto")
            with col2:
                dificuldade = st.selectbox("Dificuldade:", ['Fácil', 'Moderada', 'Difícil'], key="new_dificuldade")
                peso = st.slider("Peso:", 0, 10, 1, key="new_peso")
            
            if st.form_submit_button("➕ Adicionar"):
                if nome.strip():
                    novo_projeto = {
                        'nome': nome.strip(),
                        'trl': trl,
                        'impacto': impacto,
                        'dificuldade': dificuldade,
                        'peso': peso
                    }
                    st.session_state.projetos.append(novo_projeto)
                    st.success(f"Projeto '{nome}' adicionado!")
                else:
                    st.error("Nome do projeto é obrigatório!")
        
        # Upload de arquivos
        st.subheader("📥 Importar Projetos")
        uploaded_file = st.file_uploader("Carregar arquivo", type=['json', 'csv'])
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.json'):
                    dados_importados = json.load(uploaded_file)
                    # Validar estrutura dos dados
                    if isinstance(dados_importados, list) and all(
                        isinstance(item, dict) and 
                        all(key in item for key in ['nome', 'trl', 'impacto', 'dificuldade', 'peso'])
                        for item in dados_importados
                    ):
                        if st.button("✅ Confirmar Importação JSON"):
                            st.session_state.projetos = dados_importados
                            st.success(f"✅ {len(dados_importados)} projetos importados com sucesso!")
                    else:
                        st.error("❌ Formato JSON inválido. Verifique se possui os campos: nome, trl, impacto, dificuldade, peso")
                
                elif uploaded_file.name.endswith('.csv'):
                    df_importado = pd.read_csv(uploaded_file)
                    # Validar colunas necessárias
                    colunas_necessarias = ['nome', 'trl', 'impacto', 'dificuldade', 'peso']
                    if all(col in df_importado.columns for col in colunas_necessarias):
                        # Validar valores
                        if (df_importado['impacto'].isin(['Alto', 'Médio', 'Baixo']).all() and
                            df_importado['dificuldade'].isin(['Fácil', 'Moderada', 'Difícil']).all() and
                            df_importado['trl'].between(1, 9).all() and
                            df_importado['peso'].between(0, 10).all()):
                            
                            dados_importados = df_importado[colunas_necessarias].to_dict('records')
                            st.dataframe(df_importado.head(), use_container_width=True)
                            
                            if st.button("✅ Confirmar Importação CSV"):
                                st.session_state.projetos = dados_importados
                                st.success(f"✅ {len(dados_importados)} projetos importados com sucesso!")
                        else:
                            st.error("❌ Valores inválidos no CSV. Verifique: TRL (1-9), Peso (0-10), Impacto (Alto/Médio/Baixo), Dificuldade (Fácil/Moderada/Difícil)")
                    else:
                        st.error(f"❌ CSV deve conter as colunas: {', '.join(colunas_necessarias)}")
                        
            except Exception as e:
                st.error(f"❌ Erro ao processar arquivo: {str(e)}")
        
        # Download de arquivos
        st.subheader("📤 Exportar Projetos")
        df_export = sistema.criar_dataframe()
        
        col1, col2 = st.columns(2)
        with col1:
            # Download JSON
            json_data = json.dumps(st.session_state.projetos, indent=2, ensure_ascii=False)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name="projetos_trl.json",
                mime="application/json"
            )
        
        with col2:
            # Download CSV
            csv_data = df_export.drop('prioridade', axis=1).to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name="projetos_trl.csv",
                mime="text/csv"
            )
        
        # Reset dados
        st.subheader("🔄 Resetar Sistema")
        if st.button("🔄 Resetar para Dados Iniciais"):
            st.session_state.projetos = sistema.carregar_projetos_iniciais()
            st.success("Dados resetados!")
    
    # Aplicar filtros
    df = sistema.criar_dataframe()
    df_filtrado = df.copy()
    
    if filtro_trl != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['trl'] == int(filtro_trl)]
    if filtro_impacto != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['impacto'] == filtro_impacto]
    if filtro_dificuldade != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['dificuldade'] == filtro_dificuldade]
    
    # Layout principal
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🗂️ Lista de Projetos", "📈 Analytics", "⚙️ Gestão"])
    
    with tab1:
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Projetos", len(df_filtrado))
        with col2:
            prioridade_alta = len(df_filtrado[df_filtrado['prioridade'].isin([1, 2])])
            st.metric("Prioridade Alta (P1-P2)", prioridade_alta)
        with col3:
            trl_baixo = len(df_filtrado[df_filtrado['trl'] <= 3])
            st.metric("TRL Baixo (1-3)", trl_baixo)
        with col4:
            peso_medio = df_filtrado['peso'].mean() if not df_filtrado.empty else 0
            st.metric("Peso Médio", f"{peso_medio:.1f}")
        
        st.markdown("---")
        
        # Matriz de Priorização
        if not df_filtrado.empty:
            fig_matriz = sistema.criar_matriz_visual(df_filtrado)
            st.plotly_chart(fig_matriz, use_container_width=True)
            
            # Legenda
            st.markdown("""
            **🔴 P1-P2: Prioridade Máxima/Alta** - Projetos com maior potencial de retorno e menor risco técnico  
            **🟡 P3-P4: Prioridade Média-Alta** - Projetos promissores que requerem análise mais detalhada  
            **🟢 P5-P7: Prioridade Média** - Projetos para preenchimento de capacidade ociosa  
            **⚫ P6-P8-P9: Prioridade Baixa** - Candidatos para reavaliação ou descontinuação
            """)
        else:
            st.warning("Nenhum projeto encontrado com os filtros aplicados.")
    
    with tab2:
        # Lista de Projetos
        st.subheader("Lista de Projetos")
        
        if not df_filtrado.empty:
            # Opções de visualização
            col1, col2 = st.columns([1, 3])
            with col1:
                mostrar_apenas_alta_prioridade = st.checkbox("Apenas Alta Prioridade (P1-P3)")
            
            if mostrar_apenas_alta_prioridade:
                df_exibir = df_filtrado[df_filtrado['prioridade'] <= 3]
            else:
                df_exibir = df_filtrado
            
            # Exibir projetos em formato de tabela editável
            if len(df_exibir) > 0:
                st.dataframe(
                    df_exibir,
                    column_config={
                        "nome": st.column_config.TextColumn("Nome", width="large"),
                        "trl": st.column_config.NumberColumn("TRL", min_value=1, max_value=9),
                        "impacto": st.column_config.TextColumn("Impacto"),
                        "dificuldade": st.column_config.TextColumn("Dificuldade"),
                        "peso": st.column_config.NumberColumn("Peso", min_value=0, max_value=10),
                        "prioridade": st.column_config.NumberColumn("Prioridade")
                    },
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.info("Nenhum projeto encontrado com os critérios selecionados.")
        else:
            st.info("Nenhum projeto encontrado com os filtros aplicados.")
    
    with tab3:
        # Analytics
        st.subheader("Análises dos Projetos")
        if not df_filtrado.empty:
            sistema.criar_dashboard_analytics(df_filtrado)
            
            # Tabela de top projetos por prioridade
            st.subheader("🏆 Top 10 Projetos por Prioridade")
            top_projetos = df_filtrado.head(10)[['nome', 'prioridade', 'trl', 'impacto', 'dificuldade', 'peso']]
            st.dataframe(top_projetos, hide_index=True, use_container_width=True)
        else:
            st.info("Nenhum dado disponível para análise com os filtros aplicados.")
    
    with tab4:
        # Gestão
        st.subheader("Gestão de Projetos")
        
        # Visualizar dados atuais
        st.subheader("📊 Dados Atuais")
        total_projetos = len(st.session_state.projetos)
        st.info(f"📈 Total de projetos carregados: **{total_projetos}**")
        
        # Exportar dados (mantém funcionalidade da aba de gestão)
        st.subheader("📤 Exportar Dados Filtrados")
        sistema.exportar_dados(df_filtrado)
        
        st.markdown("---")
        
        # Editar projeto existente
        st.subheader("✏️ Editar Projeto")
        if not df_filtrado.empty:
            projeto_para_editar = st.selectbox(
                "Selecione um projeto para editar:",
                options=[''] + df_filtrado['nome'].tolist()
            )
            
            if projeto_para_editar:
                # Encontrar o projeto
                projeto_atual = next((p for p in st.session_state.projetos if p['nome'] == projeto_para_editar), None)
                
                if projeto_atual:
                    with st.form("editar_projeto"):
                        st.write(f"**Editando:** {projeto_para_editar}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            novo_trl = st.selectbox("TRL:", range(1, 10), index=projeto_atual['trl']-1, key="edit_trl")
                            novo_impacto = st.selectbox("Impacto:", ['Alto', 'Médio', 'Baixo'], 
                                                      index=['Alto', 'Médio', 'Baixo'].index(projeto_atual['impacto']), key="edit_impacto")
                        with col2:
                            nova_dificuldade = st.selectbox("Dificuldade:", ['Fácil', 'Moderada', 'Difícil'], 
                                                          index=['Fácil', 'Moderada', 'Difícil'].index(projeto_atual['dificuldade']), key="edit_dificuldade")
                            novo_peso = st.slider("Peso:", 0, 10, projeto_atual['peso'], key="edit_peso")
                        
                        if st.form_submit_button("💾 Salvar Alterações"):
                            # Atualizar o projeto
                            for i, p in enumerate(st.session_state.projetos):
                                if p['nome'] == projeto_para_editar:
                                    st.session_state.projetos[i].update({
                                        'trl': novo_trl,
                                        'impacto': novo_impacto,
                                        'dificuldade': nova_dificuldade,
                                        'peso': novo_peso
                                    })
                                    break
                            st.success(f"✅ Projeto '{projeto_para_editar}' atualizado!")
        else:
            st.info("Nenhum projeto disponível para edição.")
        
        st.markdown("---")
        
        # Excluir projetos
        st.subheader("🗑️ Excluir Projetos")
        if df_filtrado.empty:
            st.info("Nenhum projeto disponível para exclusão.")
        else:
            projeto_para_excluir = st.selectbox(
                "Selecione um projeto para excluir:",
                options=[''] + df_filtrado['nome'].tolist()
            )
            
            if projeto_para_excluir:
                if st.button(f"🗑️ Excluir '{projeto_para_excluir}'", type="secondary"):
                    st.session_state.projetos = [p for p in st.session_state.projetos if p['nome'] != projeto_para_excluir]
                    st.success(f"✅ Projeto '{projeto_para_excluir}' excluído!")

if __name__ == "__main__":
    main()