# Scripts de Automacao e Operacoes (DevOps)

Este diretorio contem utilitarios de automacao desenvolvidos para facilitar a inicializacao, encerramento e monitoramento local dos containers Docker que compoem a aplicacao Pixel Driver.

Todos os scripts possuem paridade de funcionalidade e estao disponiveis tanto em arquivos batch (`.bat`) para Windows quanto em shell scripts (`.sh`) para Linux e macOS.

---

## Catalogo de Ferramentas

### 1. Inicializacao da Stack (`start_services`)
* **Executaveis**: `start_services.bat` e `start_services.sh`
* **Operacao**: 
  1. Verifica a execucao do daemon do Docker na maquina hospedeira.
  2. Inicializa os containers em segundo plano executando o build das imagens (`docker compose up -d --build`).
  3. Monitora o healthcheck do banco MySQL (`auth_mysql_db`).
  4. Reinicia automaticamente as APIs de backend assim que o banco atinge o estado saudavel para evitar falhas de conexao no primeiro boot e criar o schema relacional corretamente.
* **Nota Windows**: Desabilita temporariamente o `DOCKER_BUILDKIT` durante o build para contornar problemas de compatibilidade e falhas de leitura em sistemas que utilizam pastas virtuais do OneDrive.

### 2. Parada da Stack (`stop_services`)
* **Executaveis**: `stop_services.bat` e `stop_services.sh`
* **Operacao**: Executa o encerramento seguro dos servicos, removendo containers, redes locais criadas e limpando os volumes de dados persistidos (`docker compose down -v`).

### 3. Visualizacao de Logs Interativa (`view_logs`)
* **Executaveis**: `view_logs.bat` e `view_logs.sh`
* **Operacao**: Fornece um menu interativo via terminal para que o desenvolvedor selecione qual container da stack deseja monitorar (`pixel_frontend_app`, `auth_server_app`, `resurce_server_app` ou `auth_mysql_db`) e o modo de visualizacao (ultimas 100 linhas ou acompanhamento continuo `-f`).

### 4. Inspecao de Containers Interativa (`inspect_container`)
* **Executaveis**: `inspect_container.bat` e `inspect_container.sh`
* **Operacao**: Interface interativa que permite selecionar um container ativo e imprimir suas configuracoes internas detalhadas de rede, variaveis de ambiente e montagens de volumes via comando `docker inspect`.

---

## Como Utilizar os Scripts

### No Windows (CMD ou PowerShell)
Os scripts bat executam nativamente na linha de comando do Windows.
```cmd
cd scripts
start_services.bat
```

### No Linux ou macOS (Bash/Zsh)
Antes do primeiro uso, conceda as devidas permissoes de execucao para os scripts da pasta:
```bash
chmod +x scripts/*.sh
./scripts/start_services.sh
```
