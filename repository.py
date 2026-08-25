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
            quantidade INTEGER,
            foto_path TEXT
            )
            ''')

    def salvar(self, produto):
        with self._conectar() as conn:
            conn.execute('''
            INSERT INTO produtos (codigo, descricao, localizacao, quantidade, foto_path)
            VALUES(?, ?, ?, ?, ?)
            ''', (produto.codigo, produto.descricao, produto.localizacao, produto.quantidade, produto.foto_path))

    def deletar (self, codigo):
        with self._conectar() as conn:
            conn.execute('DELETE FROM produtos WHERE codigo = ?', (codigo,))

    def atualizar_quantidade(self, codigo, nova_quantidade):
        with self._conectar() as conn:
            conn.execute('UPDATE produtos SET quantidade = ? WHERE codigo = ?', (nova_quantidade, codigo))

    def atualizar_produto_completo(self, produto):
        with self._conectar() as conn:
            conn.execute('''
            UPDATE produtos 
            SET descricao = ?, localizacao = ?, quantidade = ?, foto_path = ?
            WHERE codigo = ?
            ''', (produto.descricao, produto.localizacao, produto.quantidade, produto.foto_path, produto.codigo))

    def buscar_por_codigo(self, codigo):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT codigo, descricao, localizacao, quantidade, foto_path FROM produtos WHERE codigo =?',  (codigo,))
            row = cursor.fetchone()
            if row:
                from models import Produto
                return Produto(codigo=row[0], descricao=row[1], localizacao=row[2], quantidade=row[3], foto_path=row[4] if len (row) > 4 else '')
            return None

    def listar_todos(self):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT codigo, descricao, localizacao, quantidade, foto_path FROM produtos')
            rows = cursor.fetchall()
            return [Produto(codigo=r[0], descricao=r[1], localizacao=r[2], quantidade=r[3], foto_path=r[4]) for r in rows]

    def localizar_produto_geral(self, termo):
        with self._conectar() as conn:
            cursor = conn.cursor()
            query = '''
                SELECT codigo, descricao, localizacao, quantidade, foto_path
                FROM produtos
                WHERE codigo LIKE ? OR descricao LIKE ? OR localizacao LIKE ?
                '''
            termo_busca = f'%{termo}%'
            cursor.execute(query, (termo_busca, termo_busca, termo_busca))
            rows = cursor.fetchall()

            from models import Produto
            return [Produto(codigo=r[0], descricao=r[1], localizacao=r[2], quantidade=r[3], foto_path=r[4]) for r in rows]
        
