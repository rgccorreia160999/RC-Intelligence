#!/usr/bin/env python3
"""
Gerador da Campanha de Vendas - Distribuidora Itabaiana / Pratic Leve.

Espelha a mecanica do Desafio Ducamp 2026 (pontos por mix + positivacao de
carteira + ranking + premiacao), adaptada ao mix Pratic Leve e a base de RCAs
da Itabaiana.

Entradas (pasta dados/):
  vendedores.csv           cadastro de RCAs e carteira
  historico_mensal.csv     painel de vendas mes a mes, por vendedor
  produtos.csv             SKUs Pratic Leve, curva ABC e pontos por caixa
  vendas_produto_vendedor.csv  (opcional) vendas por SKU x vendedor

Saidas (pasta saida/):
  baseline_vendedores.csv  media do periodo historico, por vendedor
  metas_vendedores.csv     metas individuais da campanha
  ranking.csv              ranking apurado (ou simulado sobre o baseline)
  painel_itabaiana.html    painel visual da campanha

Uso:
  python3 gerador_campanha_itabaiana.py
"""

import csv
import json
import os
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(BASE, "dados")
SAIDA = os.path.join(BASE, "saida")

# ---------------------------------------------------------------------------
# Parametros da campanha
# ---------------------------------------------------------------------------

CAMPANHA = {
    "nome": "Desafio Pratic Leve - Itabaiana",
    "edicao": "2026/2027",
    "inicio": "01/10/2026",
    "fim": "31/01/2027",
    "meses": 4,
    "apuracao": "Fevereiro/2027",
    "viagem": "Março/2027",
    # Crescimento pedido sobre a media historica
    "crescimento_faturamento": 0.20,
    "crescimento_volume": 0.20,
    # Positivacao: percentual da carteira que cada RCA deve atingir
    "meta_positivacao": 0.45,
    # Piso de positivacao para concorrer ao premio maximo
    "corte_qualificacao": 0.40,
}

PONTUACAO = {
    "pts_por_cliente_positivado": 50,
    "bonus_meta_positivacao": 500,   # atingiu meta_positivacao no mes
    "bonus_mix_completo": 100,       # por cliente com 4+ SKUs distintos
    "bonus_pipoca": 150,             # por cliente positivado na linha Pipoca
    "min_skus_mix_completo": 4,
}

PREMIACAO = [
    ("1\u00ba lugar \u2013 Campe\u00e3o Geral", "Resort 4 di\u00e1rias, all inclusive, com acompanhante"),
    ("2\u00ba lugar \u2013 Vice-Campe\u00e3o", "Resort 3 di\u00e1rias, all inclusive, com acompanhante"),
    ("3\u00ba lugar", "Resort 2 di\u00e1rias, all inclusive, com acompanhante"),
    ("Destaque Positiva\u00e7\u00e3o", "Resort 2 di\u00e1rias, all inclusive, com acompanhante"),
    ("Destaque Linha Pipoca", "Resort 2 di\u00e1rias, all inclusive, com acompanhante"),
]


# ---------------------------------------------------------------------------
# Leitura
# ---------------------------------------------------------------------------

def ler_csv(nome):
    caminho = os.path.join(DADOS, nome)
    if not os.path.exists(caminho):
        return []
    with open(caminho, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def num(valor, padrao=0.0):
    """Converte texto para float aceitando virgula decimal."""
    if valor is None:
        return padrao
    txt = str(valor).strip().replace(".", "").replace(",", ".") if "," in str(valor) else str(valor).strip()
    try:
        return float(txt)
    except ValueError:
        return padrao


# ---------------------------------------------------------------------------
# Baseline: media dos meses disponiveis no painel
# ---------------------------------------------------------------------------

def calcular_baseline(vendedores, historico):
    """Media por vendedor dos meses presentes em historico_mensal.csv."""
    por_vendedor = defaultdict(list)
    for linha in historico:
        por_vendedor[linha["codigo"]].append(linha)

    meses = sorted({l["mes"] for l in historico})
    baseline = []

    for v in vendedores:
        cod = v["codigo"]
        registros = por_vendedor.get(cod, [])
        n = len(registros) or 1

        carteira = sum(num(r["clientes_ativos"]) for r in registros) / n if registros else num(v["clientes_ativos"])
        positivados = sum(num(r["clientes_positivados"]) for r in registros) / n
        caixas = sum(num(r["qt_vendida_cx"]) for r in registros) / n
        valor = sum(num(r["valor_vendido"]) for r in registros) / n
        peso = sum(num(r["peso_kg"]) for r in registros) / n

        baseline.append({
            "codigo": cod,
            "vendedor": v["vendedor"],
            "equipe": v["equipe"],
            "meses_apurados": len(registros),
            "carteira": round(carteira, 1),
            "positivados": round(positivados, 1),
            "pct_positivacao": round(positivados / carteira * 100, 2) if carteira else 0.0,
            "caixas": round(caixas, 1),
            "valor": round(valor, 2),
            "peso": round(peso, 2),
            "ticket_por_caixa": round(valor / caixas, 2) if caixas else 0.0,
        })

    baseline.sort(key=lambda x: x["valor"], reverse=True)
    return baseline, meses


# ---------------------------------------------------------------------------
# Metas individuais
# ---------------------------------------------------------------------------

def calcular_metas(baseline):
    metas = []
    for b in baseline:
        meta_pos_clientes = round(b["carteira"] * CAMPANHA["meta_positivacao"])
        metas.append({
            "codigo": b["codigo"],
            "vendedor": b["vendedor"],
            "equipe": b["equipe"],
            "carteira": b["carteira"],
            "base_valor": b["valor"],
            "meta_valor": round(b["valor"] * (1 + CAMPANHA["crescimento_faturamento"]), 2),
            "base_caixas": b["caixas"],
            "meta_caixas": round(b["caixas"] * (1 + CAMPANHA["crescimento_volume"])),
            "base_positivados": b["positivados"],
            "meta_positivados": meta_pos_clientes,
            "base_pct_pos": b["pct_positivacao"],
            "meta_pct_pos": round(CAMPANHA["meta_positivacao"] * 100, 1),
            "gap_positivacao": round(meta_pos_clientes - b["positivados"], 1),
        })
    return metas


# ---------------------------------------------------------------------------
# Pontuacao
# ---------------------------------------------------------------------------

def mix_referencia(produtos):
    """Participacao de cada SKU no volume total, a partir da curva ABC.

    Usada apenas para projetar pontos quando ainda nao ha venda por SKU x
    vendedor. Pesos aproximam a distribuicao observada no historico do mix.
    """
    peso_abc = {"A": 8.0, "B": 2.5, "C": 0.6}
    pesos = {p["codigo"]: peso_abc.get(p["abc"], 1.0) for p in produtos}
    total = sum(pesos.values())
    return {cod: v / total for cod, v in pesos.items()}


def pontos_por_caixa_medio(produtos, mix):
    """Pontos medios que uma caixa gera, dado um mix de vendas."""
    return sum(mix[p["codigo"]] * num(p["pontos_cx"]) for p in produtos)


def calcular_ranking(baseline, produtos, vendas_sku):
    """Ranking da campanha.

    Se vendas_produto_vendedor.csv existir, usa a venda real por SKU.
    Caso contrario projeta os pontos de mix sobre o baseline, sinalizando
    o resultado como simulacao.
    """
    pontos_sku = {p["codigo"]: num(p["pontos_cx"]) for p in produtos}
    linha_sku = {p["codigo"]: p["linha"] for p in produtos}

    real = bool(vendas_sku)
    mix = mix_referencia(produtos)
    pts_cx_medio = pontos_por_caixa_medio(produtos, mix)

    # Agrega venda real por vendedor, quando houver
    agregado = defaultdict(lambda: {"pontos_mix": 0.0, "skus": set(), "pipoca": 0})
    if real:
        clientes_por_vendedor = defaultdict(lambda: defaultdict(set))
        for r in vendas_sku:
            cod_v = r["codigo_vendedor"]
            cod_p = r["codigo_produto"]
            qt = num(r["qt_cx"])
            agregado[cod_v]["pontos_mix"] += qt * pontos_sku.get(cod_p, 0)
            agregado[cod_v]["skus"].add(cod_p)
            cliente = r.get("cliente", "")
            if cliente:
                clientes_por_vendedor[cod_v][cliente].add(cod_p)
            if linha_sku.get(cod_p) == "PIPOCA" and qt > 0 and cliente:
                agregado[cod_v]["pipoca"] += 1

    ranking = []
    for b in baseline:
        cod = b["codigo"]

        if real and cod in agregado:
            pontos_mix = agregado[cod]["pontos_mix"]
            clientes_mix_completo = sum(
                1 for skus in clientes_por_vendedor[cod].values()
                if len(skus) >= PONTUACAO["min_skus_mix_completo"]
            )
            clientes_pipoca = agregado[cod]["pipoca"]
        else:
            pontos_mix = b["caixas"] * pts_cx_medio
            # Sem venda por SKU nao ha como apurar estes bonus: ficam zerados
            clientes_mix_completo = 0
            clientes_pipoca = 0

        pontos_pos = b["positivados"] * PONTUACAO["pts_por_cliente_positivado"]
        pct_pos = b["pct_positivacao"] / 100
        bonus_meta = PONTUACAO["bonus_meta_positivacao"] if pct_pos >= CAMPANHA["meta_positivacao"] else 0
        bonus_mix = clientes_mix_completo * PONTUACAO["bonus_mix_completo"]
        bonus_pipoca = clientes_pipoca * PONTUACAO["bonus_pipoca"]

        total = pontos_mix + pontos_pos + bonus_meta + bonus_mix + bonus_pipoca

        ranking.append({
            "codigo": cod,
            "vendedor": b["vendedor"],
            "equipe": b["equipe"],
            "carteira": b["carteira"],
            "positivados": b["positivados"],
            "pct_positivacao": b["pct_positivacao"],
            "caixas": b["caixas"],
            "valor": b["valor"],
            "pontos_mix": round(pontos_mix),
            "pontos_positivacao": round(pontos_pos),
            "bonus_meta_pos": bonus_meta,
            "bonus_mix_completo": bonus_mix,
            "bonus_pipoca": bonus_pipoca,
            "pontos_total": round(total),
            "qualificado": pct_pos >= CAMPANHA["corte_qualificacao"],
        })

    ranking.sort(key=lambda x: x["pontos_total"], reverse=True)
    for i, r in enumerate(ranking, 1):
        r["posicao"] = i

    return ranking, real


# ---------------------------------------------------------------------------
# Escrita
# ---------------------------------------------------------------------------

def escrever_csv(nome, linhas):
    if not linhas:
        return
    caminho = os.path.join(SAIDA, nome)
    with open(caminho, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(linhas[0].keys()))
        w.writeheader()
        w.writerows(linhas)
    print("  gerado: saida/%s (%d linhas)" % (nome, len(linhas)))


def main():
    os.makedirs(SAIDA, exist_ok=True)

    vendedores = ler_csv("vendedores.csv")
    historico = ler_csv("historico_mensal.csv")
    produtos = ler_csv("produtos.csv")
    vendas_sku = ler_csv("vendas_produto_vendedor.csv")

    if not vendedores or not historico:
        raise SystemExit("Faltam dados/vendedores.csv ou dados/historico_mensal.csv")

    baseline, meses = calcular_baseline(vendedores, historico)
    metas = calcular_metas(baseline)
    ranking, real = calcular_ranking(baseline, produtos, vendas_sku)

    print("Campanha: %s %s" % (CAMPANHA["nome"], CAMPANHA["edicao"]))
    print("Meses no painel: %s" % ", ".join(meses))
    print("Modo de apuracao: %s" % ("REAL (venda por SKU)" if real else "SIMULADO (sobre o baseline)"))
    print("")

    escrever_csv("baseline_vendedores.csv", baseline)
    escrever_csv("metas_vendedores.csv", metas)
    escrever_csv("ranking.csv", ranking)

    # Soma dos vendedores. Difere do "Total Geral" do relatorio porque o ERP
    # deduplica clientes atendidos por mais de um RCA.
    soma_partes = {
        "carteira": sum(b["carteira"] for b in baseline),
        "positivados": sum(b["positivados"] for b in baseline),
    }

    oficiais = ler_csv("totais_mensais.csv")
    if oficiais:
        n = len(oficiais)
        totais = {
            "carteira": sum(num(o["clientes_ativos"]) for o in oficiais) / n,
            "positivados": sum(num(o["clientes_positivados"]) for o in oficiais) / n,
            "caixas": sum(num(o["qt_vendida_cx"]) for o in oficiais) / n,
            "valor": sum(num(o["valor_vendido"]) for o in oficiais) / n,
            "peso": sum(num(o["peso_kg"]) for o in oficiais) / n,
            "fonte": "Total Geral do relatorio 322 (clientes deduplicados)",
        }
    else:
        totais = {
            "carteira": soma_partes["carteira"],
            "positivados": soma_partes["positivados"],
            "caixas": sum(b["caixas"] for b in baseline),
            "valor": sum(b["valor"] for b in baseline),
            "peso": sum(b["peso"] for b in baseline),
            "fonte": "soma dos vendedores",
        }

    totais["carteira_soma_rcas"] = soma_partes["carteira"]
    totais["positivados_soma_rcas"] = soma_partes["positivados"]
    totais["pct_positivacao"] = round(totais["positivados"] / totais["carteira"] * 100, 2)
    totais["meta_valor"] = round(totais["valor"] * (1 + CAMPANHA["crescimento_faturamento"]), 2)
    totais["meta_caixas"] = round(totais["caixas"] * (1 + CAMPANHA["crescimento_volume"]))
    totais["meta_positivados"] = round(totais["carteira"] * CAMPANHA["meta_positivacao"])

    contexto = {
        "campanha": CAMPANHA,
        "pontuacao": PONTUACAO,
        "premiacao": PREMIACAO,
        "meses": meses,
        "modo_real": real,
        "baseline": baseline,
        "metas": metas,
        "ranking": ranking,
        "produtos": [dict(p, pontos_cx=int(num(p["pontos_cx"]))) for p in produtos],
        "totais": totais,
    }

    with open(os.path.join(SAIDA, "campanha.json"), "w", encoding="utf-8") as fh:
        json.dump(contexto, fh, ensure_ascii=False, indent=2)
    print("  gerado: saida/campanha.json")

    from painel import render_painel
    html = render_painel(contexto)
    with open(os.path.join(SAIDA, "painel_itabaiana.html"), "w", encoding="utf-8") as fh:
        fh.write(html)
    print("  gerado: saida/painel_itabaiana.html")

    print("")
    print("Baseline consolidado (%d mes(es)):" % len(meses))
    print("  Carteira ativa .......... %d clientes" % totais["carteira"])
    print("  Positivados ............. %d (%.2f%%)" % (totais["positivados"], totais["pct_positivacao"]))
    print("  Volume .................. %d CX/mes" % totais["caixas"])
    print("  Faturamento ............. R$ %s/mes" % ("%.2f" % totais["valor"]))
    print("")
    print("Metas da campanha:")
    print("  Faturamento ............. R$ %s/mes (+%d%%)" % ("%.2f" % totais["meta_valor"], CAMPANHA["crescimento_faturamento"] * 100))
    print("  Volume .................. %d CX/mes (+%d%%)" % (totais["meta_caixas"], CAMPANHA["crescimento_volume"] * 100))
    print("  Positivacao ............. %d clientes (%.0f%% da carteira)" % (totais["meta_positivados"], CAMPANHA["meta_positivacao"] * 100))


if __name__ == "__main__":
    main()
