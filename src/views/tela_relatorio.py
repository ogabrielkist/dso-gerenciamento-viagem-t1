import os
from controllers.controlador_relatorio import ControladorRelatorio
from models.exceptions import ListaVaziaException, OpcaoInvalidaException


class TelaRelatorio:
    def __init__(self, controlador_relatorio: ControladorRelatorio):
        self.__controlador_relatorio = controlador_relatorio

    def abre_tela(self):
        lista_opcoes = {
            1: self.relatorio_destinos_populares,
            0: self.voltar,
        }

        while True:
            try:
                self.limpar_tela()
                print("\n-------- RELATÓRIOS --------")
                print("Escolha o tipo de relatório:")
                print("1 - Destinos Mais Populares")
                print("0 - Voltar")

                opcao = int(input("Digite a opção: "))
                funcao_escolhida = lista_opcoes.get(opcao)
                if not funcao_escolhida:
                    raise OpcaoInvalidaException("Opção inválida!")

                funcao_escolhida()

            except OpcaoInvalidaException as e:
                print(f"ERRO: {str(e)}")
                input("\nPressione ENTER para continuar...")
                self.limpar_tela()
            except ValueError:
                print("ERRO: Digite um número válido!")
                input("\nPressione ENTER para continuar...")
                self.limpar_tela()
            except Exception as e:
                print(f"ERRO: {str(e)}")
                input("\nPressione ENTER para continuar...")
                self.limpar_tela()

    def relatorio_destinos_populares(self):
        try:
            self.limpar_tela()
            print("\n-------- DESTINOS MAIS POPULARES --------")

            destinos = self.__controlador_relatorio.relatorio_destinos_mais_populares()

            print(f"\n{'Posição':<8} {'Destino':<30} {'Número de Visitas':<20}")
            print("-" * 60)

            for i, (destino, visitas) in enumerate(destinos, 1):
                print(f"{i:<8} {destino:<30} {visitas:<20}")

            print(f"\nTotal de destinos analisados: {len(destinos)}")

        except ListaVaziaException as e:
            print(f"AVISO: {str(e)}")
        except Exception as e:
            print(f"ERRO: {str(e)}")

        input("\nPressione ENTER para continuar...")
        self.limpar_tela()

    def voltar(self):
        return

    def limpar_tela(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
