# internal's imports
from interface.core.terminal import Terminal
from services.inventory.product_service import ProductService
from typing import Any


class MovementMenu:

    def __init__(self) -> None:
        self._product_service = ProductService()

    def run(self) -> None:
        while True:
            Terminal.header("Inventário", "Entrada/Saída")
            Terminal.options(
                [
                    "Entrada produto",
                    "Saída produto",
                    "Voltar",
                ]
            )
            Terminal.separator()

            option = Terminal.ask_option("Digite a opção desejada", range(1, 4))

            if option == 1:
                self._product_entry()
            elif option == 2:
                self._product_exit()
            elif option == 3:
                break

    def _product_entry(self) -> None:
        Terminal.clear()
        products = self._product_service.list_products()
        rows = []
        chose_product = None
        chose_product_id = None
        entry_quantity = None

        if products:
            while True:
                products = self._product_service.list_products()
                rows: list[list[Any]] = []
                Terminal.header("Inventário", "Entrada de Produto")

                for c, product in enumerate(products, start=1):
                    status = product.status.value if hasattr(product.status, "value") else product.status
                    rows.append(
                        [
                            c,
                            product.name.title(),
                            product.category.name.capitalize(),
                            product.stock_quantity,
                            Terminal.money(product.sale_value),
                            status,
                        ]
                    )

                Terminal.header("Produtos cadastrados", "Inventário")
                Terminal.table(
                    ["ID", "Produto", "Categoria", "Estoque", "Venda", "Status"],
                    rows,
                )

                Terminal.separator()

                if chose_product is not None:
                    Terminal.field(1, 'Produto', chose_product.name.title())
                else:
                    Terminal.field(1, 'Produto', 'Não selecionado')

                if entry_quantity is not None:
                    Terminal.field(2, 'Qtd. Entrada', entry_quantity)
                else:
                    Terminal.field(2, 'Qtd. Entrada', 'Não selecionado')
                Terminal.option(3, 'Confirmar')
                Terminal.option(4, 'Cancelar')

                Terminal.separator()

                user_choice = Terminal.ask_option("Escolha a opção desejada", range(1, 5))

                if user_choice == 1:
                    chose_product_id = Terminal.ask_int('Selecione o Produto')
                    chose_product = products[chose_product_id - 1]
                    Terminal.success('Produto selecionado com sucesso')
                    Terminal.clear()

                elif user_choice == 2:
                    if chose_product is not None:
                        entry_quantity = Terminal.ask_int('Digite a quantidade desejada')
                        chose_product.add_stock(entry_quantity)
                    else:
                        Terminal.error('Nenhum produto selecionado')
                        print('')
                        Terminal.pause()

                elif user_choice == 3:
                    if chose_product and chose_product.id is not None and entry_quantity is not None and entry_quantity > 0:
                        self._product_service.save_information(chose_product, chose_product.id)
                        Terminal.success('Movimentação de entrada realizada com sucesso!')
                        print('')
                        Terminal.pause()
                        break
                    else:
                        Terminal.error('Necessário selecionar um produto ou adicionar uma quantidade maior que 0.')
                        Terminal.pause()

                elif user_choice == 4:
                    break
        else:
            Terminal.header("Inventário", "Entrada de Produto")
            print('Nenhum produto cadastrado.')
            print()
            Terminal.pause()
            
    def _product_exit(self) -> None:
            Terminal.clear()
            products = self._product_service.list_products()
            rows = []
            chose_product = None
            chose_product_id = None
            exit_quantity = None
    
            if products:
                while True:
                    products = self._product_service.list_products()
                    rows: list[list[Any]] = []
                    Terminal.header("Inventário", "Saída Manual de Produto")
    
                    for c, product in enumerate(products, start=1):
                        status = product.status.value if hasattr(product.status, "value") else product.status
                        rows.append(
                            [
                                c,
                                product.name.title(),
                                product.category.name.capitalize(),
                                product.stock_quantity,
                                Terminal.money(product.sale_value),
                                status,
                            ]
                        )
    
                    Terminal.header("Produtos cadastrados", "Inventário")
                    Terminal.table(
                        ["ID", "Produto", "Categoria", "Estoque", "Venda", "Status"],
                        rows,
                    )
    
                    Terminal.separator()
    
                    if chose_product is not None:
                        Terminal.field(1, 'Produto', chose_product.name.title())
                    else:
                        Terminal.field(1, 'Produto', 'Não selecionado')
    
                    if exit_quantity is not None:
                        Terminal.field(2, 'Qtd. Saída', exit_quantity)
                    else:
                        Terminal.field(2, 'Qtd. Saída', 'Não selecionado')
                    Terminal.option(3, 'Confirmar')
                    Terminal.option(4, 'Cancelar')
    
                    Terminal.separator()
    
                    user_choice = Terminal.ask_option("Escolha a opção desejada", range(1, 5))
    
                    if user_choice == 1:
                        chose_product_id = Terminal.ask_int('Selecione o Produto')
                        chose_product = products[chose_product_id - 1]
                        Terminal.success('Produto selecionado com sucesso')
                        Terminal.clear()
    
                    elif user_choice == 2:
                        if chose_product is not None:
                            exit_quantity = Terminal.ask_int('Digite a quantidade desejada')
                            chose_product.remove_stock(exit_quantity)
                        else:
                            Terminal.error('Nenhum produto selecionado')
                            print('')
                            Terminal.pause()
    
                    elif user_choice == 3:
                        if chose_product and chose_product.id is not None and exit_quantity is not None and exit_quantity > 0:
                            self._product_service.save_information(chose_product, chose_product.id)
                            Terminal.success('Movimentação de saída realizada com sucesso!')
                            print('')
                            Terminal.pause()
                            break
                        else:
                            Terminal.error('Necessário selecionar um produto ou adicionar uma quantidade maior que 0.')
                            Terminal.pause()
    
                    elif user_choice == 4:
                        break
            else:
                Terminal.header("Inventário", "Entrada de Produto")
                print('Nenhum produto cadastrado.')
                print()
                Terminal.pause()
