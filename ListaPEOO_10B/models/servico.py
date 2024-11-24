import json

# Modelo
class Servico:
    def __init__(self, id, descricao, valor, duracao):
        self.__id = id
        self.__descricao = descricao
        self.__valor = valor
        self.__duracao = duracao
        

    def __str__(self):
        return f"{self.get_id()} - {self.get_descricao()} - R$ {self.get_valor()} - {self.get_duracao()} min"

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_descricao(self):
        return self.__descricao

    def set_descricao(self, descricao):
        if descricao == "":
            raise ValueError("A descrição não pode ser vazia.")
        self.__descricao = descricao

    def get_valor(self):
        return self.__valor

    def set_valor(self, valor):
        if int(valor) < 0:
            raise ValueError("O valor deve ser positivo")
        self.__valor = valor

    def get_duracao(self):
        return self.__duracao

    def set_duracao(self, duracao):
        if int(duracao) < 0:
            raise ValueError("A duração deve ser positiva")
        self.__duracao = duracao

# Persistência
class Servicos:
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
            c.set_descricao(obj.get_descricao())
            c.set_valor(obj.get_valor())
            c.set_duracao(obj.get_duracao())
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
        with open("servicos.json", mode="w") as arquivo:  # w - write
            json.dump(cls.objetos, arquivo, default=lambda s: s.__dict__)

    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("servicos.json", mode="r") as arquivo:  # r - read
                texto = json.load(arquivo)
                for obj in texto:
                    c = Servico(obj["_Servico__id"], obj["_Servico__descricao"], obj["_Servico__valor"], obj["_Servico__duracao"])
                    cls.objetos.append(c)
        except FileNotFoundError:
            pass
