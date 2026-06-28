# Pixel Driver - Plataforma de Armazenamento de Arquivos

Este projeto consiste em uma solucao corporativa para armazenamento, upload, download e gerenciamento de arquivos. A arquitetura e baseada em microsservicos/servicos orientados a contexto, encapsulada e orquestrada de forma nativa por meio do Docker.

---

## Arquitetura do Sistema

O ecossistema e estruturado em tres modulos principais de responsabilidade unica:

1. **Servidor de Autenticacao (auth_server)**: Servico responsavel pela identidade, cadastro e login de usuarios, alem da emissao de sessoes criptografadas via JWT.
2. **Servidor de Recursos (resurce_server)**: Servico voltado ao armazenamento fisico de arquivos e indexacao de metadados no banco de dados. Realiza a validacao de permissoes e seguranca em nivel de usuario.
3. **Cliente Web (frontend)**: Aplicacao Single Page Application (SPA) construida em React + Vite, empacotada em servidor web Nginx para distribuicao de alta performance de ativos estaticos.

O banco de dados utilizado e o MySQL, compartilhado entre os microsservicos para permitir integridade de chaves estrangeiras de propriedade do arquivo.

---

## Decisoes Tecnicas

* **Criptografia Assimetrica para JWT**: O Servidor de Autenticacao assina os tokens de sessao utilizando uma chave privada RSA de 2048 bits. O Servidor de Recursos valida esses tokens localmente de forma assimetrica usando a respectiva chave publica, sem a necessidade de realizar chamadas REST de validacao adicionais ao Servidor de Autenticacao. Isso desacopla os servicos e reduz a latencia de rede.
* **Streaming de Downloads**: A entrega de arquivos grandes e feita por meio de streaming direto do sistema de arquivos para a conexao de rede do cliente, dividindo o envio em buffers de 8192 bytes. Essa estrategia evita o carregamento do arquivo completo na memoria RAM do Servidor de Recursos, garantindo escalabilidade.
* **Separacao de Bancos por Contexto de Execucao**: A stack em producao roda sobre o MySQL. No entanto, para garantir velocidade e isolamento absoluto durante a suite de testes unitarios locais, o sistema faz transicao automatica para o SQLite em memoria (`sqlite:///:memory:`).
* **Nginx como Servidor de Producao**: O frontend e compilado estaticamente em Docker e servido pelo Nginx com roteamento SPA ativo (fallback de rotas desconhecidas para o index.html). Foi implementada uma regra especifica para ativos na pasta `/assets/` para prevenir falso-positivo de fallback em arquivos estaticos inexistentes.
* **Subdiretorios Organizacionais**: O storage do Servidor de Recursos armazena fisicamente os uploads dentro de subdiretorios particionados por usuario (`data/users/<username>/`), evitando a degradacao de performance de indexacao do sistema de arquivos em cenarios com alto volume de dados na raiz do diretorio.

---

## Como Executar o Projeto

### Pre-requisitos
* Docker e Docker Compose instalados no sistema operacional.

### Metodo Recomendado (Docker Compose em Comando Unico)
A stack completa pode ser inicializada e configurada com apenas um comando executado na raiz do projeto:
```bash
docker compose up -d --build
```
Para inicializacao automatica com resolucao de conflitos de volumes, seguranca do Windows contra OneDrive e sincronizacao automatica de schemas de banco, recomenda-se a utilizacao dos scripts na pasta `scripts/`:

* **No Windows (cmd ou powershell):**
  ```cmd
  scripts\start_services.bat
  ```
* **No Linux ou macOS:**
  ```bash
  chmod +x scripts/*.sh
  ./scripts/start_services.sh
  ```

A aplicacao estara disponivel nas seguintes portas:
* **Frontend Web:** http://localhost:3000
* **API do Servidor de Autenticacao:** http://localhost:5000
* **API do Servidor de Recursos:** http://localhost:5001

Para parar e limpar a stack:
* **No Windows:** execute `scripts\stop_services.bat`
* **No Linux/macOS:** execute `./scripts/stop_services.sh`

---

## Funcionalidades Implementadas / Nao Implementadas

### Implementadas
* **Autenticacao**: Cadastro e login de usuarios por e-mail e senha, com persistencia de sessao automatica no LocalStorage do navegador.
* **Meus Arquivos**: Listagem completa dos arquivos do usuario com nome original, tamanho formatado e data do upload.
* **Acoes**: Download em streaming e exclusao fisica imediata no sistema de arquivos e banco de dados.
* **Upload**: Drag-and-drop de arquivos no formulario do frontend com barra de progresso em tempo real e tratamento de erros.
* **Restricoes**: Bloqueio de tamanho maximo de 10MB no frontend e backend, limite de formatos permitidos (.png, .jpg, .jpeg, .pdf, .txt) e bloqueio de acesso a arquivos de terceiros.
* **Visualizacao**: Preview centralizado na tela de arquivos do tipo imagem com barra de acao interna para download e fechamento.
* **Paginas de Erro Customizadas**: Nginx estruturado para responder com layouts personalizados do Pixel Driver em erros 403, 404 e 500.

### Nao Implementadas
* Nao ha funcionalidades pendentes ou fora de conformidade com a especificacao original de requisitos fornecida.
