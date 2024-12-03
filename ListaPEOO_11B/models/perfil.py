import json
from models.crud import CRUD

# Modelo
class Perfil:
  def __init__(self, id, nome, desc, bene):
    self.id = id
    self.nome = nome
    self.desc = desc
    self.bene = bene
  def __str__(self):
    return f"{self.nome} - {self.desc} - {self.bene}"

# Persistência
class Perfis(CRUD):
  
  @classmethod
  def salvar(cls):
    with open("perfis.json", mode="w") as arquivo:   # w - write
      json.dump(cls.objetos, arquivo, default = vars)

  @classmethod
  def abrir(cls):
    cls.objetos = []
    try:
      with open("perfis.json", mode="r") as arquivo:   # r - read
        texto = json.load(arquivo)
        for obj in texto:   
          c = Perfil(obj["id"], obj["nome"], obj["desc"], obj["bene"])
          cls.objetos.append(c)
    except FileNotFoundError:
      pass

