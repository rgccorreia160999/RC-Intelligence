# RC Intelligence

Ferramentas de inteligência comercial da RC Representações.

## Campanha Pratic Leve — Distribuidora Itabaiana

Gera o painel de vendas, as metas individuais e o ranking da campanha de incentivo da equipe de
vendas da Distribuidora Itabaiana, a partir dos relatórios do ERP da distribuidora.

A mecânica espelha o **Desafio Ducamp 2026** — pontos por mix, positivação de carteira, ranking e
premiação — adaptada ao mix Pratic Leve e à base de RCAs da Itabaiana.

### Como rodar

```bash
python3 gerador_campanha_itabaiana.py
```

Sem dependências externas: usa só a biblioteca padrão do Python 3.

### Estrutura

```
dados/                        entradas (você edita)
  vendedores.csv              cadastro de RCAs, equipe e carteira
  historico_mensal.csv        painel de vendas mês a mês, por vendedor
  totais_mensais.csv          "Total Geral" oficial do relatório, por mês
  produtos.csv                SKUs Pratic Leve, curva ABC e pontos por caixa
  vendas_produto_vendedor.csv (opcional) venda por SKU × vendedor

saida/                        gerado pelo script
  baseline_vendedores.csv     média do histórico, por vendedor
  metas_vendedores.csv        metas individuais da campanha
  ranking.csv                 ranking apurado
  campanha.json               contexto completo, para outros usos
  painel_itabaiana.html       painel visual da campanha

docs/
  regulamento_campanha.md     regulamento para divulgar à equipe

gerador_campanha_itabaiana.py cálculo da campanha
painel.py                     renderização do painel HTML
```

### Fonte dos dados

O arquivo `historico_mensal.csv` vem do relatório **322 — Venda Por Departamento**, tipo 13
(por RCA), filiais 1, 4 e 5, fornecedor **935 — Palha Indústria e Comércio de Alimentos**.

Uma linha por vendedor por mês:

```csv
mes,codigo,clientes_ativos,clientes_positivados,qt_vendida_cx,valor_vendido,peso_kg
2026-08,57,87,47,922,56622.72,1380.81
```

O `totais_mensais.csv` guarda o **Total Geral** impresso no rodapé do mesmo relatório. Ele existe
porque o ERP deduplica clientes atendidos por mais de um RCA: a soma dos vendedores em agosto/2026
dá 1.461 clientes e 399 positivados, enquanto o Total Geral do relatório é 1.440 e 398. O painel
usa o número oficial no cabeçalho e a soma por RCA no detalhamento individual.

### Estado atual dos dados

O painel está carregado com **agosto/2026** apenas. Para a média de 4 meses, acrescente as linhas
de **maio, junho e julho/2026** em `historico_mensal.csv` e `totais_mensais.csv` e rode o gerador
de novo — baseline, metas e ranking se recalculam sozinhos, sem mexer no código.

Enquanto não houver `vendas_produto_vendedor.csv`, os pontos de mix do ranking são **projetados**
sobre o volume do baseline usando a distribuição da curva ABC, e os bônus de mix completo e de
Pipoca ficam zerados — não há como apurá-los sem a venda por SKU. Com o arquivo presente, o
gerador passa sozinho para apuração real e sinaliza isso no painel. O formato esperado é:

```csv
codigo_vendedor,codigo_produto,cliente,qt_cx
57,33851,000123,4
```

### Parâmetros da campanha

Ficam no topo de `gerador_campanha_itabaiana.py`, nos dicionários `CAMPANHA`, `PONTUACAO` e
`PREMIACAO`. Mudou a meta de crescimento, o valor de um bônus ou a premiação? Edite ali e rode de
novo.
