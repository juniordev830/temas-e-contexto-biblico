import csv
import io
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class ExportacaoCliTest(unittest.TestCase):
    def test_exemplo_completo(self):
        comando = [sys.executable, str(ROOT / "app.py"), str(ROOT / "exemplo.json")]
        dados = subprocess.check_output([*comando, '--csv']).decode("utf-8")
        linhas = list(csv.reader(io.StringIO(dados), delimiter=";"))
        self.assertEqual(linhas[0], ['tema', 'papel', 'referencia', 'contexto'])
        self.assertTrue(all(len(linha) == len(linhas[0]) for linha in linhas))
        self.assertIn('Efésios 4:1–6', [celula for linha in linhas[1:] for celula in linha])

    def test_prefixos_de_planilha_preservam_o_texto_original(self):
        from relatorio_csv import celula

        for prefixo in ("＝", "＋", "－", "＠", "\t", "\r", "\n"):
            with self.subTest(prefixo=prefixo):
                texto = prefixo + "Referência"
                self.assertEqual(celula(texto), "'" + texto)
        self.assertEqual(celula("  ＝Referência"), "'  ＝Referência")
        self.assertEqual(celula("João － registro"), "João － registro")

    def test_celulas_com_formulas_e_numeros_negativos(self):
        from relatorio_csv import celula

        self.assertEqual(celula(" =A1"), "' =A1")
        self.assertEqual(celula(-2), -2)
        self.assertEqual(celula("João"), "João")
