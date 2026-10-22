
from pathlib import Path

arquivo = Path(
    "dados/brutos/textos_sumulas/833339_se.txt"
)

texto = arquivo.read_text(encoding="utf-8")
linhas = texto.splitlines()

termos = [
    "Relação de Jogadores",
    "Substituições",
    "Gols",
    "Cartões Amarelos",
    "Cartões Vermelhos"
]

print("\nESTRUTURA DA SUMULA")
print("=" * 55)

for termo in termos:
    print(f"\nPROCURANDO: {termo}")
    print("-" * 55)

    encontrados = 0

    for indice, linha in enumerate(linhas):
        if termo.casefold() in linha.casefold():

            encontrados += 1

            inicio = max(0, indice - 2)
            fim = min(len(linhas), indice + 18)

            for numero in range(inicio, fim):
                print(
                    f"{numero + 1:03d} | {linhas[numero]}"
                )

            print("-" * 55)

    if encontrados == 0:
        print("Secao nao encontrada com esse nome.")

print("\nAnalise concluida!")
