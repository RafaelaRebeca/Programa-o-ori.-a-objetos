from models.crud import CRUD
import json

class Profissional:
  def __init__(self, id, nome, espe, cons, email, senha):
    self.id = id
    self.nome = nome
    self.espe = espe
    self.cons = cons
    self.email = email
    self.senha = senha
  def __str__(self):
    return f"{self.nome} - {self.espe}"

# Persistência
class Profissionais(CRUD):
  
    @classmethod
    def salvar(cls):
      with open("profissionais.json", mode="w") as arquivo:   # w - write
        json.dump(cls.objetos, arquivo, default = vars)

    @classmethod
    def abrir(cls):
      cls.objetos = []
      try:
        with open("profissionais.json", mode="r") as arquivo:   # r - read
          texto = json.load(arquivo)
          for obj in texto:   
            c = Profissional(obj["id"], obj["nome"], obj["espe"], obj["cons"], obj["email"], obj["senha"])
            cls.objetos.append(c)
      except FileNotFoundError:
        pass
