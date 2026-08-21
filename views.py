import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QGridLayout, QPushButton, QLabel, QStackedWidget,
                             QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

class MapaEstoque(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle('Mapa Do Estoque')
        self.resize(800, 600)

        self.tela = QStackedWidget()
        self.setCentralWidget(self.tela)

        self.tela_ruas = self._criar_tela_ruas()
        self.tela_prateleiras = QWidget()
        self.tela_compras = QWidget()

        self.tela.addWidget(self.tela_ruas)
        self.tela.addWidget(self.tela_prateleiras)
        self.tela.addWidget(self.tela_compras)

    def _criar_tela_ruas(self):
        '''Visao geral do almoxarifado'''
        widget = QWidget()
        layout = QVBoxLayout(widget)

        titulo = QLabel('Visao Geral: Ruas do Almoxarifado')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet('font-size : 20px; font-weight: bold; margin-bottom: 20px;')
        layout.addWidget(titulo)

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
            QWidget().setLayout(self.tela_pratelerias.layout())

        layout = QVBoxLayout(self.tela_prateleiras)

        cabecalho = QGridLayout()
        btn_voltar = QPushButton('⬅ Voltar para Mapa Geral')
        btn_voltar.setStyleSheet(   'padding: 10px; background-color: #f44336; color: white; border-radius: 5px;')
        btn_voltar.clicked.connect(self.voltar_mapa_geral)

        titulo = QLabel(f'Detalhes da {nome_rua}')
        titulo.setStyleSheet('font-size: 18px; font-weight: bold;')

        cabecalho.addWidget(btn_voltar, 0, 0)
        cabecalho.addWidget(titulo, 0, 1)
        cabecalho.addLayout(cabecalho)

        grid_prat = QGridLayout()
        for i in range(1, 9):
            btn_prat = QPushButton(f'Prateleira {i}')
            btn_prat.setStyleSheet('''
            QPushButton {
                background-color: #2196F3; color: white;
                height: 80px; border-radius: 5px;
                }
                QPushButton:hover {background-color: #1976D2; }
            ''')

            btn_prat.clicked.connect(lambda checked, p=i: print(f'Abrindo itens da Prateleira {p} da {nome_rua}'))

            linha = (i-1)//4
            coluna = (i-1)%4
            grid_prat.addWidget(btn_prat, linha, coluna)

        layout.addLayout(grid_prat)
        layout.addStretch()

        self.telas.setCurrentIndex(1)

    def abrir_tela_compras(self):
        '''tabela de intens para comprar '''
        if self.tela_compras.layout():
            QWidget().setLayout(self.tela_compras_compras.layout())
        layout = QVBoxLayout(self.tela_compras)

        btn_voltar = QPushButton('⬅ Voltar')
        btn_voltar.setStyleSheet('padding: 10px; background-color: #607D8B; color: ehite; border-radius: 5px;')
        btn_voltar.clicked.connect(self.voltar_mapa_geral)
        layout.addWidget(btn_voltar, alignment=Qt.AlignmentFlag.AlignLeft)

        titulo = QLabel('Lista de Compras (Estoque Critico)')
        titulo.setStyleSheet('font-size: 18px: font-weight; bold; margin-top: 10px:')
        layout.addWidget(titulo)

        tabela = QTableWidget()
        tabela.setColumnCount(4)
        tabela.setHorizontalHearderLabel(['Codigo', 'Descricao', 'Loacalizacao', 'Quantidade'])
        tabela.horizontalHeader().setSectionResizeMOde(QHeaderView.ResizeMode.Stretch)

        produtos_para_comprar = self.controller.obter_lista_comprar()
        tabela.setRowCount(len(produtos_para_comprar))

        for row, produto in enumerate(produtos_para_comprar):
            cod_item = QTableWidgetItem(produto.codigo)
            desc_item = QTableWidgetItem(produto.descricao)
            loc_item = QTableWidgetItem(produto.localizacao)
            qtd_item = QTableWidgetItem(str(produto.quantidade))

            cor= QColor(produto.status_cor)
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
            self.telas.setCurrentIndex(2)
        

    def voltar_mapa_geral(self):
        '''Retornar para a visao de ruas'''
        self.telas.setCurrentIndex(0)


