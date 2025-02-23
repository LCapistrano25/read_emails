# Bibliotecas padrão
import os

# Bibliotecas de terceiros
from decouple import config

# Módulos internos de conexão e processamento de dados
from connection import Connection
from email_reader import EmailReader
from pdf_processor import PdfProcessor
from xml_processor import XmlProcessor
from file_manager import FileManager
from utils import generate_file_hash, turn_date_into_list

# Constantes e parâmetros de configuração
from parameter_words import (
    DATE, PARAM_DATE, FINAL_FOLDER, UNSAVED, TEMPORARY_FOLDER, MONTH, SEEN, BOX, BRANCHES, 
    STANDART_FOLDER, PARAM_CNPJ, CNPJ
)

IMAP_SERVER = config("IMAP_SERVER")
EMAIL = config("EMAIL")
SENHA = config("SENHA")

class EmailProcessor:
    def __init__(self, imap, email, password, folder="INBOX"):
        self._connection = Connection(imap, email, password, initial_folder=folder)
        self._inbox = EmailReader(self._connection.perform_connection())
        self._file_manager = FileManager
        self._pdf_processor = PdfProcessor
        self._xml_processor = XmlProcessor

    def search_for_emails(self, criteria="ALL"):
        """Responsável pela consulta na caixa de email"""
        try:
            return self._inbox.box(criteria=criteria)
        except Exception as e:
            print(f"Ocorreu um erro em ler os emails: {e}.")

    def extract_files(self, inbox, temp, file_type="application/pdf") -> None:
        """Responsável por baixar e salvar tipos de arquivos em uma pasta"""
        try:
            return self._inbox.extract_attachments(inbox, temp, file_type=file_type)
        except Exception as e:
            print(f"Ocorreu um erro ao salvar os arquivos: {e}")
    
    def create_directories(self, folders: dict, standart: str, temp: str, unsaved: str, final: str) -> str:
        """Responsável por criar os diretórios principais"""
        new_temp_standart = self._file_manager().create_path_to_folder(standart, temp)
        self._file_manager().create_directory(new_temp_standart)

        new_unsaved_standart = self._file_manager().create_path_to_folder(standart, unsaved)
        self._file_manager().create_directory(new_unsaved_standart)

        for _, folder in folders.items():
            new_unsaved = self._file_manager().create_path_to_folder(standart, folder, unsaved)
            new_final = self._file_manager().create_path_to_folder(standart, folder, final)
            self._file_manager().create_directory(new_unsaved)
            self._file_manager().create_directory(new_final)

        return new_temp_standart, new_unsaved_standart

    def redirect_unassigned_files(self, temp_file_path, unsaved: str, archive) -> None:
        """Responsável por dar um destino correto a arquivos sem pasta"""
        unsaved_path = self._file_manager().create_path_to_folder(unsaved, archive)
        if os.path.exists(unsaved_path):
            self._file_manager().remove_file(temp_file_path)
        else:
            self._file_manager().move_file(temp_file_path, unsaved_path)

    def clean_temporary_folder(self, general_temporary_folder: str) -> None:
        """Responsável por limpar a pasta temporária"""
        for archive in os.listdir(general_temporary_folder):    
            path = self._file_manager().create_path_to_folder(general_temporary_folder, archive)
            if not self._file_manager().exist_directory(path):
                self._file_manager().remove_file(path)

    def process_pdf(self, archive, standart_folder: str, general_temp_folder: str, unsaved_folder: str, final_folder: str):
        """Responsável por identificar os padrões nos pdfs e destinar ao local correto"""
        file_path = self._file_manager().create_path_to_folder(general_temp_folder, archive)
        pdf = self._pdf_processor(file_path)
        text = pdf.process_pdf()

        general_unsaved_folder = self._file_manager().create_path_to_folder(standart_folder, unsaved_folder)

        identifier_company = (pdf.word_search(PARAM_CNPJ, CNPJ))
        identifier_company = pdf.remove_space(identifier_company)

        if identifier_company:
            # Encontrou filial
            folder = BRANCHES.get(identifier_company, None) # Busca o nome da pasta
            if folder:
                date = pdf.word_search(PARAM_DATE, DATE) 
                branch_unsaved_folder = self._file_manager().create_path_to_folder(
                        standart_folder, folder, unsaved_folder)   
                # Encontrou o nome da pasta
                if date:
                    date = date.replace('/', '-').replace(':', '-')
                    date_list_reversed = turn_date_into_list(date)
                    
                    destinatary = self._file_manager().create_path_to_folder(
                        standart_folder, folder, final_folder, 
                        date_list_reversed[0], 
                        MONTH[date_list_reversed[1]], 
                        date_list_reversed[2]
                    )

                    hash_name = generate_file_hash(archive)
                    directory = self._file_manager().create_directory(destinatary)
                    new_file_path = self._file_manager().save_file(directory, f"{date} - {hash_name}.pdf")

                    try:
                        if not self._file_manager().exist_directory(new_file_path):
                            self._file_manager().move_file(file_path, new_file_path)
                        else:
                            self._file_manager().remove_file(file_path)
                    except PermissionError as e:
                        print(f"Erro ao renomear o arquivo: {e}")
                    except OSError as e:
                        print(f"Erro ao renomear o arquivo (OSError): {e}")
                else:
                    # Manda para pasta de INDEFINIDOS DA FILIAL
                    self.redirect_unassigned_files(file_path, branch_unsaved_folder, archive)
            else:
                # Manda para pasta de INDEFINIDOS GERAL
                self.redirect_unassigned_files(file_path, general_unsaved_folder, archive)
        else:
            # Manda para pasra de INDEFINIDOS GERAL
            self.redirect_unassigned_files(file_path, general_unsaved_folder, archive)

    def process_files(self, folders: dict, standart: str, temp: str, unsaved: str, final: str):
        """Responsável por salvar os arquivos nas pastas corretas"""        
        general_temporary_folder, _ = self.create_directories(folders, standart, temp, unsaved, final)
        
        inbox = self.search_for_emails()
        uids = self.extract_files(inbox, general_temporary_folder)

        for archive in os.listdir(general_temporary_folder):            
            extension = self._file_manager().extract_extension(archive).lower()
            if extension == '.pdf':
                self.process_pdf(archive, standart, general_temporary_folder, unsaved, final)             
            elif extension == '.xml':
                pass

        folder = SEEN
        self._inbox.mark_email_as_read(uids)
        self._inbox.create_folder(BOX, folder)
        self._inbox.move_email(uids, folder)
        self.clean_temporary_folder(general_temporary_folder)

if __name__ == "__main__":
    process = EmailProcessor(IMAP_SERVER, EMAIL, SENHA)
    process.process_files(BRANCHES, STANDART_FOLDER, TEMPORARY_FOLDER, UNSAVED, FINAL_FOLDER)
