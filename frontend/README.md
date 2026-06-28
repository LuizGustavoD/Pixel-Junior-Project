# Cliente Frontend (pixel-driver)

Este modulo consiste na interface Single Page Application (SPA) construida em React, TypeScript e compilada com o Vite. O aplicativo exibe o painel de controle do Pixel Driver para interacao do usuario.

---

## Arquitetura do Modulo

A aplicacao foi arquitetada sob os principios de design limpo e modularizacao de componentes de UI reutilizaveis:

* **`src/components/ui/`**: Componentes atomicos e primitivos de interface (`Button`, `Input`, `Card`, `ProgressBar`, `ToastProvider`, `Modal`). Nao possuem acoplamento com a regra de negocio.
* **`src/components/`**: Componentes SaaS integrados com lógica e chamadas de servico (`LoginForm`, `RegisterForm`, `UploadForm`, `FileList`).
* **`src/services/`**: Camada de conexao com as APIs:
  * `api.ts`: Wrapper centralizado do `fetch` injetando headers JWT e realizando interceptacoes de erros 401.
  * `auth.ts`: Chamadas de login, cadastro e verificacao de sessao.
  * `files.ts`: Lógica de uploads com progresso de rede (XMLHttp), downloads e delecao.
* **`src/layouts/`**: Orquestracao de layout do painel de controle principal (`DashboardLayout`).

---

## Decisoes Tecnicas

* **Design System baseado em CSS Puro**: Desenvolvido um sistema de cores dinâmico usando variaveis de cores HSL em `index.css` baseado na marca original PixelBreeders (roxo `#754CE3`), com tipografia premium importada do Google Fonts (Outfit para titulos, Inter para corpo de texto), efeitos glassmorphism e micro-animacoes nativas de transicao.
* **Upload Progressivo com XMLHttpRequest**: A API Fetch do navegador nao possui suporte nativo para monitoramento de progresso de upload no cliente. Por esta razao, o servico de upload foi desenvolvido em `XMLHttpRequest` utilizando `xhr.upload.onprogress` para alimentar uma barra de progresso percentual dinâmica.
* **Pre-visualizacao Segura de Imagens**: Para evitar o carregamento nao autorizado de arquivos protegidos, o preview de imagens nao utiliza URLs diretas no atributo `src`. O frontend requisita a imagem via API trazendo-a como um `Blob` autenticado por Token JWT, converte o blob em um Object URL (`URL.createObjectURL(blob)`) e revoga a referencia (`URL.revokeObjectURL`) ao fechar o modal para evitar vazamento de memoria (memory leaks).
* **Nginx para Producao**: O container final e empacotado em Nginx Alpine. A configuracao de rotas direciona todas as requisicoes nao reconhecidas para o `index.html` (comportamento padrao SPA) e impede redirecionamentos erroneos em `/assets/` estaticos incompativeis.

---

## Como Executar Localmente

### Usando o Servidor de Desenvolvimento Local (Vite)
1. Certifique-se de ter o Node.js v18 ou superior instalado.
2. Navegue ate a pasta do projeto:
   ```bash
   cd frontend/pixel-driver
   ```
3. Instale as dependencias locais:
   ```bash
   npm install
   ```
4. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```
   A aplicacao estara disponivel em: http://localhost:5173

5. **Nota sobre integracoes:** Por padrao, ao rodar localmente fora do Docker, as URLs apontam para `http://localhost:5000` (Auth) e `http://localhost:5001` (Resources) conforme as constantes em `src/constants/api.ts`. Certifique-se de que os servidores locais estao ativos nessas portas.

### Como Compilar a Build de Producao
Para testar a compilacao estatica do Vite:
```bash
npm run build
```

---

## Funcionalidades Implementadas / Nao Implementadas

### Implementadas
* Formulario de Login e Registro com validacoes de campos e feedbacks especificos.
* Persistencia automatica de sessao do usuario autenticado.
* Painel principal com listagem de arquivos mostrando tamanho formatado e data do upload.
* Dropzone interativo para selecao e upload de arquivos com progresso percentual e barra de carregamento.
* Visualizador centralizado de imagens com botoes internos de download de blob e fechamento do modal.
* Favicon configurado para o arquivo `.ico` oficial da marca.
* Tratamento centralizado de toasts para eventos de informacao, erro e sucesso.

### Nao Implementadas
* Nao ha funcionalidades pendentes ou em desacordo com as especificacoes de requisitos.
