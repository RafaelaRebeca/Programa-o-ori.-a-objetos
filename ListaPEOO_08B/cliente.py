import json
import streamlit as st


class Cliente:
    def __init__(self, id, nome, email, fone):
        self._id = id
        self._nome = nome
        self._email = email
        self._fone = fone

    def get_id(self):
        return self._id

    def set_id(self, value):
        self._id = value

    def get_nome(self):
        return self._nome

    def set_nome(self, value):
        if value:
            self._nome = value
        else:
            raise ValueError("Nome inválido")

    def get_email(self):
        return self._email

    def set_email(self, value):
        if value:
            self._email = value
        else:
            raise ValueError("Email inválido")

    def get_fone(self):
        return self._fone

    def set_fone(self, value):
        if value:
            self._fone = value
        else:
            raise ValueError("Telefone inválido")

    def __str__(self):
        return f"{self.get_id()} - {self.get_nome()} - {self.get_email()} - {self.get_fone()}"


class Clientes:
    objetos = []

    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        m = 0
        for c in cls.objetos:
            if c.get_id() > m:
                m = c.get_id()
        obj.set_id(m + 1)
        cls.objetos.append(obj)
        cls.salvar()

    @classmethod
    def listar(cls):
        cls.abrir()
        return cls.objetos

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
            c.set_nome(obj.get_nome())
            c.set_email(obj.get_email())
            c.set_fone(obj.get_fone())
        cls.salvar()

    @classmethod
    def excluir(cls, id_cliente):
        c = cls.listar_id(id_cliente)
        if c is not None:
            cls.objetos.remove(c)
            cls.salvar()

    @classmethod
    def salvar(cls):
        with open("clientes.json", mode="w") as arquivo:
            json.dump([vars(c) for c in cls.objetos], arquivo)

    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("clientes.json", mode="r") as arquivo:
                texto = json.load(arquivo)
                for obj in texto:
                    c = Cliente(obj["_id"], obj["_nome"], obj["_email"], obj["_fone"])
                    cls.objetos.append(c)
        except FileNotFoundError:
            pass


class View:
    @staticmethod
    def cliente_inserir(nome, email, fone):
        c = Cliente(0, nome, email, fone)
        Clientes.inserir(c)

    @staticmethod
    def cliente_listar():
        return Clientes.listar()

    @staticmethod
    def cliente_atualizar(id_cliente, nome, email, fone):
        c = Cliente(id_cliente, nome, email, fone)
        Clientes.atualizar(c)

    @staticmethod
    def cliente_excluir(id_cliente):
        Clientes.excluir(id_cliente)


class IndexUI:
    def main(self):
        manter_cliente_ui = ManterClienteUI()
        manter_cliente_ui.main()


class ManterClienteUI:
    def main(self):
        st.header("Cadastro de Clientes")

        tab1, tab2, tab3, tab4 = st.tabs(["Inserir", "Listar", "Atualizar", "Excluir"])

        with tab1:
            self.inserir_cliente()
        with tab2:
            self.listar_cliente()
        with tab3:
            self.atualizar_cliente()
        with tab4:
            self.excluir_cliente()

    def listar_cliente(self):
        st.session_state.clientes = Clientes.listar()
        clientes = st.session_state.clientes
        st.write("Clientes cadastrados:")
        for cliente in clientes:
            st.write(str(cliente))

    def inserir_cliente(self):
        nome = st.text_input("Nome do Cliente:")
        email = st.text_input("Email do Cliente:")
        fone = st.text_input("Telefone do Cliente:")
        if st.button("Inserir"):
            View.cliente_inserir(nome, email, fone)
            st.success(f"Cliente {nome} inserido com sucesso!")
         
    def atualizar_cliente(self):
        clientes = Clientes.listar()

        if clientes:
            cliente_selecionado = st.selectbox("Selecione o Cliente", [f"{c.get_id()} - {c.get_nome()}" for c in clientes])

            id_cliente = int(cliente_selecionado.split(" - ")[0])
            cliente_atual = Clientes.listar_id(id_cliente)

            novo_nome = st.text_input("Novo Nome")
            novo_email = st.text_input("Novo Email")
            novo_fone = st.text_input("Novo Telefone")

            if st.button("Atualizar"):
                cliente_atualizado = Cliente(id_cliente, novo_nome, novo_email, novo_fone)
                View.cliente_atualizar(id_cliente, novo_nome, novo_email, novo_fone)
                st.success(f"Cliente atualizado com sucesso!")
                st.rerun()
                
        else:
            st.write("Nenhum cliente cadastrado.")

    def excluir_cliente(self):
        clientes =  Clientes.listar()

        if clientes:
            cliente_selecionado = st.selectbox("Selecione o Cliente a Excluir", [f"{c.get_id()} - {c.get_nome()}" for c in clientes])

            if cliente_selecionado:
                id_cliente_str = cliente_selecionado.split(" - ")[0]
                id_cliente = int(id_cliente_str)

                if st.button("Excluir"):
                    View.cliente_excluir(id_cliente)
                    st.success(f"Cliente '{cliente_selecionado}' excluído com sucesso!")
                    st.rerun()
            


ui = IndexUI()
ui.main()
