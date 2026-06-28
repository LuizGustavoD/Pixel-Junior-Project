# Servidor de Recursos (resurce_server)

Este microsservico e responsavel pela manipulacao de arquivos fisicos e armazenamento dos respectivos metadados no banco de dados.

---

## Arquitetura do Modulo

O servico segue a Arquitetura Limpa (Clean/Hexagonal Architecture) dividida em:

* **Domain (Dominio)**: Entidade de arquivo (`File`) e definicoes dos contratos abstratos de persistencia em banco de dados (`FileRepository`) e persistencia fisica em disco (`FileStorage`).
* **Application (Aplicacao)**: Implementa a logica de negocio por meio de casos de uso:
  * `UserUploadFileUseCase`: Processa o upload fisico e salva os metadados de propriedade.
  * `UserGetFileUseCase`: Recupera metadados e monta o gerador binario para downloads.
  * `UserGetThumbnailUseCase`: Processa a miniatura de imagens em tempo de execucao.
  * `UserDeleteFileUseCase`: Limpa os metadados do banco e remove o arquivo fisico.
* **Infrastructure (Infraestrutura)**:
  * `MySQLFileRepository`: Implementacao SQLAlchemy para persistencia no MySQL.
  * `LocalStorageService`: Implementacao de leitura e escrita fisica no disco rígido.
  * Decoradores de seguranca HTTP e validadores de tamanho e extensao.

---

## Decisoes Tecnicas

* **Processamento de Miniaturas com Pillow**: Para a extracao de miniaturas (thumbnails), o sistema le a imagem original do storage fisico e usa a biblioteca `Pillow` para redimensionar a imagem mantendo a proporcao em escala `120x120` pixels. O resultado e salvo temporariamente em um buffer de memoria `BytesIO` em formato JPEG, evitando gravacao de arquivos de miniatura adicionais no disco.
* **Leitura Iterativa de Arquivos**: O download e transmitido em buffers de `8192 bytes` por meio de geradores em Python. O Flask interpreta o generator e realiza o streaming diretamente ao cliente, contornando sobrecarga de memoria RAM no servidor em arquivos grandes de ate 10MB.
* **Filtro de Seguranca de Acesso**: Todo arquivo e verificado na camada do Caso de Uso para confirmar se o `owner_id` corresponde ao usuario logado. Tentativas de acessar arquivos que pertencem a outros usuarios resultam em `UnauthorizedFileAccessException` (retornando erro 403).
* **Particionamento por Usuario**: Os arquivos sao armazenados sob o caminho estruturado `data/users/<username>/<file_uuid>`. O `username` e recuperado dinamicamente em tempo de upload. Em suites de testes locais onde a tabela de usuarios nao existe, e aplicado um fallback utilizando o ID do usuario.

---

## Como Executar Localmente

### Usando o Ambiente Virtual do Python (Sem Docker)
1. Certifique-se de que possui o Python 3.11 instalado.
2. Navegue ate a pasta do servico:
   ```bash
   cd resurce_server
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
5. Configure as variaveis de ambiente locais (para desenvolvimento local):
   ```bash
   set DATABASE_URL=sqlite:///resource.db
   set UPLOAD_DIR=data
   set JWT_PUBLIC_KEY_PATH=../auth_server/resources/public_key.pem
   ```
6. Inicialize o servidor local:
   ```bash
   python app/main.py
   ```
   O servidor iniciara na porta 5001.

### Como Executar os Testes Unitarios
Execute o comando dentro da pasta do servico:
```bash
python -m unittest tests/test_resource_endpoints.py
```

---

## Funcionalidades Implementadas / Nao Implementadas

### Implementadas
* Endpoint de listagem de arquivos do usuario logado (`/files`).
* Endpoint de upload (`/files/upload`), com validacao de tamanho maximo (10MB) e tipos permitidos (.png, .jpg, .jpeg, .pdf, .txt).
* Endpoint de download streaming (`/files/download/<file_id>`).
* Endpoint de geracao e recuperacao de miniatura (`/files/thumbnail/<file_id>`).
* Endpoint de exclusao fisica e logica (`/files/delete/<file_id>`).
* Armazenamento particionado sob a pasta `users/<username>`.

### Nao Implementadas
* Compartilhamento de arquivos entre usuarios (fora do escopo de requisitos).
