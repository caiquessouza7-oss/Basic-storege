from models import Produto, LayoutEstoque

class EstoqueController:

    def __init__(self, repository):
        self.repository = repository
        self.layout = LayoutEstoque

    def pesquisar_produto(self, termo):
        '''Pesquisar pelo nome, codigo, localização'''

        if not termo:
            return []

        termo = str(termo).lower()

        todos_produtos = self.repository.listar_todos()

        resultados = [
            produto for produto in todos_produtos
            if termo in str(produto.codigo).lower()
            or termo in str(produto.descricao).lower()
            or termo in str(produto.localizacao).lower()
        ]

        return resultados

    def registrar_novo_produto(self, codigo, descricao, localizacao, quantidade, foto_path=""):
        if self.repository.buscar_por_codigo(codigo):
            return False, f'Produto com o codigo {codigo} já existe.'

        novo_produto = Produto(codigo, descricao, localizacao, quantidade)
        self.repository.salvar(novo_produto)
        return True, 'Produto cadastrado com sucesso'

    def editar_dados_produto(self, codigo, nova_descricao, nova_localizacao, nova_quantidade, novo_foto_path=""):
        produto_existente = self.repository.buscar_por_codigo(codigo)
        if not produto_existente:
            return False, 'Produto não encontrado'

        produto_atualizado = Produto(codigo, nova_descricao, nova_localizacao, nova_quantidade, novo_foto_path)
        self.repository.atualizar_produto_completo(produto_atualizado)
        return True, 'Produto atualizado com sucesso'

    def excluir_produto(self, codigo):
        produto = self.repository.buscar_por_codigo(codigo)
        if not produto:
            return False, 'Produto não encontrado'
        self.repository.deletar(codigo)
        return True, 'Produto deletado'

    def movimentar_estoque(self, codigo, quantidade_movimento, tipo='entrada'):
        produto = self.repository.buscar_por_codigo(codigo)
        if not produto:
            return False, 'Produto não encontrado'

        if tipo == 'entrada':
            nova_quantidade = produto.quantidade + quantidade_movimento
        elif tipo == 'baixa':
            if quantidade_movimento > produto.quantidade:
                return False, f'Estoque insuficiente. Estoque atual: {produto.quantidade}'
            nova_quantidade = produto.quantidade - quantidade_movimento
        else:
            return False, 'Movimentaçao inválida'

        self.repository.atualizar_quantidade(codigo, nova_quantidade)
        return True, f'Movimentação efetuada. Saldo atual: {nova_quantidade}'
    
    def obter_lista_compras(self):
        '''Produtos com estoque baixo'''
        todos_produtos = self.repository.listar_todos()
        return [p for p in todos_produtos if p.precisa_comprar]

    def localizar_itens(self, termo):
        '''Lista de itens buscado'''
        return self.repository.localizar_produto_geral(termo)

    def listar_ruas_ativas(self):
        self.layout.inicializar_layout()
        # Retorna a lista de nomes cadastrados
        return sorted(list(self.layout.configs_ruas.keys()))

    def adicionar_nova_rua(self, nome_rua):
        if not nome_rua.strip():
            return False, 'O nome da rua não pode estar vazio.'
            
        sucesso = self.layout.adicionar_rua(nome_rua)
        if sucesso:
            return True, f'"{nome_rua}" adicionada com sucesso'
        return False, f'A "{nome_rua}" já existe'

    def excluir_rua(self, nome_rua):
        sucesso = self.layout.remover_rua(nome_rua)
        if sucesso:
            return True, f'"{nome_rua}" removida com sucesso'
        return False, f'"{nome_rua}" não encontrada'

    def atualizar_layout_rua(self, nome_rua, prateleiras, niveis, blocos):
        self.layout.inicializar_layout()
        if nome_rua in self.layout.configs_ruas:
            self.layout.configs_ruas[nome_rua] = {
                'prateleiras': prateleiras,
                'niveis': niveis,
                'blocos': blocos
            }
            return True, f'Layout de "{nome_rua}" atualizado.'
        return False, 'Rua não encontrada.'
