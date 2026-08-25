from dataclasses import dataclass

@dataclass
class Produto:
    codigo: str
    descricao: str
    localizacao: str
    quantidade: int
    foto_path: str =""

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
    configs_ruas: dict = None

    @classmethod
    def inicializar_layout(cls):
        '''Layout inicial'''
        if cls.configs_ruas is None:
            cls.configs_ruas = {
               f'Rua {i}' : {'prateleiras': 17, 'niveis': 5, 'blocos': 6} for i in range(4)
            }
    @classmethod
    def obter_config(cls, num_rua: int):
        cls.inicializar_layout()
        return cls.configs_ruas.get(num_rua, {'prateleiras': 0, 'niveis': 0, 'blocos':0 })
    
    @classmethod
    def adicionar_rua(cls, num_rua: int):
        cls.inicializar_layout()
        if num_rua not in cls.configs_ruas:
            cls.configs_ruas[num_rua] = {'prateleiras': 17, 'niveis': 5, 'blocos': 6}
            return True
        return False

    @classmethod
    def remover_rua(cls, num_rua: int):
        cls.inicializar_layout()
        if num_rua in cls.configs_ruas:
            del cls.configs_ruas[num_rua]
            return True
        return False
    

  
