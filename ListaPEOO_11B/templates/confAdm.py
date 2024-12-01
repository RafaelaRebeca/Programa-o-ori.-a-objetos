import streamlit as st
import pandas as pd
from views import View
import time
import re
from datetime import datetime

class ConfAdm:
    def main():
        st.header("Mudar Senha do Admin")
        ConfAdm.atualizar()

    def atualizar():
        cliente_id = st.session_state.get("cliente_id")
        if cliente_id is None:
            st.error("Nenhum cliente logado.")
            return

        cliente = next((c for c in View.cliente_listar() if c.id == cliente_id), None)

        if cliente:
            nova_senha = st.text_input("Informe a nova senha", type="password")
            confirmar_senha = st.text_input("Confirme a nova senha", type="password")

            if st.button("Atualizar"):
                
                if nova_senha != confirmar_senha:
                    st.error("As senhas não coincidem. Tente novamente.")
                    return

                cliente.nome = cliente.nome  # Mantém o nome atual
                cliente.email = cliente.email  # Mantém o e-mail atual
                cliente.fone = cliente.fone  # Mantém o telefone atual
                cliente.senha = nova_senha  # Atualiza a senha

                View.cliente_atualizar(cliente.id, cliente.nome, cliente.email, cliente.fone, cliente.senha, cliente.IDperfil)
                st.success("Senha atualizada com sucesso!")
                time.sleep(2)
                st.rerun()
        else:
            st.error("Cliente não encontrado.")



