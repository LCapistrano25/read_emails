import hashlib

def generate_file_hash(filename: str) -> str:
    """Gera um hash curto baseado no nome do arquivo"""
    return hashlib.sha1(filename.encode()).hexdigest()[:8]  # Pega os primeiros 8 caracteres

def turn_date_into_list(date: str) -> list:
    """Transforma data em lista [yyyy, mm, dd]"""
    new_date = date.replace('/', '-').replace(':', '-')
    date_list = new_date.split()[0]
    date_list = list(date_list.split('-'))
    return list(map(int, reversed(date_list)))