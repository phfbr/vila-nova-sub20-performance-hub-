
from pathlib import Path
import requests
import truststore
from bs4 import BeautifulSoup

truststore.inject_into_ssl()

URL = (
    "https://www.cbf.com.br/futebol-brasileiro/jogos/"
    "campeonato-brasileiro/sub-20-b/2026/"
    "vila-nova-x-operario/833339"
)

destino = Path("dados/brutos")
destino.mkdir(parents=True, exist_ok=True)

print("Investigando Vila Nova x Operario...")

try:
    resposta = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )
    resposta.raise_for_status()

    arquivo = destino / "cbf_jogo_833339.html"
    arquivo.write_text(resposta.text, encoding="utf-8")

    soup = BeautifulSoup(resposta.text, "html.parser")
    texto = soup.get_text(" ", strip=True)

    print("\nSTATUS:", resposta.status_code)
    print("Tamanho HTML:", len(resposta.content))

    print("\nSECOES ENCONTRADAS:")
    for termo in [
        "Escalação", "Documentos",
        "Súmula", "Substituição", "Cartão", "Gols"
    ]:
        print(f"{termo}: {termo.lower() in texto.lower()}")

    print("\nLINKS PARA DOCUMENTOS:")
    encontrados = set()

    for link in soup.find_all("a", href=True):
        href = link["href"]
        descricao = link.get_text(" ", strip=True)

        if any(
            palavra in (href + " " + descricao).lower()
            for palavra in ["sumula", "súmula", ".pdf", "documento"]
        ):
            if href not in encontrados:
                print(descricao or "Sem descricao", "->", href)
                encontrados.add(href)

    print("\nPREVIA DO CONTEUDO:")
    print(texto[:1800])

    print("\nHTML salvo em:", arquivo)

except requests.exceptions.RequestException as erro:
    print("Erro na requisicao:", erro)
