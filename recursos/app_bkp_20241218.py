from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import sqlite3
import pandas as pd
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key'  # Altere isso para uma chave secreta segura

# Função para inicializar o banco de dados
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
                        hora_entrada TEXT,
                        vigilante_entrada TEXT,
                        hora_saida TEXT,
                        vigilante_saida TEXT)''')

    # Criar tabela de usuários
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')

    conn.commit()
    conn.close()

# Função para inicializar o banco de dados ao iniciar o servidor
init_db()

# Rota para página de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        can_export = request.form.get('can_export', 'off') == 'on'  # Verifica se o campo 'can_export' foi marcado
        hashed_password = generate_password_hash(password)  # Gerar o hash da senha
        #print(f"Username: {username}, Can Export: {can_export}")  # Adicione isso para ver o que está sendo enviado

        conn = sqlite3.connect('controle_portaria.db')
        cursor = conn.cursor()

        try:
            # Inserir o usuário no banco de dados
            cursor.execute("INSERT INTO usuarios (username, password, can_export) VALUES (?, ?, ?)", 
                            (username, hashed_password, 1 if can_export else 0))  # Salva 1 ou 0 no banco
            conn.commit()
            return redirect(url_for('login'))  # Redireciona para a página de login após cadastro bem-sucedido
        except sqlite3.IntegrityError:
            return "Usuário já existe. Tente outro nome."  # Caso o usuário já exista

        finally:
            conn.close()

    return render_template('cadastro.html')  # Página de cadastro

# Rota para página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('controle_portaria.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        user = cursor.fetchone()

        

        #conn.close()

    #return render_template('login.html')  # Página de login


        if user:
            # Se o usuário foi encontrado, verifica a senha
            if check_password_hash(user[2], password):  # Verifica se a senha está correta
                session['user_id'] = user[0]  # Armazena o ID do usuário na sessão
                session['can_export'] = user[3]  # Armazena a permissão de exportação na sessão
                #print(f"Usuário {username} autenticado com sucesso.")  # Depuração
                print(f"Permissão de exportação para {user[1]}: {session['can_export']}")
                return redirect(url_for('index'))  # Redireciona para a página principal
            else:
                print("Senha incorreta.")  # Depuração para senha incorreta
                return "Nome de usuário ou senha incorretos."  # Caso as credenciais sejam inválidas
        else:
            print("Usuário não encontrado.")  # Depuração para usuário não encontrado
            return "Nome de usuário ou senha incorretos."  # Caso o usuário não exista

        conn.close()

    return render_template('login.html')  # Página de login



# Rota para a página inicial (apenas acessível para usuários logados)
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        print("Usuário não autenticado. Redirecionando para login.")  # Depuração para verificar sessão
        return redirect(url_for('login'))  # Redireciona para a página de login se não estiver autenticado

    print("Usuário autenticado. Carregando página inicial.")  # Depuração para verificar sessão
    return render_template('index.html')  # Página inicial da aplicação

# Função para inserir registros no banco de dados
@app.route('/inserir', methods=['POST'])
def inserir():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redireciona se o usuário não estiver logado
    
    # Captura os dados do formulário
    data_entrada = request.form['data_entrada']
    nome_completo = request.form['nome_completo']
    documento = request.form['documento']
    empresa = request.form['empresa']
    motivo = request.form['motivo']
    autorizacao = request.form['autorizacao']
    hora_entrada = request.form['hora_entrada']
    vigilante_entrada = request.form['vigilante_entrada']
    hora_saida = request.form.get('hora_saida', '')  # Hora saída pode ser opcional
    vigilante_saida = request.form.get('vigilante_saida', '')  # Vigilante saída pode ser opcional

    # Inserir no banco de dados
    conn = sqlite3.connect('controle_portaria.db')
    cursor = conn.cursor()

    cursor.execute(''' 
        INSERT INTO registros (data_entrada, nome_completo, documento, empresa, motivo, autorizacao, 
                               hora_entrada, vigilante_entrada, hora_saida, vigilante_saida)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data_entrada, nome_completo, documento, empresa, motivo, autorizacao, hora_entrada, 
          vigilante_entrada, hora_saida, vigilante_saida))
    
    conn.commit()
    conn.close()

    # Após a inserção, passamos a mensagem de sucesso para o template
    return render_template('index.html', sucesso="Registro incluído com sucesso!")

# Rota para exibir todos os registros no banco de dados com a funcionalidade de pesquisa
@app.route('/registros', methods=['GET', 'POST'])
def registros():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redireciona para a página de login se não estiver autenticado

    conn = sqlite3.connect('controle_portaria.db')
    cursor = conn.cursor()

    # Pesquisa por nome (caso o usuário tenha inserido um nome)
    nome_pesquisa = request.form.get('search_name', '')  # Pega o nome pesquisado
    if nome_pesquisa:  # Se algum nome foi digitado, executa a pesquisa
        cursor.execute("SELECT * FROM registros WHERE nome_completo LIKE ?", ('%' + nome_pesquisa + '%',))
    else:
        # Se não houver pesquisa, não mostra registros
        registros = []
        conn.close()
        return render_template('registros.html', registros=registros, nome_pesquisa=nome_pesquisa)

    registros = cursor.fetchall()
    conn.close()

    return render_template('registros.html', registros=registros, nome_pesquisa=nome_pesquisa)  # Página com os registros


# Rota para editar os campos "hora_saida" e "vigilante_saida"
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redireciona para a página de login se não estiver autenticado

    conn = sqlite3.connect('controle_portaria.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        hora_saida = request.form['hora_saida']
        vigilante_saida = request.form['vigilante_saida']
        
        cursor.execute('''UPDATE registros
                          SET hora_saida = ?, vigilante_saida = ?
                          WHERE id = ?''', (hora_saida, vigilante_saida, id))
        conn.commit()
        conn.close()

        return redirect(url_for('registros'))  # Redireciona para a lista de registros

    # Caso seja um GET, carrega os dados do registro para edição
    cursor.execute("SELECT * FROM registros WHERE id = ?", (id,))
    registro = cursor.fetchone()
    conn.close()

    return render_template('editar.html', registro=registro)  # Página de edição

# Rota para exportar registros para Excel
@app.route('/exportar', methods=['GET', 'POST'])
def exportar():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redireciona para a página de login se não estiver autenticado
     
    # Depuração: Verifique o valor de 'can_export' na sessão
    print(f"Valor de 'can_export' na sessão: {session.get('can_export')}")

    # Verificar se a chave 'can_export' está na sessão e se tem o valor 1
    if session.get('can_export') != 1:
        return "Você não tem permissão para exportar os registros. Entre em contato com o administrador."  # Retorna mensagem de erro
    
    # Caso tenha permissão, continua com a lógica de exportação
    if request.method == 'POST':
        # Obter as datas de início e fim do formulário
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']
        
        # Conectando ao banco de dados
        conn = sqlite3.connect('controle_portaria.db')
        query = '''SELECT * FROM registros WHERE data_entrada BETWEEN ? AND ?'''
        
        # Usando pandas para gerar um DataFrame
        df = pd.read_sql_query(query, conn, params=(data_inicio, data_fim))
        conn.close()

        # Criando a pasta para salvar o arquivo (caso não exista)
        output_folder = 'static/uploads'  # Pasta dentro do diretório "static"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Definindo o caminho completo para o arquivo
        file_path = os.path.join(output_folder, 'registros_exportados.xlsx')

        # Exportando os dados para o Excel
        df.to_excel(file_path, index=False)

        # Retorna o caminho do arquivo para ser baixado
        return render_template('exportar.html', file_path=file_path)  # Exibe o link para o download

    return render_template('exportar.html')  # Exibe o formulário para escolher o intervalo de datas


# Rota para servir o arquivo para download
@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory('static/uploads', filename)

#if __name__ == '__main__':
 #   app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
