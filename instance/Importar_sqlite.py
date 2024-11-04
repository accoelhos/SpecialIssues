import sqlite3
import pandas as pd
from datetime import datetime
import os

# Definir o diretório base
base_dir = os.path.dirname(os.path.abspath(__file__))

# Definir informações de cada planilha
planilhas = {
    "IEEE": {
        "arquivo": os.path.join(base_dir,"WS_IEEE.xlsx"),
        "colunas": ['Tipo', 'Título', 'Link', 'Deadline', 'Resumo'],
        "editora": "IEEE"
    },
    "Elsevier": {
        "arquivo": os.path.join(base_dir, "WS_ELSEVIER.xlsx"),
        "colunas": ['Título', 'Revista', 'Submission Deadline', 'Link', 'Resumo'],
        "editora": "Elsevier"
    }
}

# Caminho do banco de dados SQLite
db_path = os.path.join(base_dir,  'specialissues.db')

# Verificar se o arquivo de banco de dados existe
if not os.path.exists(db_path):
    print(f"Erro: Arquivo de banco de dados não encontrado em {db_path}")
    exit()

# Conectar ao banco de dados
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Função para carregar planilha e inserir dados no banco
def importar_planilha(info, nome):
    # Carregar a planilha em um DataFrame
    try:
        df = pd.read_excel(info["arquivo"], usecols=info["colunas"])
    except FileNotFoundError:
        print(f"Erro: Arquivo '{info['arquivo']}' não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao carregar a planilha '{info['arquivo']}': {e}")
        return
    
    # Renomear as colunas do DataFrame para padronizar com a tabela do banco
    df.columns = ['revista', 'titulo', 'link', 'prazo', 'detalhes']
    
    # Iterar por cada linha do DataFrame e inserir no banco de dados
    for index, row in df.iterrows():
        editora = info["editora"]
        datanot = datetime.now().strftime("%Y-%m-%d")
        
        # Ajuste para Elsevier
        if nome == "Elsevier":
            titulo = row['revista']   # Elsevier inverte revista com título
            revista = row['titulo']   # Elsevier inverte revista com título
            prazo = row['link']       # Elsevier inverte link com prazo
            link = row['prazo']       # Elsevier inverte link com prazo
            detalhes= row['detalhes']
        else:
            titulo = row['titulo']
            revista = row['revista']
            link = row['link']
            prazo = row['detalhes'] #IEE inverte detalhes com prazo
            detalhes= row['prazo']
        
        # Inserir dados no banco de dados, tratando duplicatas
        try:
            cursor.execute('''
                INSERT INTO spi (editora, revista, titulo, link, prazo, datanot, detalhes) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (editora, revista, titulo, link, prazo, datanot, detalhes))
        except sqlite3.IntegrityError as e:
            print(f"Erro ao inserir '{titulo}': {e}")

# Importar cada planilha
for nome, info in planilhas.items():
    print(f"Importando dados de: {info['editora']}")
    importar_planilha(info, nome)

# Salvar as alterações e fechar a conexão
conn.commit()
conn.close()

print("Dados importados e inseridos no banco de dados com sucesso.")
