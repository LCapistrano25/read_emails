from imap_tools import MailBox

class Connection:
    """Responsável por realizar a conexão com o email"""
    def __init__(self, imap_server, email, password, initial_folder="INBOX"):
        self._imap_server = imap_server
        self._email = email
        self._password = password
        self._initial_folder = initial_folder

    def perform_connection(self):
        """Responsável por realizar o login"""
        try:
            return MailBox(self._imap_server).login(self._email, self._password, self._initial_folder)
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            return None
        
    def get_imap_server(self):
        """Responsável por retornar o IMAP"""
        return self._imap_server
    
    def get_email(self):
        """Responsável por retornar o email"""
        return self._email
    
    def get_password(self):
        """responsável por retornar a senha"""
        return self._password
    
    def get_initial_folder(self):
        """Responsável por retornar a pasta principal do email"""
        return self._initial_folder
    
