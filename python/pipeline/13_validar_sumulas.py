
from pathlib import Path
import re
import unicodedata

# ==========================================
# VILA NOVA SUB-20 | PERFORMANCE HUB
# Etapa 13 - Validacao das sumulas oficiais
# ==========================================

pasta = Path("dados/brutos/textos_sumulas")

jogos = {
    7: 833339,
    15: 833349,
    22: 833356,
    29: 833363,
    38: 833372,
    47: 833381,
    55: 833389
}

secoes = [
    "Relação de Jogadores",
    "Gols",
    "Cartões Amarelos",
    "Cartões Vermelhos",
    "Substituições"
]

def normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(
        caractere for caractere in texto
        if not unicodedata.combining(caractere)
    ).casefold()

def extrair_secao(linhas, titulo):
    titulo_normalizado = normalizar(titulo)

    inicio = None

    for indice, linha in enumerate(linhas):
        if normalizar(linha.strip()) == titulo_normalizado:
            inicio = indice + 1
            break

    if inicio is None:
        return None

    fim = len(linhas)

    for indice in range(inicio, len(linhas)):
        linha = normalizar(linhas[indice].strip())

        if any(
            linha == normalizar(secao)
            for secao in secoes
        ):
            fim = indice
            break

        if (
            "publicacao da sumula" in linha
            or "ocorrencias / observacoes" in linha
            or "observacoes eventuais" in linha
        ):
            fim = indice
            break

    return linhas[inicio:fim]

print("\nVALIDACAO DAS 7 SUMULAS")
print("=" * 65)

for numero_jogo, id_partida in jogos.items():

    arquivo = pasta / f"{id_partida}_se.txt"

    print(f"\nJOGO {numero_jogo} | ID {id_partida}")
    print("-" * 65)

    if not arquivo.exists():
        print("ERRO: arquivo nao encontrado.")
        continue

    texto = arquivo.read_text(encoding="utf-8")
    linhas = texto.splitlines()

    for secao in secoes:
        conteudo = extrair_secao(linhas, secao)

        if conteudo is None:
            print(f"{secao}: NAO ENCONTRADA")
            continue

        linhas_validas = [
            linha.strip()
            for linha in conteudo
            if linha.strip()
        ]

        print(
            f"{secao}: ENCONTRADA "
            f"({len(linhas_validas)} linhas)"
        )

        if secao == "Gols":
            for linha in linhas_validas:
                if re.search(r"\bVila Nova\s*/\s*GO\b", linha, re.I):
                    print("  VILA:", linha[:160])

print("\nValidacao concluida!")
