
from pathlib import Path
import requests
import truststore

truststore.inject_into_ssl()

# ==========================================
# VILA NOVA SUB-20 | PERFORMANCE HUB
# Download dos documentos oficiais - CBF
# ==========================================

documentos = {
    "833339_se.pdf": (
        "https://conteudo.cbf.com.br/"
        "sumulas/2026/269427se.pdf"
    ),
    "833339_b.pdf": (
        "https://conteudo.cbf.com.br/"
        "sumulas/2026/269427b.pdf"
    ),
    "833339_rdj.pdf": (
        "https://conteudo.cbf.com.br/"
        "sumulas/2026/269427rdj.pdf"
    )
}

pasta = Path("dados/brutos/sumulas")
pasta.mkdir(parents=True, exist_ok=True)

for nome, url in documentos.items():

    print(f"\nBaixando: {nome}")

    try:
        resposta = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=30
        )
        resposta.raise_for_status()

        if not resposta.content.startswith(b"%PDF"):
            print("Resposta recebida nao e um PDF valido.")
            continue

        arquivo = pasta / nome
        arquivo.write_bytes(resposta.content)

        print("Download concluido!")
        print("Tamanho:", len(resposta.content), "bytes")
        print("Arquivo:", arquivo)

    except requests.exceptions.RequestException as erro:
        print("Erro:", erro)

print("\nProcesso finalizado!")
