from datetime import time
from views.tela_base import TelaBase


class TelaPasseioTuristico(TelaBase):
    def __init__(self):
        super().__init__()
        self._controlador_cidade = None
        self._controlador_pessoa = None

    def set_controlador_cidade(self, controlador_cidade):
        self._controlador_cidade = controlador_cidade

    def set_controlador_pessoa(self, controlador_pessoa):
        self._controlador_pessoa = controlador_pessoa

    def le_opcao(self):
        opcoes = {1: "Incluir", 2: "Listar", 3: "Excluir", 4: "Editar"}
        self.tela_opcoes("PASSEIOS TURÍSTICOS", opcoes)
        opcao = int(input("Escolha a opção: "))
        return opcao

    def pega_dados_entidade(self, dados_atuais=None):
        self.limpar_tela()
        print("\n-------- DADOS PASSEIO TURÍSTICO --------")

        atracao_atual = dados_atuais["atracao_turistica"] if dados_atuais else ""
        inicio_atual = (
            dados_atuais["horario_inicio"].strftime("%H:%M") if dados_atuais else ""
        )
        fim_atual = (
            dados_atuais["horario_fim"].strftime("%H:%M") if dados_atuais else ""
        )
        valor_atual = dados_atuais["valor"] if dados_atuais else ""

        atracao = input(f"Atração turística [{atracao_atual}]: ") or atracao_atual

        horario_inicio_str = (
            input(f"Horário de início (HH:MM) [{inicio_atual}]: ") or inicio_atual
        )
        horario_inicio = time.fromisoformat(horario_inicio_str)

        horario_fim_str = input(f"Horário de fim (HH:MM) [{fim_atual}]: ") or fim_atual
        horario_fim = time.fromisoformat(horario_fim_str)

        valor_input = input(f"Valor do passeio: R$ [{valor_atual}]: ") or str(
            valor_atual
        )
        valor = float(valor_input)

        print("\nCidades disponíveis:")
        cidades = self._controlador_cidade._entidades
        for i, cidade in enumerate(cidades, 1):
            print(f"{i} - {cidade.nome} - {cidade.pais.nome}")

        if not cidades:
            raise ValueError("Nenhuma cidade cadastrada. Cadastre uma cidade primeiro.")

        cidade_atual = dados_atuais["cidade"] if dados_atuais else None
        cidade_atual_index = None
        if cidade_atual:
            for i, cidade in enumerate(cidades):
                if cidade.id == cidade_atual.id:
                    cidade_atual_index = i + 1
                    break

        if cidade_atual_index:
            print(
                f"Cidade atual: {cidade_atual_index} - {cidade_atual.nome} - {cidade_atual.pais.nome}"
            )
            opcao_cidade_input = input(
                f"Escolha a cidade (número) [{cidade_atual_index}]: "
            ) or str(cidade_atual_index)
        else:
            opcao_cidade_input = input("Escolha a cidade (número): ")

        opcao_cidade = int(opcao_cidade_input) - 1
        if opcao_cidade < 0 or opcao_cidade >= len(cidades):
            raise ValueError("Opção de cidade inválida.")

        cidade_selecionada = cidades[opcao_cidade]

        return {
            "atracao_turistica": atracao,
            "horario_inicio": horario_inicio,
            "horario_fim": horario_fim,
            "valor": valor,
            "cidade": cidade_selecionada,
        }

    def mostra_entidade(self, dados_passeio):
        print("Atração:", dados_passeio["atracao_turistica"])
        print(
            "Horário:",
            f"{dados_passeio['horario_inicio'].strftime('%H:%M')} - {dados_passeio['horario_fim'].strftime('%H:%M')}",
        )
        print("Valor:", f"R$ {dados_passeio['valor']:.2f}")
        print(
            "Cidade:",
            f"{dados_passeio['cidade'].nome} - {dados_passeio['cidade'].pais.nome}",
        )
        print("Participantes:", len(dados_passeio["participantes_passeio"]))
        print("--------------------")

    def seleciona_entidade(self):
        atracao = input("Nome da atração turística: ")
        cidade = input("Nome da cidade: ")
        horario = input("Horário de início (HH:MM): ")
        return f"{atracao}|{cidade}|{horario}"
