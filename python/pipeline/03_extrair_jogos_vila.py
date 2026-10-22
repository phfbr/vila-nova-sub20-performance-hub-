
from pathlib import Path
import requests
import truststore
from bs4 import BeautifulSoup

truststore.inject_into_ssl()

URL = (
    "https://www.cbf.com.br/futebol-brasileiro/"
    "times/campeonato-brasileiro/sub-20-b/2026/"
    "20079?tab=historico-de-partidas"
)

pasta = Path("dados/brutos")
pasta.mkdir(parents=True, exist_ok=True)

print("Consultando partidas do Vila Nova Sub-20...")

try:
    resposta = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )
    resposta.raise_for_status()

    arquivo = pasta / "cbf_vila_nova_jogos_2026.html"
    arquivo.write_text(
        resposta.text,
        encoding="utf-8"
    )

    soup = BeautifulSoup(resposta.text, "html.parser")

    
    # Investigar a estrutura real da página
    texto = soup.get_text(" ", strip=True)

    print("Status HTTP:", resposta.status_code)
    print("Vila Nova no texto:", "Vila Nova" in texto)
    print("Jogo 55 no texto:", "Jogo 55" in texto)
    print("Sport no texto:", "Sport" in texto)

    print("\nCLASSES RELACIONADAS A JOGOS:")

    classes = set()

    for elemento in soup.find_all(class_=True):
        for classe in elemento.get("class", []):
            if any(
                termo in classe.lower()
                for termo in [
                    "game", "match", "jogo",
                    "partida", "fixture", "card"
                ]
            ):
                classes.add(classe)

    for classe in sorted(classes):
        print(classe)

    print("\nTRECHOS COM 'JOGO 55':")

    for termo in ["Jogo 55", "27/05/2026"]:
        posicao = texto.find(termo)

        if posicao >= 0:
            inicio = max(0, posicao - 150)
            fim = posicao + 300
            print(texto[inicio:fim])
        else:
            print(f"{termo}: não encontrado")

    print("\nHTML salvo em:", arquivo)

except requests.exceptions.RequestException as erro:
    print("Erro de conexão:", erro)
