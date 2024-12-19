def init_db():
    conn = sqlite3.connect('controle_portaria.db')
    cursor = conn.cursor()
    # Criar tabela de registros
    cursor.execute('''CREATE TABLE IF NOT EXISTS registros (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        data_entrada TEXT,
                        nome_completo TEXT,
                        documento TEXT,
                        empresa TEXT,
                        motivo TEXT,
                        autorizacao TEXT,
                        vigilante_entrada TEXT,
                        hora_saida TEXT,
                        vigilante_saida TEXT)''')

    # Criar tabela de usuários
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        can_export INTEGER DEFAULT 0)''')  # Novo campo 'can_export')''')
    
    conn.commit()
    conn.close()
