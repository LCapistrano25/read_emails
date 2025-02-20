import os
from imap_tools import AND, MailMessageFlags, MailBox
import mimetypes

class EmailReader:
    """Responsável por ler emails e salvar arquivos existentes"""
    def __init__(self, connection):
        self._connection = connection

    def box(self, criteria) -> MailBox:
        """Responsável por ler a caixa de email"""
        return self._connection.fetch(criteria)
    
    def mark_email_as_read(self, uid: list) -> None:
        """Responsável por marcar email como lido"""
        self._connection.flag(uid, MailMessageFlags.SEEN, value=True)

    def mark_email_as_unread(self, uid: list) -> None:
        """Responsável por marcar email como não lido"""
        self._connection.flag(uid, MailMessageFlags.SEEN, value=False)        
    
    def exist_folder(self, folder_name: str) -> bool:
        """Responsável por verificar se existe a pasta"""
        return self._connection.folder.exists(folder_name)
    
    def create_folder(self, standart: str, folder_name: str) -> None:
        """Responsável por criar a pasta"""
        self._connection.folder.set(standart)
        if not self.exist_folder(folder_name):
            self._connection.folder.create(folder_name)

    def move_email(self, uid: str, folder: str) -> None:
        """Responsável por mover email de pasta"""
        self._connection.move(uid, folder)

    def extract_attachments(self, inbox, temp, file_type=None) -> list:
        """Responsável por salvar os arquivos do email em uma pasta"""
        uids = []

        for email in inbox:
            for att in email.attachments:
                if file_type:
                    if mimetypes.guess_type(att.filename)[0] == file_type:
                        with open(fr"{temp}/{att.filename}", "wb") as f:
                            f.write(att.payload)
                        uids.append(email.uid)
        return list(set(uids))




