from datetime import datetime
from views.tela_base import TelaBase


class TelaTrechoViagem(TelaBase):
    def __init__(self):
        super().__init__()
        self._controlador_meio_transporte = None

    def set_controlador_meio_transporte(self, controlador_meio_transporte):
        self._controlador_meio_transporte = controlador_meio_transporte

    def le_opcao(self):
        opcoes = {1: "Incluir", 2: "Listar", 3: "Excluir", 4: "Editar"}
        self.tela_opcoes("TRECHOS DE VIAGEM", opcoes)
        opcao = int(input("Escolha a opção: "))
        return opcao

    def pega_dados_entidade(self, dados_atuais=None):
        self.limpar_tela()
        print("\n-------- DADOS TRECHO DE VIAGEM --------")

        data_atual = (
            dados_atuais["data"].strftime("%Y-%m-%d %H:%M") if dados_atuais else ""
        )
        origem_atual = dados_atuais["local_origem"] if dados_atuais else ""
        destino_atual = dados_atuais["local_destino"] if dados_atuais else ""

        data_str = (
            input(f"Data e hora (YYYY-MM-DD HH:MM) [{data_atual}]: ") or data_atual
        )
        data = datetime.fromisoformat(data_str)

        local_origem = input(f"Local de origem [{origem_atual}]: ") or origem_atual
        local_destino = input(f"Local de destino [{destino_atual}]: ") or destino_atual

        print("\nMeios de transporte disponíveis:")
        meios = self._controlador_meio_transporte._entidades
        for i, meio in enumerate(meios, 1):
            print(f"{i} - {meio.tipo.value} - {meio.empresa.nome}")

        if not meios:
            raise ValueError(
                "Nenhum meio de transporte cadastrado. Cadastre um meio de transporte primeiro."
            )

        meio_atual = dados_atuais["meio_transporte"] if dados_atuais else None
        meio_atual_index = None
        if meio_atual:
            for i, meio in enumerate(meios):
                if meio.id == meio_atual.id:
                    meio_atual_index = i + 1
                    break

        if meio_atual_index:
            print(
                f"Meio atual: {meio_atual_index} - {meio_atual.tipo.value} - {meio_atual.empresa.nome}"
            )
            opcao_meio_input = input(
                f"Escolha o meio de transporte (número) [{meio_atual_index}]: "
            ) or str(meio_atual_index)
        else:
            opcao_meio_input = input("Escolha o meio de transporte (número): ")

        opcao_meio = int(opcao_meio_input) - 1
        if opcao_meio < 0 or opcao_meio >= len(meios):
            raise ValueError("Opção de meio de transporte inválida.")

        meio_selecionado = meios[opcao_meio]

        return {
            "data": data,
            "local_origem": local_origem,
            "local_destino": local_destino,
            "meio_transporte": meio_selecionado,
        }

    def mostra_entidade(self, dados_trecho):
        print("Data:", dados_trecho["data"].strftime("%d/%m/%Y %H:%M"))
        print("Origem:", dados_trecho["local_origem"])
        print("Destino:", dados_trecho["local_destino"])
        print(
            "Transporte:",
            f"{dados_trecho['meio_transporte'].tipo.value} - {dados_trecho['meio_transporte'].empresa.nome}",
        )
        print("--------------------")

    def seleciona_entidade(self):
        data_str = input("Data do trecho de viagem (YYYY-MM-DD HH:MM): ")
        origem = input("Local de origem: ")
        destino = input("Local de destino: ")
        return f"{data_str}|{origem}|{destino}"
