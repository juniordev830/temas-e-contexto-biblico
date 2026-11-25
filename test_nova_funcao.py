import unittest
from app import run
class TemasAdicionais(unittest.TestCase):
    def test_intersecao(self):
        data={"tema":"Fé","temas_adicionais":["esperanca"],"passagens":[{"temas":["fé","Esperança"],"funcao":"central","referencia":"A","contexto":"Contexto A"},{"temas":["Fé"],"funcao":"apoio","referencia":"B","contexto":"Contexto B"}]}
        self.assertEqual(run(data)["total"],1)
        data["temas_adicionais"]=[]
        self.assertEqual(run(data)["total"],2)
    def test_lista_invalida(self):
        with self.assertRaises(ValueError):
            run({"tema":"Fé","temas_adicionais":"esperança","passagens":[]})
