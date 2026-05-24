# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Você deve entregar um software capaz de:

1. **Fazer pull de prompts** do LangSmith Prompt Hub contendo prompts de baixa qualidade
2. **Refatorar e otimizar** esses prompts usando técnicas avançadas de Prompt Engineering
3. **Fazer push dos prompts otimizados** de volta ao LangSmith
4. **Avaliar a qualidade** através de métricas customizadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
5. **Atingir pontuação mínima** de 0.9 (90%) em todas as métricas de avaliação

---

## Exemplo no CLI

**Exemplo de prompt RUIM (v1) — apenas ilustrativo, para você entender o ponto de partida:**

```
==================================================
Prompt: {seu_username}/bug_to_user_story_v1
==================================================

Métricas Derivadas:
  - Helpfulness: 0.45 ✗
  - Correctness: 0.52 ✗

Métricas Base:
  - F1-Score: 0.48 ✗
  - Clarity: 0.50 ✗
  - Precision: 0.46 ✗

❌ STATUS: REPROVADO
⚠️  Métricas abaixo de 0.9: helpfulness, correctness, f1_score, clarity, precision
```

**Exemplo de prompt OTIMIZADO (v2) — seu objetivo é chegar aqui:**

```bash
# Após refatorar os prompts e fazer push
python src/push_prompts.py

# Executar avaliação
python src/evaluate.py

Executando avaliação dos prompts...
==================================================
Prompt: {seu_username}/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.94 ✓
  - Correctness: 0.96 ✓

Métricas Base:
  - F1-Score: 0.93 ✓
  - Clarity: 0.95 ✓
  - Precision: 0.92 ✓

✅ STATUS: APROVADO - Todas as métricas >= 0.9
```
---

## Tecnologias obrigatórias

- **Linguagem:** Python 3.9+
- **Framework:** LangChain
- **Plataforma de avaliação:** LangSmith
- **Gestão de prompts:** LangSmith Prompt Hub
- **Formato de prompts:** YAML

---

## Pacotes recomendados

```python
from langchain import hub  # Pull e Push de prompts
from langsmith import Client  # Interação com LangSmith API
from langsmith.evaluation import evaluate  # Avaliação de prompts
from langchain_openai import ChatOpenAI  # LLM OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # LLM Gemini
```

---

## OpenAI

- Crie uma **API Key** da OpenAI: https://platform.openai.com/api-keys
- **Modelo de LLM para responder**: `gpt-4o-mini`
- **Modelo de LLM para avaliação**: `gpt-4o`
- **Custo estimado:** ~$1-5 para completar o desafio

## Gemini (modelo free)

- Crie uma **API Key** da Google: https://aistudio.google.com/app/apikey
- **Modelo de LLM para responder**: `gemini-2.5-flash`
- **Modelo de LLM para avaliação**: `gemini-2.5-flash`
- **Limite:** 15 req/min, 1500 req/dia

---

## Requisitos

### 1. Pull do Prompt inicial do LangSmith

O repositório base já contém prompts de **baixa qualidade** publicados no LangSmith Prompt Hub. Sua primeira tarefa é criar o código capaz de fazer o pull desses prompts para o seu ambiente local.

**Tarefas:**

1. Configurar suas credenciais do LangSmith no arquivo `.env` (conforme o arquivo `.env.example`)
2. Implementar o script `src/pull_prompts.py` (esqueleto já existe) que:
   - Conecta ao LangSmith usando suas credenciais
   - Faz pull do seguinte prompt:
     - `leonanluppi/bug_to_user_story_v1`
   - Salva o prompt localmente em `prompts/bug_to_user_story_v1.yml`

---

### 2. Otimização do Prompt

Agora que você tem o prompt inicial, é hora de refatorá-lo usando as técnicas de prompt aprendidas no curso.

**Tarefas:**

1. Analisar o prompt em `prompts/bug_to_user_story_v1.yml`
2. Criar um novo arquivo `prompts/bug_to_user_story_v2.yml` com suas versões otimizadas
3. Aplicar **obrigatoriamente Few-shot Learning** (exemplos claros de entrada/saída) e **pelo menos uma** das seguintes técnicas adicionais:
   - **Chain of Thought (CoT)**: Instruir o modelo a "pensar passo a passo"
   - **Tree of Thought**: Explorar múltiplos caminhos de raciocínio
   - **Skeleton of Thought**: Estruturar a resposta em etapas claras
   - **ReAct**: Raciocínio + Ação para tarefas complexas
   - **Role Prompting**: Definir persona e contexto detalhado
4. Documentar no `README.md` quais técnicas você escolheu e por quê

**Requisitos do prompt otimizado:**

- Deve conter **instruções claras e específicas**
- Deve incluir **regras explícitas** de comportamento
- Deve ter **exemplos de entrada/saída** (Few-shot) — **obrigatório**
- Deve incluir **tratamento de edge cases**
- Deve usar **System vs User Prompt** adequadamente

---

### 3. Push e Avaliação

Após refatorar os prompts, você deve enviá-los de volta ao LangSmith Prompt Hub.

**Tarefas:**

1. Implementar o script `src/push_prompts.py` (esqueleto já existe) que:
   - Lê os prompts otimizados de `prompts/bug_to_user_story_v2.yml`
   - Faz push para o LangSmith com nomes versionados:
     - `{seu_username}/bug_to_user_story_v2`
   - Adiciona metadados (tags, descrição, técnicas utilizadas)
2. Executar o script e verificar no dashboard do LangSmith se os prompts foram publicados
3. Deixá-lo público

---

### 4. Iteração

- Espera-se 3-5 iterações.
- Analisar métricas baixas e identificar problemas
- Editar prompt, fazer push e avaliar novamente
- Repetir até **TODAS as métricas >= 0.9**

### Critério de Aprovação:

```
- Helpfulness >= 0.9
- Correctness >= 0.9
- F1-Score >= 0.9
- Clarity >= 0.9
- Precision >= 0.9

MÉDIA das 5 métricas >= 0.9
```

**IMPORTANTE:** TODAS as 5 métricas devem estar >= 0.9, não apenas a média!

### 5. Testes de Validação

**O que você deve fazer:** Edite o arquivo `tests/test_prompts.py` e implemente, no mínimo, os 6 testes abaixo usando `pytest`:

- `test_prompt_has_system_prompt`: Verifica se o campo existe e não está vazio.
- `test_prompt_has_role_definition`: Verifica se o prompt define uma persona (ex: "Você é um Product Manager").
- `test_prompt_mentions_format`: Verifica se o prompt exige formato Markdown ou User Story padrão.
- `test_prompt_has_few_shot_examples`: Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
- `test_prompt_no_todos`: Garante que você não esqueceu nenhum `[TODO]` no texto.
- `test_minimum_techniques`: Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas.

**Como validar:**

```bash
pytest tests/test_prompts.py
```

---

## Estrutura obrigatória do projeto

Faça um fork do repositório base: **[Clique aqui para o template](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt)**

```
mba-ia-pull-evaluation-prompt/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Sua documentação do processo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml  # Prompt inicial (já incluso)
│   └── bug_to_user_story_v2.yml  # Seu prompt otimizado (criar)
│
├── datasets/
│   └── bug_to_user_story.jsonl   # 15 exemplos de bugs (já incluso)
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith (implementar)
│   ├── push_prompts.py       # Push ao LangSmith (implementar)
│   ├── evaluate.py           # Avaliação automática (pronto)
│   ├── metrics.py            # 5 métricas implementadas (pronto)
│   └── utils.py              # Funções auxiliares (pronto)
│
├── tests/
│   └── test_prompts.py       # Testes de validação (implementar)
│
```

**O que você deve implementar:**

- `prompts/bug_to_user_story_v2.yml` — Criar do zero com seu prompt otimizado
- `src/pull_prompts.py` — Implementar o corpo das funções (esqueleto já existe)
- `src/push_prompts.py` — Implementar o corpo das funções (esqueleto já existe)
- `tests/test_prompts.py` — Implementar os 6 testes de validação (esqueleto já existe)
- `README.md` — Documentar seu processo de otimização

**O que já vem pronto (não alterar):**

- `src/evaluate.py` — Script de avaliação completo
- `src/metrics.py` — 5 métricas implementadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
- `src/utils.py` — Funções auxiliares
- `datasets/bug_to_user_story.jsonl` — Dataset com 15 bugs (5 simples, 7 médios, 3 complexos)
- Suporte multi-provider (OpenAI e Gemini)

## Repositórios úteis

- [Repositório boilerplate do desafio](https://github.com/devfullcycle/mba-ia-prompt-engineering)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## VirtualEnv para Python

Crie e ative um ambiente virtual antes de instalar dependências:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Ordem de execução

### 1. Executar pull dos prompts ruins

```bash
python src/pull_prompts.py
```

### 2. Refatorar prompts

Edite manualmente o arquivo `prompts/bug_to_user_story_v2.yml` aplicando as técnicas aprendidas no curso.

### 3. Fazer push dos prompts otimizados

```bash
python src/push_prompts.py
```

### 4. Executar avaliação

```bash
python src/evaluate.py
```

---

## Entregável

1. **Repositório público no GitHub** (fork do repositório base) contendo:

   - Todo o código-fonte implementado
   - Arquivo `prompts/bug_to_user_story_v2.yml` 100% preenchido e funcional
   - Arquivo `README.md` atualizado com:

2. **README.md deve conter:**

   A) **Seção "Técnicas Aplicadas (Fase 2)"**:

   - Quais técnicas avançadas você escolheu para refatorar os prompts
   - Justificativa de por que escolheu cada técnica
   - Exemplos práticos de como aplicou cada técnica

   B) **Seção "Resultados Finais"**:

   - Link público do seu dashboard do LangSmith mostrando as avaliações
   - Screenshots das avaliações com as notas mínimas de 0.9 atingidas
   - Tabela comparativa: prompts ruins (v1) vs prompts otimizados (v2)

   C) **Seção "Como Executar"**:

   - Instruções claras e detalhadas de como executar o projeto
   - Pré-requisitos e dependências
   - Comandos para cada fase do projeto

3. **Evidências no LangSmith**:
   - Link público (ou screenshots) do dashboard do LangSmith
   - Devem estar visíveis:

     - Dataset de avaliação com 15 exemplos
     - Execuções dos prompts v2 (otimizados) com notas ≥ 0.9
     - Tracing detalhado de pelo menos 3 exemplos

---

## Dicas Finais

- **Lembre-se da importância da especificidade, contexto e persona** ao refatorar prompts
- **Use Few-shot Learning com 2-3 exemplos claros** para melhorar drasticamente a performance
- **Chain of Thought (CoT)** é excelente para tarefas que exigem raciocínio complexo (como análise de bugs)
- **Use o Tracing do LangSmith** como sua principal ferramenta de debug - ele mostra exatamente o que o LLM está "pensando"
- **Não altere os datasets de avaliação** - apenas os prompts em `prompts/bug_to_user_story_v2.yml`
- **Itere, itere, itere** - é normal precisar de 3-5 iterações para atingir 0.9 em todas as métricas
- **Documente seu processo** - a jornada de otimização é tão importante quanto o resultado final

## A) Técnicas utilizadas

Durante o desenvolvimento do prompt, percebi que apenas ter uma estrutura bem escrita não era suficiente para atingir o score mínimo de **0,90** exigido pelos validadores (`evaluate` e `metrics`). O prompt inicial já produzia User Stories razoáveis, porém ainda apresentava problemas de consistência, precisão e aderência semântica ao comportamento esperado pelos avaliadores. Por isso, precisei realizar ajustes progressivos e combinar diferentes técnicas de Prompt Engineering para tornar a saída mais previsível, objetiva e consistente.

O primeiro passo foi garantir o atendimento dos critérios obrigatórios do desafio. O teste exigia o uso de **Few-Shot Learning** e pelo menos uma técnica avançada adicional. Inicialmente eu utilizava apenas **Chain of Thought (CoT)**, mas percebi que isso não era suficiente para estabilizar as métricas. Assim, mantive o CoT e complementei o prompt com **Skeleton of Thought (SoT)**, **Role Prompting** e uma estrutura rigidamente controlada (**Structured Output**). O objetivo foi reduzir ambiguidades e aumentar previsibilidade.

Em seguida, reforcei o **Role Prompting**, definindo explicitamente o modelo como um:

 *Product Owner técnico sênior especializado em refinamento de bugs e escrita de User Stories ágeis.*

Esse ajuste fez diferença porque as respostas passaram a ter linguagem mais técnica, objetiva e acionável, reduzindo respostas excessivamente genéricas ou conversacionais e tornando o output mais próximo do esperado por um time de desenvolvimento.

Depois disso, implementei um **Chain of Thought interno**, mas com um detalhe importante: o raciocínio não deveria aparecer na resposta final. Ou seja, o modelo passou a “pensar passo a passo” internamente antes de responder, seguindo um fluxo obrigatório:

1. Identificar se o bug era simples, médio ou complexo;
2. Escolher a estrutura correta da resposta;
3. Aplicar regras do guia de adaptação;
4. Revisar se todas as informações relevantes do relato foram preservadas.

Essa mudança ajudou principalmente na consistência e na métrica de **Correctness**, porque reduziu respostas incoerentes ou incompletas.

Outro ajuste importante foi a implementação do **Skeleton of Thought (SoT)**. Antes disso, o prompt utilizava praticamente a mesma estrutura para qualquer bug, gerando respostas excessivas em alguns casos e insuficientes em outros. Então, passei a classificar os bugs em três níveis:

* **SIMPLES**
* **MÉDIO**
* **COMPLEXO**

Cada categoria passou a ter uma estrutura própria de saída.

* **SIMPLES:** User Story + critérios de aceitação objetivos
* **MÉDIO:** inclusão de contexto técnico e critérios adicionais quando necessário
* **COMPLEXO:** estrutura detalhada com múltiplas seções, como critérios técnicos, contexto do bug e tasks sugeridas

Esse ajuste melhorou significativamente a clareza da resposta e reduziu ruído textual.

Também ampliei o uso de **Few-Shot Learning**. O prompt inicial tinha poucos exemplos e pouca variedade de cenários. Para melhorar a aderência semântica das respostas, incluí diversos exemplos representativos, como:

* falha em botões de interface;
* validação incorreta de formulários;
* inconsistência em dashboards;
* lentidão de relatórios;
* falhas de webhook e APIs;
* race condition;
* estoque no checkout;
* modal mobile;
* Android ANR;
* bugs complexos com múltiplos problemas.

Além da variedade, os exemplos passaram a conter entradas mais realistas, critérios Given/When/Then (GWT) e contexto técnico detalhado, aumentando a similaridade entre exemplos e saídas geradas.

Outro ponto implementado foi um **Guia de Adaptação**, que funcionava como um mecanismo de padronização para bugs recorrentes. Percebi que existiam padrões de comportamento repetidos em cenários como webhook, dashboard, modal mobile, checkout e relatórios lentos. Então passei a definir explicitamente:

* persona esperada;
* objetivo esperado da User Story;
* critérios de aceite sugeridos;
* comportamentos esperados por categoria.

Isso reduziu a variabilidade das respostas e aumentou a estabilidade do modelo.

Também precisei controlar a tendência do modelo de “inventar” contexto técnico. Para isso, adicionei regras explícitas, como:

* não inventar tecnologias, endpoints ou arquitetura;
* não assumir browser, API ou banco de dados não mencionados;
* não inferir comportamentos inexistentes;
* não citar IDs específicos do relato nos critérios GWT;
* responder apenas com a User Story formatada;
* restringir estruturas complexas apenas a cenários realmente complexos.

Por fim, padronizei os **critérios de aceitação** utilizando o modelo **Given / When / Then (GWT)**, tornando-os mais testáveis e observáveis. Antes disso, muitos critérios eram vagos e pouco verificáveis. Após a mudança, passaram a seguir uma estrutura clara:

> Dado que estou visualizando um produto
> Quando clico em “Adicionar ao Carrinho”
> Então o produto deve ser adicionado ao carrinho

Essa padronização melhorou a qualidade semântica das respostas e reduziu critérios genéricos.

---

## B) Resultados finais

Após os refinamentos, o prompt passou de uma solução funcional, porém inconsistente, para um comportamento muito mais previsível e alinhado ao que os validadores automáticos esperavam.

O principal aprendizado foi perceber que não bastava gerar uma “boa User Story”; era necessário gerar uma resposta semanticamente consistente, estruturada e altamente aderente aos critérios das métricas automáticas.

Os ajustes realizados trouxeram ganhos importantes:

* aumento da **Correctness**, devido ao raciocínio interno e redução de inferências indevidas;
* melhora da **Clarity**, por meio da classificação de complexidade e organização da resposta;
* aumento da **Precision**, reduzindo ambiguidades e excesso de criatividade;
* melhora da **Helpfulness**, com critérios de aceite mais objetivos e acionáveis;
* aumento do **F1-score**, graças à maior proximidade semântica entre relato, exemplos e resposta gerada.

O ganho mais significativo veio da combinação das técnicas utilizadas:

> **Few-Shot Learning + Chain of Thought interno + Skeleton of Thought + Role Prompting + regras explícitas + guia de adaptação + padronização dos critérios de aceite (GWT)**

Com esse conjunto de refinamentos, consegui estabilizar o comportamento do prompt e atingir o score mínimo de **0,90** exigido no teste.

## 3) Como executar
## A) Primeiro é preciso copiar o .env.example e renomea-lo para .env inserindo as credencias da OPENAI e do LANGSMITH e o seu username do langsmith

## B) Ativar o ambiente virtual com o comando:
windonws: .venv/Scripts/Activate.ps1
mac: source venv/bin/activate

## C) Executar a instalação das dependencias no ambiente virtual com o comando:
pip install -r requirements.txt

## D) Entrar na pasta src com o comando:
cd src

## E) Baixar o arquivo bug_to_user_story_v1.yml de prompt do langsmith com o comando
python pull_prompts.py, ele será criado na pasta src/prompts

## F) Criar uma copia do arquivo de prompt com versao 2 e realizar a refatoração usando few shot com 6 exemplos, chain of thought, skeleton of thought, persona, role prompting e padronização de criterios de aceite GWT (Given, When, Then)

## G) Enviar o prompt para o langsmith com o comando
python push_prompts.py

## H) Sair da pasta src com o comando
cd ..

## I) Copiar o arquivo bug_to_user_story_v2.yml para a pasta prompt e executar o comando de avaliação das metricas com o evaluate
python evaluate.py

## 3) Evidencias do langsmith
link: https://smith.langchain.com/hub/laisagomes/bug_to_user_story_v2
As evidencias da aprovação e do teste encontra-se nas imagens na raiz do projeto chamada: Prompt aprovado.png
teste com sucesso.png
