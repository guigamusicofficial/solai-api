# Documento de Arquitetura e Escopo — Projeto Sol AI

## 1. Visão Geral

O projeto Sol AI tem como objetivo oferecer uma companheira virtual personalizada, com personalidade definida, memória contínua e capacidade de manter conversa consistente ao longo do tempo. A proposta do sistema é combinar interface web, backend em Python e integrações de IA para produzir uma experiência envolvente e adaptada ao perfil do usuário.

A arquitetura do projeto foi pensada para separar claramente:

- camada visual e interativa;
- camada de lógica operacional e orquestração;
- camada de persistência e memória;
- camada de integração com modelos de linguagem.

## 2. Objetivo do Projeto

O objetivo principal é criar uma experiência de IA com:

- personalidade forte e identificável;
- memória persistente do usuário;
- contexto de relacionamento e preferências;
- respostas mais naturais e menos mecânicas;
- integração com modelos externos para maior flexibilidade de resposta.

## 3. Arquitetura em 3 Pilares

### 3.1 Frontend — Interface Visual

Localização esperada: pasta web.

Responsabilidades:

- servir a interface web em HTML, CSS e JavaScript;
- receber as mensagens do usuário;
- enviar as mensagens para o backend;
- exibir respostas em tempo real.

Tecnologias previstas:

- HTML5
- CSS3
- JavaScript moderno
- comunicação via fetch para API REST

### 3.2 Backend — Lógica e Orquestração

Localização esperada: pasta src ou raiz do projeto.

Responsabilidades:

- receber solicitações HTTP do frontend;
- montar o contexto da conversa;
- carregar informações de memória e histórico;
- aplicar instruções de personalidade;
- enviar payload para a API de IA;
- devolver a resposta para o cliente.

Tecnologias previstas:

- Python
- http.server / FastAPI / HTTPServer
- OpenAI SDK ou integração com API compatível
- gerenciamento de variáveis de ambiente

### 3.3 Persistência — Memória e Histórico

Localização esperada: pasta data ou banco externo.

Responsabilidades:

- guardar informações do usuário;
- manter preferências, memorias e contexto;
- preservar histórico de conversas;
- permitir continuidade de relacionamento e consistência da personalidade.

Estratégias possíveis:

- arquivos JSON locais para prototipagem;
- PostgreSQL em Supabase para produção;
- migração de memória local para banco remoto.

## 4. Motores de IA e Integração

O sistema pode usar múltiplas rotas de IA, dependendo da estratégia de deploy e do ambiente operacional.

### 4.1 Motor principal via API customizada

A configuração de ambiente pode apontar para um endpoint externo de modelos de linguagem, por exemplo:

- OPENAI_BASE_URL
- OPENAI_API_KEY

Esse endpoint atua como ponte para o modelo principal usado pela aplicação.

### 4.2 Motor alternativo / fallback

Em cenários com necessidade de contingência, o projeto pode incluir integrações alternativas ou serviços de proxy que permitam:

- tentar modelo principal;
- capturar falhas de conexão;
- rotear requisição para fallback;
- manter a experiência contínua.

### 4.3 Prompt e personalidade

O comportamento da IA é reforçado por prompts de personalidade e contexto, especialmente em arquivos como:

- src/personality.py
- src/config.py
- src/main.py

Esses prompts controlam:

- tom da conversa;
- estilo de resposta;
- regras de relacionamento;
- prioridade de memória;
- padronização de respostas.

## 5. Estrutura de Diretórios

A estrutura ideal do projeto deve seguir uma divisão clara:

- src/ — código principal da aplicação
- data/ — arquivos persistidos em JSON ou dados temporários
- web/ — frontend estático
- legacy/ — versões antigas e experimentos
- backups/ — cópias de segurança
- docs/ — documentação técnica e de arquitetura

## 6. Fluxo do Sistema

1. O usuário envia uma mensagem pela interface web.
2. O frontend envia a mensagem ao backend.
3. O backend carrega o contexto relevante.
4. O backend aplica personalidade e regras de memória.
5. O backend envia o prompt e histórico para a API de IA.
6. A IA responde com texto natural.
7. A resposta retorna ao frontend.
8. O histórico e a memória são persistidos.

## 7. Requisitos de Persistência

Para operação estável, o sistema precisa manter:

- histórico de mensagens;
- nome do usuário;
- preferências e interesses;
- contexto de relacionamento;
- dados do perfil do personagem.

Isso favorece continuidade e personalização, especialmente em aplicações conversacionais.

## 8. Pontos de Melhoria e Próximos Passos

### 8.1 Migração para banco persistente

A integração com banco de dados deve substituir lógica local baseada em arquivos JSON por consultas a um banco externo, como PostgreSQL no Supabase.

Objetivos:

- evitar perda de memória em reinícios;
- permitir consulta eficiente do histórico;
- manter dados centralizados e seguros;
- preparar a aplicação para produção.

### 8.2 Organização por módulos

A aplicação deve seguir separação entre:

- configuração;
- memória;
- personalidade;
- geração de resposta;
- banco de dados;
- frontend.

Isso facilita manutenção, testes e evolução do projeto.

### 8.3 Refinamento de prompt e comportamento

O prompt do personagem deve ser ajustado para manter:

- consistência de personalidade;
- contexto de usuário;
- resposta natural e envolvente;
- regras claras de memória e relacionamento.

## 9. Conclusão

O projeto Sol AI tem uma arquitetura modular e flexível, desenhada para evoluir de protótipo para sistema mais robusto e persistente. A organização atual separa código, dados, web e versões antigas, o que melhora manutenção e reduz risco de erros. O próximo passo estratégico é consolidar a persistência em banco de dados e estabilizar o fluxo de comunicação entre frontend, backend e IA.
