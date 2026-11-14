'Filtre referências temáticas e veja o peso das passagens centrais e de apoio.'


from unicodedata import combining, normalize


def texto(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Use texto não vazio.")
    return value.strip()


def textos(items):
    if not isinstance(items, list):
        raise ValueError("Use uma lista de textos.")
    return [texto(item) for item in items]


def chave(value):
    return "".join(c for c in normalize("NFKD", texto(value).casefold()) if not combining(c))


def run(data):
    tema = chave(data["tema"])
    resultado = {"central": [], "apoio": []}
    for item in data["passagens"]:
        if tema not in {chave(x) for x in textos(item["temas"])}:
            continue
        funcao = item["funcao"]
        if funcao not in resultado:
            raise ValueError("Classifique a passagem como central ou apoio.")
        resultado[funcao].append({"referencia": texto(item["referencia"]),
                                  "contexto": texto(item["contexto"])})
    return {"tema": texto(data["tema"]), **resultado,
            "total": sum(len(items) for items in resultado.values())}


import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", type=Path, help="Arquivo JSON com os dados")
    args = parser.parse_args()

    try:
        with args.entrada.open(encoding="utf-8") as source:
            data = json.load(source)
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
