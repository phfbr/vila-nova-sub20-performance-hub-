
from pathlib import Path
import requests
import truststore
from bs4 import BeautifulSoup

truststore.inject_into_ssl()

BASE = (
    "https://www.cbf.com.br/futebol-brasileiro/jogos/"
    "campeonato-brasileiro/sub-20-b/2026/"
    "vila-nova-x-operario/833339"
)

pasta = Path("dados/brutos")
pasta.mkdir(parents=True, exist_ok=True)

visualizacoes = {
    "documentos": "?view=documentos",
    "escalacao": "?view=escalacao"
}

for nome, parametro in visualizacoes.items():

    print(f"\nINVESTIGANDO: {nome.upper()}")
    print("=" * 50)

    try:
        resposta = requests.get(
            BASE + parametro,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=30
        )
        resposta.raise_for_status()

        arquivo = pasta / f"cbf_833339_{nome}.html"
        arquivo.write_text(
            resposta.text,
            encoding="utf-8"
        )

        soup = BeautifulSoup(
            resposta.text,
            "html.parser"
        )

        texto = soup.get_text(" ", strip=True)

        print("Status:", resposta.status_code)
        print("Tamanho HTML:", len(resposta.content))

        print("\nPREVIA:")
        print(texto[:2000])

        print("\nLINKS PARA ARQUIVOS:")

        for link in soup.find_all("a", href=True):
            href = link["href"]

            if any(
                termo in href.lower()
                for termo in [".pdf", "sumula", "documento"]
            ):
                print(href)

        print("\nArquivo salvo:", arquivo)

    except requests.exceptions.RequestException as erro:
        print("Erro:", erro)

print("\nInvestigacao concluida!")
