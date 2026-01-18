# Imagem base Python
FROM python:3.13-slim

# Define diretório de trabalho
WORKDIR /app

# Copia apenas requirements primeiro (cache de layers)
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY app/ ./app/

# Expõe a porta da aplicação
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
