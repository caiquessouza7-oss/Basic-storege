from dataclasses import dataclass

@dataclass
class Produto:
    codigo: str
    descricao: str
    localizacao: str
    quantidade: int

    @property
    def precisa_comprar(self) -> bool:
        '''Define que o item precisa ser comprado se o estoque for 5 ou menos por hora
        ja que cada item deve ter uma classificacao especifica'''
        return self.quantidade <= 5

    @property
    def status_cor(self) -> str:
        '''Retorna uma cor baseada na quantidade de estoque'''
        if self.quantidade == 0:
            return '#FFCCCC'
        elif self.quantidade <= 5:
            return '#FFF5CC'
        return '#CCFFCC'
@dataclass
class LayoutEstoque:
    '''Estrutura do estoque'''
    ruas: int = 4
    prateleiras: int = 17
    niveis: int = 5
    blocos: int = 6
