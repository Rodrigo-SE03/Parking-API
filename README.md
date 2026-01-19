# Parking API

API REST para gerenciamento de estacionamento desenvolvida com FastAPI e MongoDB.

## Tecnologias

- Python 3.13
- FastAPI
- MongoDB (Atlas ou Local via Docker)
- Pydantic
- Pytest
- Docker

## Requisitos

- Python 3.13+
- Docker
- Mongo DB Atlas (para produção)

## Configuração do Banco de Dados

### Opção 1: MongoDB Atlas (Produção)

Para subir o projeto para ambiente de produção, é necessário configurar um cluster no MongoDB Atlas e obter a connection string para o cluster. No arquivo `.env`, use: `MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/...`.

### Opção 2: MongoDB Local

No arquivo `.env`, use: `MONGO_URI=mongodb://admin:admin@mongodb:27017`

## Desenvolvimento Local

### Rodando com Docker

1. Configure o arquivo `.env` baseado no `.env.example`: `MONGO_URI=mongodb://admin:admin@mongodb:27017`

2. Inicie os containers:

```bash
docker compose up -d
```

A API estará disponível em `http://localhost:8000`

Documentação Swagger: `http://localhost:8000/docs`

## Testes

Execute os testes com pytest:

```bash
pytest
```

### Rodando sem Docker (API local + MongoDB Atlas ou MongoDB local)

1. Crie e ative o ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure o arquivo `.env` baseado no `.env.example`:
   - Para MongoDB Atlas: use a connection string do Atlas
   - Para MongoDB local: use `mongodb://admin:admin@localhost:27017` e inicie o MongoDB localmente
    ```bash
    docker run -d --name parking-db -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=admin mongo:8.0
    ```

4. Execute a aplicação:

```bash
cd app
python main.py
```

## Endpoints

### POST /parking/
Registra a entrada de um veículo no estacionamento.

### PUT /parking/{plate}/pay
Registra o pagamento do estacionamento.

### PUT /parking/{plate}/out
Registra a saída do veículo do estacionamento.

### GET /parking/{plate}
Retorna o histórico de ações do veículo.

### DELETE /parking/{plate}
Remove um registro do banco de dados.

## Comandos Docker

```bash
# Iniciar containers (API + MongoDB local)
docker compose up -d

# Ver logs de todos os serviços
docker compose logs -f

# Ver logs apenas da API
docker logs -f --tail 100 parking-api

# Ver logs apenas do MongoDB
docker logs -f --tail 100 parking-mongodb

# Parar containers
docker compose down

# Parar containers e remover volumes (apaga dados do MongoDB local)
docker compose down -v

# Reconstruir imagem da API
docker compose build --no-cache

# Acessar o MongoDB via CLI (quando rodando com Docker)
docker exec -it parking-mongodb mongosh -u admin -p admin
```

## Variáveis de Ambiente

Variáveis necessárias no arquivo `.env`:

- `MONGO_URI`: URI de conexão com o MongoDB
  - MongoDB Atlas: `mongodb+srv://<username>:<password>@<cluster>.mongodb.net/...`
  - MongoDB Local (Docker): `mongodb://admin:admin@mongodb:27017`
- `ENV`: Ambiente de execução
  - `dev`: usa o banco `parking_db_test`
  - `prod`: usa o banco `parking_db`