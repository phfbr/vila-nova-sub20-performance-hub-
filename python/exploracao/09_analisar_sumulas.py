
from pathlib import Path
import pymupdf

# ==========================================
# VILA NOVA SUB-20 | PERFORMANCE HUB
# Etapa 9 - Analise dos PDFs oficiais
# ==========================================

pasta = Path("dados/brutos/sumulas")
saida = Path("dados/brutos/textos_sumulas")
saida.mkdir(parents=True, exist_ok=True)

arquivos = sorted(pasta.glob("833339_*.pdf"))

if not arquivos:
    print("Nenhum PDF encontrado.")
    raise SystemExit(1)

for arquivo in arquivos:
    print("\n" + "=" * 55)
    print("DOCUMENTO:", arquivo.name)

    try:
        with pymupdf.open(arquivo) as pdf:
            print("Paginas:", len(pdf))

            paginas = [
                pagina.get_text(sort=True)
                for pagina in pdf
            ]

        texto = "\n\n".join(paginas)

        destino = saida / f"{arquivo.stem}.txt"
        destino.write_text(texto, encoding="utf-8")

        print("Caracteres extraidos:", len(texto))
        print("Texto salvo em:", destino)

        termos = [
            "Vila Nova",
            "Operario",
            "Gol",
            "Cartao",
            "Substituicao",
            "Atletas"
        ]

        print("\nTERMOS IDENTIFICADOS:")

        texto_normalizado = (
            texto.casefold()
            .replace("ã", "a")
            .replace("ç", "c")
            .replace("í", "i")
            .replace("ó", "o")
            .replace("ú", "u")
        )

        for termo in termos:
            encontrado = termo.casefold() in texto_normalizado
            print(f"{termo}: {encontrado}")

        print("\nPREVIA DO DOCUMENTO:")
        print("-" * 55)
        print(texto[:2500] or "[Sem texto extraivel]")

    except Exception as erro:
        print("Erro ao analisar:", erro)

print("\nAnalise concluida!")
