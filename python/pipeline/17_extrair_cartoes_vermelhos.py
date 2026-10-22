
from pathlib import Path
import re
import pandas as pd

# ==========================================
# VILA NOVA SUB-20 | PERFORMANCE HUB
# Etapa 17 - Cartoes vermelhos
# ==========================================

origem = Path("dados/brutos/textos_sumulas")
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

padrao = re.compile(
    r"^\s*(\+?\d+(?::\d{2})?)\s+"
    r"(1T|2T)\s+"
    r"(\d+)\s+"
    r"(.+?)\s+-\s+"
    r"(.+?/[A-Z]{2})\s*$",
    re.IGNORECASE
)

eventos = []

for jogo, id_partida in jogos.items():

    arquivo = origem / f"{id_partida}_se.txt"

    if not arquivo.exists():
        print(f"Jogo {jogo}: arquivo ausente")
        continue

    linhas = arquivo.read_text(
        encoding="utf-8"
    ).splitlines()

    dentro = False
    encontrados = 0

    for linha in linhas:

        titulo = linha.strip()

        if titulo == "Cartões Vermelhos":
            dentro = True
            continue

        if dentro and (
            "Publicação da Súmula" in linha
            or titulo == "Ocorrências / Observações"
        ):
            break

        if not dentro:
            continue

        resultado = padrao.match(linha)

        if not resultado:
            continue

        tempo, periodo, camisa, jogador, equipe = (
            resultado.groups()
        )

        eventos.append({
            "id_partida": id_partida,
            "jogo": jogo,
            "tempo": tempo,
            "periodo": periodo,
            "camisa": int(camisa),
            "jogador": jogador.strip(),
            "equipe": equipe.strip(),
            "tipo_cartao": "Vermelho"
        })

        encontrados += 1

    print(f"Jogo {jogo}: {encontrados} vermelhos")

colunas = [
    "id_partida",
    "jogo",
    "tempo",
    "periodo",
    "camisa",
    "jogador",
    "equipe",
    "tipo_cartao"
]

df = pd.DataFrame(eventos, columns=colunas)

arquivo_saida = (
    destino / "fato_cartoes_vermelhos_2026.csv"
)

df.to_csv(
    arquivo_saida,
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "=" * 55)
print("CARTOES VERMELHOS POR EQUIPE")
print("=" * 55)

if df.empty:
    print("Nenhum cartao vermelho identificado.")
else:
    print(df.groupby("equipe").size().to_string())

    print("\nDETALHAMENTO")
    print(df.to_string(index=False))

print("\nTOTAL GERAL:", len(df))
print("Arquivo salvo:", arquivo_saida)
