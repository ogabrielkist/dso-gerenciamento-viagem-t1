import os
from abc import ABC, abstractmethod


class TelaBase(ABC):
    def limpar_tela(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def aguardar_enter(self):
        input("\nPressione ENTER para continuar...")

    def mostra_mensagem(self, msg, aguardar=True):
        print(msg)
        if aguardar:
            self.aguardar_enter()

    def mostra_erro(self, msg):
        print(f"ERRO: {msg}")
        self.aguardar_enter()
        self.limpar_tela()

    def mostra_sucesso(self, msg):
        print(f"SUCESSO: {msg}")
        self.aguardar_enter()
        self.limpar_tela()

    def tela_opcoes(self, titulo, opcoes):
        self.limpar_tela()
        print(f"\n-------- {titulo} --------")
        print("Escolha a opção")
        for numero, descricao in opcoes.items():
            print(f"{numero} - {descricao}")
        print("0 - Retornar")

    @abstractmethod
    def le_opcao(self):
        pass

    @abstractmethod
    def pega_dados_entidade(self, dados_atuais=None):
        pass
