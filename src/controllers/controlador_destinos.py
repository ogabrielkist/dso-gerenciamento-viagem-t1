import FreeSimpleGUI as sg
from controllers.controlador_base import ControladorBase
from views.tela_destinos_gui import TelaDestinosGUI


class ControladorDestinos(ControladorBase):
    def __init__(self, controlador_principal, controlador_pais, controlador_cidade):
        super().__init__(controlador_principal)
        self._tela = TelaDestinosGUI()
        self._ctrl_pais = controlador_pais
        self._ctrl_cidade = controlador_cidade

    def abre_tela(self):
        while True:
            paises = self._ctrl_pais.get_entidades()
            cidades = self._ctrl_cidade.get_entidades()
            event = self._tela.le_opcao(paises, cidades)

            if event in ("-VOLTAR-", sg.WIN_CLOSED):
                break
            if event == "-GERENCIAR_PAISES-":
                self._ctrl_pais.abre_tela()
            elif event == "-GERENCIAR_CIDADES-":
                self._ctrl_cidade.abre_tela()
            else:
                self._tela.mostra_erro("Ação não reconhecida.")

