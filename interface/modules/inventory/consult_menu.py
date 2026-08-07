from interface.core.terminal import Terminal
from services.inventory.product_service import ProductService
from services.inventory.category_service import CategoryService
from typing import Any


class ConsultMenu:
    def __init__(self) -> None:
        self._product_service = ProductService()
        self._category_service = CategoryService()

    def run(self) -> None:
        while True:
            Terminal.header("Inventário", "Consultas")
            Terminal.options(
                [
                    "Listar produtos",
                    "Consultar categorias",
                    "Voltar",
                ]
            )
            Terminal.separator()

            option = Terminal.ask_option("Digite a opção desejada", range(1, 4))

            if option == 1:
                self._product_stock()
            elif option == 2:
                self._categories_list()
            elif option == 3:
                break

    def _product_stock(self) -> None:
        rows: list[list[Any]] = []
        products = self._product_service.list_products()

        for product in products:
            status = product.status.value if hasattr(product.status, "value") else product.status
            rows.append(
                [
                    product.name.title(),
                    product.category.name.capitalize(),
                    product.stock_quantity,
                    Terminal.money(product.sale_value),
                    status,
                ]
            )

        Terminal.header("Produtos cadastrados", "Inventário")
        Terminal.table(
            ["Produto", "Categoria", "Estoque", "Venda", "Status"],
            rows,
        )
        print()
        Terminal.pause()
            

    def _categories_list(self):
        categories = self._category_service.list_category()
        rows: list[list[Any]] = []
        
        for category in categories:
                    rows.append(
                        [
                            category.id,
                            category.name.title()
                        ]
                    )
        
        Terminal.header('Categorias cadastradas', 'Inventário')
        Terminal.table(
            ["ID", "Nome"],
            rows
        )
        print()
        Terminal.pause()
        