
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ==========================================
# VILA NOVA SUB-20 | PERFORMANCE HUB
# Etapa 5 - Documentos das partidas
# ==========================================

arquivo = Path(
    "dados/brutos/cbf_vila_nova_jogos_2026.html"
)

html = arquivo.read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

base = "https://www.cbf.com.br"

cards = soup.select('[class*="game-card"]')

print("\nDOCUMENTOS DAS PARTIDAS")
print("=" * 55)

for card in cards:
    texto = card.get_text(" ", strip=True)

    print(f"\nPARTIDA: {texto[:110]}")

    links = card.find_all("a", href=True)

    if not links:
        print("Nenhum link encontrado neste card.")
        continue

    for link in links:
        endereco = urljoin(base, link["href"])
        descricao = link.get_text(" ", strip=True)

        print("Descricao:", descricao or "Sem descricao")
        print("URL:", endereco)

print("\nInvestigacao concluida!")
