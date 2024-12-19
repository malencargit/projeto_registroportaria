import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('controle_portaria.db')
cursor = conn.cursor()

# Verificar a estrutura da tabela usuarios
cursor.execute("PRAGMA table_info(usuarios)")
tabela_info = cursor.fetchall()

# Exibir as informações das colunas da tabela
for coluna in tabela_info:
    print(coluna)

# Fechar a conexão
conn.close()