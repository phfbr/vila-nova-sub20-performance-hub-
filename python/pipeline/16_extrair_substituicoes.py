
from pathlib import Path
import re
import pandas as pd

# ==========================================
# VILA NOVA SUB-20 | PERFORMANCE HUB
# Etapa 16 - Extracao de substituicoes
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
    r"^\s*(\d{1,2}:\d{2}|-)\s+"
    r"(1T|2T|INT)\s+"
    r"(.+?/[A-Z]{2})\s{2,}"
    r"(\d+)\s*-\s*(.+?)\s{2,}"
    r"(\d+)\s*-\s*(.+?)\s*$",
    re.IGNORECASE
)

registros = []

for jogo, id_partida in jogos.items():

    arquivo = origem / f"{id_partida}_se.txt"

    if not arquivo.exists():
        print(f"Jogo {jogo}: arquivo nao encontrado")
        continue

    linhas = arquivo.read_text(
        encoding="utf-8"
    ).splitlines()

    dentro = False
    encontrados = 0

    for linha in linhas:

        titulo = linha.strip()

        if titulo == "Substituições":
            dentro = True
            continue

        if dentro and (
            titulo.startswith("Confederação Brasileira")
            or titulo.startswith("Publicação da Súmula")
        ):
            break

        if not dentro:
            continue

        resultado = padrao.match(linha)

        if not resultado:
            continue

        (
            tempo,
            periodo,
            equipe,
            camisa_entrou,
            jogador_entrou,
            camisa_saiu,
            jogador_saiu
        ) = resultado.groups()

        registros.append({
            "id_partida": id_partida,
            "jogo": jogo,
            "tempo": tempo,
            "periodo": periodo,
            "equipe": equipe.strip(),
            "camisa_entrou": int(camisa_entrou),
            "jogador_entrou": jogador_entrou.strip(),
            "camisa_saiu": int(camisa_saiu),
            "jogador_saiu": jogador_saiu.strip()
        })

        encontrados += 1

    print(
        f"Jogo {jogo}: "
        f"{encontrados} substituicoes"
    )

df = pd.DataFrame(registros)

if df.empty:
    print("Nenhuma substituicao encontrada.")
    raise SystemExit(1)

arquivo_saida = destino / "fato_substituicoes_2026.csv"

df.to_csv(
    arquivo_saida,
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "=" * 55)
print("SUBSTITUICOES POR EQUIPE")
print("=" * 55)

print(
    df.groupby("equipe")
    .size()
    .to_string()
)

vila = df[
    df["equipe"].str.contains(
        "Vila Nova", case=False, na=False
    )
]

print("\nSUBSTITUICOES DO VILA POR JOGO")

print(
    vila.groupby("jogo")
    .size()
    .reindex(jogos.keys(), fill_value=0)
    .to_string()
)

print("\nTOTAL DO VILA:", len(vila))
print("TOTAL GERAL:", len(df))
print("Arquivo salvo:", arquivo_saida)
