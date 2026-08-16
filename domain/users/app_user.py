# internal's imports
from domain.enums.user_roles import Roles

class AppUser:
    '''Classe responsável por representar um usuário no sistema.'''
    def __init__(self,
                 id: int,
                 name: str,
                 login: str,
                 password_hash: str,
                 role: Roles):
                 
        self.id = id
        self.name = name
        self.login = login
        self.password_hash = password_hash
        self.role = role