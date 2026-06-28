# Pixel Driver - Plataforma de Armazenamento de Arquivos

Este projeto consiste em uma solução corporativa para armazenamento, upload, download e gerenciamento de arquivos. A arquitetura é baseada em microsserviços/serviços orientados a contexto, encapsulada e orquestrada de forma nativa por meio do Docker.

---

## 1. Arquitetura do Sistema

O ecossistema é estruturado em três módulos principais de responsabilidade única:

1. **Servidor de Autenticação (auth_server)**: Serviço construído em Flask responsável pela identidade, cadastro e login de usuários, além da emissao de sessões criptografadas via JWT assimétrico (RS256).
2. **Servidor de Recursos (resurce_server)**: Serviço em Flask voltado ao armazenamento físico de arquivos e indexação de metadados no banco de dados. Realiza a validação de permissões e segurança em nível de usuário, além de gerar miniaturas de imagem em tempo real.
3. **Cliente Web (frontend)**: Aplicação SPA construída em React + TypeScript + Vite, otimizada para ser responsiva e adaptável em qualquer tamanho de monitor (celulares, tablets, notebooks e telas Widescreen 4K). É empacotada com Nginx para distribuição de alta performance.

O banco de dados utilizado é o **MySQL 8.0**, compartilhado entre as APIs para garantir integridade referencial.

```mermaid
graph TD
    User[Navegador / Cliente] -->|Porta 3000| FE[Frontend Nginx + React]
    FE -->|Autenticação (Porta 5000)| AS[Auth Server API]
    FE -->|Recursos/Arquivos (Porta 5001)| RS[Resource Server API]
    AS -->|Persistência Relacional| DB[(MySQL Database)]
    RS -->|Persistência Relacional| DB
    RS -->|Validação de Assinatura JWT| AS
```

---

## 2. Decisões Técnicas Tomadas

* **Criptografia Assimétrica para JWT (RS256)**: O Servidor de Autenticação assina os tokens de sessão utilizando uma chave privada RSA de 2048 bits. O Servidor de Recursos valida esses tokens localmente de forma assimétrica usando a respectiva chave pública (exposta no endpoint `/token/public-key`), sem a necessidade de realizar chamadas REST adicionais de validação, reduzindo drasticamente a latência de rede.
* **Resiliência de Inicialização (Connection Retry Loop)**: Implementamos um loop de verificação de conexão com o banco de dados (até 10 tentativas com intervalo de 3 segundos) no boot das APIs. Isso resolve a clássica condição de corrida em que as aplicações sobem mais rápido que a inicialização de privilégios do MySQL.
* **Arquitetura Factory no Flask (App Factory)**: Refatoramos a estrutura das APIs de modo que os arquivos `main.py` atuem puramente como pontos de entrada de runtime, delegando a inicialização de conexões e montagem dos Blueprints para fábricas (`app_factory.py`) e módulos de configuração (`db_init.py`).
* **Streaming de Downloads**: A entrega de arquivos grandes é feita por meio de streaming direto do sistema de arquivos para a conexão de rede do cliente, dividindo o envio em buffers de 8192 bytes. Essa estratégia evita o carregamento do arquivo completo na memória RAM do Servidor de Recursos, garantindo escalabilidade.
* **Timezone Localizado no Frontend**: Os timestamps de upload do banco são armazenados em UTC e normalizados no frontend anexando o sufixo "Z" antes do parse. Isso faz com que o navegador efetue a conversão automática e exiba as datas no fuso horário exato do computador do usuário (ex: UTC-3 no Brasil).
* **Modal de Preview Móvel (Draggable)**: Implementamos um wrapper externo (`modal-draggable-wrapper`) no componente de Modal. Isso desacopla as coordenadas de arraste da animação CSS de zoom de entrada do modal, evitando que a regra `animation-fill-mode: forwards` anule as transformações de translação e permitindo mover a tela livremente pelo cabeçalho.
* **Layout Adaptável e Responsivo**: Aumentamos a largura máxima do painel principal para `1600px` em monitores grandes, criamos larguras máximas de nomes de arquivo dinâmicas (até `700px` em widescreen) e adicionamos empacotamento (`flex-wrap`) para botões de ação em telas pequenas (mobile/tablets).
* **Isolamento de Testes Unitários**: A stack em produção roda sobre o MySQL, enquanto as suítes de testes locais utilizam o SQLite em memória (`sqlite:///:memory:`), garantindo velocidade e isolamento absoluto de estados de teste.

---

## 3. Como Executar o Projeto

### A. Com Docker (Método Recomendado)
A stack completa pode ser inicializada e configurada com apenas um comando executado na raiz do projeto:
```bash
docker compose up -d
```
Se preferir automatizar com healthchecks do banco e reiniciar os backends no tempo certo, utilize os scripts inclusos:
* **No Windows:**
  ```cmd
  scripts\start_services.bat
  ```
* **No Linux/macOS:**
  ```bash
  chmod +x scripts/*.sh
  ./scripts/start_services.sh
  ```

A aplicação estará disponível em:
* **Frontend Web:** [http://localhost:3000](http://localhost:3000)
* **Auth Server API:** [http://localhost:5000](http://localhost:5000)
* **Resource Server API:** [http://localhost:5001](http://localhost:5001)

Para derrubar os containers e limpar os volumes:
* **Windows**: `scripts\stop_services.bat`
* **Linux/macOS**: `./scripts/stop_services.sh`

---

### B. Sem Docker (Desenvolvimento Local)
Caso deseje rodar a aplicação localmente fora de containers, siga as instruções de cada módulo:

#### 1. Auth Server
```bash
cd auth_server
python -m venv .venv
# Ativar venv (Windows: .\.venv\Scripts\activate | Linux: source .venv/bin/activate)
pip install -r requirements.txt
set DATABASE_URL=sqlite:///auth_local.db
set JWT_PRIVATE_KEY_PATH=resources/private/private_key.pem
python app/main.py
```

#### 2. Resource Server
```bash
cd resurce_server
python -m venv .venv
# Ativar venv
pip install -r requirements.txt
set DATABASE_URL=sqlite:///resource_local.db
set UPLOAD_DIR=data
set JWT_PUBLIC_KEY_PATH=../auth_server/resources/public_key.pem
python app/main.py
```

#### 3. Frontend Web
```bash
cd frontend/pixel-driver
npm install
npm run dev
```
O frontend local estará em [http://localhost:5173](http://localhost:5173).

---

## 4. Suíte de Testes

O projeto conta com cobertura completa de testes unitários e de integração:

### Executando Testes Unitários:
* **Auth Server**:
  ```bash
  .\auth_server\.venv\Scripts\python -m unittest discover -s auth_server/tests -p "*.py"
  ```
* **Resource Server**:
  ```bash
  .\resurce_server\.venv\Scripts\python -m unittest discover -s resurce_server/tests -p "*.py"
  ```

### Executando Testes de Integração (com a stack Docker ativa):
```bash
.\resurce_server\.venv\Scripts\python -m unittest tests/test_integration.py
```

Para rodar todo o pipeline de testes em um único comando no Windows, execute:
```cmd
tests\run_unit_tests.bat
```

> [!TIP]
> Os logs de validação e a lista completa dos cenários testados podem ser consultados no relatório [Tests_results.md](file:///c:/Users/luizd/OneDrive/Desktop/Junior_Project_Pixel/Tests_results.md).

---

## 5. Funcionalidades Implementadas / Não Implementadas

### Implementadas
* **Autenticação**: Cadastro e login de usuários por e-mail/senha com persistência local de sessão via tokens JWT.
* **Gerenciamento de Arquivos**: Envio (drag-and-drop com progresso), listagem (nome original, tamanho, data), download em streaming e exclusão física imediata.
* **Restrições de Segurança**: Bloqueio de arquivos maiores de 10MB, tipos de arquivos restritos (.png, .jpg, .jpeg, .pdf, .txt) e validação de propriedade (usuário X não acessa arquivos de usuário Y).
* **Interface Responsiva**: Visualizadores ajustados para telas Widescreen e dispositivos móveis, com ações de tabela centralizadas.
* **Preview de Imagem**: Botão **"Preview"** para arquivos de imagem, abrindo um modal centralizado e móvel (draggable) que permite arrastar a janela clicando no cabeçalho superior.
* **Fusos Horários**: Data de upload formatada dinamicamente utilizando a hora local do dispositivo do cliente.
* **Erros Customizados**: Páginas de erro Nginx personalizadas com o layout do Pixel Driver.

### Não Implementadas
* **Compartilhamento de arquivos entre usuários**: Fora do escopo de requisitos da aplicação.
