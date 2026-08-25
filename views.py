import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QGridLayout, QPushButton, QLabel, QStackedWidget,
                             QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView,
                             QLineEdit, QMessageBox, QSpinBox, QFormLayout, QComboBox,
                             QFileDialog, QInputDialog)
from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtCore import Qt

class MapaEstoque(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle('Mapa Do Estoque')
        self.resize(1000, 700) # Deixei um pouco mais largo para a nova tabela

        self.tela = QStackedWidget()
        self.setCentralWidget(self.tela)

        self.tela_ruas = QWidget()
        self.tela_prateleiras = QWidget()
        self.tela_niveis = QWidget()
        self.tela_blocos = QWidget()
        self.tela_compras = QWidget()
        self.tela_config = QWidget()
        self.tela_produto = QWidget()
        self.tela_edicao = QWidget()
        self.tela_estoque = QWidget() # NOVA TELA DE VISÃO GERAL (Índice 8)

        self.tela.addWidget(self.tela_ruas)
        self.tela.addWidget(self.tela_prateleiras)
        self.tela.addWidget(self.tela_niveis)
        self.tela.addWidget(self.tela_blocos)
        self.tela.addWidget(self.tela_compras)
        self.tela.addWidget(self.tela_config)
        self.tela.addWidget(self.tela_produto)
        self.tela.addWidget(self.tela_edicao)
        self.tela.addWidget(self.tela_estoque) 

        self._gerar_tela_ruas()
        self._gerar_tela_configuracao()

    def _gerar_tela_ruas(self):
        if self.tela_ruas.layout():
            QWidget().setLayout(self.tela_ruas.layout())

        layout = QVBoxLayout(self.tela_ruas)

        top_bar = QHBoxLayout()

        self.input_busca = QLineEdit()
        self.input_busca.setPlaceholderText('Localizar produto (código, nome, loc)...')
        btn_buscar = QPushButton('🔍 Buscar')
        btn_buscar.clicked.connect(self.localizar_item)
        
        # NOVO BOTÃO DA VISÃO GERAL
        btn_estoque_geral = QPushButton('📦 Estoque Geral')
        btn_estoque_geral.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        btn_estoque_geral.clicked.connect(self.abrir_tela_estoque_geral)

        btn_compras = QPushButton('🛒 Lista de Compras')
        btn_compras.clicked.connect(self.abrir_tela_compras)
        
        btn_config = QPushButton("⚙️ Configurar Estoque")
        btn_config.clicked.connect(self.abrir_tela_configuracao)

        top_bar.addWidget(self.input_busca)
        top_bar.addWidget(btn_buscar)
        top_bar.addWidget(btn_estoque_geral)
        top_bar.addWidget(btn_compras)
        top_bar.addWidget(btn_config)
        layout.addLayout(top_bar)

        titulo = QLabel('Visao Geral do Galpão')
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet('font-size: 20px; font-weight: bold; margin: 20px 0;')
        layout.addWidget(titulo)

        grid = QGridLayout()

        ruas_ativas = self.controller.listar_ruas_ativas()
        for indice, nome_rua in enumerate(ruas_ativas):
            btn_rua = QPushButton(nome_rua) # AGORA USA O NOME DIRETAMENTE
            btn_rua.setStyleSheet('''
            QPushButton{ background-color: #4CAF50; color : white; font-size: 16px; font-weight: bold; height: 100px; border-radius: 10px; }
            QPushButton:hover { background-color: #45a049; }
            ''')
            btn_rua.clicked.connect(lambda checked, r=nome_rua: self.expandir_rua(r))

            linha = indice // 4
            coluna = indice % 4
            grid.addWidget(btn_rua, linha, coluna)

        layout.addLayout(grid)
        layout.addStretch()

    def expandir_rua(self, nome_rua):
        if self.tela_prateleiras.layout():
            QWidget().setLayout(self.tela_prateleiras.layout())

        layout = QVBoxLayout(self.tela_prateleiras)

        cabecalho = QHBoxLayout()
        btn_voltar = QPushButton('⬅ Voltar para Mapa Geral')
        btn_voltar.clicked.connect(lambda: self.tela.setCurrentIndex(0))
        titulo = QLabel(f'Detalhes de: {nome_rua} (Prateleiras)')
        titulo.setStyleSheet('font-size: 18px; font-weight: bold;')

        cabecalho.addWidget(btn_voltar)
        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        layout.addLayout(cabecalho)

        config_rua = self.controller.layout.obter_config(nome_rua) # LEITURA PELO NOME DIRETO

        grid_prat = QGridLayout()
        qtd_prateleiras = config_rua['prateleiras']

        for i in range(1, qtd_prateleiras + 1):
            btn_prat = QPushButton(f'Prateleira {i}')
            btn_prat.setStyleSheet('''
            QPushButton { background-color: #2196F3; color: white; height: 80px; border-radius: 5px; }
            QPushButton:hover {background-color: #1976D2; }
            ''')
            btn_prat.clicked.connect(lambda checked, r=nome_rua, p=i: self.expandir_prateleira(r, p))
            grid_prat.addWidget(btn_prat, (i-1)//4, (i-1)%4)

        layout.addLayout(grid_prat)
        layout.addStretch()
        self.tela.setCurrentIndex(1)

    def expandir_prateleira(self, nome_rua, num_prateleira):
        if self.tela_niveis.layout():
            QWidget().setLayout(self.tela_niveis.layout())

        layout = QVBoxLayout(self.tela_niveis)
        cabecalho = QHBoxLayout()
        btn_voltar = QPushButton('⬅ Voltar')
        btn_voltar.clicked.connect(lambda: self.tela.setCurrentIndex(1))
        titulo = QLabel(f'{nome_rua} > Prateleira {num_prateleira} > Níveis')
        titulo.setStyleSheet('font-size: 18px; font-weight: bold;')

        cabecalho.addWidget(btn_voltar)
        cabecalho.addWidget(titulo)
        cabecalho.addStretch()
        layout.addLayout(cabecalho)

        config_rua = self.controller.layout.obter_config(nome_rua)

        grid = QGridLayout()
        qtd_niveis = config_rua['niveis']

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

        config_rua = self.controller.layout.obter_config(nome_rua)

        grid = QGridLayout()
        qtd_blocos = config_rua['blocos']

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

    def abrir_tela_configuracao(self):
        self._gerar_tela_configuracao()
        self.tela.setCurrentIndex(5)

    def _gerar_tela_configuracao(self):
        if self.tela_config.layout():
            QWidget().setLayout(self.tela_config.layout())

        layout = QVBoxLayout(self.tela_config)
        titulo = QLabel('Editar Layout')
        titulo.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(titulo)

        # Adicionar rua COM NOME LIVRE
        box_adicionar = QHBoxLayout()
        box_adicionar.addWidget(QLabel('Nome da Nova Rua:'))

        self.input_nova_rua = QLineEdit()
        self.input_nova_rua.setPlaceholderText('Ex: Corredor Frio')
        box_adicionar.addWidget(self.input_nova_rua)

        btn_add_rua = QPushButton("➕ Adicionar Rua")
        btn_add_rua.setStyleSheet('background-color: #2196F3; color: white; padding: 5px;')
        btn_add_rua.clicked.connect(self.ui_adicionar_rua)
        box_adicionar.addWidget(btn_add_rua)

        layout.addLayout(box_adicionar)
        layout.addWidget(QLabel('<hr>'))

        layout.addWidget(QLabel("<b> Editar ou Excluir Rua: </b>"))
        box_selecao = QHBoxLayout()
        self.combo_ruas = QComboBox()

        ruas_ativas = self.controller.listar_ruas_ativas()
        for nome_rua in ruas_ativas:
            self.combo_ruas.addItem(nome_rua, nome_rua)

        self.combo_ruas.currentIndexChanged.connect(self._atualizar_spins_da_rua)
        box_selecao.addWidget(self.combo_ruas)

        btn_excluir_rua = QPushButton("🗑️ Excluir esta Rua")
        btn_excluir_rua.setStyleSheet('background-color: #F44336; color: white; padding: 5px;')
        btn_excluir_rua.clicked.connect(self.ui_excluir_rua)
        box_selecao.addWidget(btn_excluir_rua)
        layout.addLayout(box_selecao)

        form_individual = QFormLayout()
        self.spin_prateleiras = QSpinBox()
        self.spin_prateleiras.setMinimum(1)
        self.spin_niveis = QSpinBox()
        self.spin_niveis.setMinimum(1)
        self.spin_blocos = QSpinBox()
        self.spin_blocos.setMinimum(1)

        form_individual.addRow('Número de Prateleiras: ', self.spin_prateleiras)
        form_individual.addRow('Número de Níveis: ', self.spin_niveis)
        form_individual.addRow('Número de Blocos: ', self.spin_blocos)

        layout.addLayout(form_individual)

        botoes = QHBoxLayout()
        btn_salvar = QPushButton('💾 Salvar Layout')
        btn_salvar.setStyleSheet('padding: 10px; background-color: #4CAF50; color: white; border-radius: 5px;')
        btn_salvar.clicked.connect(self.salvar_configuracao_rua)

        btn_cancelar = QPushButton('❌ Cancelar')
        btn_cancelar.clicked.connect(lambda: self.tela.setCurrentIndex(0))

        botoes.addWidget(btn_salvar)
        botoes.addWidget(btn_cancelar)
        layout.addLayout(botoes)
        layout.addStretch()

        if ruas_ativas:
            self._atualizar_spins_da_rua()

    def ui_adicionar_rua(self):
        nome_rua = self.input_nova_rua.text().strip()
        sucesso, msg = self.controller.adicionar_nova_rua(nome_rua)
        QMessageBox.information(self, 'Aviso', msg)
        if sucesso:
            self.abrir_tela_configuracao()
            self._gerar_tela_ruas()

    def ui_excluir_rua(self):
        nome_rua = self.combo_ruas.currentData()
        if nome_rua is None: return

        resposta = QMessageBox.question(self, 'Confirmação',
                                        f'Deseja apagar a rua "{nome_rua}"? Produtos ficarão sem área no mapa.',
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if resposta == QMessageBox.StandardButton.Yes:
            sucesso, msg = self.controller.excluir_rua(nome_rua)
            QMessageBox.information(self, 'Aviso', msg)
            if sucesso:
                self.abrir_tela_configuracao()
                self._gerar_tela_ruas()

    def _atualizar_spins_da_rua(self):
        nome_rua = self.combo_ruas.currentData()
        if nome_rua is not None:
            config = self.controller.layout.obter_config(nome_rua)
            self.spin_prateleiras.setValue(config['prateleiras'])
            self.spin_niveis.setValue(config['niveis'])
            self.spin_blocos.setValue(config['blocos'])

    def salvar_configuracao_rua(self):
        nome_rua = self.combo_ruas.currentData()
        if nome_rua is None: return
        sucesso, msg = self.controller.atualizar_layout_rua(
            nome_rua,
            self.spin_prateleiras.value(),
            self.spin_niveis.value(),
            self.spin_blocos.value()
        )
        QMessageBox.information(self, 'Sucesso' if sucesso else 'Erro', msg)
        self._gerar_tela_ruas()
        self.tela.setCurrentIndex(0)

    # ==========================================
    # MÓDULO NOVO: VISÃO GERAL DE TODO ESTOQUE
    # ==========================================
    def abrir_tela_estoque_geral(self):
        if self.tela_estoque.layout():
            QWidget().setLayout(self.tela_estoque.layout())
        
        layout = QVBoxLayout(self.tela_estoque)

        btn_voltar = QPushButton('⬅ Voltar')
        btn_voltar.setStyleSheet('padding: 10px; background-color: #607D8B; color: white; border-radius: 5px;')
        btn_voltar.clicked.connect(self.voltar_mapa_geral)
        layout.addWidget(btn_voltar, alignment=Qt.AlignmentFlag.AlignLeft)

        titulo = QLabel('Estoque Geral - Movimentação Rápida')
        titulo.setStyleSheet('font-size: 18px; font-weight: bold; margin-top: 10px;')
        layout.addWidget(titulo)

        tabela = QTableWidget()
        tabela.setColumnCount(5)
        tabela.setHorizontalHeaderLabels(['Código', 'Descrição', 'Local', 'Qtd Atual', 'Ações Rápidas'])
        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        produtos = self.controller.repository.listar_todos()
        tabela.setRowCount(len(produtos))

        for row, produto in enumerate(produtos):
            tabela.setItem(row, 0, QTableWidgetItem(produto.codigo))
            tabela.setItem(row, 1, QTableWidgetItem(produto.descricao))
            tabela.setItem(row, 2, QTableWidgetItem(produto.localizacao))
            
            qtd_item = QTableWidgetItem(str(produto.quantidade))
            qtd_item.setBackground(QColor(produto.status_cor))
            qtd_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            tabela.setItem(row, 3, qtd_item)

            # Painel com os botões de movimentação na tabela
            widget_acoes = QWidget()
            layout_acoes = QHBoxLayout(widget_acoes)
            layout_acoes.setContentsMargins(5, 2, 5, 2)

            btn_in = QPushButton('➕ Entrada')
            btn_in.setStyleSheet('background-color: #4CAF50; color: white;')
            btn_in.clicked.connect(lambda checked, p=produto.codigo: self.prompt_movimentacao(p, 'entrada'))

            btn_out = QPushButton('➖ Retirar')
            btn_out.setStyleSheet('background-color: #F44336; color: white;')
            btn_out.clicked.connect(lambda checked, p=produto.codigo: self.prompt_movimentacao(p, 'baixa'))

            layout_acoes.addWidget(btn_in)
            layout_acoes.addWidget(btn_out)
            
            tabela.setCellWidget(row, 4, widget_acoes)

        layout.addWidget(tabela)
        self.tela.setCurrentIndex(8)

    def prompt_movimentacao(self, codigo, tipo):
        '''Abre um pop-up rápido para entrar ou retirar itens na visão geral'''
        acao = "adicionar ao estoque" if tipo == 'entrada' else "retirar do estoque"
        qtd, ok = QInputDialog.getInt(self, "Movimentação Rápida", f"Quantidade para {acao} (Cód: {codigo}):", 1, 1, 99999)
        
        if ok:
            sucesso, msg = self.controller.movimentar_estoque(codigo, qtd, tipo)
            if sucesso:
                self.abrir_tela_estoque_geral() # Recarrega a tabela com valores atualizados
            else:
                QMessageBox.warning(self, "Erro", msg)

    # ==========================================
    # OUTROS MÉTODOS DE PRODUTOS E BUSCA
    # ==========================================
    def localizar_item(self):
        termo = self.input_busca.text().strip()
        if not termo:
            QMessageBox.warning(self, 'Atencao', 'Digite um termo para buscar.')
            return

        resultados = self.controller.localizar_itens(termo.lower())

        if not resultados:
            QMessageBox.information(self, 'Resultado', 'Nenhum produto encontrado.')
            return

        if len(resultados) == 1:
            self.abrir_pagina_produto(resultados[0].codigo)
        else:
            texto_resultado = f'Encontrados {len(resultados)} produtos:\n\n'

            for prod in resultados:
                texto_resultado += f'Cód: {prod.codigo} | Desc: {prod.descricao}\n'
                texto_resultado += f'Local: {prod.localizacao} | Qtd: {prod.quantidade}\n'
                texto_resultado += '-' * 30 + '\n'

            QMessageBox.information(self, "Busca de Produtos", texto_resultado)

    def abrir_pagina_produto(self, codigo_produto):
        produto = self.controller.repository.buscar_por_codigo(codigo_produto)

        if not produto:
            QMessageBox.warning(self, 'Erro', 'Produto não encontrado.')
            return
        if self.tela_produto.layout():
            QWidget().setLayout(self.tela_produto.layout())

        layout = QVBoxLayout(self.tela_produto)
        cabecalho_layout = QHBoxLayout()
        btn_voltar = QPushButton('⬅ Voltar')
        btn_voltar.clicked.connect(lambda: self.tela.setCurrentIndex(0))

        btn_editar = QPushButton('✏️ Editar Produto')
        btn_editar.setStyleSheet('background-color: #FFC107; color: black; font-weight: bold; padding: 5px;')        
        btn_editar.clicked.connect(lambda: self.abrir_tela_edicao_produto(produto))

        cabecalho_layout.addWidget(btn_voltar)
        cabecalho_layout.addStretch()
        cabecalho_layout.addWidget(btn_editar)
        layout.addLayout(cabecalho_layout)

        info_layout = QHBoxLayout()
        label_foto = QLabel()
        if produto.foto_path:
            pixmap = QPixmap(produto.foto_path)
            label_foto.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            label_foto.setText('Sem imagem')
            label_foto.setStyleSheet('background-color: #EEE; border: 1px solid #CCC;')
            label_foto.setFixedSize(200, 200)
            label_foto.setAlignment(Qt.AlignmentFlag.AlignCenter)

        info_layout.addWidget(label_foto)

        dados_layout = QVBoxLayout()
        dados_layout.addWidget(QLabel(f'<b>Código:</b> {produto.codigo}'))
        dados_layout.addWidget(QLabel(f'<b>Descrição:</b> {produto.descricao}'))
        dados_layout.addWidget(QLabel(f'<b>Localização:</b> {produto.localizacao}'))

        label_qtd = QLabel(f'<b> Estoque Atual: </b> {produto.quantidade}')
        label_qtd.setStyleSheet(f'background-color: {produto.status_cor}; padding: 5px;')
        dados_layout.addWidget(label_qtd)

        info_layout.addLayout(dados_layout)
        info_layout.addStretch()
        layout.addLayout(info_layout)

        mov_layout = QGridLayout()
        mov_layout.addWidget(QLabel('<b> Entrada de Item: </b>'), 0, 0)
        spin_entrada = QSpinBox()
        spin_entrada.setMinimum(1)
        spin_entrada.setMaximum(99999)
        mov_layout.addWidget(spin_entrada, 0, 1)

        btn_entrada = QPushButton('Confirmar Entrada')
        btn_entrada.setStyleSheet('background-color: #4CAF50; color: white;')
        btn_entrada.clicked.connect(lambda: self._executar_movimentacao(produto.codigo, spin_entrada.value(), 'entrada'))
        mov_layout.addWidget(btn_entrada, 0, 2)

        mov_layout.addWidget(QLabel('<b>Requisitar Retirada(Baixa):</b>'), 1, 0)
        spin_saida = QSpinBox()
        spin_saida.setMinimum(1)
        spin_saida.setMaximum(produto.quantidade if produto.quantidade > 0 else 1)
        mov_layout.addWidget(spin_saida, 1, 1)

        btn_saida = QPushButton('Confirmar Retirada')
        btn_saida.setStyleSheet('background-color: #F44336; color: white;')
        btn_saida.clicked.connect(lambda: self._executar_movimentacao(produto.codigo, spin_saida.value(), 'baixa'))
        mov_layout.addWidget(btn_saida, 1, 2)

        layout.addLayout(mov_layout)
        layout.addStretch()
        self.tela.setCurrentIndex(6)

    def _executar_movimentacao(self, codigo, quantidade, tipo):
        sucesso, msg = self.controller.movimentar_estoque(codigo, quantidade, tipo)
        if sucesso:
            QMessageBox.information(self, 'Sucesso', msg)
            self.abrir_pagina_produto(codigo)
        else:
            QMessageBox.warning(self, 'Erro', msg)

    def abrir_tela_edicao_produto(self, produto):
        if self.tela_edicao.layout():
            QWidget().setLayout(self.tela_edicao.layout())

        layout = QVBoxLayout(self.tela_edicao)

        titulo = QLabel(f'Editar Produto: {produto.codigo}')
        titulo.setStyleSheet('font-size: 20px; font-weight: bold;')
        layout.addWidget(titulo)

        form = QFormLayout()

        input_codigo = QLineEdit(produto.codigo)
        input_codigo.setEnabled(False)

        input_descricao = QLineEdit(produto.descricao)
        input_localizacao = QLineEdit(produto.localizacao)

        spin_quantidade = QSpinBox()
        spin_quantidade.setMaximum(99999)
        spin_quantidade.setValue(produto.quantidade)

        box_foto = QHBoxLayout()
        input_foto = QLineEdit(getattr(produto, 'foto_path', ''))
        btn_procurar_foto = QPushButton('Procurar...')

        def selecionar_imagem():
            caminho, _ = QFileDialog.getOpenFileName(self, 'Selecionar Imagem', '', 'Imagens (*.png *.jpg *.jpeg *.bmp)')
            if caminho:
                input_foto.setText(caminho)

        btn_procurar_foto.clicked.connect(selecionar_imagem)
        box_foto.addWidget(input_foto)
        box_foto.addWidget(btn_procurar_foto)

        form.addRow('Codigo (Bloqueado):', input_codigo)
        form.addRow('Descricao:', input_descricao)
        form.addRow('Localizacao (ex: R1.P1.N1):', input_localizacao)
        form.addRow('Quantidade em Estoque:', spin_quantidade)
        form.addRow('Caminho da Foto:', box_foto)

        layout.addLayout(form)

        botoes = QHBoxLayout()
        btn_salvar = QPushButton('💾 Salvar Alterações')
        btn_salvar.setStyleSheet('background-color: #4CAF50; color: white; padding: 10px;')

        def confirmar_edicao():
            sucesso, msg = self.controller.editar_dados_produto(
                produto.codigo,
                input_descricao.text(),
                input_localizacao.text(),
                spin_quantidade.value(),
                input_foto.text()    
            )
            QMessageBox.information(self, 'Edicao', msg)
            if sucesso:
                self.abrir_pagina_produto(produto.codigo)

        btn_salvar.clicked.connect(confirmar_edicao)

        btn_cancelar = QPushButton('❌ Cancelar')
        btn_cancelar.clicked.connect(lambda: self.abrir_pagina_produto(produto.codigo))

        botoes.addWidget(btn_salvar)
        botoes.addWidget(btn_cancelar)

        layout.addLayout(botoes)
        layout.addStretch()
        self.tela.setCurrentIndex(7)
    
    def abrir_tela_compras(self):
        if self.tela_compras.layout():
            QWidget().setLayout(self.tela_compras.layout())
        layout = QVBoxLayout(self.tela_compras)

        btn_voltar = QPushButton('⬅ Voltar')
        btn_voltar.setStyleSheet('padding: 10px; background-color: #607D8B; color: white; border-radius: 5px;')
        btn_voltar.clicked.connect(self.voltar_mapa_geral)
        layout.addWidget(btn_voltar, alignment=Qt.AlignmentFlag.AlignLeft)

        titulo = QLabel('Lista de Compras (Estoque Crítico)')
        titulo.setStyleSheet('font-size: 18px; font-weight: bold; margin-top: 10px;')
        layout.addWidget(titulo)

        tabela = QTableWidget()
        tabela.setColumnCount(4)
        tabela.setHorizontalHeaderLabels(['Código', 'Descrição', 'Localização', 'Quantidade'])
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
        self.tela.setCurrentIndex(0)
