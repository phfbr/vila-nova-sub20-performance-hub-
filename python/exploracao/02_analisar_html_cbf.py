
from pathlib import Path
from bs4 import BeautifulSoup
import re

# Arquivo HTML salvo na etapa anterior
caminho = Path("dados/brutos/cbf_sub20_2026.html")

html = caminho.read_text(encoding="utf-8")

soup = BeautifulSoup(html, "html.parser")

print("\nANALISE DO HTML DA CBF")
print("=" * 50)

# 1. Procurar termos no HTML original
termos = [
    "Vila Nova",
    "Vila",
    "Vil",
    "SUB-20 B",
    "GUSTAVO LEMOS"
]

for termo in termos:
    ocorrencias = len(
        re.findall(
            re.escape(termo),
            html,
            flags=re.IGNORECASE
        )
    )

    print(f"{termo}: {ocorrencias} ocorrencias")

# 2. Procurar trechos relacionados ao Vila Nova
print("\nTRECHOS ENCONTRADOS")
print("=" * 50)

padrao = re.compile(
    r"vila[\s\-]*nova",
    flags=re.IGNORECASE
)

resultados = list(padrao.finditer(html))

for resultado in resultados[:10]:
    inicio = max(0, resultado.start() - 200)
    fim = min(len(html), resultado.end() + 200)

    trecho = html[inicio:fim]

    print("\n--- OCORRENCIA ---")
    print(trecho)

# 3. Verificar tabelas HTML
tabelas = soup.find_all("table")

print("\nTABELAS HTML ENCONTRADAS:", len(tabelas))

# 4. Verificar scripts JSON
scripts = soup.find_all(
    "script",
    type="application/json"
)

print("SCRIPTS JSON ENCONTRADOS:", len(scripts))

# 5. Procurar links de partidas
links = soup.find_all("a", href=True)

links_partidas = [
    link.get("href")
    for link in links
    if any(
        termo in link.get("href", "").lower()
        for termo in ["partida", "jogo", "sumula"]
    )
]

print("\nLINKS RELACIONADOS A PARTIDAS:")
for link in sorted(set(links_partidas))[:20]:
    print(link)

print("\nAnalise concluida!")
