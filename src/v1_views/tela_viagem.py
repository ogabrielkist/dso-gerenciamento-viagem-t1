from datetime import date
from views.tela_base import TelaBase


class TelaViagem(TelaBase):
    def __init__(self):
        super().__init__()
        self._controlador_itinerario = None

    def set_controlador_itinerario(self, controlador_itinerario):
        self._controlador_itinerario = controlador_itinerario
        
    def le_opcao(self):
        opcoes = {
            1: "Incluir", 
            2: "Listar", 
            3: "Excluir", 
            4: "Editar",
            5: "Gerenciar Itinerários"
        }
        self.tela_opcoes("VIAGENS", opcoes)
        
        try:
            opcao = int(input("Escolha a opção: "))
            return opcao
        except ValueError:
            self.mostra_erro("Opção inválida! Digite um número.")
            return -1

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

    def gerenciar_itinerarios(self, viagem):
        """
        Contém o loop do sub-menu para gerenciar itinerários,
        """
        while True:
            self.limpar_tela()
            print(
                f"\n-------- GERENCIAR ITINERÁRIOS - Viagem {viagem.data_inicio.strftime('%d/%m/%Y')} --------"
            )
            print("1 - Adicionar Itinerário")
            print("2 - Remover Itinerário")
            print("3 - Listar Itinerários da Viagem")
            print("0 - Voltar")
            
            try:
                opcao = int(input("Escolha a opção: "))

                if opcao == 1:
                    self.adicionar_itinerario(viagem)
                elif opcao == 2:
                    self.remover_itinerario(viagem)
                elif opcao == 3:
                    self.listar_itinerarios(viagem)
                elif opcao == 0:
                    break
                else:
                    self.mostra_erro("Opção inválida.")
            except ValueError:
                self.mostra_erro("Opção deve ser um número.")

    def adicionar_itinerario(self, viagem):
        """
        Acessa o controlador de itinerários, lista os itinerários
        disponíveis e os adiciona ao modelo da viagem.
        """
        print("\nItinerários disponíveis (que ainda não estão na viagem):")
        
        itinerarios_todos = self._controlador_itinerario._entidades
        
        # Filtra para mostrar apenas os que não estão na viagem
        itinerarios_disponiveis = [
            it for it in itinerarios_todos if it not in viagem.itinerarios
        ]

        if not itinerarios_disponiveis:
            self.mostra_erro("Nenhum itinerário novo disponível para adicionar.")
            self.aguardar_enter()
            return

        for i, itinerario in enumerate(viagem.itinerarios, 1):
            print(f"{i} - Data: {itinerario.data.strftime('%d/%m/%Y')}")
            # Mostra os passeios desse itinerário
            for passeio in itinerario.passeios:
                print(f"    - {passeio.atracao_turistica}")
                print(
                    f"    Horário: {passeio.horario_inicio.strftime('%H:%M')} - {passeio.horario_fim.strftime('%H:%M')}"
                )
                print(f"    Cidade: {passeio.cidade.nome} - {passeio.cidade.pais.nome}")
                print(f"    Valor: R$ {passeio.valor:.2f}")
                print()

        try:
            opcao = int(input("Escolha o itinerário (número): ")) - 1
            if opcao < 0 or opcao >= len(itinerarios_disponiveis):
                self.mostra_erro("Opção inválida.")
                return

            itinerario_selecionado = itinerarios_disponiveis[opcao]
            
            viagem.incluir_itinerario(itinerario_selecionado)
            self.mostra_sucesso("Itinerário adicionado à viagem!")
            
        except ValueError:
            self.mostra_erro("Entrada inválida.")
        finally:
            self.aguardar_enter()

    def remover_itinerario(self, viagem):
        """
        Lista os itinerários da viagem e remove o selecionado.
        """
        if not viagem.itinerarios:
            self.mostra_erro("Nenhum itinerário nesta viagem para remover.")
            self.aguardar_enter()
            return

        print("\nItinerários nesta viagem:")
        for i, itinerario in enumerate(viagem.itinerarios, 1):
            print(f"{i} - Data: {itinerario.data.strftime('%d/%m/%Y')}")
            # Mostra os passeios desse itinerário
            for passeio in itinerario.passeios:
                print(f"    - {passeio.atracao_turistica}")
                print(
                    f"    Horário: {passeio.horario_inicio.strftime('%H:%M')} - {passeio.horario_fim.strftime('%H:%M')}"
                )
                print(f"    Cidade: {passeio.cidade.nome} - {passeio.cidade.pais.nome}")
                print(f"    Valor: R$ {passeio.valor:.2f}")
                print()

        try:
            opcao = int(input("Escolha o itinerário para remover (número): ")) - 1
            if opcao < 0 or opcao >= len(viagem.itinerarios):
                self.mostra_erro("Opção inválida.")
                return

            itinerario_remover = viagem.itinerarios[opcao] 
            
            viagem.excluir_itinerario(itinerario_remover)
            self.mostra_sucesso("Itinerário removido da viagem!")
            
        except ValueError:
            self.mostra_erro("Entrada inválida.")
        finally:
            self.aguardar_enter()

    def listar_itinerarios(self, viagem):
        """
        Apenas lista os itinerários atualmente associados à viagem.
        """
        if not viagem.itinerarios:
            self.mostra_erro("Nenhum itinerário cadastrado nesta viagem.")
            self.aguardar_enter()
            return

        print(f"\nItinerários da Viagem de {viagem.data_inicio.strftime('%d/%m/%Y')}:")
        
        for i, itinerario in enumerate(viagem.itinerarios, 1):
            print(f"{i} - Data: {itinerario.data.strftime('%d/%m/%Y')}")
            # Mostra os passeios desse itinerário
            for passeio in itinerario.passeios:
                print(f"    - {passeio.atracao_turistica}")
                print(
                    f"    Horário: {passeio.horario_inicio.strftime('%H:%M')} - {passeio.horario_fim.strftime('%H:%M')}"
                )
                print(f"    Cidade: {passeio.cidade.nome} - {passeio.cidade.pais.nome}")
                print(f"    Valor: R$ {passeio.valor:.2f}")
                print()

        self.aguardar_enter()
