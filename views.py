import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QGridLayout, QPushButton, QLabel, QStackedWidget,
                             QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView,
                             QLineEdit, QMessageBox, QSpinBox, QFormLayout)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

class MapaEstoque(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle('Mapa Do Estoque')
        self.resize(900, 700)

        self.tela = QStackedWidget()
        self.setCentralWidget(self.tela)

        self.tela_ruas = QWidget()
        self.tela_prateleiras = QWidget()
        self.tela_niveis = QWidget()
        self.tela_blocos = QWidget()
        self.tela_compras = QWidget()
        self.tela_config = QWidget()
    
        self.tela.addWidget(self.tela_ruas)
        self.tela.addWidget(self.tela_prateleiras)
        self.tela.addWidget(self.tela_niveis)
        self.tela.addWidget(self.tela_blocos)
        self.tela.addWidget(self.tela_compras)
        self.tela.addWidget(self.tela_config)

        self._gerar_tela_ruas()
        self._gerar_tela_configuracao()

    def _gerar_tela_ruas(self):
        '''Visao geral '''
        if self.tela_ruas.layout():
            QWidget().setLayout(self.tela_ruas.layout())

        layout = QVBoxLayout(self.tela_ruas)

        top_bar = QHBoxLayout()

        self.input_busca = QLineEdit()
        self.input_busca.setPlaceholderText('Localizar produto (código, nome, loc)...')
        btn_buscar = QPushButton('🔍 Buscar')
        btn_buscar.clicked.connect(self.localizar_item)

        btn_config = QPushButton("⚙️ Configurar Estoque")
        btn_config.clicked.connect(lambda: self.tela.setCurrentIndex(5))

        btn_compras = QPushButton('🛒 Lista de Compras')
        btn_compras.clicked.connect(self.abrir_tela_compras)

        top_bar.addWidget(self.input_busca)
        top_bar.addWidget(btn_buscar)
        top_bar.addWidget(btn_compras)
        top_bar.addWidget(btn_config)
        layout.addLayout(top_bar)

        titulo = QLabel('Visao Geral')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet('font-size: 20px; font-weight: bold; margin: 20px 0;')
        layout.addWidget(titulo)

        grid = QGridLayout()

        for i in range (self.controller.layout.ruas):
            nome_rua = f'Rua {i}'
            btn_rua = QPushButton(nome_rua)
            btn_rua.setStyleSheet('''
            QPushButton{ background-color: #4CAF50; color : white; font-size: 16px; font-weight: bold; height: 100px; border-radius: 10px; }
            QPushButton:hover { background-color: #45a049; }
            ''')
            btn_rua.clicked.connect(lambda checked, r=nome_rua: self.expandir_rua(r))

            linha = i // 4
            coluna = i % 4
            grid.addWidget(btn_rua, linha, coluna)

        layout.addLayout(grid)
        layout.addStretch()




    def _criar_tela_ruas(self):
        '''Visao geral do almoxarifado'''
        widget = QWidget()
        layout = QVBoxLayout(widget)

        titulo = QLabel('Visao Geral: Ruas do Almoxarifado')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet('font-size : 20px; font-weight: bold; margin-bottom: 20px;')
        layout.addWidget(titulo)

        btn_compras = QPushButton('Ver Lista de Compras')
        btn_compras.setStyleSheet('padding: 20px; font-weight: bold; margin-bottom: 20px;')
        btn_compras.clicked.connect(self.abrir_tela_compras)
        layout.addWidget(btn_compras, alignment=Qt.AlignmentFlag.AlignRight)

        grid = QGridLayout()

        ruas = ['Rua 0', 'Rua 1', 'Rua 2', 'Rua 3']

        for i, nome_rua in enumerate(ruas):
            btn_rua = QPushButton(nome_rua)

            btn_rua.setStyleSheet('''
            QPushButton{
                background-color: #4CAF50; color: white;
                font-size: 16px; font-weight: bold;
                height: 150px; border-radius: 10px;
                }
                QPushButton:hover { background-color: #45a049; }
            ''')

            btn_rua.clicked.connect(lambda checked, r=nome_rua: self.expandir_rua(r))
            grid.addWidget(btn_rua, 0, i)

        layout.addLayout(grid)
        layout.addStretch()
        return widget

    def expandir_rua(self, nome_rua):
        '''Mostrar as prateleiras da rua escolhida'''

        if self.tela_prateleiras.layout():
            QWidget().setLayout(self.tela_prateleiras.layout())

        layout = QVBoxLayout(self.tela_prateleiras)

        cabecalho = QHBoxLayout()
        btn_voltar = QPushButton('⬅ Voltar para Mapa Geral')
        btn_voltar.clicked.connect(lambda: self.tela.setCurrentIndex(0))
        titulo = QLabel(f'Detalhes da {nome_rua} (Prateleiras)')
        titulo.setStyleSheet('font-size: 18px; font-weight: bold;')


        cabecalho.addWidget(btn_voltar)
        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        layout.addLayout(cabecalho)

        grid_prat = QGridLayout()
        qtd_prateleiras = self.controller.layout.prateleiras
        for i in range(1, qtd_prateleiras + 1):
            btn_prat = QPushButton(f'Prateleira {i}')
            btn_prat.setStyleSheet('''
            QPushButton {
                background-color: #2196F3; color: white;
                height: 80px; border-radius: 5px;
                }
                QPushButton:hover {background-color: #1976D2; }
            ''')

            btn_prat.clicked.connect(lambda checked, r=nome_rua, p=i: self.expandir_prateleira(r, p))
            grid_prat.addWidget(btn_prat, (i-1)//4, (i-1)%4)

        layout.addLayout(grid_prat)
        layout.addStretch()
        self.tela.setCurrentIndex(1)

    def expandir_prateleira(self, nome_rua, num_prateleira):
        '''Gerar os niveis'''
        if self.tela_niveis.layout():
            QWidget().setLayout(self.tela_niveis.layout())

        layout = QVBoxLayout(self.tela_niveis)
        cabecalho = QHBoxLayout()
        btn_voltar = QPushButton('⬅ Voltar')
        btn_voltar.clicked.connect(lambda: self.tela.setCurrentIndex(1))
        titulo = QLabel(f'{nome_rua} > Prateleira {num_prateleira} > Níveis')
        titulo.setStyleSheet('font-size: 18px; font-weight: bold:')

        cabecalho.addWidget(btn_voltar)
        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        layout.addLayout(cabecalho)

        grid = QGridLayout()
        qtd_niveis = self.controller.layout.niveis
        for i in range(1, qtd_niveis + 1):
            btn_nivel = QPushButton(f'Nivel {i}')
            btn_nivel.setStyleSheet('''
            QPushButton  { background-color: #FF9800; color: white; height: 80px; border-radius: 5px; font-weight: bold;}
            QPushButton:hover{background-color: #F57C00; }
            ''')
            btn_nivel.clicked.connect(lambda checked, r=nome_rua, p=num_prateleira, n=i: self.expandir_nivel(r, p, n))
            grid.addWidget(btn_nivel, i, 0)

        layout.addLayout(grid)
        layout.addStretch()
        self.tela.setCurrentIndex(2)

    def expandir_nivel(self, nome_rua, num_prateleira, num_nivel):
        '''Gera blocos nos niveis '''
        if self.tela_blocos.layout():
            QWidget().setLayout(self.tela_blocos.layout())

        layout = QVBoxLayout(self.tela_blocos)
        cabecalho = QHBoxLayout()
        btn_voltar = QPushButton('⬅ Voltar')
        btn_voltar.clicked.connect(lambda: self.tela.setCurrentIndex(2))
        titulo = QLabel(f'{nome_rua} > Prateleira {num_prateleira} > Nivel {num_nivel} > Blocos')
        titulo.setStyleSheet('font-size: 18px; font-weight: bold;')
        cabecalho.addWidget(btn_voltar)
        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        layout.addLayout(cabecalho)

        grid = QGridLayout()
        qtd_blocos = self.controller.layout.blocos
        for i in range(1, qtd_blocos + 1):
            btn_bloco = QPushButton(f'Bloco {i}\n(Vazio/Cadastrar)')
            btn_bloco.setStyleSheet('''  
            QPushButton { background-color: #9C27B0; color: white; height: 100px; border-radius: 5px; }
            QPushButton:hover { background-color: #7B1FA2; }
            ''')
            grid.addWidget(btn_bloco, (i-1)//3, (i-1)%3)

        layout.addLayout(grid)
        layout.addStretch()
        self.tela.setCurrentIndex(3)

    def _gerar_tela_configuracao(self):
        '''Tela para editar quantidade de ruas prateeleiras niveis e blocos'''
        layout = QVBoxLayout(self.tela_config)
        titulo = QLabel('Editar Layout')
        titulo.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(titulo)

        form = QFormLayout()

        self.spin_ruas = QSpinBox()
        self.spin_ruas.setValue(self.controller.layout.ruas)
        self.spin_ruas.setMinimum(1)

        self.spin_prateleiras = QSpinBox()
        self.spin_prateleiras.setValue(self.controller.layout.prateleiras)
        self.spin_prateleiras.setMinimum(1)

        self.spin_niveis = QSpinBox()
        self.spin_niveis.setValue(self.controller.layout.niveis)
        self.spin_niveis.setMinimum(1)

        self.spin_blocos = QSpinBox()
        self.spin_blocos.setValue(self.controller.layout.blocos)
        self.spin_blocos.setMinimum(1)

        form.addRow('Quantidade de Ruas:', self.spin_ruas)
        form.addRow('Quantidade de Prateleiras:', self.spin_prateleiras)
        form.addRow('Quantidade de Níveis:', self.spin_niveis)
        form.addRow('Quantidade de Blocos:', self.spin_blocos)

        layout.addLayout(form)

        botoes = QHBoxLayout()
        btn_salvar = QPushButton('💾 Salvar')
        btn_salvar.setStyleSheet('padding: 10px; background-color: #4CAF50; color: white; border-radius: 5px;')
        btn_salvar.clicked.connect(self.salvar_configuracao)

        btn_cancelar = QPushButton('❌ Cancelar')
        btn_cancelar.clicked.connect(lambda: self.tela.setCurrentIndex(0))

        botoes.addWidget(btn_salvar)
        botoes.addWidget(btn_cancelar)
        layout.addLayout(botoes)
        layout.addStretch()

    def salvar_configuracao(self):
        sucesso, msg = self.controller.atualizar_layout_estoque(
            self.spin_ruas.value(),
            self.spin_prateleiras.value(),
            self.spin_niveis.value(),
            self.spin_blocos.value()
        )
        QMessageBox.information(self, 'Sucesso' if sucesso else 'Erro', msg)
        self._gerar_tela_ruas()
        self.tela.setCurrentIndex(0)

    def localizar_item(self):
        termo = self.input_busca.text().strip()
        if not termo:
            QMessageBox.warning(self, 'Atencao', 'Digite um termo para buscar.')
            return

        resultados = self.controller.localizar_itens(termo.lower())

        if not resultados:
            QMessageBox.information(self, 'Resultado', 'Nenhum produto encontrado.')
            return

        texto_resultado = f'Encontrados {len(resultados)} produtos:\n\n'

        for prod in resultados:
            texto_resultado += f'Cód: {prod.codigo} | Desc: {prod.descricao}\n'
            texto_resultado += f'Local: {prod.localizacao} | Qtd: {prod.quantidade}\n'
            texto_resultado += '-' * 30 + '\n'

        QMessageBox.information(self, "Busca de Produtos", texto_resultado)



    def abrir_tela_compras(self):
        '''tabela de intens para comprar '''
        if self.tela_compras.layout():
            QWidget().setLayout(self.tela_compras.layout())
        layout = QVBoxLayout(self.tela_compras)

        btn_voltar = QPushButton('⬅ Voltar')
        btn_voltar.setStyleSheet('padding: 10px; background-color: #607D8B; color: white; border-radius: 5px;')
        btn_voltar.clicked.connect(self.voltar_mapa_geral)
        layout.addWidget(btn_voltar, alignment=Qt.AlignmentFlag.AlignLeft)

        titulo = QLabel('Lista de Compras (Estoque Critico)')
        titulo.setStyleSheet('font-size: 18px; font-weight; bold; margin-top: 10px;')
        layout.addWidget(titulo)

        tabela = QTableWidget()
        tabela.setColumnCount(4)
        tabela.setHorizontalHeaderLabels(['Codigo', 'Descricao', 'Localização', 'Quantidade'])
        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        produtos_para_comprar = self.controller.obter_lista_compras()
        tabela.setRowCount(len(produtos_para_comprar))

        for row, produto in enumerate(produtos_para_comprar):
            cod_item = QTableWidgetItem(produto.codigo)
            desc_item = QTableWidgetItem(produto.descricao)
            loc_item = QTableWidgetItem(produto.localizacao)
            qtd_item = QTableWidgetItem(str(produto.quantidade))

            cor = QColor(produto.status_cor)
            for item in [cod_item, desc_item, loc_item, qtd_item]:
                item.setBackground(cor)

            tabela.setItem(row, 0, cod_item) 
            tabela.setItem(row, 1, desc_item)
            tabela.setItem(row, 2, loc_item)
            tabela.setItem(row, 3, qtd_item)

        layout.addWidget(tabela)
        self.tela.setCurrentIndex(4)
        

    def voltar_mapa_geral(self):
        '''Retornar para a visao de ruas'''
        self.tela.setCurrentIndex(0)


