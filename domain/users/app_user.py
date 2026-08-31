class AppUser:
    '''Classe responsável por representar um usuário no sistema.'''
    def __init__(self,
                 name: str,
                 email: str,
                 password: str,
                 admin: bool,
                 id: int | None = None
                ):
                 
        self._id = id
        self._name = name
        self._email = email
        self._password = password
        self._admin = admin
        
    @property
    def id(self) -> int | None:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def password(self) -> str:
        return self._password
    
    @property
    def admin(self) -> bool:
        return self._admin