from datetime import date
from views.tela_base import TelaBase


class TelaViagem(TelaBase):
    def le_opcao(self):
        opcoes = {1: "Incluir", 2: "Listar", 3: "Excluir", 4: "Editar"}
        self.tela_opcoes("VIAGENS", opcoes)
        opcao = int(input("Escolha a opção: "))
        return opcao

    def pega_dados_entidade(self, dados_atuais=None):
        self.limpar_tela()
        print("\n-------- DADOS VIAGEM --------")

        data_inicio_atual = (
            dados_atuais["data_inicio"].strftime("%Y-%m-%d") if dados_atuais else ""
        )
        data_fim_atual = (
            dados_atuais["data_fim"].strftime("%Y-%m-%d") if dados_atuais else ""
        )
        valor_atual = dados_atuais["valor_total_pacote"] if dados_atuais else ""

        data_inicio_str = (
            input(f"Data de início (YYYY-MM-DD) [{data_inicio_atual}]: ")
            or data_inicio_atual
        )
        data_inicio = date.fromisoformat(data_inicio_str)

        data_fim_str = (
            input(f"Data de fim (YYYY-MM-DD) [{data_fim_atual}]: ") or data_fim_atual
        )
        data_fim = date.fromisoformat(data_fim_str)

        valor_input = input(f"Valor total do pacote: R$ [{valor_atual}]: ") or str(
            valor_atual
        )
        valor_total = float(valor_input)

        return {
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "valor_total_pacote": valor_total,
        }

    def mostra_entidade(self, dados_viagem):
        print("ID:", dados_viagem["id"])
        print("Data início:", dados_viagem["data_inicio"].strftime("%d/%m/%Y"))
        print("Data fim:", dados_viagem["data_fim"].strftime("%d/%m/%Y"))
        print("Valor total:", f"R$ {dados_viagem['valor_total_pacote']:.2f}")
        print("Participantes:", len(dados_viagem["participantes"]))
        print("Destinos:", len(dados_viagem["destinos_visitados"]))
        print("--------------------")

    def seleciona_entidade(self):
        id = input("ID da viagem que deseja selecionar: ")
        return id
