# Usar uma imagem base do Python
FROM python:3.10-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /SCAP

# Copiar os arquivos do seu projeto para dentro do contêiner
COPY . /SCAP

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta em que o Flask vai rodar
EXPOSE 5000

# Comando para rodar o aplicativo Flask
CMD ["python", "SCAP/app.py"]