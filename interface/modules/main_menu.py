from interface.core.terminal import Terminal
from interface.modules.cash.cash_menu import CashMenu
from interface.modules.inventory.inventory_menu import InventoryMenu


class MainMenu:
    def __init__(self):
        self._cash_menu = CashMenu()
        self._inventory_menu = InventoryMenu()

    def run(self) -> None:
        while True:
            Terminal.header("ERP - Biodigital", "Menu principal")
            Terminal.options(
                [
                    "Inventário",
                    "Caixa",
                    "Relatórios PDF",
                    "Sair",
                ]
            )
            Terminal.separator()

            user_choice = Terminal.ask_option("Escolha a opção desejada", range(1, 5))

            if user_choice == 1:
                self._inventory_menu.run()
            elif user_choice == 2:
                self._cash_menu.run()
            elif user_choice == 3:
                Terminal.warning("Relatórios PDF em desenvolvimento.")
                Terminal.pause()
            elif user_choice == 4:
                Terminal.success("Sistema encerrado.")
                break
