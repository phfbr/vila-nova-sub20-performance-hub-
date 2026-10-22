# Vila Nova Sub-20 Performance Hub 🔴⚪

**Análise de desempenho esportivo do Vila Nova Sub-20 no Campeonato Brasileiro Sub-20 B de 2026**, desenvolvida com **Python e Power BI**, a partir de dados de súmulas oficiais da CBF.

O projeto transforma registros de partidas, jogadores, gols, cartões e substituições em um painel interativo com cinco páginas, permitindo explorar resultados coletivos, confrontos, desempenho individual e disciplina.

> **Escopo:** 7 partidas analisadas. Os indicadores representam esse recorte e não necessariamente a temporada completa.

## Visão geral

![Visão Geral](imagens/pagina-01.png)

## Indicadores do recorte

| Indicador | Resultado |
|---|---:|
| Partidas | 7 |
| Vitórias | 3 |
| Empates | 2 |
| Derrotas | 2 |
| Pontos | 11 |
| Aproveitamento | 52,4% |
| Gols marcados | 15 |
| Gols sofridos | 16 |
| Saldo de gols | -1 |
| Jogadores utilizados | 32 |
| Participações em jogos | 117 |
| Cartões amarelos | 31 |
| Cartões vermelhos | 2 |

**Nota metodológica:** o total de 15 gols inclui um gol contra do adversário a favor do Vila Nova; os 14 gols atribuídos ao elenco consideram apenas os gols marcados por atletas da equipe. Participações em jogos correspondem a titularidades e entradas em campo, não a simples presença na lista de relacionados.

## Páginas do dashboard

### 01 — Visão Geral

Resumo de resultados, evolução por partida, gols marcados e sofridos, desempenho como mandante e visitante e destaques individuais.

![Página 01 — Visão Geral](imagens/pagina-01.png)

### 02 — Performance Coletiva

Evolução do saldo de gols, produção ofensiva, gols acumulados, aproveitamento e comparação de resultados por local.

![Página 02 — Performance Coletiva](imagens/pagina-02.png)

### 03 — Análise de Partidas

Histórico de confrontos e detalhes dinâmicos da partida selecionada, incluindo gols, cartões e substituições.

![Página 03 — Análise de Partidas](imagens/pagina-03.png)

### 04 — Desempenho Individual

Rankings de artilharia, partidas e titularidades, tabela de jogadores e perfil individual interativo.

![Página 04 — Desempenho Individual](imagens/pagina-04.png)

### 05 — Disciplina e Elenco

Distribuição e evolução de cartões, jogadores advertidos, disciplina individual e utilização do elenco por partida.

![Página 05 — Disciplina e Elenco](imagens/pagina-05.png)

## Tecnologias utilizadas

- **Python:** organização, limpeza, tratamento e validação dos dados.
- **Power Query:** transformação e preparação das tabelas no Power BI.
- **Power BI:** modelagem de dados, medidas DAX, visualizações e interações.
- **DAX:** indicadores de resultados, desempenho coletivo e individual, cartões e evolução acumulada.

## Processo de desenvolvimento

1. **Coleta:** consolidação de dados de sete súmulas oficiais da CBF.
2. **Tratamento:** padronização de campos e estruturação de bases de partidas, atletas, gols, cartões e substituições.
3. **Modelagem:** construção de tabelas de dimensão e fato, relacionamentos e medidas.
4. **Validação:** conferência de totais, estatísticas individuais e comportamento dos filtros.
5. **Visualização:** desenvolvimento de cinco páginas interativas com identidade visual consistente.

## Estrutura do repositório

```text
vila-nova-sub20-performance-hub/
├── README.md
├── imagens/
│   ├── pagina-01.png
│   ├── pagina-02.png
│   ├── pagina-03.png
│   ├── pagina-04.png
│   └── pagina-05.png
├── dashboard/       # Arquivo .pbix (a adicionar)
├── dados/           # Bases permitidas para compartilhamento (a adicionar)
└── scripts/         # Scripts Python revisados (a adicionar)
```

## Fonte e limitações

- **Fonte primária:** súmulas oficiais da Confederação Brasileira de Futebol (CBF), referentes às sete partidas analisadas.
- As estatísticas se limitam aos eventos registrados nas súmulas e aos campos tratados no projeto.
- O dashboard não pretende medir métricas de rastreamento ou desempenho físico não presentes na fonte.
- Este é um projeto independente de portfólio, sem vínculo oficial com o Vila Nova Futebol Clube ou com a CBF.

## Próximas melhorias

- Disponibilizar o arquivo Power BI e os scripts revisados.
- Documentar o dicionário de dados e as principais medidas DAX.
- Adicionar, quando aplicável, um link de visualização online do relatório.

---

**Projeto de portfólio em análise de dados e Business Intelligence.**
