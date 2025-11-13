from abc import ABC, abstractmethod


class ControladorBase(ABC):
    def __init__(self, controlador_principal):
        self._controlador_principal = controlador_principal
        self._tela = None
        self._mapa_opcoes = {}

    def le_opcao(self):
        """
        Lê a opção da tela. Este método deve ser implementado pela tela específica.
        """
        return self._tela.le_opcao()

    def abre_tela(self):
        """
        Loop principal do controlador. Lê a opção da tela e
        executa a função correspondente do _mapa_opcoes.
        """
        while True:
            try:
                opcao = self.le_opcao()
                if opcao == 0:
                    break
                
                funcao_escolhida = self._mapa_opcoes.get(opcao)
                if funcao_escolhida:
                    funcao_escolhida()
                else:
                    self._tela.mostra_erro("Opção inválida, tente novamente.")
            
            except Exception as e:
                self._tela.mostra_erro(f"Ocorreu um erro: {e}")
