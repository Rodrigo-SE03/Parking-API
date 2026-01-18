# Parking API

API REST para gerenciamento de estacionamento desenvolvida com FastAPI e MongoDB.

## Tecnologias

- Python 3.13
- FastAPI
- MongoDB
- Pydantic
- Pytest
- Docker & Docker Compose

## Requisitos

- Docker e Docker Compose
- Python 3.13+ (para desenvolvimento local)

## Instalação e Execução

### Com Docker (Recomendado)

1. Clone o repositório
2. Configure as variáveis de ambiente:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e altere as credenciais do MongoDB.

3. Inicie os containers:

```bash
docker-compose up --build
```

A API estará disponível em `http://localhost:8000`

Documentação Swagger: `http://localhost:8000/docs`

### Desenvolvimento Local

1. Crie e ative o ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure o arquivo `.env` com a URI do MongoDB local

4. Execute a aplicação:

```bash
cd app
python main.py
```

## Testes

Execute os testes com pytest:

```bash
pytest
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

## Estrutura do Projeto

```
app/
├── main.py              # Ponto de entrada da aplicação
├── core/
│   └── configs.py       # Configurações e variáveis de ambiente
├── db/
│   └── mongo.py         # Conexão com MongoDB
└── parking/
    ├── router.py        # Definição das rotas
    ├── service.py       # Lógica de negócio
    ├── crud.py          # Operações no banco de dados
    ├── schemas.py       # Modelos de dados (Pydantic)
    ├── errors.py        # Definição de erros da API
    └── utils/
        └── helper_functions.py
```

## Comandos Docker

```bash
# Iniciar containers
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar containers
docker-compose down

# Remover volumes (limpa o banco de dados)
docker-compose down -v

# Reconstruir imagens
docker-compose build --no-cache
```

## Variáveis de Ambiente

Variáveis necessárias no arquivo `.env`:

- `MONGO_USERNAME`: Usuário do MongoDB
- `MONGO_PASSWORD`: Senha do MongoDB
- `MONGO_URI`: URI de conexão com o MongoDB
- `ENV`: Ambiente de execução (dev/prod)
