import os

class FileManager:
    """Responsável por lidar com a criação de pastas, mover arquivos e renomea-los"""
    def __init__(self):
        self._directory = None

    def exist_directory(self, directory: str) -> bool:
        """Responsável por verificar se existe a pasta"""
        if not os.path.exists(directory):
            return False
        return True

    def create_directory(self, directory: str) -> str:
        """Responsável por criar pasta"""
        if not self.exist_directory(directory):
            os.makedirs(directory)
        return directory
    
    def save_file(self, directory, filename) -> str:
        """Responsável por salvar arquivo numa pasta específica"""
        return os.path.join(directory, filename)

    def move_file(self, origin: str, destination: str) -> None:
        """Responsável por mover arquivo para outro local"""
        # Verifique se o diretório de destino existe
        destination_dir = os.path.dirname(destination)  # Pega apenas o diretório de destino, sem o nome do arquivo
        
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)  # Cria o diretório se não existir
        
        # Mover o arquivo para o diretório de destino
        os.rename(origin, destination)

    def rename_file(self, old_name: str, new_name: str):
        """Responsável por renomear arquivo"""
        os.rename(old_name, new_name)

    def remove_file(self, directory):
        """Responsável por deletar um arquivo"""
        os.remove(directory)
