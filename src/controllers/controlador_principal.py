from .controlador_pessoa import ControladorPessoa
from .controlador_pais import ControladorPais
from .controlador_cidade import ControladorCidade
from .controlador_empresa_transporte import ControladorEmpresaTransporte
from .controlador_meio_transporte import ControladorMeioTransporte
from .controlador_viagem import ControladorViagem
from .controlador_trecho_viagem import ControladorTrechoViagem
from .controlador_passeio_turistico import ControladorPasseioTuristico
from .controlador_passagem import ControladorPassagem
from .controlador_pagamento import ControladorPagamento
from .controlador_itinerario_viagem import ControladorItinerarioViagem
from .controlador_relatorio import ControladorRelatorio
from .controlador_destinos import ControladorDestinos

from views.tela_principal_gui import TelaPrincipalGUI


class ControladorPrincipal:
    def __init__(self):
        self.__tela = TelaPrincipalGUI()

        self.__ctrl_pessoa = ControladorPessoa(self)
        self.__ctrl_pais = ControladorPais(self)
        self.__ctrl_empresa = ControladorEmpresaTransporte(self)
        self.__ctrl_cidade = ControladorCidade(self, self.__ctrl_pais)
        self.__ctrl_meio_transporte = ControladorMeioTransporte(
            self, self.__ctrl_empresa
        )
        self.__ctrl_trecho = ControladorTrechoViagem(self, self.__ctrl_meio_transporte)
        self.__ctrl_passagem = ControladorPassagem(
            self, self.__ctrl_pessoa, self.__ctrl_trecho
        )
        self.__ctrl_passeio = ControladorPasseioTuristico(
            self, self.__ctrl_cidade, self.__ctrl_pessoa
        )
        self.__ctrl_itinerario = ControladorItinerarioViagem(self, self.__ctrl_passeio)
        self.__ctrl_viagem = ControladorViagem(self, self.__ctrl_itinerario, self.__ctrl_pessoa)
        self.__ctrl_pagamento = ControladorPagamento(
            self, self.__ctrl_pessoa, self.__ctrl_viagem
        )
        self.__ctrl_relatorio = ControladorRelatorio(self)
        self.__ctrl_destinos = ControladorDestinos(
            self, self.__ctrl_pais, self.__ctrl_cidade
        )

    def inicia_sistema(self):
        self.abre_tela()

    def cadastra_pessoa(self):
        self.__ctrl_pessoa.abre_tela()

    def cadastra_pais(self):
        self.__ctrl_pais.abre_tela()

    def cadastra_cidade(self):
        self.__ctrl_cidade.abre_tela()

    def cadastra_empresa_transporte(self):
        self.__ctrl_empresa.abre_tela()

    def cadastra_meio_transporte(self):
        self.__ctrl_meio_transporte.abre_tela()

    def cadastra_viagem(self):
        self.__ctrl_viagem.abre_tela()

    def cadastra_trecho_viagem(self):
        self.__ctrl_trecho.abre_tela()

    def cadastra_passeio_turistico(self):
        self.__ctrl_passeio.abre_tela()

    def cadastra_passagem(self):
        self.__ctrl_passagem.abre_tela()

    def cadastra_pagamento(self):
        self.__ctrl_pagamento.abre_tela()

    def cadastra_itinerario_viagem(self):
        self.__ctrl_itinerario.abre_tela()

    def relatorios(self):
        self.__ctrl_relatorio.abre_tela()

    def gerenciar_destinos(self):
        self.__ctrl_destinos.abre_tela()

    def encerra_sistema(self):
        exit(0)

    def abre_tela(self):
        lista_opcoes = {
            1: self.cadastra_pessoa,
            2: self.cadastra_pais,
            3: self.cadastra_cidade,
            4: self.cadastra_empresa_transporte,
            5: self.cadastra_meio_transporte,
            6: self.cadastra_passagem,
            7: self.cadastra_trecho_viagem,
            8: self.cadastra_passeio_turistico,
            9: self.cadastra_pagamento,
            10: self.cadastra_viagem,
            11: self.cadastra_itinerario_viagem,
            12: self.relatorios,
            13: self.gerenciar_destinos,
            0: self.encerra_sistema,
        }

        while True:
            opcao_escolhida = self.__tela.mostrar_menu_principal()
            funcao_escolhida = lista_opcoes.get(opcao_escolhida)

            if funcao_escolhida:
                funcao_escolhida()
                if opcao_escolhida == 0:
                    break
            else:
                self.__tela.mostra_erro("Opção de menu inválida. Chave não encontrada.")
