from config import *

class Users(Base):
    __tablename__ = "usuarios"
    ID = Column(Integer, primary_key = True, autoincrement = True)
    nome = Column(String(50), nullable = False)
    cpf = Column(String(11), nullable = False)
    idade = Column(Integer, nullable = False)
    estado_civil = Column(String(12), nullable = False)

Base.metadata.create_all(engine)