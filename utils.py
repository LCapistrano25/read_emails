import hashlib

def generate_file_hash(filename: str) -> str:
    """Gera um hash curto baseado no nome do arquivo"""
    return hashlib.sha1(filename.encode()).hexdigest()[:8]  # Pega os primeiros 8 caracteres
