from unittest import TestCase

from fastapi import status
from fastapi.testclient import TestClient

from gerenciador_tarefas.main import TarefasList, app


class TestTarefasGet(TestCase):
    def setUp(self) -> None:
        self.cliente = TestClient(app)

    def test_rota_tarefas_deve_aceitar_post(self):
        reposta = self.cliente.post("/tarefas")
        self.assertNotEqual(status.HTTP_405_METHOD_NOT_ALLOWED, reposta.status_code)

    def test_tarefa_deve_possuir_titulo(self):
        reposta = self.cliente.post("/tarefas", json={})
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, reposta.status_code)

    def test_titulo_deve_conter_3_a_15_caracteres(self):
        reposta = self.cliente.post("/tarefas", json={"titulo": 2 * "*"})
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, reposta.status_code)
        reposta = self.cliente.post("/tarefas", json={"titulo": 16 * "*"})
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, reposta.status_code)

    def test_tarefa_criada_deve_possuir_descrição(self):
        reposta = self.cliente.post("/tarefas", json={"titulo": "tarefa_teste"})
        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, reposta.status_code)

    def test_quando_criar_uma_tarefa_ele_deve_ser_retornada(self):
        tarefa_esperada = {"titulo": "titulo", "descricao": "descricao"}
        resposta = self.cliente.post("/tarefas", json=tarefa_esperada)
        tarefa_criada = resposta.json()
        self.assertEqual(tarefa_esperada["titulo"], tarefa_criada["titulo"])
        self.assertEqual(tarefa_esperada["descricao"], tarefa_criada["descricao"])
        TarefasList.clear()

    def test_quando_criar_duas_tarefas_devem_ter_ids_diferentes(self):
        tarefa1 = {"titulo": "titulo1", "descricao": "descricao1"}
        tarefa2 = {"titulo": "titulo2", "descricao": "descricao1"}
        resposta1 = self.cliente.post("/tarefas", json=tarefa1)
        resposta2 = self.cliente.post("/tarefas", json=tarefa2)
        self.assertEqual(status.HTTP_201_CREATED, resposta1.status_code)
        self.assertEqual(status.HTTP_201_CREATED, resposta2.status_code)
        self.assertNotEqual(resposta1.json()["id"], resposta2.json()["id"])
        TarefasList.clear()

    def test_quando_criar_status_deve_ser_nao_finalizado(self):
        tarefa = {"titulo": "titulo", "descricao": "descricao"}
        resposta = self.cliente.post("/tarefas", json=tarefa)
        self.assertEqual("não finalizado", resposta.json()["estado"])
        TarefasList.clear()

    def test_quando_criar_tarefa_deve_persistir(self):
        tarefa = {"titulo": "titulo", "descricao": "descricao"}
        self.cliente.post("/tarefas", json=tarefa)
        numero_tarefas = len(TarefasList)
        self.assertEqual(1, numero_tarefas)
        TarefasList.clear()

    def test_quando_criar_deve_persistir_ate_10(self):
        tarefa = {"titulo": "titulo", "descricao": "descricao"}
        i = 0
        while i < 15:
            self.cliente.post("/tarefas", json=tarefa)
            i += 1

        numero_tarefas = len(TarefasList)
        self.assertEqual(10, numero_tarefas)
        TarefasList.clear()
