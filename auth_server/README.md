# Servidor de Autenticacao (auth_server)

Este microsservico e responsavel por gerenciar o ciclo de vida de usuarios, autenticacao e emissao de sessoes criptografadas via JSON Web Tokens (JWT).

---

## Arquitetura do Modulo

O servico foi estruturado utilizando principios de Arquitetura Limpa (Clean/Hexagonal Architecture) para desacoplar a logica de negocio dos detalhes de infraestrutura:

* **Domain (Dominio)**: Contem as entidades de negocio (`User`) e os contratos/interfaces de repositorio (`UserRepository`). Nao possui dependencias de bibliotecas externas.
* **Application (Aplicacao)**: Implementa os casos de uso do sistema (`RegisterUser` e `LoginUser`). Recebe Data Transfer Objects (DTOs) e orquestra a execucao das regras de negocio.
* **Infrastructure (Infraestrutura)**: Contem os adaptadores tecnologicos concretos:
  * Camada de dados com SQLAlchemy e banco MySQL (`MySQLUserRepository`).
  * Rotas HTTP expostas por meio do framework Flask.
  * Servico de criptografia para hashing de senhas e geracao de tokens JWT assimetricos.

---

## Decisoes Tecnicas

* **BCrypt**: Hashing de senhas utilizando o algoritmo de derivacao de chave BCrypt com um custo padrao de 12 rounds, oferecendo alta resistencia contra ataques de forca bruta ou rainbow tables.
* **JWT Assimetrico**: A assinatura de sessao utiliza o algoritmo RS256. A chave privada RSA e mantida estritamente dentro do container do `auth_server` para assinatura no endpoint `/auth/login`, enquanto a chave publica correspondente e exposta publicamente ou copiada para outros containers para que realizem a validacao.
* **Testes de Endpoints**: A suite de testes unitarios em [test_auth_endpoints.py](file:///c:/Users/luizd/OneDrive/Desktop/Junior_Project_Pixel/auth_server/tests/test_auth_endpoints.py) utiliza um banco de dados SQLite em memoria (`sqlite:///:memory:`). Os testes realizam o teardown completo do schema a cada execucao para isolamento total dos estados de teste.

---

## Como Executar Localmente

### Usando o Ambiente Virtual do Python (Sem Docker)
1. Certifique-se de que possui o Python 3.11 instalado.
2. Navegue ate a pasta do servico:
   ```bash
   cd auth_server
   ```
3. Crie e ative o ambiente virtual:
   ```bash
   python -m venv .venv
   # No Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   # No Linux/macOS:
   source .venv/bin/activate
   ```
4. Instale as dependencias necessarias:
   ```bash
   pip install -r requirements.txt
   ```
5. Configure as variaveis de ambiente locais (para SQLite local em desenvolvimento):
   ```bash
   set DATABASE_URL=sqlite:///auth.db
   set JWT_PRIVATE_KEY_PATH=resources/private/private_key.pem
   ```
6. Inicialize o servidor local:
   ```bash
   python app/main.py
   ```
   O servidor iniciara na porta 5000.

### Como Executar os Testes Unitarios
Execute o comando dentro da pasta do servico:
```bash
python -m unittest tests/test_auth_endpoints.py
```

---

## Funcionalidades Implementadas / Nao Implementadas

### Implementadas
* Endpoint de cadastro de usuarios (`/auth/register`), validando duplicidade de e-mail e username.
* Endpoint de login (`/auth/login`), validando credenciais criptografadas e emitindo token JWT assimetrico com tempo de expiracao de 2 horas.
* Endpoint de verificacao de assinatura de token (`/token/verify`).
* Criptografia de senhas com BCrypt e persistencia em banco de dados relacional.

### Nao Implementadas
* Recuperacao ou alteracao de senha de usuario (fora do escopo de requisitos).
