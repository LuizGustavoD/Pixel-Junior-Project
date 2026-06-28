# Pixel Driver - Plataforma de Armazenamento de Arquivos

Este projeto consiste em uma solução corporativa para armazenamento, upload, download e gerenciamento de arquivos. A arquitetura é baseada em microsserviços/serviços orientados a contexto, encapsulada e orquestrada de forma nativa por meio do Docker.

---

## 1. Arquitetura do Sistema

O ecossistema é estruturado em três módulos principais de responsabilidade única:

1. **Servidor de Autenticação (auth_server)**: Serviço construído em Flask responsável pela identidade, cadastro e login de usuários, além da emissao de sessões criptografadas via JWT assimétrico (RS256).
2. **Servidor de Recursos (resurce_server)**: Serviço em Flask voltado ao armazenamento físico de arquivos e indexação de metadados no banco de dados. Realiza a validação de permissões e segurança em nível de usuário, além de gerar miniaturas de imagem em tempo real.
3. **Cliente Web (frontend)**: Aplicação SPA construída em React + TypeScript + Vite, otimizada para ser responsiva e adaptável em qualquer tamanho de monitor (celulares, tablets, notebooks e telas Widescreen 4K). É empacotada com Nginx para distribuição de alta performance.

O banco de dados relacional utilizado é o **MySQL 8.0**, compartilhado entre as APIs de back-end para fins de manutenção de integridade referencial de chaves estrangeiras relacionadas à propriedade dos arquivos indexados.

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

## 5. Diretrizes de Uso de Inteligência Artificial (IA)

Este projeto foi concebido seguindo um modelo de desenvolvimento híbrido, em que o papel da inteligência artificial foi estritamente delimitado como ferramenta de suporte operacional, preservando a engenharia de software intelectual sob responsabilidade humana:

* **Decisões Arquiteturais e Padrões de Projeto (Autoria Humana)**: Toda a arquitetura do sistema incluindo a escolha do padrão Clean Architecture/Hexagonal nos back-ends, a assinatura e validação assimétrica de chaves criptográficas RS256, o modelo de banco de dados compartilhado, o fluxo de controle de concorrência com loops de retries para persistência de dados e a arquitetura das SPA (Single Page Application) foi desenhada e decidida autonomamente.
* **Estilo Visual e Experiência do Usuário (Autoria Humana)**: O design visual do frontend (layouts, paleta de cores primárias/secundárias, tipografia e arranjos responsivos dos containers) e a lógica de componentes personalizados foram estruturados diretamente por mim.
* **Papel da Inteligência Artificial (Suporte e Automação)**: A IA foi empregada como ferramenta de aceleração para tarefas de alta repetitividade e baixo nível de decisão conceitual:
  * Escrita e parametrização de testes unitários repetitivos contra a interface do Flask.
  * Geração e preenchimento de dados mockados (fixtures) para suítes de validação de ponta a ponta.
  * Auxílio na escrita de código boilerplate de componentes visuais React já definidos.
  * Validações sintáticas e correções automáticas de tipagem estática (TypeScript).
  * Tarefas repetitivas e criação de componentes no REACT com ênfase estética (validação humana feita).
  * Implementações e correções de código (validação e testes feitos de forma humana)

---

## 6. Funcionalidades Implementadas / Não Implementadas

### A. Funcionalidades Obrigatórias (100% Implementadas)
* **Autenticação**:
  * Cadastro e login de usuários (e-mail e senha) com armazenamento seguro de hashes (`Bcrypt` com custo 12).
  * Sessão persistente via gravação e validação local de tokens JWT no `localStorage`.
  * Restrição rígida de rotas e ações para requisições não autenticadas.
* **Página Principal — Meus Arquivos**:
  * Tabela exibindo nome original do arquivo, tamanho formatado legível (Bytes, KB, MB) e data de upload localizada para o fuso horário da máquina do usuário.
  * Ações rápidas de download e exclusão de registros.
* **Upload de Arquivos**:
  * Formulário interativo no frontend com suporte a arrastar-e-soltar (Drag-and-Drop) e seletor.
  * Limitação estrita no frontend e backend para tamanho máximo de **10MB** e extensões permitidas (`.png`, `.jpg`, `.jpeg`, `.pdf`, `.txt`).
  * Feedback dinâmico de carregamento com barra de progresso em tempo real, mensagens de sucesso e erros detalhados.
* **Download de Arquivos**:
  * Validação de segurança que permite o download exclusivo de arquivos de propriedade do próprio usuário autenticado.
  * Implementação de streaming binário para otimização de banda e memória RAM.
* **Exclusão de Arquivos**:
  * Validação de propriedade do arquivo antes do processamento.
  * Estratégia de **soft delete** (marcação lógica `is_deleted = True` no banco de dados) combinada com a **deleção física imediata** no storage do servidor para liberação de espaço em disco.
* **Backend / API & Metadata**:
  * APIs modulares independentes para autenticação (`auth_server`) e controle de arquivos/recursos (`resurce_server`).
  * Modelagem de metadados completa contendo: `id` (UUID), `owner_id` (usuário), `original_name`, `storage_name` (chave única física), `content_type`, `size`, `created_at` e a flag de estado ativo (`is_deleted`).

### B. Pontos Extras (Bônus)
* **Preview de Imagens (Implementado)**: Botão **"Preview"** para arquivos de imagem, abrindo um visualizador em modal responsivo, centralizado e **móvel** (draggable) que pode ser movido pelo cabeçalho superior.
* **Download com Streaming (Implementado)**: Transferência binária feita em buffers de `8192 bytes` por geradores em Python direto ao cliente HTTP.
* **Implementação de Cache (Implementado)**: Geração de miniaturas (thumbnails) na escala `120x120px` mantida puramente em buffer RAM via Pillow, evitando escritas duplicadas no disco físico, além de políticas de cache estático via Nginx.
* **Abstração de Storage (Implementado)**: Persistência física baseada na interface abstrata `FileStorage`, deixando o código pronto para migração instantânea para provedores de nuvem (S3 ou MinIO) sem alterar a camada de aplicação.
* **Deploy da Aplicação (Não Implementado em Produção)**: A aplicação foi totalmente conteinerizada com Docker Compose Multi-Stage, restando apenas o deploy automatizado em provedores de nuvem em produção.
* **Versionamento de Arquivos e Links com Expiração (Não Implementado)**: Fora do escopo entregue.
