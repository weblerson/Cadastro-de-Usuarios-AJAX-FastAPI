from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from config import *
from models import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
    allow_credentials = True
)

class User(BaseModel):
    ID: Optional[int]
    name: Optional[str]
    cpf: Optional[str]
    age: Optional[int]
    marital_state: Optional[str]

@app.get("/read")
def get_users():
    try:
        users = []
        for user in session.query(Users).all():
            users.append({"id": user.ID,
                        "nome": user.nome,
                        "cpf": user.cpf,
                        "idade": user.idade,
                        "estado_civil": user.estado_civil})

        return {"success": True, "content": users}

    except:
        return {"success": False, "content": "Ocorreu um erro ao consultar o banco."}

@app.post("/find")
def find_users(_user: User):
    if ID:
        try:
            if not session.query(session.query(Users).filter(Users.ID == _user.ID).exists()).one()[0]:
                return {"success": False, "content": f"Não existe nenhum usuário de ID {_user.ID} cadastrado."}

            user = session.query(Users).filter(Users.ID == _user.ID).one()

            return {"success": True, "content": {"id": user.ID,
                                                "nome": user.nome,
                                                "cpf": user.cpf,
                                                "idade": user.idade,
                                                "estado_civil": user.estado_civil}}

        except:
            return {"success": False, "content": "Ocorreu um erro ao consultar o banco."}

    else:
        return {"success": False, "content": "Passe um ID válido para consulta."}

@app.post("/register")
def register_users(_user: User):
    if _user.name and _user.age and _user.marital_state:
        if len(_user.cpf) != 11:
            return {"success": False, "content": "O CPF deve ter 11 dígitos"}

        try:
            if session.query(session.query(Users).filter(Users.cpf == _user.cpf).exists()).one()[0]:
                return {"success": False, "content": f"Um usuário de CPF {_user.cpf} já existe. Impossível realizar o cadastro."}

            session.add(Users(nome = _user.name, cpf = _user.cpf, idade = _user.age, estado_civil = _user.marital_state))
            session.commit()

            return {"success": True, "content": "Usuário cadastrado com sucesso!"}

        except:
            return {"success": False, "content": "Ocorreu um erro ao consultar o banco."}

    else:
        return {"success": False, "content": "Preencha todos os campos."}

@app.post("/change")
def change_users(ID: int, new_name: str):
    if ID and new_name:
        try:
            if not session.query(session.query(Users).filter(Users.ID == ID).exists()).one()[0]:
                return {"success": False, "content": f"Não existe nenhum usuário de ID {ID} cadastrado. Impossível realizar a alteração."}

            session.query(Users).filter(Users.ID == ID).update({Users.nome: new_name})
            session.commit()

            return {"success": True, "content": f"Nome do usuário de ID {ID} alterado com sucesso para {new_name}!"}

        except:
            return {"success": False, "content": "Ocorreu um erro ao consultar o banco."}
                    
    else:
        return {"success": False, "content": "Preencha todos os campos para realizar a alteração."}

@app.post("/delete")
def delete_users(ID: int):
    if ID:
        try:
            if not session.query(session.query(Users).filter(Users.ID == ID).exists()).one()[0]:
                return {"success": False, "content": f"Não existe nenhum usuário de ID {ID} cadastrado. Impossível realizar a remoção."}

            session.query(Users).filter(Users.ID == ID).delete()
            session.commit()

            return {"success": True, "content": f"Usuário de ID {ID} removido com sucesso!"}

        except:
            return {"success": False, "content": "Ocorreu um erro ao consultar o banco."}

    else:
        return {"success": False, "content": "Preencha o campo de ID para realizar a remoção."}