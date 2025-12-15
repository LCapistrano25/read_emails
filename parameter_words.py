from decouple import config

# 📅 Expressões Regulares para Data
DATE = r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}|\d{2}/\d{2}/\d{4}"
PARAM_DATE = r"(emiss?[\w&]+|emissão|emiss[oó]o|emiss&o|emissão|emiss3o|emissio|data\s*de\s*geração\s*da\s*nfs-e)"

CNPJ =''

PARAM_CNPJ = r"cnpj\s*"


# 📂 Configurações de Diretórios
STANDART_FOLDER = config('STANDART_FOLDER')
TEMPORARY_FOLDER = config('TEMPORARY_FOLDER')
FINAL_FOLDER = config('FINAL_FOLDER')
UNSAVED = config('UNSAVED')

# 📄 Tipo de Arquivo
FILE_TYPE = "application/pdf"

# 📬 Configuração da Caixa de Email
BOX = config('BOX')
SEEN = config('SEEN')

# 📆 Meses do Ano
MONTH = {
    1: 'JANEIRO',   2: 'FEVEREIRO', 3: 'MARÇO',     4: 'ABRIL',
    5: 'MAIO',      6: 'JUNHO',     7: 'JULHO',     8: 'AGOSTO',
    9: 'SETEMBRO',  10: 'OUTUBRO',  11: 'NOVEMBRO', 12: 'DEZEMBRO'
}

# 🛖 Filiais
BRANCHES = {
    "00.000.000/0001-10": "PALMAS",
}

