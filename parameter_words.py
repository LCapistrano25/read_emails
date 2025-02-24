from decouple import config

# 📅 Expressões Regulares para Data
DATE = r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}|\d{2}/\d{2}/\d{4}"
PARAM_DATE = r"(emiss?[\w&]+|emissão|emiss[oó]o|emiss&o|emissão|emiss3o|emissio|data\s*de\s*geração\s*da\s*nfs-e)"

CNPJ = r"30\.698\.208\s*/?\s*0001\s*-\s*97|" \
        r"30\.698\.208\s*/?\s*0002\s*-\s*78|" \
        r"30\.698\.208\s*/?\s*0003\s*-\s*59|" \
        r"30\.698\.208\s*/?\s*0005\s*-\s*10|" \
        r"30\.698\.208\s*/?\s*0004\s*-\s*30|" \
        r"30\.698\.208\s*/?\s*0007\s*-\s*82|" \
        r"30\.698\.208\s*/?\s*0008\s*-\s*63|" \
        r"30\.698\.208\s*/?\s*0006\s*-\s*00"

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
    "30.698.208/0001-97": "PALMAS",
    "30.698.208/0002-78": "GURUPI",
    "30.698.208/0003-59": "PORANGATU",
    "30.698.208/0005-10": "BALSAS",
    "30.698.208/0004-30": "IMPERATRIZ",
    "30.698.208/0007-82": "TERESINA",
    "30.698.208/0008-63": "PALMAS - SEMINOVOS",
    "30.698.208/0006-00": "SAO LUIZ"
}

