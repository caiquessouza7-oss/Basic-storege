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

        todos_produtos = self.repositpory.listar_todos()

        resultados = [
            produto for produto in todos_produtos
            if termo in str(produto.codigo).lower()
            or termo in str(produto.descricao).lower()
            or termo in str(produto.localizacao).lower()
        ]

        return resultados

    def registrar_novo_produto(self, codigo, descricao, localizacao, quantidade):
        if self.repository.buscar_por_codigo(codigo):
            return False, f'Produto com o codigo {codigo} já existe.'

        novo_produto = Produto(codigo, descricao, localizacao, quantidade)
        self.repository.salvar(novo_produto)
        return True, 'Produto cadastrado com sucesso'

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

    def atualizar_layout_estoque(self, ruas, pratelerias, niveis, blocos):
        '''Atualizar as configuracoes do estoque'''
        self.layout.ruas = ruas
        self.layout.prateleiras = pratelerias
        self.layout.niveis = niveis
        self.layout.blocos = blocos
        return True, 'Layout do estoque atualizado'
