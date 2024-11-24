from models.cliente import Cliente, Clientes
from models.horario import Horario, Horarios
from models.servico import Servico, Servicos
from datetime import datetime, timedelta

class View:
    def cliente_admin():
        for c in View.cliente_listar():
            if c.get_email() == "admin": return
        View.cliente_inserir("admin", "admin", "1234", "1234")

    def cliente_inserir(nome, email, fone, senha):
        for c in View.cliente_listar():

            if c.get_email() == email:
                raise ValueError(f"Email {email} já cadastrado.")

            if not nome or nome.strip() == "":
                raise ValueError("O campo 'nome' não pode estar vazio.")

            if not email or email.strip() == "":
                raise ValueError("O campo 'email' não pode estar vazio.")

            if not fone or fone.strip() == "":
                raise ValueError("O campo 'fone' não pode estar vazio.")

            if not senha or senha.strip() == "":
                raise ValueError("O campo 'senha' não pode estar vazio.")
    
        c = Cliente(0, nome, email, fone, senha)
        Clientes.inserir(c)

    def cliente_listar():
        return Clientes.listar()    

    def cliente_listar_id(id):
        return Clientes.listar_id(id)    

    def cliente_atualizar(id, nome, email, fone, senha):

        for c in View.cliente_listar():
            if c.get_email() == email and c.get_id() != id:
                raise ValueError(f"Email {email} já cadastrado.")

            if not nome or nome.strip() == "":
                raise ValueError("O campo 'nome' não pode estar vazio.")

            if not email or email.strip() == "":
                raise ValueError("O campo 'email' não pode estar vazio.")

            if not fone or fone.strip() == "":
                raise ValueError("O campo 'fone' não pode estar vazio.")

            if not senha or senha.strip() == "":
                raise ValueError("O campo 'senha' não pode estar vazio.")
    

        c = Cliente(0, nome.strip(), email.strip(), fone.strip(), senha.strip())
        Clientes.inserir(c)

    def cliente_excluir(id):
        c = Cliente(id, "", "", "", "")
        for h in Horarios.listar():
            if h.get_id_cliente() == id:
                raise ValueError(f"Cliente com ID possui horário agendado e não pode ser excluído.")
        Clientes.excluir(c)    

    def cliente_autenticar(email, senha):
        for c in View.cliente_listar():
            if c.get_email() == email and c.get_senha() == senha:
                return {"id" : c.get_id(), "nome" : c.get_nome() }
        return None

    def horario_inserir(data, confirmado, id_cliente, id_servico):
        if id_cliente is None or id_servico is None or id_cliente == 0 or id_servico == 0:
            raise ValueError("Cliente ou Serviço inválido. Verifique as opções selecionadas.")
        
        cliente = Clientes.listar_id(id_cliente)
        servico = Servicos.listar_id(id_servico)

        if cliente is None:
            raise ValueError(f"Cliente com ID {id_cliente} não encontrado.")
        if servico is None:
            raise ValueError(f"Serviço com ID {id_servico} não encontrado.")
        
        horario = Horario(0, data, confirmado, id_cliente, id_servico)
        Horarios.inserir(horario)




    def horario_listar():
        return Horarios.listar()    

    def horario_listar_disponiveis():
        horarios = View.horario_listar()
        disponiveis = []
        for h in horarios:
            if h.get_data() >= datetime.now() and h.get_id_cliente() == 0: 
                disponiveis.append(h)
        return disponiveis   

    def horario_atualizar(id, data, confirmado, id_cliente, id_servico):
        if Clientes.listar_id(id_cliente) is None:
            raise ValueError(f"Cliente não encontrado.")
        if Servicos.listar_id(id_servico) is None:
            raise ValueError(f"Serviço não encontrado.")
        
        c = Horario(id, data)
        c.set_confirmado(confirmado)
        c.set_id_cliente(id_cliente)
        c.set_id_servico(id_servico)
    
        Horarios.atualizar(c)

    def horario_excluir(id):
        c = Horario(id, None)
        h = Horarios.listar_id(id)

        if h is None or h.get_id_cliente() != 0:  
            raise ValueError(f"Não é possível excluir um horário agendado ou inexistente.")
            
        Horarios.excluir(c)    

    def horario_abrir_agenda(data, hora_inicio, hora_fim, intervalo):
       
        try:
            di = datetime.strptime(data + " " + hora_inicio, "%d/%m/%Y %H:%M")
            df = datetime.strptime(data + " " + hora_fim, "%d/%m/%Y %H:%M")
        except ValueError:
            raise ValueError("Formato de data e hora inválido. Utilize o formato dd/mm/aaaa HH:MM.")
        
        if di >= df:
            raise ValueError("A hora de início deve ser anterior à hora de término.")
        
        if intervalo <= 0:
            raise ValueError("O intervalo deve ser positivo.")
        
        d = timedelta(minutes=intervalo)
        x = di
        while x <= df:
            View.horario_inserir(x, False, None, None)  
            x = x + d

    def servico_inserir(descricao, valor, duracao):
        if descricao == "" or int(valor) <= 0 or int(duracao) <= 0:
            raise ValueError("Descrição, valor ou duração inválidos.")
        c = Servico(0, descricao, valor, duracao)
        Servicos.inserir(c)

    def servico_listar():
        return Servicos.listar()    

    def servico_listar_id(id):
        return Servicos.listar_id(id)    

    def servico_atualizar(id, descricao, valor, duracao):
        if descricao == "" or int(valor) <= 0 or int(duracao) <= 0:
            raise ValueError("Descrição, valor ou duração inválidos.")
        c = Servico(id, descricao, valor, duracao)
        Servicos.atualizar(c)

    def servico_excluir(id):
        c = Servico(id, "", 0, 0)
        for h in Horarios.listar():
            if h.get_id_servico() == id:
                raise ValueError(f"Serviço com ID {id} não pode ser excluído, pois está agendado.")
        Servicos.excluir(c)
