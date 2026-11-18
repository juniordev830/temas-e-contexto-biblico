import csv


def celula(valor):
    """Mantém texto com aparência de fórmula como texto em planilhas."""
    if isinstance(valor, str) and valor.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + valor
    return valor


def linhas(relatorio):
    for papel in ("central", "apoio"):
        for passagem in relatorio[papel]:
            yield relatorio["tema"], papel, passagem["referencia"], passagem["contexto"]


def escrever_csv(relatorio, destino):
    escritor = csv.writer(destino, delimiter=";", quoting=csv.QUOTE_ALL, lineterminator="\n")
    escritor.writerow(('tema', 'papel', 'referencia', 'contexto'))
    for linha in linhas(relatorio):
        escritor.writerow([celula(valor) for valor in linha])
