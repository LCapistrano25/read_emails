import os
from decouple import config
from connection import Connection
from email_reader import EmailReader
from pdf_processor import PdfProcessor
from xml_processor import XmlProcessor
from file_manager import FileManager
from parameter_words import DATE, PARAM_DATE, FINAL_FOLDER, UNSAVED, TEMPORARY_FOLDER, MONTH

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

    def process_files(self, temp, unsaved, final):
        """Responsável por salvar"""
        self._file_manager().create_directory(temp)
        self._file_manager().create_directory(unsaved)
        self._file_manager().create_directory(final)
        
        inbox = self.search_for_emails()
        uids = self.extract_files(inbox, temp)
        
        for archive in os.listdir(temp):
            file_path = f"{temp}/{archive}"

            if archive.endswith(".pdf"):
                pdf = self._pdf_processor(file_path)
                text = pdf.process_pdf()
                word = pdf.word_search(PARAM_DATE, DATE)

                print(f"\n")
                print(file_path)
                print(text)
                print(f"\n")

                if word:
                    word = word.replace('/', '-').replace(':', '-')
                    word_list = word.split()[0]
                    word_list = list(word_list.split('-'))
                    word_list_reversed = list(map(int, reversed(word_list)))
                    
                    destinatary = f"{final}/{word_list_reversed[0]}/{MONTH[word_list_reversed[1]]}/{word_list_reversed[2]}/" 

                    directory = self._file_manager().create_directory(destinatary)
                    new_file_path = self._file_manager().save_file(directory, f"{word}.pdf")

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
                    unsaved_path = os.path.join(unsaved, archive)
                    if os.path.exists(unsaved_path):
                        self._file_manager().remove_file(file_path)
                    else:
                        self._file_manager().move_file(file_path, unsaved_path)
                
            elif archive.endswith(".xml"):
                print(archive)

        folder = 'INBOX.Seen'
        self._inbox.mark_email_as_read(uids)
        self._inbox.create_folder('INBOX', folder)

if __name__ == "__main__":
    process = EmailProcessor(IMAP_SERVER, EMAIL, SENHA)
    process.process_files(TEMPORARY_FOLDER, UNSAVED, FINAL_FOLDER)
