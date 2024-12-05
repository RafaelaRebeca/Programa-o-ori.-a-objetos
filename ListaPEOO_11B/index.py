from templates.manterclienteUI import ManterClienteUI
from templates.manterhorarioUI import ManterHorarioUI
from templates.manterservicoUI import ManterServicoUI
from templates.manterperfilUI import ManterPerfilUI
from templates.manterprofUI import ManterProfUI
from templates.abriragendaUI import AbrirAgendaUI
from templates.abrircontaUI import AbrirContaUI
from templates.listarhorarioUI import ListarHorarioUI
from templates.proagendaUI import ProAgendaUI
from templates.confAdm import ConfAdm
from templates.confUser import ConfUser
from templates.loginUI import LoginUI
from views import View

import streamlit as st

class IndexUI:
    def menu_visitante():
        op = st.sidebar.selectbox("Menu", ["Entrar no Sistema", "Abrir Conta"])
        if op == "Entrar no Sistema": LoginUI.main()
        if op == "Abrir Conta": AbrirContaUI.main()
               
    def menu_admin():            
        op = st.sidebar.selectbox("Menu", ["Cadastro de Clientes", "Cadastro de Horários", "Cadastro de Serviços", "Cadastro de Perfis", "Cadastro de Profissionais", "Mudar Senha", "Abrir Agenda do Dia"])
        if op == "Cadastro de Clientes": ManterClienteUI.main()
        if op == "Cadastro de Horários": ManterHorarioUI.main()
        if op == "Cadastro de Serviços": ManterServicoUI.main()
        if op == "Cadastro de Perfis": ManterPerfilUI.main()
        if op == "Cadastro de Profissionais": ManterProfUI.main()
        if op == "Abrir Agenda do Dia": AbrirAgendaUI.main()
        if op == "Mudar Senha": ConfAdm.main()

    def menu_cliente():
        op = st.sidebar.selectbox("Menu", ["Horários Disponíveis", "Configurações de Conta"])
        if op == "Horários Disponíveis": ListarHorarioUI.main()
        if op == "Configurações de Conta": ConfUser.main()

    def menu_pro():
        op = st.sidebar.selectbox("Menu", ["Agenda do Dia"])
        if op == "Agenda do Dia": ProAgendaUI.main()

    def sair_do_sistema():
        if st.sidebar.button("Sair"):
            del st.session_state["cliente_id"]
            del st.session_state["cliente_nome"]
            st.rerun()
    



    def sidebar():
        if "tipo" not in st.session_state:
            # usuário não está logado
            IndexUI.menu_visitante()   
        else:
            
            tipo = st.session_state.get("tipo", "")
            st.sidebar.write("Bem-vindo(a), " + st.session_state["cliente_nome"])    

            if tipo == "cliente":
                IndexUI.menu_cliente()

            elif tipo == "profissional":
                IndexUI.menu_pro()

            elif tipo == "admin":
                IndexUI.menu_admin() 
            

            
            # controle de sair do sistema
            IndexUI.sair_do_sistema()
    




    def main():
        # verifica a existe o usuário admin
        View.cliente_admin()
        # monta o sidebar
        IndexUI.sidebar()
       
IndexUI.main()
