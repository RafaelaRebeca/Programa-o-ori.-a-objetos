
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
class Profissionais:
  objetos = []    # atributo estático

  @classmethod
  def inserir(cls, obj):
    cls.abrir()
    m = 0
    for c in cls.objetos:
      if c.id > m: m = c.id
    obj.id = m + 1
    cls.objetos.append(obj)
    cls.salvar()

  @classmethod
  def listar_id(cls, id):
    cls.abrir()
    for c in cls.objetos:
      if c.id == id: return c
    return None  
  
  @classmethod
  def atualizar(cls, obj):
    c = cls.listar_id(obj.id)
    if c != None:
      c.nome = obj.nome
      c.espe = obj.espe
      c.cons = obj.cons
      c.email = obj.email
      c.senha = obj.senha
      cls.salvar()

  @classmethod
  def excluir(cls, obj):
    c = cls.listar_id(obj.id)
    if c != None:
      cls.objetos.remove(c)
      cls.salvar()
  
  @classmethod
  def listar(cls):
    cls.abrir()
    cls.objetos.sort(key=lambda profissional: profissional.nome)
    return cls.objetos

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
