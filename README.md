# RiskOS — Plataforma Unificada de Inteligência de Risco

> Uma camada de decisão que conecta detecção de fraude e previsão de churn em tempo real, transformando dois scores isolados em uma ação de negócio.

---

## 1. O problema

Empresas que lidam com transações e assinaturas (fintechs, marketplaces, SaaS) constroem,
quase sempre, sistemas de risco **isolados**: um time cuida de fraude, outro cuida de churn,
e raramente os dois conversam. O resultado prático:

- Um cliente que está prestes a cancelar (alto risco de churn) sofre uma transação bloqueada
  por engano (falso positivo de fraude) — e a empresa acelera a própria perda.
- Um time de CS recebe um alerta de churn sem nenhum contexto sobre o comportamento
  transacional do cliente, e perde tempo investigando o que o sistema de fraude já sabia.
- Decisões de risco viram **números em dashboards separados**, não **ações coordenadas**.

O RiskOS nasce para resolver exatamente isso: uma camada única que recebe os sinais de
fraude e de churn, decide a ação certa, e explica o porquê — em vez de apenas exibir um score.

## 2. Como o RiskOS nasceu

Este projeto não começou do zero. Ele é a evolução natural de três sistemas que já existiam
de forma independente:

| Componente | Status | Papel no RiskOS |
|---|---|---|
| [`PipeLineETL`](#) | Existente | Espinha dorsal de ingestão e padronização de dados |
| [`FraudDetector`](#) | Existente | Fonte do score de risco transacional |
| [`ChurnAnalytics`](#) | Existente | Fonte do score de risco de retenção |
| **Motor de Decisão** | Novo | Combina os dois scores em uma ação |
| **Dashboard Executivo** | Novo | Visão unificada de risco para o negócio |
| **Camada de Explicabilidade (LLM)** | Novo | Traduz a decisão em linguagem de negócio |

A decisão consciente de **reaproveitar e elevar** os três sistemas, em vez de recomeçar,
reflete como sistemas de risco evoluem em empresas reais: raramente nascem unificados —
são integrados aos poucos, com contratos de dados cada vez mais rígidos.

## 3. Arquitetura

```
                    ┌─────────────────────────┐
                    │     Fontes de dados      │
                    │  transações · eventos ·  │
                    │   CRM · suporte · NPS    │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │       PipeLineETL          │
                    │  ingestão · limpeza ·      │
                    │  padronização contínua     │
                    └────────────┬─────────────┘
                                 │
                ┌────────────────┴────────────────┐
                │                                  │
     ┌──────────▼──────────┐          ┌───────────▼───────────┐
     │   FraudDetector      │          │    ChurnAnalytics      │
     │ score de risco       │          │  score de risco de     │
     │ transacional         │          │  retenção               │
     └──────────┬──────────┘          └───────────┬───────────┘
                │                                  │
                └────────────────┬─────────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │     Motor de Decisão       │
                    │  cruza os dois scores e    │
                    │  decide a ação              │
                    └────────────┬─────────────┘
                                 │
            ┌────────────────────┼────────────────────┐
            │                    │                    │
  ┌─────────▼────────┐ ┌─────────▼────────┐ ┌─────────▼────────┐
  │ Bloquear          │ │ Acionar CS        │ │ Alerta em         │
  │ transação          │ │                   │ │ tempo real         │
  └─────────┬────────┘ └─────────┬────────┘ └─────────┬────────┘
            │                    │                    │
            └────────────────────┼────────────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │   Dashboard Executivo      │
                    │  ARR em risco · fraude     │
                    │  evitada · ROI              │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │ Camada de Explicabilidade  │
                    │         (LLM)               │
                    │  por que essa decisão        │
                    │  foi tomada                  │
                    └───────────────────────────┘
```

### Por que um Motor de Decisão, e não só dois dashboards lado a lado?

Porque a decisão de negócio real **depende da combinação** dos dois scores, não de cada um
isoladamente. Exemplos de regras que o motor resolve:

| Score de Fraude | Score de Churn | Ação |
|---|---|---|
| Alto | Alto | Investigar com prioridade máxima — pode ser conta comprometida, não o cliente saindo |
| Alto | Baixo | Bloquear transação, cliente engajado normalmente |
| Baixo | Alto | Acionar Customer Success, sem tocar nas transações |
| Baixo | Baixo | Nenhuma ação — monitorar |

Esse cruzamento é o que transforma dois modelos de ML em um **sistema de decisão**, e é a
peça que normalmente falta em projetos de portfólio.

## 4. Decisões de arquitetura (e por quê)

- **Contrato de eventos único entre os 3 sistemas** — em vez de cada serviço expor sua própria
  estrutura de dados, definimos um schema comum de "sinal de risco" (ver `docs/api-contract.md`).
  Isso permite adicionar um quarto ou quinto modelo no futuro sem reescrever o motor de decisão.
- **Motor de decisão como serviço separado** — não embutido em nenhum dos dois modelos, para
  que a lógica de negócio (as regras de combinação de scores) possa evoluir independente dos
  modelos de ML.
- **Explicabilidade como camada própria** — separar "prever" de "explicar" permite trocar o
  modelo de LLM sem afetar os modelos de risco, e mantém o motor de decisão determinístico e
  testável.
- **Docker Compose para ambiente local** — o sistema inteiro (3 serviços + banco + dashboard)
  sobe com um único comando, o que facilita tanto o desenvolvimento quanto a demonstração.

## 5. Stack

- **Linguagem:** Python 3.11+ (FastAPI nos serviços)
- **Orquestração local:** Docker Compose
- **Banco de dados:** PostgreSQL (dados transacionais) + Redis (cache de scores)
- **Mensageria entre serviços:** REST interno (fase 1) → fila de eventos (fase 2, ver roadmap)
- **Dashboard:** Next.js + TypeScript
- **Explicabilidade:** API de LLM (Claude/GPT-4)
- **CI/CD:** GitHub Actions


## 6. Impacto de negócio (estimado)

> Os números abaixo são estimativas de impacto baseadas em benchmarks de mercado para
> fintechs/SaaS de médio porte, usados para fins de demonstração do potencial da solução.

- Redução de falsos positivos em fraude ao cruzar com sinal de churn: **15-20%**
- Redução de churn não detectado em clientes com atividade transacional suspeita: **10-15%**
- Tempo de resposta da operação a um evento de risco: de **dias para minutos**

## 7. Como rodar localmente

```bash
git clone <este-repositório>
cd riskos
docker-compose up
```

O dashboard ficará disponível em `http://localhost:3000`.
