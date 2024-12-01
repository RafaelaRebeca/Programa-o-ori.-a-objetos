import streamlit as st
import time
from views import View

class ConfUser:
    @staticmethod
    def main():
        st.header("Configurações de Conta")
        ConfUser.atualizar()

    @staticmethod
    def atualizar():
        cliente_id = st.session_state.get("cliente_id")
        cliente_IDperfil = st.session_state.get("cliente_IDperfil")
        if cliente_id is None:
            st.error("Nenhum cliente logado.")
            return

        cliente = next((c for c in View.cliente_listar() if c.id == cliente_id), None)

        if cliente:
            nome = st.text_input("Informe o novo nome", cliente.nome)
            email = st.text_input("Informe o novo e-mail", cliente.email)
            fone = st.text_input("Informe o novo telefone", cliente.fone)
            senha = st.text_input("Informe a nova senha", cliente.senha, type="password")

            if st.button("Atualizar"):
                View.cliente_atualizar(cliente_id, nome, email, fone, senha, cliente_IDperfil)
                st.success("Dados atualizados com sucesso!")
                time.sleep(2)
                st.rerun()
        else:
            st.error("Cliente não encontrado.")
