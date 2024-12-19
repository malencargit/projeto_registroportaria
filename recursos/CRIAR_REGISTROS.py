import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('controle_portaria.db')
cursor = conn.cursor()

# Inserir dados na tabela usuarios
cursor.execute("INSERT INTO usuarios (username, password, can_export) VALUES (?, ?, ?)",
               ('nome_usuario', 'senha_usuario', 1))  # 1 ou 0 para 'can_export'

# Commit e fechar a conexão
conn.commit()
conn.close()