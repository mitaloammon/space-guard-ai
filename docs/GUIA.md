# SPACE GUARD AI
## Guia de instalação, requisitos e execução local

### 1. Objetivo deste documento

Este documento apresenta os requisitos e procedimentos necessários para instalar, configurar e executar o SPACE GUARD AI localmente em um computador Windows.

A execução utiliza Docker, que permite iniciar o backend e o frontend em ambientes separados e organizados, sem exigir a instalação manual de todas as dependências de desenvolvimento no computador.

---

### 2. Requisitos para executar o projeto

#### 2.1. Requisitos de software

| Ferramenta | Finalidade |
|---|---|
| Windows 10 ou 11 | Sistema operacional recomendado para este guia. |
| Docker Desktop | Executar os serviços do projeto em containers. |
| Docker Compose | Construir e iniciar os serviços em conjunto. |
| Visual Studio Code | Editar arquivos e acompanhar o desenvolvimento. |
| Git | Clonar o repositório e controlar versões do código. |
| Navegador atualizado | Acessar a interface do sistema. |

**Importante:** para executar o projeto utilizando Docker, não é necessário instalar Python e Node.js diretamente no Windows. As dependências dessas tecnologias são instaladas nos respectivos containers, conforme os Dockerfiles do projeto.

#### 2.2. Configuração do Docker

O Docker Desktop deve estar instalado e em execução.

Recomenda-se utilizar o mecanismo baseado em WSL 2, caso disponível na instalação do Windows.

O Docker Compose também precisa estar disponível.

Para verificar a instalação, abra o PowerShell e execute:

```powershell
docker --version
docker compose version
```

Os comandos devem apresentar as versões instaladas.

Para verificar se o Docker está funcionando:

```powershell
docker info
```

Se o comando apresentar informações do servidor Docker sem erros, o ambiente estará pronto para receber os serviços.

#### 2.3. Requisitos de hardware

Recomenda-se:

- Computador com processador de 64 bits.
- Memória RAM suficiente para executar o Windows, Docker Desktop e os containers simultaneamente.
- Espaço livre em disco para o projeto, imagens Docker e dependências.
- Conexão com a internet durante a primeira compilação e instalação das dependências.

A necessidade de recursos pode variar conforme a configuração do Docker Desktop e os demais programas em execução.

---

### 3. Tecnologias utilizadas (Stack)

O SPACE GUARD AI utiliza as seguintes tecnologias:

| Tecnologia | Aplicação no projeto |
|---|---|
| Python 3.12+ | Linguagem principal do backend e processamento dos dados. |
| FastAPI | Construção da API e disponibilização dos serviços. |
| Pydantic | Validação e organização dos dados. |
| Uvicorn | Servidor responsável por executar a aplicação FastAPI. |
| Vue 3 | Construção da interface visual. |
| TypeScript | Tipagem e organização do código frontend. |
| Vite | Ferramenta de desenvolvimento e compilação do frontend. |
| Pinia | Gerenciamento de estado da interface, quando utilizado. |
| WebSocket | Comunicação e atualização de informações em tempo real. |
| Docker | Isolamento e execução dos serviços. |
| Docker Compose | Orquestração dos containers do projeto. |

#### Como as tecnologias trabalham juntas?

- O Python processa os dados da simulação e executa a lógica do monitoramento.
- O FastAPI disponibiliza as informações por meio de uma API.
- O WebSocket transmite atualizações para a interface.
- O Vue 3 apresenta os indicadores, alertas e controles da simulação.
- O Docker executa e integra os serviços.

---

### 4. Preparação do projeto

#### Passo 1 — Obter o código-fonte

Caso o projeto já esteja no computador, localize sua pasta.

Caso ainda não esteja, clone o repositório Git utilizando:

```powershell
git clone URL_DO_REPOSITORIO
```

Entre na pasta do projeto:

```powershell
cd space-guard-ai
```

O terminal deverá estar posicionado na raiz do projeto, onde se encontra o arquivo `docker-compose.yml`.

#### Passo 2 — Abrir o projeto no Visual Studio Code

Execute:

```powershell
code .
```

Isso abrirá a pasta atual no Visual Studio Code.

Também é possível abrir o VS Code manualmente e selecionar a pasta do projeto.

#### Passo 3 — Verificar os arquivos principais

Na raiz do projeto, verifique a presença dos seguintes arquivos e diretórios:

```text
space-guard-ai/
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── Dockerfile
│
├── docs/
│   └── SPECIFICATION.md
│
├── .env.example
├── .dockerignore
├── .gitignore
└── docker-compose.yml
```

Essa é a estrutura de referência do projeto. Alguns arquivos podem variar conforme a evolução da implementação.

#### Passo 4 — Verificar as configurações de ambiente

Na raiz do projeto, localize o arquivo `.env.example`.

Ele contém as configurações de exemplo previstas para a execução.

Caso o projeto exija um arquivo `.env`, crie uma cópia utilizando:

```powershell
Copy-Item .env.example .env
```

Confira os valores e ajuste somente as configurações necessárias.

Não compartilhe chaves de API ou credenciais em repositórios públicos.

Se a configuração atual não exigir variáveis adicionais, não invente valores para preencher o arquivo.

---

### 5. Executando o sistema com Docker

#### Passo 1 — Verificar a configuração do Docker Compose

Na raiz do projeto, execute:

```powershell
docker compose config
```

Esse comando verifica se a configuração do Docker Compose pode ser interpretada corretamente.

Para listar os serviços:

```powershell
docker compose config --services
```

Na configuração atual, são esperados os serviços:

- backend
- frontend

#### Passo 2 — Construir as imagens

Execute:

```powershell
docker compose build
```

O Docker irá preparar as imagens necessárias para executar os serviços.

Na primeira execução, esse processo pode demorar porque as imagens e dependências precisam ser baixadas.

#### Passo 3 — Iniciar o sistema

Execute:

```powershell
docker compose up -d
```

O parâmetro `-d` permite que os containers continuem executando em segundo plano.

Para construir as imagens e iniciar os serviços em um único comando, também é possível utilizar:

```powershell
docker compose up --build -d
```

#### Passo 4 — Verificar os containers

Execute:

```powershell
docker compose ps
```

Verifique se os serviços aparecem como ativos.

#### Passo 5 — Consultar os logs

Execute:

```powershell
docker compose logs --tail=100
```

Para acompanhar os logs continuamente:

```powershell
docker compose logs -f
```

Para sair da visualização contínua, pressione `Ctrl + C`. Isso não deve encerrar os containers.

---

### 6. Acessando o sistema

Após a inicialização dos serviços, utilize o navegador para acessar os endereços abaixo:

| Serviço | Endereço |
|---|---|
| Interface do sistema | http://localhost:5173 |
| Backend / API | http://localhost:8000 |
| Documentação da API | http://localhost:8000/docs |
| Verificação de saúde | http://localhost:8000/health |

Essas portas correspondem à configuração de referência atual. Caso sejam alteradas no Docker Compose, os endereços também deverão ser ajustados.

#### O que verificar?

**Interface:** a página do SPACE GUARD AI deve carregar e apresentar o painel de monitoramento.

**Documentação da API:** a página do FastAPI deve exibir os endpoints disponíveis.

**Health check:** o endpoint `/health` deve retornar uma resposta indicando a condição do serviço.

---

### 7. Como utilizar o sistema

Depois de acessar a interface, a demonstração pode seguir esta sequência:

**1. Painel de telemetria**

Visualize os indicadores simulados:

- Oxigênio.
- Pressão.
- Temperatura.
- Bateria.
- Radiação.
- Comunicação.

**2. Painel de controle da simulação**

Selecione um cenário predefinido ou altere manualmente os valores dos indicadores.

**3. Monitoramento de alertas**

Observe como o sistema identifica condições que ultrapassam os limites demonstrativos e apresenta alertas na interface.

**4. Atualização em tempo real**

Acompanhe as alterações dos indicadores e alertas transmitidas pelo WebSocket.

**5. Assistente inteligente**

Utilize a funcionalidade de assistência conversacional caso esteja implementada e configurada na versão executada.

---

### 8. Como encerrar ou reiniciar o sistema

Para parar os containers:

```powershell
docker compose stop
```

Para iniciar novamente os serviços já criados:

```powershell
docker compose start
```

Para encerrar e remover os containers da execução atual:

```powershell
docker compose down
```

Para reconstruir as imagens e iniciar novamente:

```powershell
docker compose up --build -d
```

**Atenção:** evite utilizar `docker compose down -v` sem necessidade. Essa opção também pode remover volumes associados aos serviços.

---

### 9. Solução de problemas comuns

**Problema: Docker não está em execução.**

Solução: abra o Docker Desktop, aguarde a inicialização e tente novamente.

**Problema: a porta 5173 ou 8000 já está sendo utilizada.**

Solução: verifique se outro processo está ocupando a porta ou ajuste o mapeamento no `docker-compose.yml`.

**Problema: o frontend não carrega.**

Solução: verifique os logs do serviço:

```powershell
docker compose logs frontend
```

**Problema: a API não responde.**

Solução: verifique os logs do backend:

```powershell
docker compose logs backend
```

**Problema: alterações no código não aparecem.**

Solução: verifique se os arquivos estão sendo compartilhados com os containers e se a configuração utiliza recarga automática. Caso necessário, reconstrua e reinicie os serviços.

---

### 10. Observações sobre o funcionamento

O SPACE GUARD AI é um protótipo de demonstração.

Os dados de telemetria utilizados representam condições simuladas e não correspondem a leituras reais de equipamentos espaciais.

Os limites utilizados para geração de alertas são demonstrativos e não devem ser interpretados como parâmetros operacionais oficiais da NASA.

O Docker é utilizado para facilitar a execução e integração dos componentes do projeto, enquanto Python, FastAPI, Vue 3 e WebSocket compõem a estrutura principal da aplicação.

A utilização de inteligência artificial depende da implementação e configuração do provedor correspondente. A presença da estrutura do assistente, isoladamente, não significa que exista integração funcional com um modelo externo.

### 11. Resumo da execução

A sequência básica para executar o projeto é:

```powershell
# 1. Entrar na pasta do projeto
cd C:\Users\MITALO\Desktop\space-guard-ai

# 2. Verificar os serviços
docker compose config --services

# 3. Construir e iniciar o sistema
docker compose up --build -d

# 4. Verificar os containers
docker compose ps

# 5. Consultar os logs
docker compose logs --tail=100
```

Depois, acessar:

`http://localhost:5173`

**Resultado esperado:** os serviços backend e frontend estarão executando em containers Docker, permitindo acessar a interface do SPACE GUARD AI e utilizar as funcionalidades disponíveis na versão instalada.