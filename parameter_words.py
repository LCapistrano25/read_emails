from decouple import config

DATE = r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}|\d{2}/\d{2}/\d{4}"

PARAM_DATE = ["emissao", "emisso", "emissdo", "emiss&o", "emissão", "EMISSÃO:", "Emiss3o"]

TEMPORARY_FOLDER = config('TEMPORARY_FOLDER')
FINAL_FOLDER = config('FINAL_FOLDER')
UNSAVED = config('UNSAVED')

FILE_TYPE = "application/pdf"

BOX = config('BOX')
SEEN = config('SEEN')

MONTH = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro'
}