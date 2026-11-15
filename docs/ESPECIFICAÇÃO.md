# SPACE GUARD AI
## Documento de apresentação e visão geral do sistema

### 1. O que é o SPACE GUARD AI?

O SPACE GUARD AI é um protótipo de assistente inteligente desenvolvido para auxiliar astronautas durante atividades e missões espaciais, por meio do monitoramento de informações relacionadas às condições do traje e do ambiente da missão.

A proposta é disponibilizar informações importantes de maneira clara, identificar condições anormais e oferecer assistência contextual ao astronauta.

### 2. Qual é a finalidade do sistema?

O objetivo principal é demonstrar como a inteligência artificial, o monitoramento de dados e a automação podem trabalhar juntos para auxiliar o astronauta.

O sistema foi concebido para:

- Monitorar informações relacionadas às condições da missão.
- Acompanhar indicadores como oxigênio, pressão, temperatura, bateria e radiação.
- Identificar alterações que ultrapassem limites de demonstração configurados.
- Gerar alertas para chamar a atenção do astronauta.
- Disponibilizar um assistente inteligente para explicar informações e fornecer orientações contextuais.
- Apresentar os dados de maneira organizada em uma interface visual.

### 3. Como o sistema funciona?

O funcionamento pode ser compreendido em cinco etapas:

**1. Coleta de informações**

O sistema recebe dados simulados que representam os indicadores monitorados durante uma missão espacial.

**2. Processamento e monitoramento**

Os dados são processados pelo sistema, que acompanha suas alterações e verifica se existem condições fora dos limites configurados para a demonstração.

**3. Identificação de situações anormais**

Quando um parâmetro ultrapassa determinado limite, o mecanismo de monitoramento identifica a condição e gera um alerta correspondente.

**4. Apresentação das informações**

Os indicadores e alertas são apresentados na interface visual, com atualizações em tempo real.

**5. Assistência inteligente**

A proposta do assistente é interpretar o contexto da missão, explicar alertas e fornecer informações relevantes ao astronauta.

### 4. Principais funcionalidades

**Painel de telemetria**

Apresenta os principais indicadores monitorados:

- Oxigênio: disponibilidade simulada de oxigênio.
- Pressão: pressão simulada do ambiente ou traje, conforme a configuração.
- Temperatura: temperatura monitorada na simulação.
- Bateria: nível de energia disponível.
- Radiação: taxa simulada de exposição à radiação.
- Comunicação: estado da conexão simulada.

**Painel de controle da simulação**

Permite testar o comportamento do sistema de duas maneiras:

- Selecionando cenários predefinidos, como baixa disponibilidade de oxigênio, temperatura elevada e falha de comunicação.
- Alterando manualmente os valores dos indicadores para simular diferentes condições.

**Sistema de alertas**

Identifica condições anormais e apresenta alertas correspondentes na interface, permitindo acompanhar situações que exigem atenção.

**Assistente inteligente**

Tem como finalidade auxiliar o astronauta na compreensão das informações da missão, explicando alertas e oferecendo respostas contextuais.

### 5. Tecnologias utilizadas

O projeto utiliza tecnologias que trabalham em conjunto para processar os dados, executar o monitoramento e apresentar as informações.

- **Python:** responsável pela lógica principal e pelo processamento dos dados.
- **FastAPI:** responsável pela comunicação entre os serviços e disponibilização das informações.
- **Vue 3 e TypeScript:** utilizados na construção da interface visual do sistema.
- **WebSocket:** permite transmitir atualizações de telemetria e alertas em tempo real.
- **Docker:** organiza e executa os componentes do projeto em ambientes isolados.

### 6. Como executar o sistema?

O projeto utiliza Docker para facilitar sua execução.

Na pasta principal do projeto, basta abrir o terminal e executar:

`docker compose up --build`

Após a inicialização dos serviços, a interface pode ser acessada pelo navegador:

`http://localhost:5173`

A documentação da API também pode ser consultada em:

`http://localhost:8000/docs`

### 7. Aplicação prática e demonstração

Durante uma demonstração, é possível iniciar a simulação em condições normais, acompanhar os indicadores e, em seguida, selecionar um cenário ou alterar manualmente um parâmetro.

Por exemplo, ao elevar a temperatura simulada acima do limite configurado, o sistema identifica a condição e apresenta um alerta na interface.

Esse processo demonstra a integração entre simulação, processamento de dados, monitoramento e comunicação em tempo real.

### 8. Limitações e evolução

O SPACE GUARD AI está sendo desenvolvido como um protótipo demonstrativo.

Atualmente, os indicadores são simulados. O projeto não está conectado a sensores reais de trajes espaciais, não possui integração operacional com equipamentos de astronautas e não representa um sistema certificado pela NASA.

A integração com fontes públicas de dados espaciais e a evolução do assistente inteligente são possibilidades de desenvolvimento, respeitando a distinção entre informações científicas externas e dados utilizados para monitoramento.

### 9. Resumo do projeto

O SPACE GUARD AI busca demonstrar como um assistente inteligente pode apoiar o astronauta por meio do monitoramento de dados, identificação de condições anormais, geração de alertas e disponibilização de informações contextuais.

Sua proposta central é reunir monitoramento, automação e inteligência artificial em uma interface de fácil utilização, contribuindo para a consciência situacional durante uma missão espacial.