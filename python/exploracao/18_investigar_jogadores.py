
from pathlib import Path
import pymupdf

# ==========================================
# VILA NOVA SUB-20 | PERFORMANCE HUB
# Etapa 18 - Investigar tabela de jogadores
# ==========================================

arquivo = Path(
    "dados/brutos/sumulas/833339_se.pdf"
)

with pymupdf.open(arquivo) as pdf:
    pagina = pdf[0]

    palavras = pagina.get_text("words", sort=True)

print("\nTABELA DE JOGADORES - POSICOES NO PDF")
print("=" * 75)

# Localizar a regiao da relacao de jogadores
cabecalhos = [
    palavra for palavra in palavras
    if palavra[4].lower() == "jogadores"
]

if not cabecalhos:
    print("Cabecalho nao encontrado.")
    raise SystemExit(1)

y_inicio = cabecalhos[0][1]

for palavra in palavras:
    x0, y0, x1, y1, texto, *_ = palavra

    if y_inicio <= y0 <= y_inicio + 280:
        print(
            f"X={x0:6.1f} | "
            f"Y={y0:6.1f} | "
            f"{texto}"
        )

print("\nInvestigacao concluida!")
