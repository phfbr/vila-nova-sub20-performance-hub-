
from pathlib import Path
import pymupdf

# ==========================================
# VILA NOVA SUB-20 | PERFORMANCE HUB
# Etapa 12 - Extracao de textos das sumulas
# ==========================================

origem = Path("dados/brutos/sumulas")
destino = Path("dados/brutos/textos_sumulas")

destino.mkdir(parents=True, exist_ok=True)

jogos = {
    7: 833339,
    15: 833349,
    22: 833356,
    29: 833363,
    38: 833372,
    47: 833381,
    55: 833389
}

print("\nEXTRACAO DAS SUMULAS")
print("=" * 55)

total = 0

for numero_jogo, id_partida in jogos.items():

    arquivo = origem / f"{id_partida}_se.pdf"

    if not arquivo.exists():
        print(f"Jogo {numero_jogo}: PDF nao encontrado")
        continue

    try:
        with pymupdf.open(arquivo) as pdf:
            paginas = [
                pagina.get_text(sort=True)
                for pagina in pdf
            ]

        texto = "\n\n".join(paginas)

        saida = destino / f"{id_partida}_se.txt"
        saida.write_text(texto, encoding="utf-8")

        print(
            f"Jogo {numero_jogo}: "
            f"{len(paginas)} paginas | "
            f"{len(texto)} caracteres"
        )

        total += 1

    except Exception as erro:
        print(f"Jogo {numero_jogo}: erro - {erro}")

print("\nSUMULAS PROCESSADAS:", total)
print("Textos salvos em:", destino)
