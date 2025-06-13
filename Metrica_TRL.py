<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Métricas de Progressão TRL</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --trl-1-3: #e74c3c;
            --trl-4-6: #f39c12;
            --trl-7-9: #2ecc71;
            --primary: #3498db;
            --light-bg: #f8f9fa;
            --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f7fa;
            color: #333;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50, #3498db);
            color: white;
            padding: 20px 0;
            margin-bottom: 30px;
        }
        
        .trl-card {
            background: white;
            border-radius: 10px;
            box-shadow: var(--card-shadow);
            transition: transform 0.3s ease;
            height: 100%;
        }
        
        .trl-card:hover {
            transform: translateY(-5px);
        }
        
        .trl-1-3 {
            border-top: 4px solid var(--trl-1-3);
        }
        
        .trl-4-6 {
            border-top: 4px solid var(--trl-4-6);
        }
        
        .trl-7-9 {
            border-top: 4px solid var(--trl-7-9);
        }
        
        .progress-container {
            background-color: #e9ecef;
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
        }
        
        .progress-bar {
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 12px;
        }
        
        .progress-1-3 {
            background-color: var(--trl-1-3);
        }
        
        .progress-4-6 {
            background-color: var(--trl-4-6);
        }
        
        .progress-7-9 {
            background-color: var(--trl-7-9);
        }
        
        .project-table th {
            background-color: #2c3e50;
            color: white;
        }
        
        .project-table tbody tr:hover {
            background-color: rgba(52, 152, 219, 0.1);
        }
        
        .dashboard-card {
            background: white;
            border-radius: 10px;
            box-shadow: var(--card-shadow);
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .checklist-item {
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
        
        .checklist-item:last-child {
            border-bottom: none;
        }
        
        .sync-point {
            background: #e3f2fd;
            border-left: 4px solid var(--primary);
            padding: 15px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 15px;
        }
        
        .trl-badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            color: white;
        }
        
        .badge-1 { background-color: #e74c3c; }
        .badge-2 { background-color: #e67e22; }
        .badge-3 { background-color: #f39c12; }
        .badge-4 { background-color: #f1c40f; }
        .badge-5 { background-color: #2ecc71; }
        .badge-6 { background-color: #27ae60; }
        .badge-7 { background-color: #16a085; }
        .badge-8 { background-color: #2980b9; }
        .badge-9 { background-color: #2c3e50; }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 5px;
        }
        
        .status-pending { background-color: #e74c3c; }
        .status-progress { background-color: #f39c12; }
        .status-completed { background-color: #2ecc71; }
        
        .priority-high { background-color: rgba(231, 76, 60, 0.2); }
        .priority-medium { background-color: rgba(243, 156, 18, 0.2); }
        .priority-low { background-color: rgba(46, 204, 113, 0.2); }
        
        .nav-tabs .nav-link.active {
            font-weight: bold;
            border-bottom: 3px solid var(--primary);
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-md-8">
                    <h1><i class="fas fa-chart-line me-2"></i>Métricas de Progressão TRL</h1>
                    <p class="lead">Sistema de acompanhamento e gestão de maturidade tecnológica</p>
                </div>
                <div class="col-md-4 text-end">
                    <div class="d-inline-block bg-white text-dark p-2 rounded">
                        <i class="fas fa-calendar me-1 text-primary"></i> 
                        <span id="current-date"></span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="container mb-5">
        <!-- Dashboard Resumo -->
        <div class="row mb-4">
            <div class="col-md-4">
                <div class="trl-card trl-1-3 p-3">
                    <h5 class="d-flex justify-content-between">
                        <span><i class="fas fa-flask me-2"></i>Zona de Descoberta</span>
                        <span class="badge bg-danger">TRL 1-3</span>
                    </h5>
                    <p class="mb-1">Exploração de possibilidades e fundamentos científicos</p>
                    <div class="d-flex justify-content-between mt-3">
                        <span>Projetos: <strong>16</strong></span>
                        <span>Alocação: <strong>40%</strong></span>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="trl-card trl-4-6 p-3">
                    <h5 class="d-flex justify-content-between">
                        <span><i class="fas fa-cogs me-2"></i>Zona de Desenvolvimento</span>
                        <span class="badge bg-warning">TRL 4-6</span>
                    </h5>
                    <p class="mb-1">Validação e integração de componentes tecnológicos</p>
                    <div class="d-flex justify-content-between mt-3">
                        <span>Projetos: <strong>8</strong></span>
                        <span>Alocação: <strong>35%</strong></span>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="trl-card trl-7-9 p-3">
                    <h5 class="d-flex justify-content-between">
                        <span><i class="fas fa-rocket me-2"></i>Zona de Transferência</span>
                        <span class="badge bg-success">TRL 7-9</span>
                    </h5>
                    <p class="mb-1">Preparação para implementação comercial</p>
                    <div class="d-flex justify-content-between mt-3">
                        <span>Projetos: <strong>0</strong></span>
                        <span>Alocação: <strong>25%</strong></span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Barra de Progresso das Transições -->
        <div class="dashboard-card mb-4">
            <h3 class="mb-4"><i class="fas fa-tasks me-2"></i>Progresso das Transições TRL</h3>
            <div class="row">
                <!-- Transições TRL 1-4 -->
                <div class="col-md-3 mb-3">
                    <h6>TRL 1 → 2</h6>
                    <div class="progress-container mb-2">
                        <div class="progress-bar progress-1-3" style="width: 15%;">15%</div>
                    </div>
                    <div class="d-flex justify-content-between small">
                        <span><i class="fas fa-project-diagram me-1"></i> Projetos: 10</span>
                        <span class="text-danger"><i class="fas fa-exclamation-circle me-1"></i> Pendente</span>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <h6>TRL 2 → 3</h6>
                    <div class="progress-container mb-2">
                        <div class="progress-bar progress-1-3" style="width: 25%;">25%</div>
                    </div>
                    <div class="d-flex justify-content-between small">
                        <span><i class="fas fa-project-diagram me-1"></i> Projetos: 12</span>
                        <span class="text-danger"><i class="fas fa-exclamation-circle me-1"></i> Pendente</span>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <h6>TRL 3 → 4</h6>
                    <div class="progress-container mb-2">
                        <div class="progress-bar progress-1-3" style="width: 40%;">40%</div>
                    </div>
                    <div class="d-flex justify-content-between small">
                        <span><i class="fas fa-project-diagram me-1"></i> Projetos: 6</span>
                        <span class="text-warning"><i class="fas fa-sync-alt me-1"></i> Em Progresso</span>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <h6>TRL 4 → 5</h6>
                    <div class="progress-container mb-2">
                        <div class="progress-bar progress-4-6" style="width: 30%;">30%</div>
                    </div>
                    <div class="d-flex justify-content-between small">
                        <span><i class="fas fa-project-diagram me-1"></i> Projetos: 1</span>
                        <span class="text-warning"><i class="fas fa-sync-alt me-1"></i> Em Progresso</span>
                    </div>
                </div>
                
                <!-- Transições TRL 5-9 -->
                <div class="col-md-3 mb-3">
                    <h6>TRL 5 → 6</h6>
                    <div class="progress-container mb-2">
                        <div class="progress-bar progress-4-6" style="width: 20%;">20%</div>
                    </div>
                    <div class="d-flex justify-content-between small">
                        <span><i class="fas fa-project-diagram me-1"></i> Projetos: 5</span>
                        <span class="text-danger"><i class="fas fa-exclamation-circle me-1"></i> Pendente</span>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <h6>TRL 6 → 7</h6>
                    <div class="progress-container mb-2">
                        <div class="progress-bar progress-7-9" style="width: 0%;">0%</div>
                    </div>
                    <div class="d-flex justify-content-between small">
                        <span><i class="fas fa-project-diagram me-1"></i> Projetos: 0</span>
                        <span class="text-danger"><i class="fas fa-exclamation-circle me-1"></i> Pendente</span>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <h6>TRL 7 → 8</h6>
                    <div class="progress-container mb-2">
                        <div class="progress-bar progress-7-9" style="width: 0%;">0%</div>
                    </div>
                    <div class="d-flex justify-content-between small">
                        <span><i class="fas fa-project-diagram me-1"></i> Projetos: 0</span>
                        <span class="text-danger"><i class="fas fa-exclamation-circle me-1"></i> Pendente</span>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <h6>TRL 8 → 9</h6>
                    <div class="progress-container mb-2">
                        <div class="progress-bar progress-7-9" style="width: 0%;">0%</div>
                    </div>
                    <div class="d-flex justify-content-between small">
                        <span><i class="fas fa-project-diagram me-1"></i> Projetos: 0</span>
                        <span class="text-danger"><i class="fas fa-exclamation-circle me-1"></i> Pendente</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Portões de Qualidade e Lista de Projetos -->
        <div class="row">
            <div class="col-lg-4">
                <div class="dashboard-card">
                    <h4><i class="fas fa-door-open me-2"></i>Portões de Qualidade</h4>
                    
                    <div class="sync-point">
                        <h5>Ponto de Sincronização</h5>
                        <p class="mb-1"><strong>Equipe Responsável:</strong> Equipe de Pesquisa Básica</p>
                        <p class="mb-1"><strong>Entregável Principal:</strong> Relatório de Conceito Científico</p>
                        <p class="mb-2"><strong>Timeline Estimado:</strong> 2-4 semanas</p>
                        <div class="d-flex align-items-center">
                            <span class="status-indicator status-pending"></span>
                            <strong class="text-danger">Aguardando aprovação das métricas</strong>
                        </div>
                    </div>
                    
                    <h6>TRL 1 → 2: Conceito para Formulação</h6>
                    <div class="mb-3">
                        <div class="checklist-item">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="check1">
                                <label class="form-check-label" for="check1">Revisão bibliográfica completa documentada</label>
                            </div>
                        </div>
                        <div class="checklist-item">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="check2">
                                <label class="form-check-label" for="check2">Princípios científicos fundamentais identificados</label>
                            </div>
                        </div>
                        <div class="checklist-item">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="check3">
                                <label class="form-check-label" for="check3">Relatório de viabilidade teórica aprovado</label>
                            </div>
                        </div>
                        <div class="checklist-item">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="check4">
                                <label class="form-check-label" for="check4">Definição clara do problema tecnológico</label>
                            </div>
                        </div>
                    </div>
                    
                    <h6>TRL 3 → 4: Validação Laboratorial</h6>
                    <div>
                        <div class="checklist-item">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="check5">
                                <label class="form-check-label" for="check5">Demonstração de funcionalidade básica em testes independentes</label>
                            </div>
                        </div>
                        <div class="checklist-item">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="check6">
                                <label class="form-check-label" for="check6">Documentação completa dos princípios de funcionamento</label>
                            </div>
                        </div>
                        <div class="checklist-item">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="check7">
                                <label class="form-check-label" for="check7">Identificação clara dos próximos desafios técnicos</label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-lg-8">
                <div class="dashboard-card">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h4><i class="fas fa-list-ul me-2"></i>Lista de Projetos</h4>
                        <div>
                            <button class="btn btn-sm btn-outline-primary me-2"><i class="fas fa-filter"></i> Filtros</button>
                            <button class="btn btn-sm btn-primary"><i class="fas fa-plus"></i> Novo Projeto</button>
                        </div>
                    </div>
                    
                    <div class="table-responsive">
                        <table class="table table-hover project-table">
                            <thead>
                                <tr>
                                    <th>Projeto</th>
                                    <th>TRL</th>
                                    <th>Peso Total</th>
                                    <th>Impacto Ponderado</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="priority-high">
                                    <td>Pesquisa Materiais - LabMat UFSC</td>
                                    <td><span class="trl-badge badge-1">1</span></td>
                                    <td>9</td>
                                    <td>0.9</td>
                                    <td><span class="status-indicator status-pending"></span> Pendente</td>
                                </tr>
                                <tr class="priority-high">
                                    <td>Microbolhas Banheira</td>
                                    <td><span class="trl-badge badge-4">4</span></td>
                                    <td>8</td>
                                    <td>3.2</td>
                                    <td><span class="status-indicator status-progress"></span> Em Progresso</td>
                                </tr>
                                <tr class="priority-high">
                                    <td>Microbolhas no Arejador</td>
                                    <td><span class="trl-badge badge-5">5</span></td>
                                    <td>8</td>
                                    <td>4.0</td>
                                    <td><span class="status-indicator status-progress"></span> Em Progresso</td>
                                </tr>
                                <tr class="priority-high">
                                    <td>Gerador de Ozônio - OEM</td>
                                    <td><span class="trl-badge badge-5">5</span></td>
                                    <td>8</td>
                                    <td>4.0</td>
                                    <td><span class="status-indicator status-progress"></span> Em Progresso</td>
                                </tr>
                                <tr class="priority-medium">
                                    <td>BacteriaFree para esmalte cerâmico</td>
                                    <td><span class="trl-badge badge-5">5</span></td>
                                    <td>7</td>
                                    <td>3.5</td>
                                    <td><span class="status-indicator status-progress"></span> Em Progresso</td>
                                </tr>
                                <tr class="priority-medium">
                                    <td>Super Filtro (Água alcalina e antioxidante)</td>
                                    <td><span class="trl-badge badge-3">3</span></td>
                                    <td>7</td>
                                    <td>2.1</td>
                                    <td><span class="status-indicator status-progress"></span> Em Progresso</td>
                                </tr>
                                <tr class="priority-medium">
                                    <td>WaterTrain (Neoperl)</td>
                                    <td><span class="trl-badge badge-3">3</span></td>
                                    <td>7</td>
                                    <td>2.1</td>
                                    <td><span class="status-indicator status-progress"></span> Em Progresso</td>
                                </tr>
                                <tr class="priority-low">
                                    <td>Inteligência Artificial</td>
                                    <td><span class="trl-badge badge-1">1</span></td>
                                    <td>3</td>
                                    <td>0.3</td>
                                    <td><span class="status-indicator status-pending"></span> Pendente</td>
                                </tr>
                                <tr class="priority-low">
                                    <td>Banheiro WellNess (Feira ExpoRvestir 2025)</td>
                                    <td><span class="trl-badge badge-5">5</span></td>
                                    <td>3</td>
                                    <td>1.5</td>
                                    <td><span class="status-indicator status-progress"></span> Em Progresso</td>
                                </tr>
                                <tr class="priority-low">
                                    <td>Óxido de Nióbio</td>
                                    <td><span class="trl-badge badge-1">1</span></td>
                                    <td>2</td>
                                    <td>0.2</td>
                                    <td><span class="status-indicator status-pending"></span> Pendente</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    
                    <div class="d-flex justify-content-between align-items-center mt-3">
                        <div>Mostrando 10 de 29 projetos</div>
                        <ul class="pagination pagination-sm">
                            <li class="page-item disabled"><a class="page-link" href="#"><i class="fas fa-chevron-left"></i></a></li>
                            <li class="page-item active"><a class="page-link" href="#">1</a></li>
                            <li class="page-item"><a class="page-link" href="#">2</a></li>
                            <li class="page-item"><a class="page-link" href="#">3</a></li>
                            <li class="page-item"><a class="page-link" href="#"><i class="fas fa-chevron-right"></i></a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Sincronização com Desenvolvimento -->
        <div class="dashboard-card mt-4">
            <h4><i class="fas fa-sync-alt me-2"></i>Pontos de Sincronização com Desenvolvimento</h4>
            <div class="row mt-4">
                <div class="col-md-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title"><span class="trl-badge badge-6">TRL 6</span> Briefings Técnicos</h5>
                            <p class="card-text">Tecnologias que atingem TRL 6 estão prontas para briefings técnicos detalhados com a equipe de desenvolvimento.</p>
                            <div class="d-flex align-items-center">
                                <span class="status-indicator status-pending"></span>
                                <strong class="text-danger ms-2">0 projetos prontos</strong>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title"><span class="trl-badge badge-7">TRL 7</span> Componentes Experimentais</h5>
                            <p class="card-text">Tecnologias no TRL 7 podem começar a ser incorporadas em projetos de desenvolvimento como componentes experimentais.</p>
                            <div class="d-flex align-items-center">
                                <span class="status-indicator status-pending"></span>
                                <strong class="text-danger ms-2">0 projetos prontos</strong>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title"><span class="trl-badge badge-8">TRL 8</span> Produtos Críticos</h5>
                            <p class="card-text">Apenas tecnologias no TRL 8 ou 9 devem ser consideradas para incorporação em produtos de cronograma crítico.</p>
                            <div class="d-flex align-items-center">
                                <span class="status-indicator status-pending"></span>
                                <strong class="text-danger ms-2">0 projetos prontos</strong>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="bg-dark text-white py-4">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5>Sistema de Métricas TRL</h5>
                    <p class="mb-0">Transformando a gestão de inovação de uma arte intuitiva em uma disciplina científica.</p>
                </div>
                <div class="col-md-6 text-end">
                    <p class="mb-0">Desenvolvido com base na Metodologia TRL para Inovação<br>Atualizado em: <span id="update-date"></span></p>
                </div>
            </div>
        </div>
    </footer>

    <script>
        // Atualizar datas
        const now = new Date();
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        document.getElementById('current-date').textContent = now.toLocaleDateString('pt-BR', options);
        document.getElementById('update-date').textContent = now.toLocaleDateString('pt-BR', options);
        
        // Simular cálculos de impacto ponderado
        document.querySelectorAll('.priority-high').forEach(row => {
            row.addEventListener('click', function() {
                this.classList.toggle('table-active');
            });
        });
        
        // Simulação de progresso
        const progressBars = document.querySelectorAll('.progress-bar');
        progressBars.forEach(bar => {
            const width = bar.style.width;
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.width = width;
            }, 300);
        });
    </script>
</body>
</html>