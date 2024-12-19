import sqlite3

def ver_registros():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('controle_portaria.db')
    cursor = conn.cursor()
    
    # Executa uma consulta para pegar todos os registros
    cursor.execute("SELECT * FROM registros")
    registros = cursor.fetchall()  # Recupera todos os registros da tabela
    
    # Exibe os registros no console
    for registro in registros:
        print(registro)  # Imprime cada registro no console
    
    # Fecha a conexão
    conn.close()

# Chama a função para exibir os registros
ver_registros()
