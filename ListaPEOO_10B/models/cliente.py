# Lista de Clientes
# C - Create - Insere um objeto na lista
# R - Read   - Listar os objetos da lista
# U - Update - Atualizar um objeto na lista
# D - Delete - Exclui um objeto da lista

import json

# Modelo
class Cliente:

    def __init__(self, id, nome, email, fone, senha):
        self.__id = id
        self.__nome = nome
        self.__email = email
        self.__fone = fone
        self.__senha = senha

    def __str__(self):
        return f"{self.get_nome()} - {self.get_email()} - {self.get_fone()}"


    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id


    def get_nome(self):
        return self.__nome

    def set_nome(self, nome):
        if nome != "":
          self.__nome = nome
        else:
          raise ValueError("Nome não pode ser vazio")

    def get_email(self):
        return self.__email

    def set_email(self, email):
        if email != "":
          self.__email = email
        else:
          raise ValueError("Email não pode ser vazio")

    def get_fone(self):
        return self.__fone

    def set_fone(self, fone):
        if fone != "":
          self.__fone = fone
        else:
          raise ValueError("fone não pode ser vazio")


    def get_senha(self):
        return self.__senha

    def set_senha(self, senha):
        if senha != "":
          self.__senha = senha
        else:
          raise ValueError("senha não pode ser vazio")

    

# Persistência
class Clientes:
  objetos = []    # atributo estático

  @classmethod
  def inserir(cls, obj):
    cls.abrir()
    if cls.objetos:
        max_id = max(c.get_id() for c in cls.objetos)
    else:
        max_id = 0  
    obj.set_id(max_id + 1)
    cls.objetos.append(obj)
    cls.salvar()


  @classmethod
  def listar_id(cls, id):
    cls.abrir()
    for c in cls.objetos:
      if c.get_id() == id: return c
    return None  
  
  @classmethod
  def atualizar(cls, obj):
    c = cls.listar_id(obj.get_id())
    if c != None:
      c.get_nome() == obj.get_nome()
      c.get_email() == obj.get_email()
      c.get_fone() == obj.get_fone()
      c.get_senha() == obj.get_senha()
      cls.salvar()

  @classmethod
  def excluir(cls, obj):
    c = cls.listar_id(obj.get_id())
    if c != None:
      cls.objetos.remove(c)
      cls.salvar()
  
  @classmethod
  def listar(cls):
    cls.abrir()
    cls.objetos.sort(key=lambda cliente: cliente.get_nome())
    return cls.objetos

  @classmethod
  def salvar(cls):
    with open("clientes.json", mode="w") as arquivo:
        json.dump(
            [{"id": c.get_id(), "nome": c.get_nome(), "email": c.get_email(), "fone": c.get_fone(), "senha": c.get_senha()} 
             for c in cls.objetos],
            arquivo
        )
  @classmethod
  def abrir(cls):
    cls.objetos = []
    try:
        with open("clientes.json", mode="r") as arquivo:
            texto = json.load(arquivo)
            for obj in texto:
                if all(k in obj for k in ["id", "nome", "email", "fone", "senha"]):
                    c = Cliente(obj["id"], obj["nome"], obj["email"], obj["fone"], obj["senha"])
                    cls.objetos.append(c)
                else:
                    print(f"Objeto inválido encontrado: {obj}")
    except FileNotFoundError:
        pass
