from typing import Dict
from scipy.stats import norm

# Índices dos itens reversos (base 0)
ITENS_REVERSOS = [
    2, 7, 9, 10, 13, 14, 16, 23, 24, 26, 27, 28, 29,
    30, 31, 33, 35, 36, 37, 39, 43, 46, 47, 48, 49
]

# Fatores da escala AQ-50
FATORES = {
    "habilidades_sociais":    [0, 10, 12, 14, 21, 35, 43, 44, 46, 47],
    "atencao_alternada":      [1, 3, 9, 15, 24, 31, 33, 36, 42, 45],
    "atencao_a_detalhes":     [4, 5, 8, 11, 18, 22, 27, 28, 29, 48],
    "comunicacao":            [6, 16, 17, 25, 26, 30, 32, 34, 37, 38],
    "imaginacao":             [2, 7, 13, 19, 20, 23, 39, 40, 41, 49]
}

# Médias e DPs por grupo
MEDIA_DP_AQ50 = {
    "controle_masculino": {
        "habilidades_sociais": (2.6, 2.3),
        "atencao_alternada": (3.9, 1.9),
        "atencao_a_detalhes": (5.3, 2.3),
        "comunicacao": (2.4, 1.9),
        "imaginacao": (2.3, 1.7),
        "total": (16.4, 6.3),
    },
    "controle_feminino": {
        "habilidades_sociais": (2.3, 2.2),
        "atencao_alternada": (3.6, 1.8),
        "atencao_a_detalhes": (5.4, 2.3),
        "comunicacao": (2.1, 1.8),
        "imaginacao": (1.9, 1.5),
        "total": (15.4, 5.7),
    },
    "autista_masculino": {
        "habilidades_sociais": (7.4, 2.0),
        "atencao_alternada": (7.7, 1.9),
        "atencao_a_detalhes": (6.6, 2.3),
        "comunicacao": (7.2, 2.0),
        "imaginacao": (6.2, 2.2),
        "total": (35.1, 6.9),
    },
    "autista_feminino": {
        "habilidades_sociais": (7.9, 1.4),
        "atencao_alternada": (8.9, 1.0),
        "atencao_a_detalhes": (6.9, 2.1),
        "comunicacao": (7.3, 2.1),
        "imaginacao": (7.0, 1.5),
        "total": (38.1, 4.4),
    },
}


def corrigir_aq50_estatistico(respostas_dict: Dict[str, int], grupo: str) -> Dict:
    """
    <docstrings>
    Corrige o AQ-50 em modo binário, calcula escore por fator, z-score e percentil estimado.

    Args:
        respostas_dict (dict): Respostas no formato {"item_1": int, ..., "item_50": int}
        grupo (str): Nome do grupo normativo. Ex: "controle_masculino"

    Returns:
        dict: Dicionário com escore, z-score e percentil estimado para cada fator e total.
    """
    respostas_binarias = []
    for i in range(50):
        valor = respostas_dict.get(f"item_{i+1}")

        try:
            valor = int(valor)
        except (TypeError, ValueError):
            valor = None

        if valor is None:
            binario = 0
        elif i in ITENS_REVERSOS:
            binario = 1 if valor <= 2 else 0
        else:
            binario = 1 if valor >= 3 else 0

        respostas_binarias.append(binario)

    resultados = {}

    for nome_fator, indices in FATORES.items():
        escore = sum(respostas_binarias[i] for i in indices)
        media, dp = MEDIA_DP_AQ50[grupo][nome_fator]
        z = (escore - media) / dp
        percentil = round(norm.cdf(z) * 100, 1)
        resultados[nome_fator] = {"escore": escore, "z": round(z, 2), "percentil_estimado": percentil}

    escore_total = sum(respostas_binarias)
    media, dp = MEDIA_DP_AQ50[grupo]["total"]
    z = (escore_total - media) / dp
    percentil = round(norm.cdf(z) * 100, 1)
    resultados["total"] = {"escore": escore_total, "z": round(z, 2), "percentil_estimado": percentil}

    return resultados
