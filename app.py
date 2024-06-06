from flask import Flask, request, render_template, redirect, url_for
import fitz 
import pandas as pd

app = Flask(__name__)

# Extrair tabelas do pdf
def extract_tables_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    tables = [] # Armazenar tabelas
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        # Processar o texto para encontrar tabelas (simples exemplo para CSV-like dados)
        lines = text.split('\n')
        data = [line.split() for line in lines if line.strip()]
        tables.append(pd.DataFrame(data))
    return tables

# Rota página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota pós-upload do Pdf
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'Nenhum arquivo selecionado'
    
    if file and file.filename.endswith('.pdf'): # Verifica se arquivo é pdf
        try:
            tables = extract_tables_from_pdf(file)
            html_tables = "" # Armazena as tabelas em html
            for i, table in enumerate(tables):
                html_tables += f'<h2>Tabela {i+1}</h2>{table.to_html()}'
            return f'<h2>Informações Extraídas:</h2> {html_tables}' # Retorna as tabelas no HTML
        except Exception as e:
            return str(e)
    else:
        return 'Formato de arquivo não suportado'

if __name__ == '__main__':
    app.run(debug=True) # Executa Flask em debug
