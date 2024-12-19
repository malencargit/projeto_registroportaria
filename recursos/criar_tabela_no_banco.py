from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados SQLite
def connect_db():
    conn = sqlite3.connect("controle_portaria.db")
    return conn

# Função para criar a tabela "registros" caso ela não exista
def create_table():
    conn = connect_db()
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

# Rota para a página inicial, onde vemos os registros
@app.route('/')
def index():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registros")
    records = cursor.fetchall()
    conn.close()
    return render_template('index.html', records=records)

# Rota para atualizar um registro
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = connect_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        # Atualiza os dados do registro
        hora_saida = request.form['hora_saida']
        vigilante_saida = request.form['vigilante_saida']
        cursor.execute('''UPDATE registros SET hora_saida = ?, vigilante_saida = ? WHERE id = ?''',
                       (hora_saida, vigilante_saida, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    # Exibe o formulário com os dados atuais
    cursor.execute("SELECT * FROM registros WHERE id = ?", (id,))
    record = cursor.fetchone()
    conn.close()
    return render_template('update.html', record=record)

if __name__ == '__main__':
    # Cria a tabela antes de iniciar o servidor
    create_table()
    app.run(debug=True)
