import re
import fitz
import pytesseract
from pdf2image import convert_from_path
from unidecode import unidecode
import logging

class PdfProcessor:
    """Responsável por processar o PDF e extrair texto"""
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text_content = ""
        logging.basicConfig(level=logging.INFO)

    def has_embedded_text(self) -> bool:
        """Verifica se o PDF já tem OCR embutido (texto pesquisável)."""
        try:
            doc = fitz.open(self.pdf_path)
            for page in doc:
                if page.get_text().strip():
                    return True
            return False
        except Exception as e:
            logging.error(f"Erro ao verificar texto embutido: {e}")
            return False

    def extract_text_from_pdf(self) -> str:
        """Extrai texto diretamente de um PDF pesquisável."""
        try:
            doc = fitz.open(self.pdf_path)
            return "\n".join(page.get_text() for page in doc if page.get_text().strip())
        except Exception as e:
            logging.error(f"Erro ao extrair texto do PDF: {e}")
            return ""

    def extract_text_with_ocr(self) -> str:
        """Aplica OCR em um PDF sem texto embutido."""
        try:
            images = convert_from_path(self.pdf_path)
            custom_config = r'--oem 3 --psm 6'  # Adiciona configurações do Tesseract
            return "\n".join(pytesseract.image_to_string(img, config=custom_config) for img in images)
        except Exception as e:
            logging.error(f"Erro ao aplicar OCR no PDF: {e}")
            return ""

    def process_pdf(self) -> str:
        """Decide automaticamente a melhor forma de extrair o texto do PDF."""
        if self.has_embedded_text():
            logging.info("O PDF já tem OCR. Extraindo texto diretamente...")
            self.text_content = self.extract_text_from_pdf()
        else:
            logging.info("O PDF NÃO tem OCR. Aplicando OCR com Tesseract...")
            self.text_content = self.extract_text_with_ocr()
        return self.text_content

    def _convert_text_to_list(self) -> list:
        """Transforma o texto em lista"""
        return self.text_content.split("\n")
    
    def word_search(self, params: list, word_search: str) -> str:
        """Buscar um dado específico numa lista de palavras"""
        words = params
        text_list = self._convert_text_to_list()
        text_list = [item for item in text_list if item and item.strip()]
        found = False
        print(text_list)
        for text in text_list:
            if found:
                word = re.search(f"{word_search}", text)
                if word:
                    return word.group()
            if re.search(f"{words}", unidecode(text.lower())):
                found = True
                word = re.search(f"{word_search}", text)
                if word:
                    return word.group()
        return None
