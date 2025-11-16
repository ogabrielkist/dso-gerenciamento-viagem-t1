from views.tela_base import TelaBase


class TelaPassagem(TelaBase):
    def __init__(self):
        super().__init__()
        self._controlador_pessoa = None
        self._controlador_trecho = None

    def set_controlador_pessoa(self, controlador_pessoa):
        self._controlador_pessoa = controlador_pessoa

    def set_controlador_trecho(self, controlador_trecho):
        self._controlador_trecho = controlador_trecho

    def le_opcao(self):
        opcoes = {
            1: "Incluir",
            2: "Listar",
            3: "Excluir",
            4: "Editar",
            5: "Confirmar Compra",
        }
        self.tela_opcoes("PASSAGENS", opcoes)
        opcao = int(input("Escolha a opção: "))
        return opcao

    def pega_dados_entidade(self, dados_atuais=None):
        self.limpar_tela()
        print("\n-------- DADOS PASSAGEM --------")

        print("\nPassageiros disponíveis:")
        pessoas = self._controlador_pessoa._entidades
        for i, pessoa in enumerate(pessoas, 1):
            print(f"{i} - {pessoa.nome} ({pessoa.identificacao})")

        if not pessoas:
            raise ValueError("Nenhuma pessoa cadastrada. Cadastre uma pessoa primeiro.")

        passageiro_atual = dados_atuais["passageiro"] if dados_atuais else None
        passageiro_atual_index = None
        if passageiro_atual:
            for i, pessoa in enumerate(pessoas):
                if pessoa.id == passageiro_atual.id:
                    passageiro_atual_index = i + 1
                    break

        if passageiro_atual_index:
            print(
                f"Passageiro atual: {passageiro_atual_index} - {passageiro_atual.nome}"
            )
            opcao_passageiro_input = input(
                f"Escolha o passageiro (número) [{passageiro_atual_index}]: "
            ) or str(passageiro_atual_index)
        else:
            opcao_passageiro_input = input("Escolha o passageiro (número): ")

        opcao_passageiro = int(opcao_passageiro_input) - 1
        if opcao_passageiro < 0 or opcao_passageiro >= len(pessoas):
            raise ValueError("Opção de passageiro inválida.")

        passageiro_selecionado = pessoas[opcao_passageiro]

        print("\nTrechos de viagem disponíveis:")
        trechos = self._controlador_trecho._entidades
        for i, trecho in enumerate(trechos, 1):
            print(
                f"{i} - {trecho.local_origem} -> {trecho.local_destino} ({trecho.data.strftime('%d/%m/%Y %H:%M')})"
            )

        if not trechos:
            raise ValueError(
                "Nenhum trecho de viagem cadastrado. Cadastre um trecho primeiro."
            )

        trecho_atual = dados_atuais["trecho"] if dados_atuais else None
        trecho_atual_index = None
        if trecho_atual:
            for i, trecho in enumerate(trechos):
                if trecho.id == trecho_atual.id:
                    trecho_atual_index = i + 1
                    break

        if trecho_atual_index:
            print(
                f"Trecho atual: {trecho_atual_index} - {trecho_atual.local_origem} -> {trecho_atual.local_destino}"
            )
            opcao_trecho_input = input(
                f"Escolha o trecho (número) [{trecho_atual_index}]: "
            ) or str(trecho_atual_index)
        else:
            opcao_trecho_input = input("Escolha o trecho (número): ")

        opcao_trecho = int(opcao_trecho_input) - 1
        if opcao_trecho < 0 or opcao_trecho >= len(trechos):
            raise ValueError("Opção de trecho inválida.")

        trecho_selecionado = trechos[opcao_trecho]

        print("\nResponsáveis pela compra disponíveis:")
        for i, pessoa in enumerate(pessoas, 1):
            print(f"{i} - {pessoa.nome} ({pessoa.identificacao})")

        responsavel_atual = dados_atuais["responsavel_compra"] if dados_atuais else None
        responsavel_atual_index = None
        if responsavel_atual:
            for i, pessoa in enumerate(pessoas):
                if pessoa.id == responsavel_atual.id:
                    responsavel_atual_index = i + 1
                    break

        if responsavel_atual_index:
            print(
                f"Responsável atual: {responsavel_atual_index} - {responsavel_atual.nome}"
            )
            opcao_responsavel_input = input(
                f"Escolha o responsável (número) [{responsavel_atual_index}]: "
            ) or str(responsavel_atual_index)
        else:
            opcao_responsavel_input = input("Escolha o responsável (número): ")

        opcao_responsavel = int(opcao_responsavel_input) - 1
        if opcao_responsavel < 0 or opcao_responsavel >= len(pessoas):
            raise ValueError("Opção de responsável inválida.")

        responsavel_selecionado = pessoas[opcao_responsavel]

        return {
            "passageiro": passageiro_selecionado,
            "trecho": trecho_selecionado,
            "responsavel_compra": responsavel_selecionado,
        }

    def mostra_entidade(self, dados_passagem):
        status = "Comprada" if dados_passagem["compra_efetuada"] else "Pendente"
        print("Passageiro:", dados_passagem["passageiro"].nome)
        print(
            "Trecho:",
            f"{dados_passagem['trecho'].local_origem} -> {dados_passagem['trecho'].local_destino}",
        )
        print("Data:", dados_passagem["trecho"].data.strftime("%d/%m/%Y %H:%M"))
        print("Status:", status)
        print("Responsável:", dados_passagem["responsavel_compra"].nome)
        print("--------------------")

    def seleciona_entidade(self):
        passageiro = input("Nome do passageiro: ")
        origem = input("Local de origem do trecho: ")
        destino = input("Local de destino do trecho: ")
        return f"{passageiro}|{origem}|{destino}"
