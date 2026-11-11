def calcular_media(valores: list[float]) -> float:
    """
    Calcula a média de uma lista de valores.

    Args:
        valores: Lista de valores numéricos.

    Returns:
        Média aritmética dos valores.

    Raises:
        ValueError: Se a lista estiver vazia.
    """
    if not valores:
        raise ValueError("A lista não pode estar vazia.")

    return sum(valores) / len(valores)