import mysql.connector

# Conecta o Banco de Dados com o python
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="eu_indico"
    )
