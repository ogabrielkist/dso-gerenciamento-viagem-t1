from datetime import date
from views.tela_base import TelaBase


class TelaItinerarioViagem(TelaBase):
    def __init__(self):
        super().__init__()
        self._controlador_viagem = None
        self._controlador_passeio = None

    def set_controlador_viagem(self, controlador_viagem):
        self._controlador_viagem = controlador_viagem

    def set_controlador_passeio(self, controlador_passeio):
        self._controlador_passeio = controlador_passeio

    def le_opcao(self):
        opcoes = {
            1: "Incluir",
            2: "Listar",
            3: "Excluir",
            4: "Editar",
            5: "Gerenciar Passeios",
        }
        self.tela_opcoes("ITINERÁRIOS DE VIAGEM", opcoes)
        opcao = int(input("Escolha a opção: "))
        return opcao

    def pega_dados_entidade(self, dados_atuais=None):
        self.limpar_tela()
        print("\n-------- DADOS ITINERÁRIO DE VIAGEM --------")

        data_atual = dados_atuais["data"].strftime("%Y-%m-%d") if dados_atuais else ""

        data_str = (
            input(f"Data do itinerário (YYYY-MM-DD) [{data_atual}]: ") or data_atual
        )
        data = date.fromisoformat(data_str)

        return {
            "data": data,
        }

    def mostra_entidade(self, dados_itinerario):
        print("--------------------")
        print("ID:", dados_itinerario["id"])
        print("Data:", dados_itinerario["data"].strftime("%d/%m/%Y"))
        print("Passeios:", len(dados_itinerario["passeios"]))
        for i, passeio in enumerate(dados_itinerario["passeios"], 1):
            print(
                f"  {i} - {passeio.atracao_turistica} ({passeio.horario_inicio.strftime('%H:%M')} - {passeio.horario_fim.strftime('%H:%M')})"
            )
        print("--------------------")

    def seleciona_entidade(self):
        id = input("ID do itinerário que deseja selecionar: ")
        return id

    def gerenciar_passeios(self, itinerario):
        while True:
            self.limpar_tela()
            print(
                f"\n-------- GERENCIAR PASSEIOS - {itinerario.data.strftime('%d/%m/%Y')} --------"
            )
            print("1 - Adicionar Passeio")
            print("2 - Remover Passeio")
            print("3 - Listar Passeios")
            print("0 - Voltar")

            opcao = int(input("Escolha a opção: "))

            if opcao == 1:
                self.adicionar_passeio(itinerario)
            elif opcao == 2:
                self.remover_passeio(itinerario)
            elif opcao == 3:
                self.listar_passeios(itinerario)
            elif opcao == 0:
                break

    def adicionar_passeio(self, itinerario):
        print("\nPasseios disponíveis:")
        passeios = self._controlador_passeio._entidades
        for i, passeio in enumerate(passeios, 1):
            print(f"{i} - {passeio.atracao_turistica} - {passeio.cidade.nome}")

        if not passeios:
            self.mostra_erro("Nenhum passeio cadastrado.")
            return

        opcao = int(input("Escolha o passeio (número): ")) - 1
        if opcao < 0 or opcao >= len(passeios):
            self.mostra_erro("Opção inválida.")
            return

        passeio_selecionado = passeios[opcao]
        itinerario.incluir_passeio(passeio_selecionado)
        self.mostra_sucesso("Passeio adicionado ao itinerário!")

    def remover_passeio(self, itinerario):
        if not itinerario.passeios:
            self.mostra_erro("Nenhum passeio no itinerário.")
            return

        print("\nPasseios no itinerário:")
        for i, passeio in enumerate(itinerario.passeios, 1):
            print(f"{i} - {passeio.atracao_turistica} - {passeio.cidade.nome}")

        opcao = int(input("Escolha o passeio para remover (número): ")) - 1
        if opcao < 0 or opcao >= len(itinerario.passeios):
            self.mostra_erro("Opção inválida.")
            return

        passeio_remover = itinerario.passeios[opcao]
        itinerario.excluir_passeio(passeio_remover)
        self.mostra_sucesso("Passeio removido do itinerário!")

    def listar_passeios(self, itinerario):
        if not itinerario.passeios:
            self.mostra_erro("Nenhum passeio no itinerário.")
            return

        print(f"\nPasseios do dia {itinerario.data.strftime('%d/%m/%Y')}:")
        for i, passeio in enumerate(itinerario.passeios, 1):
            print(f"{i} - {passeio.atracao_turistica}")
            print(
                f"    Horário: {passeio.horario_inicio.strftime('%H:%M')} - {passeio.horario_fim.strftime('%H:%M')}"
            )
            print(f"    Cidade: {passeio.cidade.nome} - {passeio.cidade.pais.nome}")
            print(f"    Valor: R$ {passeio.valor:.2f}")
            print()

        self.aguardar_enter()
