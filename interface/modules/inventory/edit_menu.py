from interface.core.terminal import Terminal
from services.inventory.product_service import ProductService
from typing import Any

class EditMenu:
    
    def __init__(self):
        self._product_service = ProductService()
    
    def run(self) -> None:
        while True:
            Terminal.header("Inventário", "Edições de produto")
            Terminal.options(
                [
                    "Mudar nome",
                    "Mudar valor de venda",
                    "Mudar preço de custo",
                    "Mudar status",
                    "Mudar categoria",
                    "Voltar",
                ]
            )
            Terminal.separator()

            option = Terminal.ask_option("Digite a opção desejada", range(1, 7))

            if option == 1:
                self.change_product_name()
            elif option == 2:
                self.change_sale_value()
            elif option == 3:
                Terminal.error('Função em desenvolvimento')
                Terminal.pause()
            elif option == 4:
                Terminal.error('Função em desenvolvimento')
                Terminal.pause()
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
    
                    user_choice = Terminal.ask_option("Escolha a opção desejada", range(1, 5))
    
                    if user_choice == 1:
                        chose_product_id = Terminal.ask_int('Selecione o Produto')
                        chose_product = products[chose_product_id - 1]
                        Terminal.success('Produto selecionado com sucesso')
                        Terminal.clear()
    
                    elif user_choice == 2:
                        if chose_product is not None:
                            new_name = Terminal.ask('Digite o novo nome do produto')
                            exib_name = new_name
                        else:
                            Terminal.error('Nenhum produto selecionado')
                            print('')
                            Terminal.pause()
    
                    elif user_choice == 3:
                        if chose_product and chose_product.id is not None and new_name is not None:
                            chose_product.change_name(new_name)
                            self._product_service.save_information(chose_product, chose_product.id)
                            Terminal.success('Nome alterado com sucesso.')
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
                    Terminal.header("Área de Edição", "Alterar Preço de Venda")
                    rows: list[list[Any]] = []
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
    
                    if new_sale_value is not None:
                        Terminal.field(2, 'Novo Preço de Venda', new_sale_value)
                    else:
                        Terminal.field(2, 'Novo Preço de Venda', 'Não Informado')
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
                            new_sale_value = Terminal.ask_decimal('Digite o novo preço de venda do produto')
                            
                        else:
                            Terminal.error('Nenhum produto selecionado')
                            print('')
                            Terminal.pause()
    
                    elif user_choice == 3:
                        if chose_product and chose_product.id is not None and new_sale_value is not None:
                            chose_product.change_sale_value(new_sale_value)
                            self._product_service.save_information(chose_product, chose_product.id)
                            Terminal.success('Nome alterado com sucesso.')
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