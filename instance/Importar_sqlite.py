import sqlite3
import pandas as pd
from datetime import datetime

# Defina as informações de cada planilha
planilhas = {
    "IEEE": {
        "arquivo": "WS_IEEE.xlsx",
        "colunas": ['Tipo', 'Título', 'Link', 'Deadline', 'Resumo'],
        "editora": "IEEE"
    },
    "Elsevier": {
        "arquivo": "WS_ELSEVIER.xlsx",
        "colunas": ['Título', 'Revista', 'Submission Deadline', 'Link', 'Resumo'],
        "editora": "Elsevier"
    },
    "Springer": {
        "arquivo": "WS_Springer.xlsx",
        "colunas": ['Nome do Jornal', 'Link do Jornal', 'Título do Update', 'Link do Update', 'Prazo de Submissão', 'Resumo'],
        "editora": "Springer"
    }
}

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('specialissues.db')
cursor = conn.cursor()

# Função para carregar planilha e inserir dados no banco
def importar_planilha(info, nome):
    # Verifique os nomes das colunas para garantir que estão corretos
    df = pd.read_excel(info["arquivo"], sheet_name=0)  # Carregar a planilha sem especificar as colunas
    print(f"Colunas reais da planilha {nome}: {df.columns}")
    
    # Verifique se as colunas que você quer usar realmente existem na planilha
    if set(info["colunas"]).issubset(df.columns):
        # Carregar a planilha com as colunas corretas
        df = pd.read_excel(info["arquivo"], usecols=info["colunas"])
    else:
        print(f"As colunas especificadas não foram encontradas na planilha {nome}. Verifique os nomes.")
        return

    # Para a planilha Springer, excluir a coluna 'Link do jornal' (verifique se realmente existe)
    if nome == "Springer" and 'Link do Jornal' in df.columns:
        df = df.drop(columns=['Link do Jornal'])
    
    # Renomear as colunas do DataFrame para padronizar com a tabela do banco
    if nome == "Springer":
        df.columns = ['revista', 'link_update', 'titulo', 'prazo', 'detalhes']
    else:
        df.columns = ['revista', 'titulo', 'link', 'prazo', 'detalhes']
    
    # Iterar por cada linha do DataFrame e inserir no banco de dados
    for index, row in df.iterrows():
        # Definir valores fixos para a editora e data atual
        editora = info["editora"]
        datanot = datetime.now().strftime("%Y-%m-%d")
        
        # Ajustes para Elsevier: inverter titulo com revista e link com prazo
        if nome == "Elsevier":
            titulo = row['revista']
            revista = row['titulo']
            prazo = row['link']
            link = row['prazo']
            detalhes = row['detalhes']
        # Ajustes para Springer: título e link de update
        elif nome == "Springer":
            titulo = row['link_update']
            revista = row['revista']
            link = row['titulo']  # Link do update da Springer
            prazo = row['prazo']
            detalhes = row['detalhes']
        else:
            titulo = row['titulo']
            revista = row['revista']
            link = row['link']
            prazo = row['detalhes']
            detalhes = row['prazo']

        # Inserir dados no banco de dados, tratando duplicatas
        try:
            cursor.execute(''' 
                INSERT OR IGNORE INTO spi (editora, revista, titulo, link, prazo, datanot, detalhes) 
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
