from abc import ABC, abstractmethod


class ControladorBase(ABC):
    
    def __init__(self, controlador_principal):
        """
        Armazena a referência ao controlador principal.
        """
        self._controlador_principal = controlador_principal

    @abstractmethod
    def abre_tela(self):
        raise NotImplementedError
