
from pathlib import Path
import re
import pandas as pd

# ==========================================
# VILA NOVA SUB-20 | PERFORMANCE HUB
# Etapa 14 - Extracao de gols oficiais
# ==========================================

pasta = Path("dados/brutos/textos_sumulas")
saida = Path("dados/tratados")
saida.mkdir(parents=True, exist_ok=True)

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
    r"(NR|PN|CT|FT)\s+"
    r"(.+?)\s{2,}"
    r"(.+?)\s*$"
)

eventos = []

for jogo, id_partida in jogos.items():

    arquivo = pasta / f"{id_partida}_se.txt"

    if not arquivo.exists():
        print(f"Jogo {jogo}: arquivo ausente")
        continue

    linhas = arquivo.read_text(
        encoding="utf-8"
    ).splitlines()

    dentro_gols = False
    encontrados = 0

    for linha in linhas:

        if linha.strip() == "Gols":
            dentro_gols = True
            continue

        if dentro_gols and (
            linha.strip().startswith("NR =")
            or linha.strip() == "Cartões Amarelos"
        ):
            break

        if not dentro_gols:
            continue

        resultado = padrao.match(linha)

        if not resultado:
            continue

        tempo, periodo, camisa, tipo, nome, equipe = (
            resultado.groups()
        )

        equipe = equipe.strip()
        nome = nome.strip()

        # CT = gol contra.
        # O beneficiado e o adversario do atleta.
        if tipo == "CT":
            beneficiado = (
                "Adversario"
                if "Vila Nova" in equipe
                else "Vila Nova"
            )
        else:
            beneficiado = (
                "Vila Nova"
                if "Vila Nova" in equipe
                else "Adversario"
            )

        eventos.append({
            "id_partida": id_partida,
            "jogo": jogo,
            "tempo": tempo,
            "periodo": periodo,
            "camisa": int(camisa),
            "jogador": nome,
            "equipe_jogador": equipe,
            "tipo_gol": tipo,
            "equipe_beneficiada": beneficiado,
            "gol_vila": int(
                beneficiado == "Vila Nova"
            )
        })

        encontrados += 1

    print(
        f"Jogo {jogo}: "
        f"{encontrados} eventos de gol"
    )

df = pd.DataFrame(eventos)

if df.empty:
    print("\nNenhum gol extraido.")
    raise SystemExit(1)

arquivo_saida = saida / "fato_gols_2026.csv"

df.to_csv(
    arquivo_saida,
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "=" * 55)
print("RESUMO DOS GOLS")
print("=" * 55)

resumo = df.groupby("jogo").agg(
    gols_vila=("gol_vila", "sum"),
    eventos=("jogo", "size")
)

print(resumo.to_string())

print("\nTOTAL DE GOLS DO VILA:", df["gol_vila"].sum())
print("TOTAL DE EVENTOS:", len(df))
print("\nArquivo salvo:", arquivo_saida)
