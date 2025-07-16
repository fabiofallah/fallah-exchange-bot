# Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Copia e instala as dependências primeiro (boa prática de cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do projeto
COPY . .

# Expõe a porta (opcional, mas recomendado)
EXPOSE 8080

# Comando de inicialização
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
