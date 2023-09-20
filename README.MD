# GameStore FLASK APP

## GameStore

## Tecnologias utilizadas
- Flask
- Docker
- Python
- SQLAlchemy

## Pré-requisitos

- Docker: [Instalação do Docker](https://docs.docker.com/get-docker/)
- Conta no IGDB para obter a chave da API: [IGDB Developer](https://www.igdb.com/api)
- Conta no Twitch para obter a chave da API: [Twitch Developer](https://dev.twitch.tv/console/apps/create)


## Configuração

1. Clone este repositório:

2. Configure o arquivo .env com as chaves da API do IGDB e Twitch:

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