import streamlit as st
import pandas as pd
from views import View
import time
from datetime import datetime

class ManterHorarioUI:
    def main():
        st.header("Cadastro de Horários")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterHorarioUI.listar()
        with tab2: ManterHorarioUI.inserir()
        with tab3: ManterHorarioUI.atualizar()
        with tab4: ManterHorarioUI.excluir()

    def listar():
        horarios = View.horario_listar()
        if len(horarios) == 0: 
            st.write("Nenhum horário cadastrado")
        else:  
            dic = []

            for obj in horarios:
                cliente = View.cliente_listar_id(obj.get_id_cliente())
                servico = View.servico_listar_id(obj.get_id_servico())

                cliente_nome = cliente.get_nome() if cliente else "Cliente não encontrado"
                servico_desc = servico.get_descricao() if servico else "Serviço não encontrado"
            
                dic.append({
                    "id": obj.get_id(),
                    "data": obj.get_data(),
                    "confirmado": obj.get_confirmado(),
                    "cliente": cliente_nome,  
                    "serviço": servico_desc   
                })
            df = pd.DataFrame(dic)
            st.dataframe(df)

    def inserir():
        clientes = View.cliente_listar()
        servicos = View.servico_listar()
        data = st.text_input("Informe a data e horário do serviço", datetime.now().strftime("%d/%m/%Y %H:%M"))
        confirmado = st.checkbox("Confirmado")
        cliente = st.selectbox("Informe o cliente", clientes, index=None)
        servico = st.selectbox("Informe o serviço", servicos, index=None)
        if st.button("Inserir"):
            try:
                id_cliente = None
                id_servico = None
                if cliente is not None:
                    id_cliente = cliente.get_id()
                if servico is not None:
                    id_servico = servico.get_id()

                if id_cliente is None or id_servico is None:
                    raise ValueError("Cliente ou Serviço inválido. Verifique as opções selecionadas.")
                
                if isinstance(data, str):
                    data_informada = datetime.strptime(data, "%d/%m/%Y %H:%M")
                elif isinstance(data, datetime):
                    data_informada = data
                else:
                    raise ValueError("Formato de data inválido. Insira uma data válida no formato DD/MM/YYYY HH:MM.")

                if data_informada < datetime.now():
                    raise ValueError("A data informada é anterior ao momento atual. Insira uma data futura.")

                View.horario_inserir(data_informada, id_cliente, id_servico)
                st.success("Horário inserido com sucesso")
                time.sleep(2)
                st.rerun()
            except ValueError as e:
                st.error(f"Erro: {e}")


    def atualizar():
        horarios = View.horario_listar()
        if len(horarios) == 0: 
            st.write("Nenhum horário cadastrado")
        else:
            clientes = View.cliente_listar()
            servicos = View.servico_listar()
            op = st.selectbox("Atualização de horário", horarios)
            data = st.text_input("Informe a nova data e horário do serviço", op.get_data().strftime("%d/%m/%Y %H:%M"))
            confirmado = st.checkbox("Nova confirmação", op.get_confirmado())
            id_cliente = None if op.get_id_cliente() in [0, None] else op.get_id_cliente()
            id_servico = None if op.get_id_servico() in [0, None] else op.get_id_servico()
            cliente = st.selectbox("Informe o novo cliente", clientes, next((i for i, c in enumerate(clientes) if c.get_id() == id_cliente), None))
            servico = st.selectbox("Informe o novo serviço", servicos, next((i for i, s in enumerate(servicos) if s.get_id() == id_servico), None))
            
            if st.button("Atualizar"):
                try:
                    id_cliente = None
                    id_servico = None
                    if cliente != None: id_cliente = cliente.get_id()
                    if servico != None: id_servico = servico.get_id()
                    if id_cliente is None or id_servico is None:
                        raise ValueError("Cliente ou Serviço inválido. Verifique as opções selecionadas.")
                    
                    data_inf = datetime.strptime(data, "%d/%m/%Y %H:%M")
                    if data_inf < datetime.now():
                        raise ValueError("A data informada é anterior ao momento atual. Insira uma data futura.")


                    View.horario_atualizar(op.get_id(), datetime.strptime(data, "%d/%m/%Y %H:%M"), confirmado, id_cliente, id_servico)

                    st.success("Horário atualizado com sucesso")
                    time.sleep(2)
                    st.rerun()

                except ValueError as e:
                    st.error(f"Erro: {e}")

    def excluir():
        horarios = View.horario_listar()
        if len(horarios) == 0: 
            st.write("Nenhum horário cadastrado")
        else:
            op = st.selectbox("Exclusão de horário", horarios)
            try:
                if st.button("Excluir"):
                    View.horario_excluir(op.get_id())
                    st.success("Horário excluído com sucesso")
                    time.sleep(2)
                    st.rerun()
            except ValueError as e:
                st.error(f"Erro: {e}")