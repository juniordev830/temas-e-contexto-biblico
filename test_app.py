import json
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import sys
import unittest

from app import run

ROOT = Path(__file__).resolve().parent


class ProjetoTest(unittest.TestCase):
    def test_exemplo_documentado(self):
        data = json.loads((ROOT / "exemplo.json").read_text(encoding="utf-8"))
        result = run(data)
        self.assertEqual(result['total'], 2)

    def test_classifica_a_funcao_independentemente_de_caixa_e_espacos(self):
        data = {"tema": "fé", "passagens": [
            {"temas": ["fé"], "funcao": " CENTRAL ", "referencia": "João 3:16", "contexto": "Diálogo"},
            {"temas": ["fé"], "funcao": "Apoio", "referencia": "Hebreus 11:1", "contexto": "Introdução"},
        ]}
        result = run(data)
        self.assertEqual(result["central"][0]["referencia"], "João 3:16")
        self.assertEqual(result["apoio"][0]["referencia"], "Hebreus 11:1")

    def test_cli_aceita_json_utf8_com_bom(self):
        exemplo = (ROOT / "exemplo.json").read_text(encoding="utf-8")
        with TemporaryDirectory() as pasta:
            entrada = Path(pasta) / "entrada.json"
            entrada.write_text(exemplo, encoding="utf-8-sig")
            resultado = subprocess.run(
                [sys.executable, str(ROOT / "app.py"), str(entrada)],
                capture_output=True, text=True, encoding="utf-8", check=True,
            )
        self.assertEqual(json.loads(resultado.stdout), run(json.loads(exemplo)))

    def test_cli_com_exemplo(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "app.py"), str(ROOT / "exemplo.json")],
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        self.assertEqual(json.loads(result.stdout)['total'], 2)

    def test_rejeita_dados_incompletos(self):
        with self.assertRaises((KeyError, ValueError, TypeError)):
            run({})
