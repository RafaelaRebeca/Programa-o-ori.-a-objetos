import json
from datetime import datetime

class Horario:
    def __init__(self, id, data):
        self.__id = id
        self.__data = data
        self.__confirmado = False
        self.__id_cliente = 0
        self.__id_servico = 0

    def __str__(self):
        return f"{self.get_id()} - {self.get_data().strftime('%d/%m/%Y %H:%M')}"

    def to_json(self):
      dic = {}
      dic["id"] = self.get_id()
      dic["data"] = self.get_data().strftime("%d/%m/%Y %H:%M")
      dic["confirmado"] = self.get_confirmado()
      dic["id_cliente"] = self.get_id_cliente()
      dic["id_servico"] = self.get_id_servico()
      return dic

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_data(self):
        return self.__data

    def set_data(self, data):
        if not isinstance(data, datetime):
            raise ValueError("O atributo 'data' deve ser um objeto datetime.")
        self.__data = data

    def get_confirmado(self):
        return self.__confirmado

    def set_confirmado(self, confirmado):
        if not isinstance(confirmado, bool):
            raise ValueError("O atributo 'confirmado' deve ser do tipo booleano.")
        self.__confirmado = confirmado

    def get_id_cliente(self):
        return self.__id_cliente

    def set_id_cliente(self, id_cliente):
        if not isinstance(id_cliente, int) or id_cliente < 0:
            raise ValueError("O atributo 'id_cliente' deve ser um número inteiro não negativo.")

        else:
          self.__id_cliente = id_cliente

    def get_id_servico(self):
        return self.__id_servico

    def set_id_servico(self, id_servico):
        if not isinstance(id_servico, int) or id_servico < 0:
            raise ValueError("O atributo 'id_servico' deve ser um número inteiro não negativo.")

        else:
            self.__id_servico = id_servico    

class Horarios:
    objetos = []  # atributo estático

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
            if c.get_id() == id:
                return c
        return None

    @classmethod
    def atualizar(cls, obj):
        c = cls.listar_id(obj.get_id())
        if c is not None:
            c.set_data(obj.get_data())
            c.set_confirmado(obj.get_confirmado())
            c.set_id_cliente(obj.get_id_cliente())
            c.set_id_servico(obj.get_id_servico())
            cls.salvar()

    @classmethod
    def excluir(cls, obj):
        c = cls.listar_id(obj.get_id())
        if c is not None:
            cls.objetos.remove(c)
            cls.salvar()

    @classmethod
    def listar(cls):
        cls.abrir()
        return cls.objetos

    @classmethod
    def salvar(cls):
        with open("horarios.json", mode="w") as arquivo:   # w - write
            json.dump(cls.objetos, arquivo, default = Horario.to_json)


    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("horarios.json", mode="r") as arquivo:   # r - read
                texto = json.load(arquivo)
                for obj in texto:   
                    c = Horario(obj["id"], datetime.strptime(obj["data"], "%d/%m/%Y %H:%M"))
                    c.confirmado = obj["confirmado"]
                    c.id_cliente = obj["id_cliente"]
                    c.id_servico = obj["id_servico"]
                    cls.objetos.append(c)
        except FileNotFoundError:
            pass