import FreeSimpleGUI as sg
from abc import ABC 


class TelaBaseGUI(ABC):
    def __init__(self):
        sg.theme('LightBrown6') 
        sg.set_options(font=('Bookman Old Style', 12))

    def mostra_erro(self, mensagem):
        """
        Exibe um popup de erro.
        """
        sg.popup_error("ERRO", mensagem)
        
    def mostra_sucesso(self, mensagem):
        """
        Exibe um popup de sucesso.
        """
        sg.popup_ok("Sucesso", mensagem)
    
    def mostra_mensagem(self, titulo, mensagem):
        """
        Exibe um popup genérico.
        """
        sg.popup(titulo, mensagem)
        
    def aguardar_confirmacao(self, titulo, mensagem):
        """
        Exibe um popup modal que apenas aguarda o OK.
        """
        sg.popup_ok(titulo, mensagem)
