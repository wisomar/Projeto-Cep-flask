# Usar uma imagem base oficial do Python
FROM python:3.9

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar os arquivos do projeto para o diretório de trabalho
COPY . /app

# Instalar as dependências do projeto (supondo que um arquivo requirements.txt exista)
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta onde a aplicação vai rodar (opcional, se for um servidor)
EXPOSE 5000

# Definir o comando para rodar a aplicação (ajuste conforme necessário)
CMD ["python", "app/app.py"]
