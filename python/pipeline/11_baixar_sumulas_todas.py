
from pathlib import Path
from urllib.parse import urljoin
import requests
import truststore
from bs4 import BeautifulSoup

truststore.inject_into_ssl()

BASE = "https://www.cbf.com.br"

jogos = {
    7: 833339,
    15: 833349,
    22: 833356,
    29: 833363,
    38: 833372,
    47: 833381,
    55: 833389
}

pasta = Path("dados/brutos/sumulas")
pasta.mkdir(parents=True, exist_ok=True)

sessao = requests.Session()
sessao.headers.update({
    "User-Agent": "Mozilla/5.0"
})

for numero_jogo, id_partida in jogos.items():

    print(f"\nJOGO {numero_jogo}")

    # Acessar a pagina de documentos da partida
    url = (
        f"{BASE}/futebol-brasileiro/jogos/"
        f"campeonato-brasileiro/sub-20-b/2026/"
        f"jogo/{id_partida}?view=documentos"
    )

    try:
        resposta = sessao.get(url, timeout=30)
        resposta.raise_for_status()

        soup = BeautifulSoup(
            resposta.text, "html.parser"
        )

        links = set()

        for link in soup.find_all("a", href=True):
            href = urljoin(BASE, link["href"])

            if (
                "conteudo.cbf.com.br/sumulas/" in href
                and href.lower().endswith("se.pdf")
            ):
                links.add(href)

        if not links:
            print("Sumula nao encontrada.")
            continue

        for pdf_url in sorted(links):

            pdf = sessao.get(pdf_url, timeout=30)
            pdf.raise_for_status()

            if not pdf.content.startswith(b"%PDF"):
                print("Arquivo invalido:", pdf_url)
                continue

            arquivo = pasta / f"{id_partida}_se.pdf"
            arquivo.write_bytes(pdf.content)

            print("Sumula salva:", arquivo.name)

    except requests.exceptions.RequestException as erro:
        print("Erro:", erro)

print("\nDownloads finalizados!")
