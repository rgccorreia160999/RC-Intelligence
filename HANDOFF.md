# Resumo de transferência — Campanha Pratic Leve / Distribuidora Itabaiana

Construído em `rgccorreia160999/RC-Intelligence`, branch
`claude/dashboards-distribuidores-atualizacao-2-8zrtc4`, em 05/09/2026.
Este repositório estava **vazio** (nenhum commit) quando o trabalho começou —
por isso estes são os primeiros commits dele.

Painel publicado: https://claude.ai/code/artifact/93e91509-5349-4e4d-ae35-423f36810de5

---

## 1. O que foi construído

Um gerador que monta a campanha de incentivo da equipe de vendas da Distribuidora
Itabaiana (linha Pratic Leve) a partir dos relatórios do ERP da distribuidora, e
renderiza o painel visual da campanha.

| Arquivo | O que faz |
|---|---|
| `gerador_campanha_itabaiana.py` | Calcula baseline, metas individuais e ranking. Só stdlib do Python 3. |
| `painel.py` | Renderiza o painel HTML (tema claro/escuro, sem dependências). |
| `dados/vendedores.csv` | Cadastro dos 16 RCAs, equipe e carteira. |
| `dados/historico_mensal.csv` | Painel de vendas mês a mês, por vendedor. **Só agosto/2026 carregado.** |
| `dados/totais_mensais.csv` | "Total Geral" oficial do relatório, por mês. |
| `dados/produtos.csv` | 16 SKUs Pratic Leve, curva ABC e pontos por caixa. |
| `docs/regulamento_campanha.md` | Regulamento pronto para divulgar à equipe. |
| `saida/` | Gerado pelo script: baseline, metas, ranking, campanha.json, painel HTML. |

Rodar: `python3 gerador_campanha_itabaiana.py`

## 2. De onde vieram os dados

**Modelo da mecânica** — `RANKING CAMPANHA DUCAMP.xlsx` (Google Drive). O
`gerador_campanha_ducamp.py` citado como referência está num caminho local
(`RC_Vendas/Lima frios/Ducamp/`) e não foi acessível nesta sessão; a mecânica foi
reconstruída a partir da planilha, que contém tudo: pontos por SKU inversos ao
giro (mussarela processada 1 pt, doce de leite e manteiga 10 pts), positivação por
produto, POS/BASE por vendedor, ranking por equipe (AGRESTE / SERTÃO / TELEVENDAS)
e o resumo com meta 420 / positivação 831 / 198%.

**Baseline de vendas** — relatório **322 — Venda Por Departamento**, tipo 13 (por
RCA), filiais 1, 4 e 5, fornecedor **935 — PALHA INDÚSTRIA E COM DE ALIMENTOS
EIRELI**, período 01/08/2026 a 31/08/2026. No Drive: `venda pratic.pdf`.

**Mix de produtos** — `dashboard_pratic_leve_jan_abr_2026.xlsx` (Drive), de onde
saíram os 16 SKUs com código, volume, faturamento e curva ABC.

## 3. Números do baseline (agosto/2026)

| Indicador | Valor |
|---|---|
| Carteira ativa | 1.440 clientes |
| Positivados | 398 (27,6%) |
| Volume | 5.520 CX |
| Faturamento | R$ 343.539,58 |
| Peso | 8.162,21 kg |
| RCAs | 16 |

Por vendedor (código, nome, carteira, positivados, %, caixas, R$):

```
57   FABIO TELES DALTRO              87   47  54,0%   922  56.622,72
42   GINALDO COSTA SANTOS           126   45  35,7%   890  55.683,77
117  ANSELMO CERQUEIRA CARVALHO      71   22  31,0%   518  30.599,31
133  ANDRE JOSE DE SOUZA            100   46  46,0%   438  29.076,58
107  LUCAS SOUZA ALVES              148    5   3,4%   545  28.852,45
55   JOANDERSON MEDRADE DOS SANTOS  111   44  39,6%   324  23.039,53
63   ILENILDO JUNIOR MELO            76   31  40,8%   368  22.876,35
20   ARQUIMEDES NUNES BEZERRA         4    3  75,0%   350  22.871,00
114  MARCOS ANTONIO DE JESUS VIANA  133   55  41,4%   303  19.487,21
134  VIVIANE DOS SANTOS             138   46  33,3%   245  18.176,93
37   RIVALDO DA CRUZ SOARES FILHO    65    3   4,6%   266  13.876,53
135  SALLANO VITOR DA HORA SANTOS    84   27  32,1%   142   9.723,09
51   MICHELLE HORA XAVIER            92    3   3,3%    82   5.710,21
129  ANA CLEA DE JESUS NASCIMENTO    74    6   8,1%    64   3.179,00
49   EDINALDO CAMPOS DE OLIVEIRA     98    6   6,1%    43   2.368,80
10   JOSE LEONARDO MENEZES SANTOS    54   10  18,5%    20   1.396,10
```

**Atenção a uma inconsistência real:** a soma por vendedor dá 1.461 clientes e 399
positivados, mas o Total Geral do relatório diz 1.440 e 398. O ERP deduplica
clientes atendidos por mais de um RCA. O painel usa o número oficial no cabeçalho
e a soma por RCA no detalhamento individual — por isso existe o
`totais_mensais.csv` separado.

## 4. A campanha desenhada

**Desafio Pratic Leve — Itabaiana 2026/2027**, de 01/10/2026 a 31/01/2027,
apuração em fevereiro, viagem em março.

**Diagnóstico que a sustenta:** 1.440 clientes ativos, só 398 compram Pratic Leve.
Três quartos da carteira nunca receberam o produto. Por isso a campanha premia
positivação e mix, não volume.

**Pontuação**

- 1 a 10 pts por caixa, conforme o SKU — curva A vale pouco (Ondulada Natural
  20x40g = 1 pt), Pipoca vale 10. Palha Premium é curva A mas recebe 4 pts por
  decisão comercial: caiu 38% de março para abril/2026.
- 50 pts por cliente positivado no mês.
- +500 pts por mês em que o RCA atingir 45% de positivação da carteira.
- +100 pts por cliente que levar 4+ SKUs distintos.
- +150 pts por cliente positivado na linha Pipoca (lançamento).
- **Corte:** só concorre ao prêmio máximo quem fechar com 40%+ de positivação
  média — impede que a campanha seja vencida por volume concentrado em poucos
  clientes grandes.

**Metas:** faturamento +20% (R$ 412.247,50/mês), volume +20% (6.624 CX/mês),
positivação de 27,6% para 45% (+250 clientes).

**Premiação:** resort all inclusive com acompanhante em cinco faixas — 1º (4
diárias), 2º (3), 3º (2), Destaque Positivação (2) e Destaque Linha Pipoca (2).
Os dois destaques são independentes do ranking geral, para que quem tem carteira
menor também dispute.

**Ranking simulado sobre agosto** — cinco já passam do corte de 40%: Fábio
(54,0%), André (46,0%), Marcos (41,4%), Ilenildo (40,8%) e Arquimedes (75,0%, mas
com carteira de apenas 4 clientes, que é um caso à parte). Lucas tem a maior
carteira da equipe (148) e positiva 3,4% — o maior espaço isolado da campanha.

## 5. O que ainda falta

**a) Média de 4 meses.** Foi o que se pediu, mas só agosto/2026 estava disponível.
As metas atuais estão calculadas sobre um mês só, o que é frágil — agosto pode ter
sido atípico. Faltam os relatórios 322 de **maio, junho e julho/2026**. Basta
acrescentar as linhas em `historico_mensal.csv` e `totais_mensais.csv` e rodar o
gerador: baseline, metas e ranking se recalculam sozinhos, sem tocar no código.

**b) Venda por SKU × vendedor.** Sem ela, os pontos de mix do ranking estão
*projetados* pela curva ABC, e os bônus de mix completo e de Pipoca ficam zerados
— não há como apurá-los sem saber quem vendeu o quê. Com o arquivo
`dados/vendas_produto_vendedor.csv` presente, o gerador passa sozinho para
apuração real e sinaliza isso no painel. Formato:

```csv
codigo_vendedor,codigo_produto,cliente,qt_cx
57,33851,000123,4
```

**c) Confirmar com a distribuidora:** as equipes (hoje todos estão como
`ITABAIANA`, exceto Arquimedes como `KEY ACCOUNT` — o Ducamp separava AGRESTE /
SERTÃO / TELEVENDAS, e a Itabaiana provavelmente tem divisão parecida), o período
da campanha, e o orçamento da premiação.

## 6. Decisões que valem revisar

- **Pontos por SKU** (`dados/produtos.csv`) — atribuídos por curva ABC e por queda
  recente, não validados com a Pratic Leve. É o parâmetro que mais muda o
  comportamento da equipe.
- **Meta de +20%** — escolhida como padrão, não derivada de histórico ou de acordo
  comercial.
- **Corte de 40%** — protege contra volume concentrado, mas deixa 11 dos 16 RCAs
  fora do prêmio máximo no cenário de agosto. Pode ser agressivo demais para a
  primeira edição.
- **Arquimedes (código 20)** tem carteira de 4 clientes e R$ 22.871 em agosto —
  é key account, não RCA de rota. Competindo no mesmo ranking ele distorce o
  indicador de positivação. Marcado como `KEY ACCOUNT` em `vendedores.csv`, mas
  ainda não recebe tratamento separado no cálculo.

Todos os parâmetros ficam no topo de `gerador_campanha_itabaiana.py`, nos
dicionários `CAMPANHA`, `PONTUACAO` e `PREMIACAO`.
