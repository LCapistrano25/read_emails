# 📩 Email Processor

O **Email Processor** é um sistema automatizado para ler emails, baixar anexos (PDF/XML) e organizar os arquivos em pastas estruturadas com base nas informações extraídas dos documentos.

## 🚀 Funcionalidades
- 📬 **Leitura de emails via IMAP**
- 📎 **Extração automática de anexos**
- 🗂 **Organização de arquivos por data**
- 🏷 **Marcação de emails como lidos**
- 📂 **Movimentação de emails para pastas específicas**

## 🛠 Tecnologias Utilizadas
- **Python** 🐍
- **IMAP Tools** 📧
- **Decouple** 🔑 (para gerenciamento de variáveis de ambiente)

## 📦 Estrutura do Projeto
```
📂 LerEmail
 ┣ 📜 main.py              # Arquivo principal que inicia o processamento
 ┣ 📜 connection.py        # Gerencia a conexão com o servidor de email
 ┣ 📜 email_reader.py      # Responsável pela leitura e manipulação dos emails
 ┣ 📜 pdf_processor.py     # Processamento de PDFs e extração de informações
 ┣ 📜 xml_processor.py     # Processamento de arquivos XML
 ┣ 📜 file_manager.py      # Gerenciamento de arquivos e diretórios
 ┣ 📜 parameter_words.py   # Definição de palavras-chave e parâmetros
 ┣ 📜 utils.py             # Funções auxiliares ao processo
 ┣ 📄 .env                 # Configuração de credenciais (IMAP, email, senha)
 ┗ 📜 README.md            # Documentação do projeto
```

## 🔧 Como Usar
### 1️⃣ Clone este repositório:
```bash
git clone https://github.com/LCapistrano25/read_emails.git
```

### 2️⃣ Instale as dependências:
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure o arquivo `.env`:
Crie um arquivo `.env` na raiz do projeto e adicione:
```env
IMAP_SERVER=imap.seuemail.com
EMAIL=seuemail@example.com
SENHA=suasenha

TEMPORARY_FOLDER="pasta/"
FINAL_FOLDER="pasta/"
UNSAVED="pasta/"

SEEN='pasta.lidos'
BOX='caixa'
```

### 4️⃣ Execute o projeto:
```bash
python main.py
```

## 📌 Melhorias Futuras
- ✅ Suporte para novos formatos de arquivos
- ✅ Interface gráfica para configuração
- ✅ Integração com armazenamento em nuvem

Contribuições são bem-vindas! 🚀