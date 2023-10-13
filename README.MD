# Ecommerce FLASK APP


## Tecnologias utilizadas
- Flask
- Docker
- Python
- SQLAlchemy
- Stripe

## Pré-requisitos

- Docker: [Instalação do Docker](https://docs.docker.com/get-docker/)
- Conta no Stripe: [Stripe](https://stripe.com/br)


## Configuração

1. Clone este repositório:

2. Configure o arquivo .env com as chaves da API do Stripe:

3. Execute o comando para criar a imagem do docker:

```bash
    docker compose up --build
```
4. acesse o endereço http://localhost:5000

5. Para acessar o swagger da aplicação acesse o endereço http://localhost:5000/swagger


### Pré populando o banco de dados

Para inicializar o banco de dados execute os comandos abaixo:

```bash
    docker exec -it "Container_Name" python db init
    docker exec -it "Container_Name" python db migrate
    docker exec -it "Container_Name" python db upgrade
```