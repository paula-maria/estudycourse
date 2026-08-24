# Decisões Arquiteturais — Sistema de Metas

## Sprint 6 — Study Goals

Este documento registra as decisões arquiteturais definidas para o sistema de metas do StudyCourses.

---

## 1. Objetivo

O sistema de metas deve permitir que o estudante defina objetivos de estudo independentes ou relacionados a um plano de estudos, acompanhe seu progresso e mantenha múltiplas metas simultaneamente.

A arquitetura deve permitir evoluir futuramente para recursos como gamificação, streaks, recomendações e diferentes tipos de metas sem exigir uma reestruturação da entidade principal.

---

## 2. Relação com StudyPlan

Uma meta **pode existir sem um `StudyPlan`**.

O relacionamento será opcional:

```text
StudyGoal
├── user_id       obrigatório
└── study_plan_id opcional
```

Isso permite dois cenários:

### Meta vinculada a plano

```text
StudyPlan
└── StudyGoal
    └── Zerar edital
```

### Meta independente

```text
StudyGoal
└── Estudar Python
```

Essa decisão permite que o estudante estabeleça objetivos mesmo quando não possui edital ou plano de estudos formal.

---

## 3. Múltiplas metas simultâneas

Um usuário poderá possuir várias metas ativas ao mesmo tempo.

Exemplo:

```text
Usuário
├── Meta principal
│   └── Zerar edital
├── Meta secundária
│   └── Estudar pontos fracos
├── Meta secundária
│   └── Resolver 500 questões
└── Meta independente
    └── Aprender Python
```

As metas não são mutuamente exclusivas.

---

## 4. Sobreposição de metas

Metas podem se sobrepor.

Uma mesma sessão de estudo poderá contribuir para mais de uma meta.

Exemplo:

```text
Sessão:
Direito Constitucional — 120 minutos
```

Pode contribuir simultaneamente para:

```text
✓ Zerar edital
✓ Estudar pontos fracos
✓ Meta semanal de estudo
```

### Decisão arquitetural

A relação entre `StudySession` e `StudyGoal` **não será exclusiva**.

A sessão continuará independente da meta, e o progresso das metas será calculado conforme suas regras de negócio.

Isso evita acoplar uma sessão a uma única meta.

---

## 5. Meta principal

O sistema terá o conceito de meta principal através do campo:

```text
is_primary
```

Inicialmente, a regra será:

> Um usuário pode possuir apenas uma meta principal ativa.

As demais metas ativas serão consideradas secundárias.

Exemplo:

```text
User
├── Goal A → is_primary = true
├── Goal B → is_primary = false
└── Goal C → is_primary = false
```

---

## 6. Conclusão da meta principal

Quando uma meta atingir 100% ou mais do objetivo:

```text
progress >= 100%
```

ela será marcada automaticamente como:

```text
COMPLETED
```

Caso existam metas secundárias ativas, o sistema poderá sugerir que uma delas se torne a nova meta principal.

### Decisão

A promoção automática **não será obrigatória na primeira versão**.

O sistema deverá inicialmente sugerir:

```text
A meta principal foi concluída.

Deseja tornar "Pontos fracos" sua nova meta principal?
```

A troca será confirmada pelo usuário.

Futuramente poderá ser criada uma configuração de promoção automática.

---

## 7. Tipos de meta

A primeira versão terá dois tipos:

```text
TIME
CONTENT
```

### TIME

Meta baseada em tempo de estudo.

Exemplo:

```text
Estudar 10 horas
```

O valor será armazenado em minutos.

Exemplo:

```text
target_value = 600
```

### CONTENT

Meta baseada na quantidade de conteúdo concluído.

Exemplo:

```text
Concluir 100 assuntos
```

Nesse caso:

```text
target_value = 100
```

Essa estrutura permite adicionar novos tipos posteriormente sem modificar completamente a arquitetura.

---

## 8. Cálculo do percentual

O percentual de progresso **não será armazenado diretamente no banco**.

Serão armazenados:

```text
target_value
current_value
```

O percentual será calculado pelo Service:

```text
current_value / target_value × 100
```

Exemplo:

```text
target_value = 600
current_value = 300

300 / 600 × 100 = 50%
```

### Motivo

Evita inconsistência entre valores armazenados.

Não haverá necessidade de manter:

```text
target_value = 600
current_value = 300
progress_percentage = 50
```

O percentual sempre será derivado dos valores atuais.

---

## 9. Limite visual do percentual

O progresso real poderá ultrapassar 100%.

Exemplo:

```text
target = 600
current = 720

progresso real = 120%
```

Porém, a interface poderá representar a barra visualmente limitada a 100%.

A meta será considerada concluída quando:

```text
current_value >= target_value
```

---

## 10. Status das metas

Serão utilizados cinco status:

```text
ACTIVE
COMPLETED
PAUSED
CANCELLED
EXPIRED
```

### ACTIVE

Meta em andamento.

### COMPLETED

Meta atingiu ou ultrapassou 100%.

### PAUSED

Meta temporariamente interrompida pelo usuário.

### CANCELLED

Meta abandonada ou encerrada pelo usuário.

### EXPIRED

Meta possuía uma data limite que terminou sem atingir o objetivo.

---

## 11. Estrutura conceitual de StudyGoal

A entidade será estruturada inicialmente como:

```text
StudyGoal
├── id
├── user_id
├── study_plan_id       opcional
├── title
├── description
├── goal_type
├── target_value
├── current_value
├── start_date
├── end_date
├── status
├── is_primary
├── created_at
└── updated_at
```

---

## 12. Regras de integridade

As seguintes regras deverão ser respeitadas:

1. Toda meta pertence obrigatoriamente a um usuário.
2. `study_plan_id` é opcional.
3. Um usuário pode ter várias metas.
4. Metas podem existir simultaneamente.
5. Metas podem se sobrepor.
6. Apenas uma meta principal ativa poderá existir por usuário.
7. `target_value` deve ser maior que zero.
8. `current_value` não deve ser negativo.
9. O percentual será calculado pelo Service.
10. Uma meta com progresso >= 100% poderá ser marcada como `COMPLETED`.
11. Uma meta expirada sem conclusão poderá ser marcada como `EXPIRED`.
12. Uma meta pausada não será considerada uma meta ativa.
13. Uma meta cancelada não poderá continuar acumulando progresso.

---

## 13. Evolução futura

A arquitetura deverá permitir posteriormente:

- metas diárias;
- metas semanais;
- metas mensais;
- metas por matéria;
- metas por quantidade de questões;
- metas por desempenho;
- streaks;
- gamificação;
- pontos e recompensas;
- recomendações automáticas;
- promoção automática de metas secundárias;
- metas baseadas em desempenho em questões.

Essas funcionalidades não fazem parte da primeira implementação da Sprint 6.

---

## 14. Decisões resumidas

| Decisão | Definição |
|---|---|
| Meta sem `StudyPlan` | Sim |
| Múltiplas metas | Sim |
| Metas sobrepostas | Sim |
| Meta principal | Sim |
| Metas secundárias | Sim |
| Relação exclusiva com sessão | Não |
| Tipos iniciais | `TIME`, `CONTENT` |
| Percentual armazenado | Não |
| Percentual calculado | Service |
| Meta concluída | `progress >= 100%` |
| Promoção de secundária | Sugestão ao usuário |
| Status | `ACTIVE`, `COMPLETED`, `PAUSED`, `CANCELLED`, `EXPIRED` |
| `study_plan_id` | Opcional |

---

## 15. Fluxo arquitetural

```text
                    User
                     │
                     ▼
                 StudyGoal
                     │
          ┌──────────┴──────────┐
          │                     │
     StudyPlan              Independente
          │
          ▼
     StudySession
          │
          ▼
    Goal Progress
          │
          ▼
       Service
          │
          ├── percentual
          ├── status
          └── conclusão
```

A entidade `StudyGoal` permanece independente de `StudySession`, permitindo que uma sessão contribua para diferentes metas sem criar acoplamento direto entre as entidades.
