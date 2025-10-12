from controllers import ControladorPessoa
from models.exceptions import OpcaoInvalidaException


class ControladorPrincipal:
    def __init__(self):
        self.__ctrl_pessoa = ControladorPessoa(self)

    def inicia_sistema(self):
        self.abre_tela()

    def cadastra_pessoa(self):
        self.__ctrl_pessoa.abre_tela()

    def cadastra_viagem(self):
        print("Funcionalidade de Viagens ainda não implementada.")

    def encerra_sistema(self):
        exit(0)

    def abre_tela(self):
        lista_opcoes = {
            1: self.cadastra_pessoa,
            2: self.cadastra_viagem,
            0: self.encerra_sistema,
        }

        while True:
            try:
                print("\n-------- SISTEMA DE VIAGENS --------")
                print("Escolha sua opção")
                print("1 - Gerenciar Pessoas")
                print("0 - Sair")

                opcao = int(input("Digite a opção: "))
                funcao_escolhida = lista_opcoes.get(opcao)
                if not funcao_escolhida:
                    raise OpcaoInvalidaException("Opção inválida!")

                funcao_escolhida()

            except OpcaoInvalidaException as e:
                print(str(e))
