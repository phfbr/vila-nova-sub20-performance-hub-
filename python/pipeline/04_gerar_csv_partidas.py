
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
import re

# ==========================================
# VILA NOVA SUB-20 | PERFORMANCE HUB
# Extracao de partidas - CBF 2026
# ==========================================

origem = Path("dados/brutos/cbf_vila_nova_jogos_2026.html")
destino = Path("dados/tratados/partidas_vila_nova_2026.csv")

destino.parent.mkdir(parents=True, exist_ok=True)

html = origem.read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

# Localizar cards de jogos
cards = soup.select('[class*="game-card"]')

print("Cards encontrados:", len(cards))

partidas = []

# Interpretar o texto de cada card
padrao_placar = re.compile(
    r"([A-Za-z]{3})\s+(\d+)\s+X\s+"
    r"([A-Za-z]{3})\s+(\d+)",
    re.IGNORECASE
)

padrao_data = re.compile(
    r"\d{2}/\d{2}/\d{4}"
)

padrao_jogo = re.compile(
    r"Jogo\s+(\d+)",
    re.IGNORECASE
)

for card in cards:
    texto = card.get_text(" ", strip=True)

    placar = padrao_placar.search(texto)
    data = padrao_data.search(texto)
    jogo = padrao_jogo.search(texto)

    if not (placar and data and jogo):
        continue

    mandante = placar.group(1).upper()
    gols_mandante = int(placar.group(2))
    visitante = placar.group(3).upper()
    gols_visitante = int(placar.group(4))

    # Considerar apenas partidas do Vila Nova
    if "VIL" not in (mandante, visitante):
        continue

    mando = "Casa" if mandante == "VIL" else "Fora"

    gols_pro = (
        gols_mandante if mando == "Casa"
        else gols_visitante
    )

    gols_contra = (
        gols_visitante if mando == "Casa"
        else gols_mandante
    )

    if gols_pro > gols_contra:
        resultado = "Vitoria"
    elif gols_pro < gols_contra:
        resultado = "Derrota"
    else:
        resultado = "Empate"

    partidas.append({
        "competicao": "Brasileiro Sub-20 B",
        "temporada": 2026,
        "jogo": int(jogo.group(1)),
        "data": pd.to_datetime(
            data.group(),
            format="%d/%m/%Y"
        ),
        "mandante": mandante,
        "visitante": visitante,
        "gols_mandante": gols_mandante,
        "gols_visitante": gols_visitante,
        "mando_vila": mando,
        "gols_pro": gols_pro,
        "gols_contra": gols_contra,
        "resultado": resultado,
        "fonte": "CBF"
    })

# Criar DataFrame
df = pd.DataFrame(partidas)

if df.empty:
    print("Nenhuma partida extraida.")
    raise SystemExit(1)

# Ordenar por data
df = df.sort_values("data")

# Remover duplicatas
df = df.drop_duplicates(subset=["jogo"])

# Salvar CSV
df.to_csv(
    destino,
    index=False,
    sep=";",
    encoding="utf-8-sig",
    date_format="%Y-%m-%d"
)

print("\nPARTIDAS EXTRAIDAS:")
print(df.to_string(index=False))

print("\nRESUMO:")
print("Partidas:", len(df))
print("Vitorias:", (df["resultado"] == "Vitoria").sum())
print("Empates:", (df["resultado"] == "Empate").sum())
print("Derrotas:", (df["resultado"] == "Derrota").sum())
print("Gols pro:", df["gols_pro"].sum())
print("Gols contra:", df["gols_contra"].sum())

print("\nCSV salvo em:", destino)
