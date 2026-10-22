
from pathlib import Path
import pandas as pd
import unicodedata
import re

BASE = Path("dados/tratados")

def normalizar(texto):
    if pd.isna(texto):
        return ""
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(
        c for c in texto if not unicodedata.combining(c)
    )
    return re.sub(r"\s+", " ", texto).strip().upper()

def carregar(nome):
    return pd.read_csv(
        BASE / nome,
        sep=";",
        dtype={"id_cbf": "string"}
    )

jogadores = carregar("fato_jogadores_partidas_2026.csv")
gols = carregar("fato_gols_2026.csv")
amarelos = carregar("fato_cartoes_amarelos_2026.csv")
vermelhos = carregar("fato_cartoes_vermelhos_2026.csv")
substituicoes = carregar("fato_substituicoes_2026.csv")

jogadores["nome_norm"] = jogadores["nome_sumula"].map(normalizar)
jogadores["apelido_norm"] = jogadores["apelido"].map(normalizar)

# A camisa so e unica dentro de uma equipe e partida.
# Portanto, auditamos exclusivamente eventos do Vila Nova.

def conferir_eventos(df, nome, coluna_camisa, coluna_equipe):
    vila = df[
        df[coluna_equipe]
        .astype(str)
        .str.contains("Vila Nova", case=False, na=False)
    ].copy()

    referencia = jogadores[
        ["id_partida", "camisa", "id_cbf"]
    ].rename(columns={
        "camisa": coluna_camisa
    })

    conferencia = vila.merge(
        referencia,
        on=["id_partida", coluna_camisa],
        how="left",
        indicator=True
    )

    pendentes = conferencia[
        conferencia["_merge"] != "both"
    ]

    print(f"\n{nome}")
    print("-" * 55)
    print("Eventos do Vila:", len(vila))
    print("Camisas encontradas:", len(conferencia) - len(pendentes))
    print("Sem correspondencia:", len(pendentes))

    if not pendentes.empty:
        colunas = [
            c for c in [
                "jogo", coluna_camisa, "jogador",
                "jogador_entrou", "jogador_saiu"
            ]
            if c in pendentes.columns
        ]
        print(pendentes[colunas].to_string(index=False))

    return conferencia

print("=" * 60)
print("AUDITORIA CRUZADA - VILA NOVA SUB-20")
print("=" * 60)

conferir_eventos(
    gols, "GOLS", "camisa", "equipe_jogador"
)

conferir_eventos(
    amarelos, "CARTOES AMARELOS", "camisa", "equipe"
)

conferir_eventos(
    vermelhos, "CARTOES VERMELHOS", "camisa", "equipe"
)

conferir_eventos(
    substituicoes,
    "SUBSTITUICOES - ENTRADAS",
    "camisa_entrou",
    "equipe"
)

conferir_eventos(
    substituicoes,
    "SUBSTITUICOES - SAIDAS",
    "camisa_saiu",
    "equipe"
)

print("\n" + "=" * 60)
print("INTEGRIDADE DOS IDs CBF")
print("=" * 60)

print("Registros jogador/partida:", len(jogadores))
print("IDs CBF distintos:", jogadores["id_cbf"].nunique())
print(
    "Duplicacoes por partida/ID:",
    jogadores.duplicated(["id_partida", "id_cbf"]).sum()
)

print("\nAuditoria concluida.")
