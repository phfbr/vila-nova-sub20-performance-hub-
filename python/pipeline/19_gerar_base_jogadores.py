
from pathlib import Path
import re
import pandas as pd
import pymupdf

# ==========================================
# VILA NOVA SUB-20 | PERFORMANCE HUB
# Etapa 19 - Extracao corrigida de jogadores
# ==========================================

origem = Path("dados/brutos/sumulas")
destino = Path("dados/tratados")
destino.mkdir(parents=True, exist_ok=True)

jogos = {
    7: 833339,
    15: 833349,
    22: 833356,
    29: 833363,
    38: 833372,
    47: 833381,
    55: 833389
}

colunas = [
    "id_partida", "jogo", "id_cbf",
    "camisa", "apelido", "nome_sumula",
    "titular", "reserva", "goleiro"
]

registros = []

def extrair_campo(palavras, inicio, fim):
    itens = [
        p for p in palavras
        if inicio <= p[0] < fim
    ]
    itens.sort(key=lambda p: p[0])
    return " ".join(p[4] for p in itens).strip()

for jogo, id_partida in jogos.items():

    arquivo = origem / f"{id_partida}_se.pdf"

    if not arquivo.exists():
        raise FileNotFoundError(arquivo)

    with pymupdf.open(arquivo) as pdf:
        palavras = pdf[0].get_text("words")

    # Localizar o titulo da relacao
    titulos = [
        p for p in palavras
        if p[4].casefold() == "jogadores"
    ]

    if not titulos:
        raise ValueError(
            f"Jogo {jogo}: relacao nao encontrada"
        )

    y_titulo = titulos[0][1]

    # Encontrar a palavra Vila no cabecalho
    candidatos = [
        p for p in palavras
        if p[4].casefold() == "vila"
        and y_titulo < p[1] < y_titulo + 30
    ]

    if len(candidatos) != 1:
        raise ValueError(
            f"Jogo {jogo}: nao foi possivel "
            "identificar a coluna do Vila Nova"
        )

    vila_esquerda = candidatos[0][0] < 290

    if vila_esquerda:
        deslocamento = 0
        limite_inicio = 40
        limite_fim = 290
    else:
        deslocamento = 258
        limite_inicio = 298
        limite_fim = 550

    print(
        f"\nJogo {jogo}: Vila Nova na "
        f"{'ESQUERDA' if vila_esquerda else 'DIREITA'}"
    )

    # A tabela inicia apos o cabecalho
    y_inicio = y_titulo + 35

    linhas = {}

    for palavra in palavras:
        x0, y0, *_ = palavra

        if not (limite_inicio <= x0 < limite_fim):
            continue

        if y0 < y_inicio:
            continue

        chave = round(y0 / 3) * 3
        linhas.setdefault(chave, []).append(palavra)

    encontrados = 0

    for palavras_linha in linhas.values():

        camisa = extrair_campo(
            palavras_linha,
            40 + deslocamento,
            58 + deslocamento
        )

        apelido = extrair_campo(
            palavras_linha,
            58 + deslocamento,
            115 + deslocamento
        )

        nome = extrair_campo(
            palavras_linha,
            115 + deslocamento,
            212 + deslocamento
        )

        situacao = extrair_campo(
            palavras_linha,
            212 + deslocamento,
            230 + deslocamento
        )

        id_cbf = extrair_campo(
            palavras_linha,
            250 + deslocamento,
            290 + deslocamento
        )

        if not re.fullmatch(r"\d{1,2}", camisa):
            continue

        if not re.fullmatch(r"\d{5,8}", id_cbf):
            continue

        if not re.match(r"^[TR]", situacao):
            continue

        registros.append({
            "id_partida": id_partida,
            "jogo": jogo,
            "id_cbf": id_cbf,
            "camisa": int(camisa),
            "apelido": apelido,
            "nome_sumula": nome,
            "titular": int(situacao.startswith("T")),
            "reserva": int(situacao.startswith("R")),
            "goleiro": int("(g)" in situacao.lower())
        })

        encontrados += 1

    print(f"Jogadores extraidos: {encontrados}")

df = pd.DataFrame(registros, columns=colunas)

# Validar antes de substituir os CSVs existentes
resumo = df.groupby("jogo").agg(
    relacionados=("id_cbf", "count"),
    titulares=("titular", "sum"),
    reservas=("reserva", "sum")
)

print("\n" + "=" * 60)
print("VALIDACAO FINAL")
print("=" * 60)
print(resumo.to_string())

duplicados = df.duplicated(
    ["id_partida", "id_cbf"]
).sum()

if len(resumo) != len(jogos):
    raise ValueError("Nem todas as partidas foram extraidas.")

if (resumo["titulares"] != 11).any():
    raise ValueError("Ha partidas sem 11 titulares.")

if duplicados:
    raise ValueError(
        f"Foram encontrados {duplicados} IDs duplicados."
    )

dim = (
    df.sort_values(["jogo", "id_cbf"])
    .drop_duplicates("id_cbf")
    [["id_cbf", "apelido", "nome_sumula", "goleiro"]]
    .copy()
)

df.to_csv(
    destino / "fato_jogadores_partidas_2026.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

dim.to_csv(
    destino / "dim_jogadores_2026.csv",
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print("\nJOGADORES UNICOS:", len(dim))
print("REGISTROS JOGADOR/PARTIDA:", len(df))
print("DUPLICADOS:", duplicados)
print("\nArquivos atualizados com sucesso!")
