#!/usr/bin/env python3
"""Renderiza o painel HTML da campanha a partir do contexto do gerador."""

import html as _html


def esc(txt):
    return _html.escape(str(txt))


def brl(valor):
    """Formata em real brasileiro: 1234567.89 -> 1.234.567,89"""
    txt = "%.2f" % float(valor)
    inteiro, dec = txt.split(".")
    neg = inteiro.startswith("-")
    inteiro = inteiro.lstrip("-")
    partes = []
    while len(inteiro) > 3:
        partes.insert(0, inteiro[-3:])
        inteiro = inteiro[:-3]
    partes.insert(0, inteiro)
    return ("-" if neg else "") + ".".join(partes) + "," + dec


def milhar(valor):
    return brl(valor).split(",")[0]


def pct(valor, casas=1):
    """Percentual no padrao brasileiro: 27.64 -> 27,6%"""
    return ("%.*f" % (casas, float(valor))).replace(".", ",") + "%"


def primeiro_nome(nome):
    partes = nome.split()
    return partes[0] if partes else nome


CSS = """
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">
<style>
.pn {
  color-scheme: light;
  --surface-0: #f4f3f0;
  --surface-1: #fcfcfb;
  --surface-2: #eceae5;
  --border:    #dcdad3;
  --text-1:    #0b0b0b;
  --text-2:    #52514e;
  --text-3:    #86847d;
  --azul:      #2a78d6;
  --azul-fraco:#cde2fb;
  --laranja:   #eb6834;
  --laranja-fraco:#fbe0d4;
  --ouro:      #eda100;
  --bom:       #1baf7a;
  --alerta:    #e34948;
  --radius: 10px;
  background: var(--surface-0);
  color: var(--text-1);
  --fonte-display: "Archivo", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --fonte-texto: "IBM Plex Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-family: var(--fonte-texto);
  font-size: 15px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}
@media (prefers-color-scheme: dark) {
  :root:where(:not([data-theme="light"])) .pn {
    color-scheme: dark;
    --surface-0: #121211;
    --surface-1: #1a1a19;
    --surface-2: #232322;
    --border:    #34342f;
    --text-1:    #ffffff;
    --text-2:    #c3c2b7;
    --text-3:    #8f8e85;
    --azul:      #3987e5;
    --azul-fraco:#184f95;
    --laranja:   #d95926;
    --laranja-fraco:#6b2a10;
    --ouro:      #c98500;
    --bom:       #199e70;
    --alerta:    #e66767;
  }
}
:root[data-theme="dark"] .pn {
  color-scheme: dark;
  --surface-0: #121211;
  --surface-1: #1a1a19;
  --surface-2: #232322;
  --border:    #34342f;
  --text-1:    #ffffff;
  --text-2:    #c3c2b7;
  --text-3:    #8f8e85;
  --azul:      #3987e5;
  --azul-fraco:#184f95;
  --laranja:   #d95926;
  --laranja-fraco:#6b2a10;
  --ouro:      #c98500;
  --bom:       #199e70;
  --alerta:    #e66767;
}

.pn * { box-sizing: border-box; }
.pn-wrap { max-width: 1080px; margin: 0 auto; padding: 28px 20px 64px; }

/* ---------- cabecalho ---------- */
.pn-hero {
  background: linear-gradient(135deg, var(--azul) 0%, #1c5cab 100%);
  border-radius: var(--radius);
  padding: 30px 30px 26px;
  color: #fff;
  margin-bottom: 26px;
}
.pn-kicker { font-size: 12px; letter-spacing: .14em; text-transform: uppercase; opacity: .82; margin: 0 0 8px; font-weight: 600; }
.pn-hero h1 { margin: 0 0 6px; font-family: var(--fonte-display); font-size: 32px; line-height: 1.1; font-weight: 800; letter-spacing: -.02em; text-wrap: balance; }
.pn-hero .pn-sub { margin: 0; font-size: 15px; opacity: .9; }
.pn-premio-tag {
  display: inline-block; margin-top: 16px; padding: 8px 15px;
  background: rgba(255,255,255,.16); border: 1px solid rgba(255,255,255,.3);
  border-radius: 100px; font-size: 14px; font-weight: 600;
}

/* ---------- blocos ---------- */
.pn-sec { margin-bottom: 34px; }
.pn-sec > h2 {
  font-size: 12px; letter-spacing: .12em; text-transform: uppercase;
  color: var(--text-3); margin: 0 0 4px; font-weight: 700;
}
.pn-sec > .pn-lead { margin: 0 0 16px; color: var(--text-2); font-size: 14px; }

.pn-card {
  background: var(--surface-1); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 20px;
}

/* ---------- metas ---------- */
.pn-metas { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 14px; }
.pn-meta { background: var(--surface-1); border: 1px solid var(--border); border-radius: var(--radius); padding: 18px 20px; }
.pn-meta-rot { font-size: 12px; text-transform: uppercase; letter-spacing: .08em; color: var(--text-3); font-weight: 600; margin-bottom: 12px; }
.pn-meta-de { font-size: 13px; color: var(--text-2); }
.pn-meta-de b { font-variant-numeric: tabular-nums; font-weight: 600; color: var(--text-1); }
.pn-meta-para { font-family: var(--fonte-display); font-size: 28px; font-weight: 800; letter-spacing: -.02em; color: var(--laranja); font-variant-numeric: tabular-nums; margin: 2px 0 3px; }
.pn-meta-delta { font-size: 13px; color: var(--text-2); }

/* ---------- barras ---------- */
.pn-tabela { width: 100%; border-collapse: collapse; font-size: 14px; }
.pn-tabela th {
  text-align: left; font-size: 11px; text-transform: uppercase; letter-spacing: .07em;
  color: var(--text-3); font-weight: 700; padding: 0 10px 9px; border-bottom: 1px solid var(--border);
}
.pn-tabela th.num, .pn-tabela td.num { text-align: right; font-variant-numeric: tabular-nums; }
.pn-tabela td { padding: 9px 10px; border-bottom: 1px solid var(--border); vertical-align: middle; }
.pn-tabela tr:last-child td { border-bottom: none; }
.pn-pos { font-family: var(--fonte-display); font-weight: 800; font-size: 16px; color: var(--text-3); width: 34px; font-variant-numeric: tabular-nums; }
.pn-pos.top { color: var(--ouro); }
.pn-nome { font-weight: 600; }
.pn-eq { font-size: 11px; color: var(--text-3); text-transform: uppercase; letter-spacing: .05em; }

.pn-barra-cel { width: 34%; min-width: 130px; }
.pn-barra { background: var(--surface-2); border-radius: 4px; height: 16px; overflow: hidden; }
.pn-barra > span { display: block; height: 100%; border-radius: 4px; background: var(--azul); }
.pn-barra.laranja > span { background: var(--laranja); }

/* barra de positivacao com marca de meta */
.pn-pos-wrap { position: relative; }
.pn-meta-marca {
  position: absolute; top: -3px; bottom: -3px; width: 2px; background: var(--laranja);
}
.pn-meta-marca::after {
  content: ""; position: absolute; top: -4px; left: -3px;
  border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 5px solid var(--laranja);
}

.pn-legenda { display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 14px; font-size: 13px; color: var(--text-2); }
.pn-legenda span { display: inline-flex; align-items: center; gap: 7px; }
.pn-chip { width: 11px; height: 11px; border-radius: 3px; flex: none; }

.pn-tag { display: inline-block; padding: 2px 8px; border-radius: 100px; font-size: 11px; font-weight: 700; letter-spacing: .04em; }
.pn-tag.ok { background: var(--azul-fraco); color: var(--azul); }
.pn-tag.no { background: var(--surface-2); color: var(--text-3); }
:root[data-theme="dark"] .pn .pn-tag.ok, .pn .pn-tag.ok { }
.pn-abc { display: inline-block; width: 20px; height: 20px; line-height: 20px; text-align: center; border-radius: 5px; font-size: 11px; font-weight: 700; }
.pn-abc.A { background: var(--azul-fraco); color: var(--azul); }
.pn-abc.B { background: var(--surface-2); color: var(--text-2); }
.pn-abc.C { background: var(--laranja-fraco); color: var(--laranja); }
.pn-pts { font-family: var(--fonte-display); font-weight: 800; font-size: 15px; color: var(--laranja); font-variant-numeric: tabular-nums; }

/* ---------- premiacao ---------- */
.pn-premios { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 14px; }
.pn-premio { background: var(--surface-1); border: 1px solid var(--border); border-radius: var(--radius); padding: 18px; }
.pn-premio.destaque { border-color: var(--ouro); border-width: 2px; }
.pn-premio h3 { margin: 0 0 6px; font-family: var(--fonte-display); font-size: 15px; font-weight: 700; letter-spacing: -.01em; }
.pn-premio p { margin: 0; font-size: 14px; color: var(--text-2); }

/* ---------- regras ---------- */
.pn-regras { list-style: none; padding: 0; margin: 0; }
.pn-regras li { display: flex; gap: 14px; padding: 12px 0; border-bottom: 1px solid var(--border); align-items: baseline; }
.pn-regras li:last-child { border-bottom: none; }
.pn-regras .pn-val { flex: none; min-width: 92px; font-weight: 700; color: var(--azul); font-variant-numeric: tabular-nums; }

.pn-nota {
  background: var(--surface-2); border-left: 3px solid var(--laranja);
  border-radius: 0 var(--radius) var(--radius) 0; padding: 15px 18px; font-size: 14px; color: var(--text-2);
}
.pn-nota b { color: var(--text-1); }
.pn-rodape { margin-top: 34px; padding-top: 18px; border-top: 1px solid var(--border); font-size: 12.5px; color: var(--text-3); }

.pn-scroll { overflow-x: auto; }
.pn :focus-visible { outline: 2px solid var(--azul); outline-offset: 2px; border-radius: 3px; }
@media (prefers-reduced-motion: reduce) { .pn * { animation: none !important; transition: none !important; } }
@media (max-width: 620px) {
  .pn-hero { padding: 24px 20px; }
  .pn-hero h1 { font-size: 24px; }
  .pn-barra-cel { display: none; }
}
</style>
"""


def _bloco_metas(ctx):
    t = ctx["totais"]
    c = ctx["campanha"]
    itens = [
        ("Faturamento / mês", "R$ " + brl(t["valor"]), "R$ " + brl(t["meta_valor"]),
         "+%d%%  ·  R$ %s a mais por mês" % (c["crescimento_faturamento"] * 100, brl(t["meta_valor"] - t["valor"]))),
        ("Volume / mês", milhar(t["caixas"]) + " CX", milhar(t["meta_caixas"]) + " CX",
         "+%d%%  ·  %s caixas a mais" % (c["crescimento_volume"] * 100, milhar(t["meta_caixas"] - t["caixas"]))),
        ("Positivação da carteira", pct(t["pct_positivacao"]), pct(c["meta_positivacao"] * 100, 0),
         "%d para %d clientes  ·  +%d a positivar" % (t["positivados"], t["meta_positivados"], t["meta_positivados"] - t["positivados"])),
        ("Carteira ativa", "%d clientes" % t["carteira"], "%d RCAs" % len(ctx["baseline"]),
         "média de %d clientes por vendedor" % round(t["carteira"] / len(ctx["baseline"]))),
    ]
    cards = []
    for rot, de, para, delta in itens:
        cards.append(
            '<div class="pn-meta"><div class="pn-meta-rot">%s</div>'
            '<div class="pn-meta-de">hoje <b>%s</b></div>'
            '<div class="pn-meta-para">%s</div>'
            '<div class="pn-meta-delta">%s</div></div>'
            % (esc(rot), esc(de), esc(para), esc(delta))
        )
    return '<div class="pn-metas">%s</div>' % "".join(cards)


def _bloco_ranking(ctx):
    rk = ctx["ranking"]
    if not rk:
        return ""
    topo = max(r["pontos_total"] for r in rk) or 1
    linhas = []
    for r in rk:
        larg = r["pontos_total"] / topo * 100
        classe_pos = "pn-pos top" if r["posicao"] <= 3 else "pn-pos"
        tag = ('<span class="pn-tag ok">apto</span>' if r["qualificado"]
               else '<span class="pn-tag no">abaixo do corte</span>')
        linhas.append(
            '<tr>'
            '<td class="%s">%d</td>'
            '<td><div class="pn-nome">%s</div><div class="pn-eq">%s</div></td>'
            '<td class="pn-barra-cel"><div class="pn-barra"><span style="width:%.1f%%"></span></div></td>'
            '<td class="num"><b>%s</b></td>'
            '<td class="num">%d / %d</td>'
            '<td class="num">%s</td>'
            '<td>%s</td>'
            '</tr>'
            % (classe_pos, r["posicao"], esc(r["vendedor"]), esc(r["equipe"]), larg,
               milhar(r["pontos_total"]), r["positivados"], r["carteira"],
               pct(r["pct_positivacao"]), tag)
        )
    return (
        '<div class="pn-card pn-scroll"><table class="pn-tabela">'
        '<thead><tr><th></th><th>Vendedor</th><th>Pontos</th><th class="num">Total</th>'
        '<th class="num">Positivados</th><th class="num" style="white-space:nowrap">%% Pos.</th><th>Prêmio</th></tr></thead>'
        '<tbody>%s</tbody></table></div>' % "".join(linhas)
    )


def _bloco_positivacao(ctx):
    """Barras de positivacao por vendedor com marca da meta."""
    base = sorted(ctx["baseline"], key=lambda x: x["pct_positivacao"], reverse=True)
    meta = ctx["campanha"]["meta_positivacao"] * 100
    escala = 100.0
    linhas = []
    for b in base:
        larg = min(b["pct_positivacao"] / escala * 100, 100)
        cor = "" if b["pct_positivacao"] >= meta else " laranja"
        linhas.append(
            '<tr>'
            '<td><div class="pn-nome">%s</div><div class="pn-eq">%d clientes na carteira</div></td>'
            '<td class="pn-barra-cel"><div class="pn-pos-wrap">'
            '<div class="pn-barra%s"><span style="width:%.1f%%"></span></div>'
            '<div class="pn-meta-marca" style="left:%.1f%%"></div>'
            '</div></td>'
            '<td class="num"><b>%s</b></td>'
            '<td class="num">%d</td>'
            '</tr>'
            % (esc(b["vendedor"]), b["carteira"], cor, larg, meta,
               pct(b["pct_positivacao"]), b["positivados"])
        )
    legenda = (
        '<div class="pn-legenda">'
        '<span><i class="pn-chip" style="background:var(--azul)"></i>já atinge a meta</span>'
        '<span><i class="pn-chip" style="background:var(--laranja)"></i>abaixo da meta</span>'
        '<span><i class="pn-chip" style="background:var(--laranja);width:2px;height:13px;border-radius:1px"></i>'
        'meta de %s da carteira</span>'
        '</div>' % pct(meta, 0)
    )
    return (
        '<div class="pn-card">%s<div class="pn-scroll"><table class="pn-tabela">'
        '<thead><tr><th>Vendedor</th><th>Positivação da carteira</th>'
        '<th class="num">%%</th><th class="num">Clientes</th></tr></thead>'
        '<tbody>%s</tbody></table></div></div>' % (legenda, "".join(linhas))
    )


def _bloco_produtos(ctx):
    prods = sorted(ctx["produtos"], key=lambda p: (-int(p["pontos_cx"]), p["produto"]))
    linhas = []
    for p in prods:
        linhas.append(
            '<tr><td class="num pn-pts">%s</td>'
            '<td><span class="pn-abc %s">%s</span></td>'
            '<td>%s</td><td class="pn-eq">%s</td><td class="num pn-eq">%s</td></tr>'
            % (p["pontos_cx"], esc(p["abc"]), esc(p["abc"]), esc(p["produto"]),
               esc(p["linha"]), esc(p["codigo"]))
        )
    return (
        '<div class="pn-card pn-scroll"><table class="pn-tabela">'
        '<thead><tr><th class="num">Pts/CX</th><th>ABC</th><th>Produto</th>'
        '<th>Linha</th><th class="num">Código</th></tr></thead>'
        '<tbody>%s</tbody></table></div>' % "".join(linhas)
    )


def _bloco_regras(ctx):
    p = ctx["pontuacao"]
    c = ctx["campanha"]
    regras = [
        ("1 a 10 pts", "Por caixa vendida, conforme a tabela de pontos do SKU. Quanto mais difícil o giro, mais vale."),
        ("%d pts" % p["pts_por_cliente_positivado"], "Por cliente positivado no mês (cliente que comprou pelo menos um item Pratic Leve)."),
        ("+%d pts" % p["bonus_meta_positivacao"], "Bônus por mês em que o vendedor atingir %.0f%% de positivação da sua carteira." % (c["meta_positivacao"] * 100)),
        ("+%d pts" % p["bonus_mix_completo"], "Por cliente que levar %d ou mais SKUs diferentes no mês." % p["min_skus_mix_completo"]),
        ("+%d pts" % p["bonus_pipoca"], "Por cliente positivado na linha Pipoca, que é o lançamento da campanha."),
        ("Corte", "Só concorre ao prêmio máximo quem fechar o período com no mínimo %.0f%% de positivação média da carteira." % (c["corte_qualificacao"] * 100)),
    ]
    itens = "".join(
        '<li><span class="pn-val">%s</span><span>%s</span></li>' % (esc(v), esc(d))
        for v, d in regras
    )
    return '<div class="pn-card"><ul class="pn-regras">%s</ul></div>' % itens


def _bloco_premios(ctx):
    cards = []
    for i, (titulo, desc) in enumerate(ctx["premiacao"]):
        classe = "pn-premio destaque" if i == 0 else "pn-premio"
        cards.append('<div class="%s"><h3>%s</h3><p>%s</p></div>' % (classe, esc(titulo), esc(desc)))
    return '<div class="pn-premios">%s</div>' % "".join(cards)


def render_painel(ctx):
    c = ctx["campanha"]
    t = ctx["totais"]
    meses = ctx["meses"]

    if ctx["modo_real"]:
        nota = (
            '<div class="pn-nota"><b>Apuração com venda por SKU.</b> O ranking acima usa '
            '<code>dados/vendas_produto_vendedor.csv</code>, então os pontos de mix, o bônus de mix completo '
            'e o bônus da linha Pipoca estão apurados de verdade.</div>'
        )
    else:
        nota = (
            '<div class="pn-nota"><b>Leia antes de divulgar.</b> O painel esta carregado com '
            '<b>%d mês de histórico (%s)</b>, extraído do relatório 322 &ndash; Venda Por Departamento, por RCA, '
            'fornecedor 935 PALHA. A média de 4 meses pedida precisa dos relatórios de '
            'maio, junho e julho/2026 &ndash; basta acrescentar as linhas em <code>dados/historico_mensal.csv</code> '
            'e rodar o gerador de novo, que todas as metas se recalculam sozinhas. '
            'Os pontos do ranking estão <b>projetados</b> sobre o volume do baseline: o bônus de mix completo '
            'e o de Pipoca só entram quando existir a venda por SKU &times; vendedor.</div>'
            % (len(meses), ", ".join(meses))
        )

    return """<title>Desafio Pratic Leve Itabaiana</title>
%s
<div class="pn"><div class="pn-wrap">

  <div class="pn-hero">
    <p class="pn-kicker">RC Representações &middot; Pratic Leve &middot; Distribuidora Itabaiana</p>
    <h1>%s</h1>
    <p class="pn-sub">Campanha de %s a %s &middot; apuração em %s &middot; %d vendedores &middot; %d clientes na carteira</p>
    <div class="pn-premio-tag">Prêmio: resort all inclusive, com acompanhante, para os campeões</div>
  </div>

  <div class="pn-sec">
    <h2>Onde estamos e onde queremos chegar</h2>
    <p class="pn-lead">Base apurada no painel de vendas da distribuidora. As metas são o alvo de cada mês da campanha.</p>
    %s
  </div>

  <div class="pn-sec">
    <h2>A conta da campanha</h2>
    <p class="pn-lead">Pontua quem vende mix, não quem vende volume. O peso está no produto difícil e no cliente novo.</p>
    %s
  </div>

  <div class="pn-sec">
    <h2>Tabela de pontos por produto</h2>
    <p class="pn-lead">Curva A gira sozinha e vale pouco. Pipoca e as rústicas maiores são onde a campanha se ganha.</p>
    %s
  </div>

  <div class="pn-sec">
    <h2>Positivação por vendedor</h2>
    <p class="pn-lead">A carteira tem %d clientes ativos e só %s compram Pratic Leve hoje. Esse é o maior espaço da campanha.</p>
    %s
  </div>

  <div class="pn-sec">
    <h2>Ranking</h2>
    <p class="pn-lead">Ordenado por pontos. A coluna Prêmio mostra quem está acima do corte de %s de positivação.</p>
    %s
  </div>

  <div class="pn-sec">
    <h2>Premiação</h2>
    <p class="pn-lead">Viagem prevista para %s, com acompanhante em todas as faixas.</p>
    %s
  </div>

  <div class="pn-sec">
    %s
  </div>

  <p class="pn-rodape">Gerado por gerador_campanha_itabaiana.py &middot; fonte: relatório 322 &ndash; Venda Por Departamento (por RCA), fornecedor 935 PALHA INDÚSTRIA, e mix Pratic Leve da base ABC. Estrutura baseada no Desafio Ducamp 2026.</p>

</div></div>
""" % (
        CSS,
        esc(c["nome"] + " " + c["edicao"]),
        esc(c["inicio"]), esc(c["fim"]), esc(c["apuracao"]),
        len(ctx["baseline"]), t["carteira"],
        _bloco_metas(ctx),
        _bloco_regras(ctx),
        _bloco_produtos(ctx),
        t["carteira"], pct(t["pct_positivacao"]),
        _bloco_positivacao(ctx),
        pct(c["corte_qualificacao"] * 100, 0),
        _bloco_ranking(ctx),
        esc(c["viagem"]),
        _bloco_premios(ctx),
        nota,
    )
