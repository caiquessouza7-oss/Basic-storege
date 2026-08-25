import sys
from PyQt6.QtWidgets import QApplication
from repository import ProdutoRepository
from controllers import EstoqueController
from views import MapaEstoque

if __name__ == '__main__':
    repo = ProdutoRepository('estoque.db')
    controller = EstoqueController(repo)

    controller.registrar_novo_produto('99061501', 'EMBOLO ALUMINIO 30MM', 'R1.P1.N1', 7, '')
    controller.registrar_novo_produto('99061502', 'EMBOLO ALUMINIO 30MM', 'R1.P1.N1', 3, '')
    controller.registrar_novo_produto('99061503', 'EMBOLO ALUMINIO 30MM', 'R1.P1.N1', 0, '')

    app = QApplication(sys.argv)
    view = MapaEstoque(controller)
    view.show()
    sys.exit(app.exec())
