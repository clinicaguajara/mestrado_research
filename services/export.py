def preparar_resultado_exportacao_estatistico(resultado: dict) -> dict:
    """
    Converte a saída da função corrigir_aq50_estatistico() em formato plano para exportação.

    Args:
        resultado (dict): Dicionário com estrutura {fator: {escore, z, percentil_estimado}}

    Returns:
        dict: Estrutura plana com chaves 'escore_x', 'z_x', 'percentil_x'
    """
    exportado = {}
    for fator, valores in resultado.items():
        exportado[f"escore_{fator}"] = valores["escore"]
        exportado[f"z_{fator}"] = valores["z"]
        exportado[f"percentil_{fator}"] = valores["percentil_estimado"]
    return exportado
