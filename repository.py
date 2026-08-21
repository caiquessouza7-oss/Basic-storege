import sqlite3
from models import Produto

class ProdutoRepository:
    '''lidar com o banco de dados'''
    def __init__(self, db_name='estoque.db'):
        self.db_name = db_name
        self._criar_tabela_vazia()

    def _conectar(self):
        return sqlite3.connect(self.db_name)

    def _criar_tabela_vazia(self):
        with self._conectar() as conn:
            conn.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
            codigo TEXT PRIMARY KEY, 
            descricao TEXT, 
            localizacao TEXT,
            quantidade INTEGER
            )
            ''')

    def salvar(self, produto):
        with self._conectar() as conn:
            conn.execute('''
            INSERT INTO produtos (codigo, descricao, localizacao, quantidade)
            VALUES(?, ?, ?, ?)
            ''', (produto.codigo, produto.descricao, produto.localizacao, produto.quantidade))

    def deletar (self, codigo):
        with self._conectar() as conn:
            conn.execute('DELETE FROM produtos WHERE codigo = ?', (codigo,))

    def atualizar_quantidade(self, codigo, nova_quantidade):
        with self._conectar() as conn:
            conn.execute('UPDATE produtos SET quantidade = ? WHERE codigo = ?', (nova_quantidade, codigo))

    def buscar_por_codigo(self, codigo):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT codigo, descricao, localizacao, quantidade FROM produtos WHERE codigo =?',  (codigo,))
            row = cursor.fetchone()
            if row:
                from models import Produto
                return Produto(codigo=row[0], descricao=row[1], localizacao=row[2], quantidade=row[3])
            return None

    def listar_toods(self):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.exxecute('SELECT codigo, descricao, localizacao, quantidade FROM produtos')
            rows = cursor.fetchall()
            return [Produto(codigo=r[0], deszcricao=r[1], localizacao=r[2], quantidade=r[3]) for r in rows]