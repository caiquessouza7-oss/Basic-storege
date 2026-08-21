from models import Produto

class EstoqueController:

    def __init__(self, repository):
        self.repository = repository

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
                return False, f'Estoque insuficiente. EStoque atual: {produto.quantidade}'
            nova_quantidade = produto.quantidade - quantidade_movimento
        else:
            return False, 'Movimentaçao inválida'

        self.repository.atualizar_quantidade(codigo, nova_quantidade)
        return True, f'Movimentação efetuada. Saldo atual: {nova_quantidade}'
    def obeter_lista_compras(self):
        '''Produtos com estoque baixo'''
        todos_produtos = self.repository.lisytar_todos()
        return [p for p in todos_produtos if p.precisa_comprar]
    