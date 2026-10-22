
from pathlib import Path

import requests
import truststore
from bs4 import BeautifulSoup

# ==========================================
# VILA NOVA SUB-20 PERFORMANCE HUB
# TEMPORADA 2026 - CBF
# ==========================================

# Utilizar certificados do Windows
truststore.inject_into_ssl()

URL = (
    "https://www.cbf.com.br/futebol-brasileiro/"
    "tabelas/campeonato-brasileiro/sub-20-b/"
    "2026?documento=Tabela+Detalhada"
)

destino = Path("dados/brutos")
destino.mkdir(parents=True, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html"
}

print("Consultando site oficial da CBF...")

try:
    resposta = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    resposta.raise_for_status()

    print("Status HTTP:", resposta.status_code)

    arquivo = destino / "cbf_sub20_2026.html"

    arquivo.write_text(
        resposta.text,
        encoding="utf-8"
    )

    soup = BeautifulSoup(
        resposta.text,
        "html.parser"
    )

    texto = soup.get_text(
        separator=" ",
        strip=True
    )

    print("\nRESULTADO DA EXTRACAO")
    print("----------------------------")
    print("Tamanho HTML:", len(resposta.content))
    print("Vila Nova encontrado:", "vila nova" in texto.lower())
    print("Tabela encontrada:", "tabela" in texto.lower())

    print("\nPREVIA DOS DADOS:")
    print(texto[:1000])

    print("\nArquivo salvo em:", arquivo)

except requests.exceptions.SSLError as erro:
    print("\nERRO SSL:")
    print(erro)

except requests.exceptions.RequestException as erro:
    print("\nERRO DE CONEXAO:")
    print(erro)
