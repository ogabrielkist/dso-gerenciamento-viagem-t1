from datetime import date
from views.tela_base import TelaBase


class TelaPagamento(TelaBase):
    def __init__(self):
        super().__init__()
        self._controlador_pessoa = None
        self._controlador_viagem = None

    def set_controlador_pessoa(self, controlador_pessoa):
        self._controlador_pessoa = controlador_pessoa

    def set_controlador_viagem(self, controlador_viagem):
        self._controlador_viagem = controlador_viagem

    def le_opcao(self):
        opcoes = {1: "Incluir", 2: "Listar", 3: "Excluir", 4: "Editar"}
        self.tela_opcoes("PAGAMENTOS", opcoes)
        opcao = int(input("Escolha a opção: "))
        return opcao

    def pega_dados_entidade(self, dados_atuais=None):
        self.limpar_tela()
        print("\n-------- DADOS PAGAMENTO --------")

        data_atual = dados_atuais["data"].strftime("%Y-%m-%d") if dados_atuais else ""
        valor_atual = dados_atuais["valor_pago"] if dados_atuais else ""

        data_str = (
            input(f"Data do pagamento (YYYY-MM-DD) [{data_atual}]: ") or data_atual
        )
        data = date.fromisoformat(data_str)

        valor_input = input(f"Valor pago: R$ [{valor_atual}]: ") or str(valor_atual)
        valor_pago = float(valor_input)

        print("\nPagadores disponíveis:")
        pessoas = self._controlador_pessoa._entidades
        for i, pessoa in enumerate(pessoas, 1):
            print(f"{i} - {pessoa.nome} ({pessoa.identificacao})")

        if not pessoas:
            raise ValueError("Nenhuma pessoa cadastrada. Cadastre uma pessoa primeiro.")

        pagador_atual = dados_atuais["pagador"] if dados_atuais else None
        pagador_atual_index = None
        if pagador_atual:
            for i, pessoa in enumerate(pessoas):
                if pessoa.id == pagador_atual.id:
                    pagador_atual_index = i + 1
                    break

        if pagador_atual_index:
            print(f"Pagador atual: {pagador_atual_index} - {pagador_atual.nome}")
            opcao_pagador_input = input(
                f"Escolha o pagador (número) [{pagador_atual_index}]: "
            ) or str(pagador_atual_index)
        else:
            opcao_pagador_input = input("Escolha o pagador (número): ")

        opcao_pagador = int(opcao_pagador_input) - 1
        if opcao_pagador < 0 or opcao_pagador >= len(pessoas):
            raise ValueError("Opção de pagador inválida.")

        pagador_selecionado = pessoas[opcao_pagador]

        print("\nViagens disponíveis:")
        viagens = self._controlador_viagem._entidades
        for i, viagem in enumerate(viagens, 1):
            print(
                f"{i} - {viagem.data_inicio.strftime('%d/%m/%Y')} a {viagem.data_fim.strftime('%d/%m/%Y')} - R$ {viagem.valor_total_pacote:.2f}"
            )

        if not viagens:
            raise ValueError("Nenhuma viagem cadastrada. Cadastre uma viagem primeiro.")

        viagem_atual = dados_atuais["viagem"] if dados_atuais else None
        viagem_atual_index = None
        if viagem_atual:
            for i, viagem in enumerate(viagens):
                if viagem.id == viagem_atual.id:
                    viagem_atual_index = i + 1
                    break

        if viagem_atual_index:
            print(
                f"Viagem atual: {viagem_atual_index} - {viagem_atual.data_inicio.strftime('%d/%m/%Y')} a {viagem_atual.data_fim.strftime('%d/%m/%Y')}"
            )
            opcao_viagem_input = input(
                f"Escolha a viagem (número) [{viagem_atual_index}]: "
            ) or str(viagem_atual_index)
        else:
            opcao_viagem_input = input("Escolha a viagem (número): ")

        opcao_viagem = int(opcao_viagem_input) - 1
        if opcao_viagem < 0 or opcao_viagem >= len(viagens):
            raise ValueError("Opção de viagem inválida.")

        viagem_selecionada = viagens[opcao_viagem]

        print("\nTipos de pagamento:")
        print("1 - Dinheiro")
        print("2 - PIX")
        print("3 - Cartão de Crédito")

        tipo_atual = dados_atuais.get("tipo", "") if dados_atuais else ""
        tipo_input = (
            input(f"Escolha o tipo de pagamento (1-3) [{tipo_atual}]: ") or tipo_atual
        )

        tipo_pagamento = int(tipo_input)

        dados_base = {
            "data": data,
            "valor_pago": valor_pago,
            "pagador": pagador_selecionado,
            "viagem": viagem_selecionada,
            "tipo": tipo_pagamento,
        }

        if tipo_pagamento == 2:
            cpf_atual = dados_atuais.get("cpf_pagador", "") if dados_atuais else ""
            cpf = input(f"CPF do pagador [{cpf_atual}]: ") or cpf_atual
            dados_base["cpf_pagador"] = cpf
        elif tipo_pagamento == 3:
            numero_atual = dados_atuais.get("numero_cartao", "") if dados_atuais else ""
            bandeira_atual = dados_atuais.get("bandeira", "") if dados_atuais else ""
            numero = input(f"Número do cartão [{numero_atual}]: ") or numero_atual
            bandeira = (
                input(f"Bandeira do cartão [{bandeira_atual}]: ") or bandeira_atual
            )
            dados_base["numero_cartao"] = numero
            dados_base["bandeira"] = bandeira

        return dados_base

    def mostra_entidade(self, dados_pagamento):
        print("Data:", dados_pagamento["data"].strftime("%d/%m/%Y"))
        print("Valor:", f"R$ {dados_pagamento['valor_pago']:.2f}")
        print("Pagador:", dados_pagamento["pagador"].nome)
        print(
            "Viagem:",
            f"{dados_pagamento['viagem'].data_inicio.strftime('%d/%m/%Y')} a {dados_pagamento['viagem'].data_fim.strftime('%d/%m/%Y')}",
        )
        print("Tipo:", dados_pagamento["tipo"])
        if "cpf_pagador" in dados_pagamento:
            print("CPF:", dados_pagamento["cpf_pagador"])
        if "numero_cartao" in dados_pagamento:
            print("Cartão:", dados_pagamento["numero_cartao"])
            print("Bandeira:", dados_pagamento["bandeira"])
        print("--------------------")

    def seleciona_entidade(self):
        data_str = input("Data do pagamento (YYYY-MM-DD): ")
        pagador = input("Nome do pagador: ")
        valor = input("Valor pago: ")
        return f"{data_str}|{pagador}|{valor}"
