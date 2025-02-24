# Bibliotecas padrão
import os
import time

# Bibliotecas de terceiros
from decouple import config

# Módulos internos de conexão e processamento de dados
from connection import Connection
from email_reader import EmailReader
from pdf_processor import PdfProcessor
from xml_processor import XmlProcessor
from file_manager import FileManager
from control_log import ControlLog
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
        self._control_log = ControlLog

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
            if self._file_manager().exist_directory(path):
                self._file_manager().remove_file(path)

    def process_pdf(self, archive, standart_folder: str, general_temp: str, unsaved_folder: str, final_folder: str):
        """Responsável por identificar os padrões nos pdfs e destinar ao local correto"""
        file_path = self._file_manager().create_path_to_folder(general_temp, archive)
        pdf = self._pdf_processor(file_path)
        text = pdf.process_pdf()

        general_unsaved_folder = self._file_manager().create_path_to_folder(standart_folder, unsaved_folder)

        identifier_company = pdf.word_search(PARAM_CNPJ, CNPJ)
        identifier_company = pdf.remove_space(identifier_company)

        self._control_log().log_info(archive)
        if identifier_company:
            folder = BRANCHES.get(identifier_company, None)
            if folder:
                self._control_log().log_info(f"Filial identificada -> {folder}")
                branch_unsaved_folder = self._file_manager().create_path_to_folder(
                        standart_folder, folder, unsaved_folder)   

                date = pdf.word_search(PARAM_DATE, DATE) 
                if date:
                    date = date.replace('/', '-').replace(':', '-')
                    date_list_reversed = turn_date_into_list(date)
                    
                    self._control_log().log_info(f"Data de emissão encontrada -> {date}")
                    destinatary = self._file_manager().create_path_to_folder(
                        standart_folder, folder, final_folder, 
                        date_list_reversed[0], 
                        MONTH[date_list_reversed[1]], 
                        date_list_reversed[2]
                    )

                    self._control_log().log_info(f"Destino da Nota Identificado -> {destinatary}")

                    hash_name = generate_file_hash(archive)
                    directory = self._file_manager().create_directory(destinatary)
                    new_filename = f"{date} - {hash_name}.pdf"
                    new_file_path = self._file_manager().save_file(directory, new_filename)

                    try:
                        if not self._file_manager().exist_directory(new_file_path):
                            self._control_log().log_info(f"Movendo arquivo para novo diretório -> {new_file_path}\n")
                            self._file_manager().move_file(file_path, new_file_path)
                        else:
                            self._control_log().log_info(f"Excluíndo arquivo, pois já existe no diretório -> {new_filename}\n")
                            self._file_manager().remove_file(file_path)
                    except PermissionError as e:
                        self._control_log().log_error(f"Erro ao renomear o arquivo: {e}\n")
                    except OSError as e:
                        self._control_log().log_error(f"Erro ao renomear o arquivo (OSError): {e}\n")
                else:
                    self._control_log().log_warning(f"Data de emissão não encontrada")
                    self._control_log().log_warning(f"Movendo para pasta de indefinidos de {folder}\n")
                    self.redirect_unassigned_files(file_path, branch_unsaved_folder, archive)
            else:
                self._control_log().log_warning(f"Filial não encontrada")
                self._control_log().log_warning(f"Movendo para pasta de indefinidos gerais.\n")
                self.redirect_unassigned_files(file_path, general_unsaved_folder, archive)
        else:
            self._control_log().log_warning(f"Filial não encontrada")
            self._control_log().log_warning(f"Movendo para pasta de indefinidos gerais.\n")
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

        time.sleep(10)
        self.clean_temporary_folder(general_temporary_folder)

if __name__ == "__main__":
    process = EmailProcessor(IMAP_SERVER, EMAIL, SENHA)
    process.process_files(BRANCHES, STANDART_FOLDER, TEMPORARY_FOLDER, UNSAVED, FINAL_FOLDER)
