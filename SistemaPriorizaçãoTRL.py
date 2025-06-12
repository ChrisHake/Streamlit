import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from typing import Dict, List, Tuple

class TRLMatrixSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Priorização TRL - Gestão de Projetos")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Dados dos projetos
        self.projetos = self.carregar_projetos_iniciais()
        self.projetos_filtrados = self.projetos.copy()
        
        # Configurar interface
        self.criar_interface()
        self.atualizar_lista_projetos()
        
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
    
    def criar_interface(self):
        """Cria a interface principal do sistema"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid do root
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="Sistema de Priorização TRL - Gestão de Projetos", 
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame esquerdo - Lista de projetos
        frame_esquerdo = ttk.LabelFrame(main_frame, text="Projetos", padding="10")
        frame_esquerdo.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        frame_esquerdo.columnconfigure(0, weight=1)
        frame_esquerdo.rowconfigure(1, weight=1)
        
        # Botões de ação
        frame_botoes = ttk.Frame(frame_esquerdo)
        frame_botoes.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(frame_botoes, text="Adicionar Projeto", command=self.adicionar_projeto).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(frame_botoes, text="Editar Projeto", command=self.editar_projeto).grid(row=0, column=1, padx=5)
        ttk.Button(frame_botoes, text="Excluir Projeto", command=self.excluir_projeto).grid(row=0, column=2, padx=5)
        ttk.Button(frame_botoes, text="Salvar Dados", command=self.salvar_dados).grid(row=0, column=3, padx=5)
        ttk.Button(frame_botoes, text="Carregar Dados", command=self.carregar_dados).grid(row=0, column=4, padx=(5, 0))
        
        # Lista de projetos (Treeview)
        self.tree = ttk.Treeview(frame_esquerdo, columns=('TRL', 'Impacto', 'Dificuldade', 'Peso', 'Prioridade'), show='tree headings')
        self.tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar colunas
        self.tree.heading('#0', text='Projeto')
        self.tree.heading('TRL', text='TRL')
        self.tree.heading('Impacto', text='Impacto')
        self.tree.heading('Dificuldade', text='Dificuldade')
        self.tree.heading('Peso', text='Peso')
        self.tree.heading('Prioridade', text='Prioridade')
        
        self.tree.column('#0', width=300)
        self.tree.column('TRL', width=50)
        self.tree.column('Impacto', width=80)
        self.tree.column('Dificuldade', width=90)
        self.tree.column('Peso', width=60)
        self.tree.column('Prioridade', width=80)
        
        # Scrollbar para a lista
        scrollbar = ttk.Scrollbar(frame_esquerdo, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Frame direito - Matriz e filtros
        frame_direito = ttk.LabelFrame(main_frame, text="Matriz de Priorização", padding="10")
        frame_direito.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame_direito.columnconfigure(0, weight=1)
        frame_direito.rowconfigure(2, weight=1)
        
        # Filtros
        frame_filtros = ttk.LabelFrame(frame_direito, text="Filtros", padding="5")
        frame_filtros.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(frame_filtros, text="TRL:").grid(row=0, column=0, padx=(0, 5))
        self.filtro_trl = ttk.Combobox(frame_filtros, values=['Todos'] + [str(i) for i in range(1, 10)], width=8)
        self.filtro_trl.set('Todos')
        self.filtro_trl.grid(row=0, column=1, padx=(0, 10))
        self.filtro_trl.bind('<<ComboboxSelected>>', self.aplicar_filtros)
        
        ttk.Label(frame_filtros, text="Impacto:").grid(row=0, column=2, padx=(0, 5))
        self.filtro_impacto = ttk.Combobox(frame_filtros, values=['Todos', 'Alto', 'Médio', 'Baixo'], width=10)
        self.filtro_impacto.set('Todos')
        self.filtro_impacto.grid(row=0, column=3, padx=(0, 10))
        self.filtro_impacto.bind('<<ComboboxSelected>>', self.aplicar_filtros)
        
        ttk.Button(frame_filtros, text="Limpar Filtros", command=self.limpar_filtros).grid(row=0, column=4)
        
        # Matriz visual
        self.criar_matriz_visual(frame_direito)
        
        # Estatísticas
        self.frame_stats = ttk.LabelFrame(frame_direito, text="Estatísticas", padding="5")
        self.frame_stats.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        self.atualizar_estatisticas()
    
    def criar_matriz_visual(self, parent):
        """Cria a representação visual da matriz de priorização"""
        frame_matriz = ttk.Frame(parent)
        frame_matriz.grid(row=2, column=0, pady=10)
        
        # Título da matriz
        ttk.Label(frame_matriz, text="Matriz de Priorização TRL", 
                 font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=4, pady=(0, 10))
        
        # Headers
        ttk.Label(frame_matriz, text="DIFICULDADE →").grid(row=1, column=0, columnspan=4)
        ttk.Label(frame_matriz, text="IMPACTO ↓", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W)
        
        # Cabeçalhos das colunas
        cols = ["", "FÁCIL", "MODERADA", "DIFÍCIL"]
        for i, col in enumerate(cols):
            label = ttk.Label(frame_matriz, text=col, font=('Arial', 9, 'bold'))
            label.grid(row=3, column=i, padx=5, pady=2)
        
        # Linhas da matriz
        rows = ["ALTO", "MÉDIO", "BAIXO"]
        priorities = [
            [1, 2, 3],  # Alto impacto
            [4, 5, 6],  # Médio impacto
            [7, 8, 9]   # Baixo impacto
        ]
        
        colors = {
            1: '#e74c3c', 2: '#e74c3c', 3: '#f39c12',  # Vermelho, Vermelho, Laranja
            4: '#f39c12', 5: '#f1c40f', 6: '#95a5a6',  # Laranja, Amarelo, Cinza
            7: '#f1c40f', 8: '#95a5a6', 9: '#95a5a6'   # Amarelo, Cinza, Cinza
        }
        
        self.matriz_labels = {}
        for i, row in enumerate(rows):
            # Label da linha
            ttk.Label(frame_matriz, text=row, font=('Arial', 9, 'bold')).grid(row=4+i, column=0, padx=5, pady=2, sticky=tk.W)
            
            # Células da matriz
            for j in range(3):
                priority = priorities[i][j]
                frame_cell = tk.Frame(frame_matriz, bg=colors[priority], width=80, height=50)
                frame_cell.grid(row=4+i, column=j+1, padx=2, pady=2)
                frame_cell.grid_propagate(False)
                
                label = tk.Label(frame_cell, text=f"P{priority}", bg=colors[priority], 
                               fg='white', font=('Arial', 10, 'bold'))
                label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
                
                count_label = tk.Label(frame_cell, text="0", bg=colors[priority], 
                                     fg='white', font=('Arial', 8))
                count_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
                
                self.matriz_labels[(row, j)] = count_label
        
        # Legenda
        frame_legenda = ttk.Frame(frame_matriz)
        frame_legenda.grid(row=7, column=0, columnspan=4, pady=(10, 0))
        
        legenda_items = [
            ("P1-P2: Prioridade Máxima/Alta", '#e74c3c'),
            ("P3-P4: Prioridade Média-Alta", '#f39c12'),
            ("P5-P7: Prioridade Média", '#f1c40f'),
            ("P6-P8-P9: Prioridade Baixa", '#95a5a6')
        ]
        
        for i, (text, color) in enumerate(legenda_items):
            frame_item = tk.Frame(frame_legenda, bg=color, width=15, height=15)
            frame_item.grid(row=i//2, column=(i%2)*2, padx=5, pady=2, sticky=tk.W)
            frame_item.grid_propagate(False)
            
            ttk.Label(frame_legenda, text=text, font=('Arial', 8)).grid(row=i//2, column=(i%2)*2+1, padx=(5, 20), pady=2, sticky=tk.W)
    
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
    
    def atualizar_lista_projetos(self):
        """Atualiza a lista de projetos na interface"""
        # Limpar tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Adicionar projetos filtrados
        projetos_ordenados = sorted(self.projetos_filtrados, 
                                  key=lambda x: (self.calcular_prioridade(x['impacto'], x['dificuldade']), -x['peso']))
        
        for projeto in projetos_ordenados:
            prioridade = self.calcular_prioridade(projeto['impacto'], projeto['dificuldade'])
            self.tree.insert('', 'end', text=projeto['nome'], 
                           values=(projeto['trl'], projeto['impacto'], projeto['dificuldade'], 
                                 projeto['peso'], f"P{prioridade}"))
        
        self.atualizar_matriz_contadores()
        self.atualizar_estatisticas()
    
    def atualizar_matriz_contadores(self):
        """Atualiza os contadores na matriz visual"""
        # Resetar contadores
        contadores = {('ALTO', 0): 0, ('ALTO', 1): 0, ('ALTO', 2): 0,
                     ('MÉDIO', 0): 0, ('MÉDIO', 1): 0, ('MÉDIO', 2): 0,
                     ('BAIXO', 0): 0, ('BAIXO', 1): 0, ('BAIXO', 2): 0}
        
        # Contar projetos por categoria
        for projeto in self.projetos_filtrados:
            impacto = projeto['impacto'].upper()
            dificuldade_map = {'Fácil': 0, 'Moderada': 1, 'Difícil': 2}
            dificuldade_idx = dificuldade_map.get(projeto['dificuldade'], 2)
            
            key = (impacto, dificuldade_idx)
            if key in contadores:
                contadores[key] += 1
        
        # Atualizar labels
        for key, count in contadores.items():
            if key in self.matriz_labels:
                self.matriz_labels[key].config(text=str(count))
    
    def atualizar_estatisticas(self):
        """Atualiza as estatísticas dos projetos"""
        # Limpar frame de estatísticas
        for widget in self.frame_stats.winfo_children():
            widget.destroy()
        
        total_projetos = len(self.projetos_filtrados)
        if total_projetos == 0:
            ttk.Label(self.frame_stats, text="Nenhum projeto encontrado").grid(row=0, column=0)
            return
        
        # Contar por prioridade
        prioridades = {}
        for projeto in self.projetos_filtrados:
            prioridade = self.calcular_prioridade(projeto['impacto'], projeto['dificuldade'])
            prioridades[prioridade] = prioridades.get(prioridade, 0) + 1
        
        # Contar por TRL
        trls = {}
        for projeto in self.projetos_filtrados:
            trl = projeto['trl']
            trls[trl] = trls.get(trl, 0) + 1
        
        # Exibir estatísticas
        ttk.Label(self.frame_stats, text=f"Total de Projetos: {total_projetos}", 
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, sticky=tk.W)
        
        # Prioridades
        ttk.Label(self.frame_stats, text="Por Prioridade:", font=('Arial', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        for i, (prioridade, count) in enumerate(sorted(prioridades.items())):
            ttk.Label(self.frame_stats, text=f"P{prioridade}: {count}").grid(row=2+i//3, column=i%3, sticky=tk.W, padx=(0, 10))
        
        # TRLs mais comuns
        ttk.Label(self.frame_stats, text="TRLs mais comuns:", font=('Arial', 9, 'bold')).grid(row=5, column=0, sticky=tk.W, pady=(10, 0))
        trls_ordenados = sorted(trls.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (trl, count) in enumerate(trls_ordenados):
            ttk.Label(self.frame_stats, text=f"TRL {trl}: {count}").grid(row=6+i//3, column=i%3, sticky=tk.W, padx=(0, 10))
    
    def adicionar_projeto(self):
        """Adiciona um novo projeto"""
        dialog = ProjetoDialog(self.root, "Adicionar Projeto")
        self.root.wait_window(dialog.dialog)
        
        if dialog.resultado:
            self.projetos.append(dialog.resultado)
            self.aplicar_filtros()
    
    def editar_projeto(self):
        """Edita o projeto selecionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um projeto para editar.")
            return
        
        # Encontrar projeto pelo nome
        nome_projeto = self.tree.item(selection[0])['text']
        projeto = next((p for p in self.projetos if p['nome'] == nome_projeto), None)
        
        if projeto:
            dialog = ProjetoDialog(self.root, "Editar Projeto", projeto)
            self.root.wait_window(dialog.dialog)
            
            if dialog.resultado:
                # Atualizar projeto
                projeto.update(dialog.resultado)
                self.aplicar_filtros()
    
    def excluir_projeto(self):
        """Exclui o projeto selecionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um projeto para excluir.")
            return
        
        nome_projeto = self.tree.item(selection[0])['text']
        
        if messagebox.askyesno("Confirmar", f"Deseja realmente excluir o projeto '{nome_projeto}'?"):
            self.projetos = [p for p in self.projetos if p['nome'] != nome_projeto]
            self.aplicar_filtros()
    
    def aplicar_filtros(self, event=None):
        """Aplica os filtros selecionados"""
        filtro_trl = self.filtro_trl.get()
        filtro_impacto = self.filtro_impacto.get()
        
        self.projetos_filtrados = []
        for projeto in self.projetos:
            # Filtro TRL
            if filtro_trl != 'Todos' and str(projeto['trl']) != filtro_trl:
                continue
            
            # Filtro Impacto
            if filtro_impacto != 'Todos' and projeto['impacto'] != filtro_impacto:
                continue
            
            self.projetos_filtrados.append(projeto)
        
        self.atualizar_lista_projetos()
    
    def limpar_filtros(self):
        """Remove todos os filtros"""
        self.filtro_trl.set('Todos')
        self.filtro_impacto.set('Todos')
        self.projetos_filtrados = self.projetos.copy()
        self.atualizar_lista_projetos()
    
    def salvar_dados(self):
        """Salva os dados em arquivo JSON"""
        try:
            with open('projetos_trl.json', 'w', encoding='utf-8') as f:
                json.dump(self.projetos, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados: {str(e)}")
    
    def carregar_dados(self):
        """Carrega os dados de arquivo JSON"""
        try:
            if os.path.exists('projetos_trl.json'):
                with open('projetos_trl.json', 'r', encoding='utf-8') as f:
                    self.projetos = json.load(f)
                self.aplicar_filtros()
                messagebox.showinfo("Sucesso", "Dados carregados com sucesso!")
            else:
                messagebox.showwarning("Aviso", "Arquivo de dados não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {str(e)}")

class ProjetoDialog:
    def __init__(self, parent, titulo, projeto=None):
        self.resultado = None
        
        # Criar dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(titulo)
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centralizar dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Campos
        ttk.Label(main_frame, text="Nome do Projeto:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.entry_nome = ttk.Entry(main_frame, width=40)
        self.entry_nome.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(main_frame, text="TRL (1-9):").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.combo_trl = ttk.Combobox(main_frame, values=[str(i) for i in range(1, 10)], width=10)
        self.combo_trl.grid(row=3, column=0, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(main_frame, text="Impacto:").grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.combo_impacto = ttk.Combobox(main_frame, values=['Alto', 'Médio', 'Baixo'], width=15)
        self.combo_impacto.grid(row=5, column=0, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(main_frame, text="Dificuldade:").grid(row=6, column=0, sticky=tk.W, pady=(0, 5))
        self.combo_dificuldade = ttk.Combobox(main_frame, values=['Fácil', 'Moderada', 'Difícil'], width=15)
        self.combo_dificuldade.grid(row=7, column=0, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(main_frame, text="Peso (0-10):").grid(row=8, column=0, sticky=tk.W, pady=(0, 5))
        self.entry_peso = ttk.Entry(main_frame, width=10)
        self.entry_peso.grid(row=9, column=0, sticky=tk.W, pady=(0, 20))
        
        # Botões
        frame_botoes = ttk.Frame(main_frame)
        frame_botoes.grid(row=10, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(frame_botoes, text="Salvar", command=self.salvar).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(frame_botoes, text="Cancelar", command=self.cancelar).grid(row=0, column=1)
        
        # Preencher campos se for edição
        if projeto:
            self.entry_nome.insert(0, projeto['nome'])
            self.combo_trl.set(str(projeto['trl']))
            self.combo_impacto.set(projeto['impacto'])
            self.combo_dificuldade.set(projeto['dificuldade'])
            self.entry_peso.insert(0, str(projeto['peso']))
        else:
            # Valores padrão
            self.combo_trl.set('1')
            self.combo_impacto.set('Médio')
            self.combo_dificuldade.set('Moderada')
            self.entry_peso.insert(0, '1')
        
        # Focar no campo nome
        self.entry_nome.focus()
        
        # Configurar grid
        main_frame.columnconfigure(0, weight=1)
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
    
    def salvar(self):
        """Salva os dados do projeto"""
        try:
            nome = self.entry_nome.get().strip()
            if not nome:
                messagebox.showerror("Erro", "Nome do projeto é obrigatório!")
                return
            
            trl = int(self.combo_trl.get())
            if not (1 <= trl <= 9):
                messagebox.showerror("Erro", "TRL deve estar entre 1 e 9!")
                return
            
            impacto = self.combo_impacto.get()
            if impacto not in ['Alto', 'Médio', 'Baixo']:
                messagebox.showerror("Erro", "Selecione um impacto válido!")
                return
            
            dificuldade = self.combo_dificuldade.get()
            if dificuldade not in ['Fácil', 'Moderada', 'Difícil']:
                messagebox.showerror("Erro", "Selecione uma dificuldade válida!")
                return
            
            peso = int(self.entry_peso.get())
            if not (0 <= peso <= 10):
                messagebox.showerror("Erro", "Peso deve estar entre 0 e 10!")
                return
            
            self.resultado = {
                'nome': nome,
                'trl': trl,
                'impacto': impacto,
                'dificuldade': dificuldade,
                'peso': peso
            }
            
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Erro", "Valores numéricos inválidos!")
    
    def cancelar(self):
        """Cancela a operação"""
        self.dialog.destroy()

def main():
    """Função principal para executar o sistema"""
    root = tk.Tk()
    app = TRLMatrixSystem(root)
    
    # Configurar comportamento de fechamento
    def on_closing():
        if messagebox.askokcancel("Sair", "Deseja salvar os dados antes de sair?"):
            app.salvar_dados()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Executar aplicação
    root.mainloop()

if __name__ == "__main__":
    main()