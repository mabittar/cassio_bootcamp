from enum import Enum
from uuid import UUID, uuid4

from fastapi import FastAPI, status
from pydantic import BaseModel, constr

TarefasList = []


class TarefaEstado(str, Enum):
    finalizado = "finalizado"
    nao_finalizado = "não finalizado"


class TarefaBase(BaseModel):
    titulo: constr(min_length=3, max_length=15)  # type: ignore
    descricao: constr(max_length=224)  # type: ignore
    estado: TarefaEstado = TarefaEstado.nao_finalizado


class TarefaResponse(TarefaBase):
    id: UUID  # type: ignore


app = FastAPI()


@app.get("/tarefas")
def listar():
    return TarefasList


@app.post(
    "/tarefas", response_model=TarefaResponse, status_code=status.HTTP_201_CREATED
)
def criar(tarefa: TarefaBase):
    nova_tarefa = tarefa.dict()
    nova_tarefa.update({"id": uuid4()})
    response = TarefaResponse(**nova_tarefa)
    TarefasList.append(nova_tarefa)
    if len(TarefasList) > 10:
        TarefasList.pop()
    return response
