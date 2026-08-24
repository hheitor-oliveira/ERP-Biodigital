class AppUser:
    '''Classe responsável por representar um usuário no sistema.'''
    def __init__(self,
                 id: int,
                 name: str,
                 email: str,
                 password: str,
                 
                ):
                 
        self._id = id
        self._name = name
        self._email = email
        self._password = password