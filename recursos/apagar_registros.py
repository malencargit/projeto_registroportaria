import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('controle_portaria.db')
cursor = conn.cursor()

# Comando SQL para apagar todos os registros da tabela 'registros'
cursor.execute("DELETE FROM registros")

# Confirmar a operação e fechar a conexão
conn.commit()
conn.close()

print("Todos os registros foram apagados com sucesso!")
