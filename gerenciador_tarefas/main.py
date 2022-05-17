from fastapi import FastAPI


TarefasModel = []

app = FastAPI()


@app.get("/tarefas")
def listar():
    return TarefasModel
