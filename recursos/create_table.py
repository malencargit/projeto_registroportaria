import sqlite3

def create_table():
    conn = sqlite3.connect("controle_portaria.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS registros (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome_completo TEXT,
                        documento TEXT,
                        empresa TEXT,
                        motivo TEXT,
                        autorizacao TEXT,
                        data_entrada TEXT,
                        hora_entrada TEXT,
                        vigilante_entrada TEXT,
                        hora_saida TEXT,
                        vigilante_saida TEXT)''')
    conn.commit()
    conn.close()

create_table()
print("Tabela 'registros' criada com sucesso!")
