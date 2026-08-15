from interface.core.terminal import Terminal
from services.inventory.product_service import ProductService
from domain.enums.status import Status
from typing import Any

class EditMenu:

    def __init__(self):
        self._product_service = ProductService()
        self._status = Status

    def run(self) -> None:
        while True:
            Terminal.header("Inventário", "Edições de produto")
            Terminal.options(
                [
                    "Alterar nome",
                    "Alterar valor de venda",
                    "Alterar preço de custo",
                    "Alterar status",
                    "Alterar categoria",
                    "Voltar",
                ]
            )
            Terminal.separator()

            option = Terminal.ask_option(
                "Digite a opção desejada", range(1, 7))

            if option == 1:
                self.change_product_name()
            elif option == 2:
                self.change_sale_value()
            elif option == 3:
                self.change_cost_price()
            elif option == 4:
                self.change_product_status()
            elif option == 5:
                Terminal.error('Função em desenvolvimento')
                Terminal.pause()
            elif option == 6:
                break

    def change_product_name(self):
        
        Terminal.clear()
        products = self._product_service.list_products()
        rows = []
        chose_product = None
        chose_product_id = None
        new_name = None
        exib_name = None
    
        if products:
            while True:
                products = self._product_service.list_products()
                rows: list[list[Any]] = []
                Terminal.header("Área de Edição", "Alterar Nome de Produto")
    
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

                Terminal.header("Produtos cadastrados", "Inventário")
                Terminal.table(
                    ["ID", "Produto", "Categoria", "Estoque", "Preço de Custo","Valor de Venda", "Status"],
                    rows,
                )

                Terminal.separator()

                if chose_product is not None:
                    Terminal.field(1, 'Produto', chose_product.name.title())
                else:
                    Terminal.field(1, 'Produto', 'Não selecionado')

                if new_name is not None:
                    Terminal.field(2, 'Novo Nome', exib_name)
                else:
                    Terminal.field(2, 'Novo Nome', 'Não selecionado')
                Terminal.option(3, 'Confirmar')
                Terminal.option(4, 'Cancelar')

                Terminal.separator()

                user_choice = Terminal.ask_option(
                    "Escolha a opção desejada", range(1, 5))

                if user_choice == 1:
                    chose_product_id = Terminal.ask_int('Selecione o Produto')
                    chose_product = products[chose_product_id - 1]
                    Terminal.success('Produto selecionado com sucesso')
                    Terminal.clear()

                elif user_choice == 2:
                    if chose_product is not None:
                        new_name = Terminal.ask(
                            'Digite o novo nome do produto')
                        exib_name = new_name
                    else:
                        Terminal.error('Nenhum produto selecionado')
                        print('')
                        Terminal.pause()

                elif user_choice == 3:
                    if chose_product and chose_product.id is not None and new_name is not None:
                        chose_product.change_name(new_name)
                        self._product_service.save_information(
                            chose_product, chose_product.id)
                        Terminal.success('Nome alterado com sucesso.')
                        print('')
                        Terminal.pause()
                        break
                    else:
                        Terminal.error(
                            'Necessário selecionar um produto ou adicionar uma quantidade maior que 0.')
                        Terminal.pause()

                elif user_choice == 4:
                    break
        else:
            Terminal.header("Área de Edição", "Alterar Nome do Produto")
            print('Nenhum produto cadastrado.')
            print()
            Terminal.pause()

    def change_sale_value(self):

        Terminal.clear()
        products = self._product_service.list_products()
        rows = []
        chose_product = None
        chose_product_id = None
        new_sale_value = None

        if products:
            while True:
                products = self._product_service.list_products()
                Terminal.header("Área de Edição", "Alterar Valor de Venda")
                rows: list[list[Any]] = []
                for c, product in enumerate(products, start=1):
                    status = product.status.value if hasattr(
                        product.status, "value") else product.status
                    rows.append(
                        [
                            c,
                            product.name.title(),
                            product.category.name.capitalize(),
                            product.stock_quantity,
                            Terminal.money(product.cost_price),
                            Terminal.money(product.sale_value),
                            status,
                        ]
                    )

                Terminal.header("Produtos cadastrados", "Inventário")
                Terminal.table(
                    ["ID", "Produto", "Categoria", "Estoque", "Preço de Custo","Valor de Venda", "Status"],
                    rows,
                )

                Terminal.separator()

                if chose_product is not None:
                    Terminal.field(1, 'Produto', chose_product.name.title())
                else:
                    Terminal.field(1, 'Produto', 'Não selecionado')

                if new_sale_value is not None:
                    Terminal.field(2, 'Novo Valor de Venda', new_sale_value)
                else:
                    Terminal.field(2, 'Novo Valor de Venda', 'Não Informado')
                Terminal.option(3, 'Confirmar')
                Terminal.option(4, 'Cancelar')

                Terminal.separator()

                user_choice = Terminal.ask_option(
                    "Escolha a opção desejada", range(1, 5))

                if user_choice == 1:
                    chose_product_id = Terminal.ask_int('Selecione o Produto')
                    chose_product = products[chose_product_id - 1]
                    Terminal.success('Produto selecionado com sucesso')
                    Terminal.clear()

                elif user_choice == 2:
                    if chose_product is not None:
                        new_sale_value = Terminal.ask_decimal(
                            'Digite o novo valor de venda do produto')

                    else:
                        Terminal.error('Nenhum produto selecionado')
                        print('')
                        Terminal.pause()

                elif user_choice == 3:
                    if chose_product and chose_product.id is not None and new_sale_value is not None:
                        chose_product.change_sale_value(new_sale_value)
                        self._product_service.save_information(
                            chose_product, chose_product.id)
                        Terminal.success('Valor de venda alterado com sucesso.')
                        print('')
                        Terminal.pause()
                        break
                    else:
                        Terminal.error(
                            'Necessário selecionar um produto ou adicionar uma quantidade maior que 0.')
                        Terminal.pause()

                elif user_choice == 4:
                    break
        else:
            Terminal.header("Área de Edição", "Alterar Valor de Venda")
            print('Nenhum produto cadastrado.')
            print()
            Terminal.pause()

    def change_cost_price(self):

        Terminal.clear()
        products = self._product_service.list_products()
        rows = []
        chose_product = None
        chose_product_id = None
        new_cost_price = None

        if products:
            while True:
                products = self._product_service.list_products()
                Terminal.header("Área de Edição", "Alterar Preço de Custo")
                rows: list[list[Any]] = []
                for c, product in enumerate(products, start=1):
                    status = product.status.value if hasattr(
                        product.status, "value") else product.status
                    rows.append(
                        [
                            c,
                            product.name.title(),
                            product.category.name.capitalize(),
                            product.stock_quantity,
                            Terminal.money(product.cost_price),
                            Terminal.money(product.sale_value),
                            status,
                        ]
                    )

                Terminal.header("Produtos cadastrados", "Inventário")
                Terminal.table(
                    ["ID", "Produto", "Categoria", "Estoque", "Preço de Custo","Valor de Venda", "Status"],
                    rows,
                )

                Terminal.separator()

                if chose_product is not None:
                    Terminal.field(1, 'Produto', chose_product.name.title())
                else:
                    Terminal.field(1, 'Produto', 'Não selecionado')

                if new_cost_price is not None:
                    Terminal.field(2, 'Novo Preço de Custo', new_cost_price)
                else:
                    Terminal.field(2, 'Novo Preço de Custo', 'Não Informado')
                Terminal.option(3, 'Confirmar')
                Terminal.option(4, 'Cancelar')

                Terminal.separator()

                user_choice = Terminal.ask_option(
                    "Escolha a opção desejada", range(1, 5))

                if user_choice == 1:
                    chose_product_id = Terminal.ask_int('Selecione o Produto')
                    chose_product = products[chose_product_id - 1]
                    Terminal.success('Produto selecionado com sucesso')
                    Terminal.clear()

                elif user_choice == 2:
                    if chose_product is not None:
                        new_cost_price = Terminal.ask_decimal(
                            'Digite o novo preço de custo do produto')

                    else:
                        Terminal.error('Nenhum produto selecionado')
                        print('')
                        Terminal.pause()

                elif user_choice == 3:
                    if chose_product and chose_product.id is not None and new_cost_price is not None:
                        chose_product.change_cost_price(new_cost_price)
                        self._product_service.save_information(
                            chose_product, chose_product.id)
                        Terminal.success('Preço de custo alterado com sucesso')
                        print('')
                        Terminal.pause()
                        break
                    else:
                        Terminal.error(
                            'Digite um valor válido.')
                        Terminal.pause()
                        break

                elif user_choice == 4:
                    break
        else:
            Terminal.header("Área de Edição", "Alterar Preço de Custo")
            print('Nenhum produto cadastrado.')
            print()
            Terminal.pause()

    def change_product_status(self):

        Terminal.clear()
        products = self._product_service.list_products()
        rows = []
        chose_product = None
        chose_product_id = None
        new_product_status = None

        if products:
            while True:
                products = self._product_service.list_products()
                Terminal.header("Área de Edição", "Alterar Status")
                rows: list[list[Any]] = []
                for c, product in enumerate(products, start=1):
                    status = product.status.value if hasattr(
                        product.status, "value") else product.status
                    rows.append(
                        [
                            c,
                            product.name.title(),
                            product.category.name.capitalize(),
                            product.stock_quantity,
                            Terminal.money(product.cost_price),
                            Terminal.money(product.sale_value),
                            status,
                        ]
                    )

                Terminal.header("Produtos cadastrados", "Inventário")
                Terminal.table(
                    ["ID", "Produto", "Categoria", "Estoque", "Preço de Custo","Valor de Venda", "Status"],
                    rows,
                )

                Terminal.separator()

                if chose_product is not None:
                    Terminal.field(1, 'Produto', chose_product.name.title())
                else:
                    Terminal.field(1, 'Produto', 'Não selecionado')

                if new_product_status is not None:
                    Terminal.field(2, 'Novo Status do Produto', (new_product_status.name))
                else:
                    Terminal.field(2, 'Novo Status do Produto', 'Não Informado')
                Terminal.option(3, 'Confirmar')
                Terminal.option(4, 'Cancelar')

                Terminal.separator()

                user_choice = Terminal.ask_option(
                    "Escolha a opção desejada", range(1, 5))

                if user_choice == 1:
                    chose_product_id = Terminal.ask_int('Selecione o Produto')
                    chose_product = products[chose_product_id - 1]
                    Terminal.success('Produto selecionado com sucesso')
                    Terminal.clear()

                elif user_choice == 2:
                    if chose_product is not None:
                        Terminal.field(1, 'Ativo', (self._status.ACTIVE.name))
                        Terminal.field(2, 'Inativo', (self._status.INACTIVE.name))
                        Terminal.field(3, 'Descontinuado', (self._status.DISCONTINUED.name))
                        Terminal.field(4, 'Saber mais', '-')
                        user_status_choice = Terminal.ask_option(
                                            "Escolha a opção desejada", range(1, 5))
                        if user_status_choice == 1:
                            new_product_status = self._status.ACTIVE
                        elif user_status_choice == 2:
                            new_product_status = self._status.INACTIVE
                        elif user_status_choice == 3:
                            new_product_status = self._status.DISCONTINUED
                        elif user_status_choice == 4:
                            Terminal.clear()
                            Terminal.separator()
                            Terminal.field(1, 'Ativo', "Um produto ativo pode receber entrada no estoque e ser vendido")
                            Terminal.field(2, 'Inativo', "Um produto inativo não pode receber entrada no estoque nem ser vendido")
                            Terminal.field(3, 'Ativo', "Um produto descontinuado não pode receber entrada mas pode ser vendido")
                            Terminal.separator()
                            Terminal.pause()
                            continue
                            
                        else:
                            print('Escolha um valor válido. (1 - 4)') 
                            
                    else:
                        Terminal.error('Nenhum produto selecionado')
                        print('')
                        Terminal.pause()

                elif user_choice == 3:
                    if chose_product and chose_product.id is not None and new_product_status is not None:
                        chose_product.change_status(new_product_status)
                        self._product_service.save_information(
                            chose_product, chose_product.id)
                        Terminal.success('Status alterado com sucesso.')
                        print('')
                        Terminal.pause()
                        break
        else:
            Terminal.header("Inventário", "Entrada de Produto")
            print('Nenhum produto cadastrado.')
            print()
            Terminal.pause()