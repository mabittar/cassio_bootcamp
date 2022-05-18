from unittest import TestCase

from fastapi import status
from fastapi.testclient import TestClient

from gerenciador_tarefas.main import TarefasList, app


class TestTarefasGet(TestCase):
    def setUp(self) -> None:
        self.cliente = TestClient(app)

    def test_quando_listar_tarefas_devo_ter_como_retorno_codigo_de_status_200(self):
        resposta = self.cliente.get("/tarefas")
        self.assertEqual(status.HTTP_200_OK, resposta.status_code)

    def test_quando_listar_tarefas_formato_de_retorno_deve_ser_json(self):
        resposta = self.cliente.get("/tarefas")
        assert resposta.headers["Content-Type"] == "application/json"

    def test_quando_listar_tarefas_retorno_deve_ser_uma_lista(self):
        resposta = self.cliente.get("/tarefas")
        assert isinstance(resposta.json(), list)

    def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_id(self):
        TarefasList.append(
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "titulo": "titulo 1",
                "descricao": "descricao 1",
                "estado": "finalizado",
            }
        )
        resposta = self.cliente.get("/tarefas")
        assert "id" in resposta.json().pop()
        TarefasList.clear()

    def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_titulo(self):
        TarefasList.append(
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "titulo": "titulo 1",
                "descricao": "descricao 1",
                "estado": "finalizado",
            }
        )
        resposta = self.cliente.get("/tarefas")
        assert "titulo" in resposta.json().pop()
        TarefasList.clear()

    def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_descricao(self):
        TarefasList.append(
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "titulo": "titulo 1",
                "descricao": "descricao 1",
                "estado": "finalizado",
            }
        )
        resposta = self.cliente.get("/tarefas")
        assert "descricao" in resposta.json().pop()
        TarefasList.clear()

    def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_um_estado(self):
        TarefasList.append(
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "titulo": "titulo 1",
                "descricao": "descricao 1",
                "estado": "finalizado",
            }
        )
        resposta = self.cliente.get("/tarefas")
        assert "estado" in resposta.json().pop()
        TarefasList.clear()
