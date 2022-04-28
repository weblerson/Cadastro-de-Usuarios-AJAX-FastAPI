from config import *
from models import Users

class UsersController:
    @classmethod
    def read(cls):
        try:
            users = []
            for user in session.query(Users).all():
                users.append({"id": user.ID,
                            "nome": user.nome,
                            "cpf": user.cpf,
                            "idade": user.idade,
                            "estado_civil": user.estado_civil})

            return {"response": users}

        except:
            return {"response": "Ocorreu um erro ao consultar o banco."}

    @classmethod
    def register(cls, name: str, cpf: str, age: int, marital_state: str):
        if name and age and marital_state:
            if len(cpf) != 11:
                return {"success": False, "content": "O CPF deve ter 11 dígitos"}

            if session.query(session.query(Users).filter(Users.cpf == cpf).exists()).one()[0]:
                session.query(Users).filter(Users.cpf == cpf).one()
                return {"success": False, "content": f"Um usuário de CPF {cpf} já existe. Impossível realizar o cadastro."}

            try:
                session.add(Users(nome = name, cpf = cpf, idade = age, estado_civil = marital_state))
                session.commit()

                return {"success": True, "content": "Usuário cadastrado com sucesso!"}

            except:
                return {"success": False, "content": "Ocorreu um erro ao consultar o banco."}

        else:
            return {"success": False, "content": "Preencha todos os campos."}

if __name__ == "__main__":
    print(UsersController.read())