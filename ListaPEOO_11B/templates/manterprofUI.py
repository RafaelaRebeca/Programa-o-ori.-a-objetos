import streamlit as st
import pandas as pd
from views import View
import time

class ManterProfUI:
    def main():
        st.header("Cadastro de Profissionais")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterProfUI.listar()
        with tab2: ManterProfUI.inserir()
        with tab3: ManterProfUI.atualizar()
        with tab4: ManterProfUI.excluir()

    def listar():
        pros = View.profissional_listar()
        if len(pros) == 0: 
            st.write("Nenhum profissional cadastrado")
        else:    
            #for obj in clientes: st.write(obj)
            dic = []
            for obj in pros: dic.append(obj.__dict__)
            df = pd.DataFrame(dic)
            st.dataframe(df)

    def inserir():

        nome = st.text_input("Informe o nome do profissional")
        espe = st.text_input("Informe a especialização")
        cons = st.text_input("Informe o conselho")
        email = st.text_input("Informe o e-mail")
        senha = st.text_input("Informe a senha", type="password")
        if st.button("Inserir"):
            View.profissional_inserir(nome, espe, cons, email, senha)
            st.success("Profissional inserido com sucesso")
            time.sleep(2)
            st.rerun()

    def atualizar():
        pros = View.profissional_listar()
        if len(pros) == 0: 
            st.write("Nenhum profissional cadastrado")
        else:
            op = st.selectbox("Atualização de pro", pros)
            nome = st.text_input("Informe o novo nome do profissional", op.nome)
            espe = st.text_input("Informe o novo especialização", op.espe)
            cons = st.text_input("Informe o novo conselho", op.cons)
            email = st.text_input("Informe a nova email", op.email)
            senha = st.text_input("Informe a nova senha:", op.senha, type="password")
            if st.button("Atualizar"):
                View.profissional_atualizar(op.id, nome, espe, cons, email, senha)
                st.success("Profissional atualizado com sucesso")
                time.sleep(2)
                st.rerun()

    def excluir():
        pros = View.profissional_listar()
        if len(pros) == 0: 
            st.write("Nenhum profissional cadastrado")
        else:
            op = st.selectbox("Exclusão de profissional", pros)
            if st.button("Excluir"):
                View.profissional_excluir(op.id)
                st.success("Profissional excluído com sucesso")
                time.sleep(2)
                st.rerun()