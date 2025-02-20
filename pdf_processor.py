import re
import fitz
import pytesseract
from pdf2image import convert_from_path
from unidecode import unidecode

class PdfProcessor:
    """Responsável por processar o pdf e extrair texto"""
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text_content = ""

    def has_embedded_text(self) -> bool:
        """Verifica se o PDF já tem OCR embutido (texto pesquisável)."""
        doc = fitz.open(self.pdf_path)
        for page in doc:
            if page.get_text().strip():
                return True
        return False

    def extract_text_from_pdf(self) -> str:
        """Extrai texto diretamente de um PDF pesquisável."""
        doc = fitz.open(self.pdf_path)
        return "\n".join(page.get_text() for page in doc if page.get_text().strip())

    def extract_text_with_ocr(self) -> str:
        """Aplica OCR em um PDF sem texto embutido."""
        images = convert_from_path(self.pdf_path)
        return "\n".join(pytesseract.image_to_string(img) for img in images)

    def process_pdf(self) -> str:
        """Decide automaticamente a melhor forma de extrair o texto do PDF."""
        if self.has_embedded_text():
            print("O PDF já tem OCR. Extraindo texto diretamente...")
            self.text_content = self.extract_text_from_pdf()
        else:
            print("O PDF NÃO tem OCR. Aplicando OCR com Tesseract...")
            self.text_content = self.extract_text_with_ocr()
        return self.text_content

    def _convert_text_to_list(self) -> list:
        """Transforma o texto em lista"""
        return self.text_content.split("\n")
    
    def word_search(self, params: list, word_search: str):
        """Buscar um dado específico numa lista de palavras"""
        words = r"|".join(params)
        text_list = self._convert_text_to_list()
        found = False
        for text in text_list:
            if found:
                word = re.search(f"{word_search}", text)
                if word:
                    return word.group()
                return None
            if re.search(f"{words}", unidecode(text.lower())):
                found = True
        return None
