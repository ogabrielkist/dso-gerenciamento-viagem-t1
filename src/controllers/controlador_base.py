from abc import ABC, abstractmethod
from models.exceptions import (
    EntidadeJaExisteException,
    EntidadeNaoEncontradaException,
    ListaVaziaException,
    OpcaoInvalidaException,
)


class ControladorBase(ABC):
    def __init__(self, controlador_principal):
        self.__controlador_principal = controlador_principal
        self._entidades = []
        self._tela = None
        self._mapa_opcoes = {}

    def incluir(self):
        try:
            dados = self._tela.pega_dados_entidade()
            entidade = self._criar_entidade(dados)
            self._entidades.append(entidade)
            self._tela.mostra_sucesso("Entidade incluída com sucesso!")
        except EntidadeJaExisteException as e:
            self._tela.mostra_erro(str(e))
        except Exception as e:
            self._tela.mostra_erro(f"Erro ao incluir: {str(e)}")

    def listar(self):
        try:
            if not self._entidades:
                raise ListaVaziaException("Nenhuma entidade cadastrada.")

            self._tela.limpar_tela()
            for entidade in self._entidades:
                dados = self._entidade_para_dict(entidade)
                self._tela.mostra_entidade(dados)

            self._tela.aguardar_enter()
            self._tela.limpar_tela()
        except ListaVaziaException as e:
            self._tela.mostra_erro(str(e))

    def excluir(self):
        try:
            if not self._entidades:
                raise ListaVaziaException("Nenhuma entidade cadastrada.")

            self._tela.limpar_tela()
            for entidade in self._entidades:
                dados = self._entidade_para_dict(entidade)
                self._tela.mostra_entidade(dados)

            identificador = self._tela.seleciona_entidade()
            entidade_encontrada = self._buscar_entidade(identificador)

            if not entidade_encontrada:
                raise EntidadeNaoEncontradaException("Entidade não encontrada.")

            self._entidades.remove(entidade_encontrada)
            self._tela.mostra_sucesso("Entidade removida com sucesso!")
        except ListaVaziaException as e:
            self._tela.mostra_erro(str(e))
        except EntidadeNaoEncontradaException as e:
            self._tela.mostra_erro(str(e))
        except Exception as e:
            self._tela.mostra_erro(f"Erro ao excluir: {str(e)}")

    def editar(self):
        try:
            if not self._entidades:
                raise ListaVaziaException("Nenhuma entidade cadastrada.")

            self._tela.limpar_tela()
            for entidade in self._entidades:
                dados = self._entidade_para_dict(entidade)
                self._tela.mostra_entidade(dados)

            identificador = self._tela.seleciona_entidade()
            entidade_encontrada = self._buscar_entidade(identificador)

            if not entidade_encontrada:
                raise EntidadeNaoEncontradaException("Entidade não encontrada.")

            dados_atuais = self._entidade_para_dict(entidade_encontrada)
            dados = self._tela.pega_dados_entidade(dados_atuais)
            self._atualizar_entidade(entidade_encontrada, dados)
            self._tela.mostra_sucesso("Entidade editada com sucesso!")
        except ListaVaziaException as e:
            self._tela.mostra_erro(str(e))
        except EntidadeNaoEncontradaException as e:
            self._tela.mostra_erro(str(e))
        except Exception as e:
            self._tela.mostra_erro(f"Erro ao editar: {str(e)}")

    def retornar(self):
        self.__controlador_principal.abre_tela()

    def abre_tela(self):
        while True:
            try:
                opcao_escolhida = self._tela.le_opcao()

                if opcao_escolhida == 0:
                    self.retornar()
                    break

                funcao_escolhida = self._mapa_opcoes.get(opcao_escolhida)
                if not funcao_escolhida:
                    raise OpcaoInvalidaException("Opção inválida!")

                funcao_escolhida()

            except OpcaoInvalidaException as e:
                self._tela.mostra_erro(str(e))
            except Exception as e:
                self._tela.mostra_erro(f"Erro inesperado: {str(e)}")

    def _buscar_entidade(self, identificador):
        for entidade in self._entidades:
            if self._obter_identificador(entidade) == identificador:
                return entidade
        return None

    @abstractmethod
    def _criar_entidade(self, dados):
        pass

    @abstractmethod
    def _atualizar_entidade(self, entidade, dados):
        pass

    @abstractmethod
    def _entidade_para_dict(self, entidade):
        pass

    def _obter_identificador(self, entidade):
        return entidade.id
