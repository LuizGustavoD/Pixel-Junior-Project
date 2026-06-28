# Estrategia e Infraestrutura de Testes

Este diretorio contem a suite de testes de integracao de ponta a ponta (E2E) e os scripts de orquestracao unificada para testes unitarios e de integracao do ecossistema Pixel Driver.

---

## Estrutura de Testes do Ecossistema

O plano de testes e dividido em duas categorias principais de validacao:

### 1. Testes Unitarios
Cada microsservico (`auth_server` e `resurce_server`) possui sua propria suite de testes isolada localizada em suas respectivas pastas `tests/`:
* **Isolamento de Estado**: Os testes de unidade utilizam um banco de dados SQLite em memoria (`sqlite:///:memory:`) para garantir idempotencia. A criacao do schema e o descarte dos dados (teardown) ocorrem a cada teste executado, impedindo vazamento de estado entre os cenarios de teste.
* **Mocks de Dependencias**: Servicos externos, como conexoes SMTP, chamadas HTTP de rede e acessos a disco sao mockados nas suites locais para garantir velocidade e execucao local deterministica.

### 2. Testes de Integracao (E2E)
Localizados neste diretorio ([test_integration.py](file:///c:/Users/luizd/OneDrive/Desktop/Junior_Project_Pixel/tests/test_integration.py)):
* **Escopo**: Simula o comportamento completo do fluxo de trabalho do usuario final contra os containers reais da aplicacao (MySQL, Auth Server e Resource Server) orquestrados pelo Docker Compose.
* **Fluxo Validado**:
  1. Cadastro e login de usuario.
  2. Geracao e verificacao assimetrica de tokens JWT.
  3. Upload de arquivos com validacao de tamanho e tipo.
  4. Escrita física e estruturada dos arquivos em disco (`data/users/<username>`).
  5. Download em streaming de arquivos autorizados.
  6. Geracao de miniaturas (thumbnails).
  7. Exclusao de arquivos e limpeza do storage fisico.

---

## Script Unificado de Execucao (Test Runner)

Para rodar toda a esteira de integracao continua localmente, foram disponibilizados scripts executaveis:
* **Windows**: `tests/run_unit_tests.bat`
* **Linux / macOS**: `tests/run_unit_tests.sh`

### Fluxo de Execucao do Runner
1. **Automated Setup**: O script verifica a existencia dos ambientes virtuais locais (`.venv`) em cada microsservico. Caso nao existam (ex: clonagem recente do repositorio), o runner cria os ambientes virtuais e instala as dependencias de forma automatica e silenciosa.
2. **Suite Unitria**: Executa os testes de unidade do `auth_server` e em seguida os do `resurce_server`. Se qualquer teste falhar, a execucao e abortada imediatamente.
3. **Orquestracao Docker**: Inicia os containers em segundo plano (`docker compose up -d --build`).
4. **Suite de Integracao**: Dispara o script `test_integration.py` contra as portas dos containers expostas na maquina hospedeira.
5. **Teardown**: Desliga e remove todos os containers, redes e volumes criados durante a etapa Docker, mantendo a maquina limpa.

### Como Executar os Testes

* **No Windows:**
  ```cmd
  tests\run_unit_tests.bat
  ```
* **No Linux ou macOS:**
  ```bash
  chmod +x tests/run_unit_tests.sh
  ./tests/run_unit_tests.sh
  ```
