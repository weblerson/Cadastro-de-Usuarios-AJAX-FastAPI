from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import *
from models import Usuarios

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_credentials = True
)

@app.get("/read")
def get_users():
    try:
        users = [users.append({"id": user.id,
            "nome": user.nome,
            "cpf": user.cpf,
            "idade": user.idade,
            "estado_civil": user.estado_civil}) for user in session.query(Usuarios).all()]

        return {"response": users}

    except:
        return {"response": "Ocorreu um erro ao consultar o banco."}

@app.post("/find")
def find_users(ID: int):
    try:
        if ID:
            if not session.query(Usuarios).filter(Usuarios.id == ID).one():
                return {"response": f"Não existe nenhum usuário de ID {ID} cadastrado. Impossível realizar a alteração."}

            user = session.query(Usuarios).filter(Usuarios.id == ID).one()

            return {"response": {"id": user.id,
                                "nome": user.nome,
                                "cpf": user.cpf,
                                "idade": user.idade,
                                "estado_civil": user.estado_civil}}

        else:
            return {"response": "Passe um ID válido para consulta."}

    except:
        return {"response": "Ocorreu um erro ao consultar o banco."}

@app.post("/register")
def register_users(name: str, cpf: str, age: int, marital_state: str):
    try:
        if name and age and marital_state:
            if len(cpf.strip()) < 11 or len(cpf.strip()) > 11:
                return {"response": "O CPF deve ter 11 dígitos"}

            if session.query(Usuarios).filter(Usuarios.cpf == cpf).one():
                return {"response": f"Um usuário de CPF {cpf} já existe. Impossível realizar o cadastro."}

            session.add(Usuarios(nome = name, cpf = cpf, idade = age, estado_civil = marital_state))
            session.commit()

            return {"response": "Usuário cadastrado com sucesso!"}

        else:
            return {"response": "Preencha todos os campos."}

    except:
        return {"response": "Ocorreu um erro ao consultar o banco."}

@app.post("/change")
def change_users(ID: int, new_name: str):
    try:
        if ID and new_name:
            if not session.query(Usuarios).filter(Usuarios.id == ID).one():
                return {"response": f"Não existe nenhum usuário de ID {ID} cadastrado. Impossível realizar a alteração."}

            session.query(Usuarios).filter(Usuarios.id == ID).update({Usuarios.nome: new_name})
            session.commit()

            return {"response": f"Nome do usuário de ID {ID} alterado com sucesso para {new_name}!"}
                        
        else:
            return {"response": "Preencha todos os campos para realizar a alteração."}

    except:
        return {"response": "Ocorreu um erro ao consultar o banco."}

@app.post("/delete")
def delete_users(ID: int):
    try:
        if ID:
            if not session.query(Usuarios).filter(Usuarios.id == ID).one():
                return {"response": f"Não existe nenhum usuário de ID {ID} cadastrado. Impossível realizar a remoção."}

            session.query(Usuarios).filter(Usuarios.id == ID).delete()
            session.commit()

        else:
            return {"response": "Preencha o campo de ID para realizar a remoção."}

    except:
        return {"response": "Ocorreu um erro ao consultar o banco."}