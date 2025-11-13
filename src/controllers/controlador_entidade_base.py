from abc import abstractmethod
from controllers.controlador_base import ControladorBase
from models.exceptions import EntidadeJaExisteException, EntidadeNaoEncontradaException, ListaVaziaException

class ControladorEntidadeBase(ControladorBase):
    """
    Classe base abstrata para controladores que gerenciam
    o CRUD de uma entidade (Pessoa, Viagem, etc.)
    """
    def __init__(self, controlador_principal):
        super().__init__(controlador_principal)
        self._dao = None
        self._entidades = []

    @abstractmethod
    def _criar_entidade(self, dados):
        raise NotImplementedError

    @abstractmethod
    def _atualizar_entidade(self, entidade, dados):
        raise NotImplementedError

    @abstractmethod
    def _entidade_para_dict(self, entidade):
        raise NotImplementedError

    def _obter_identificador(self, entidade):
        return entidade.id

    def _buscar_entidade(self, identificador):
        for entidade in self._entidades:
            if str(self._obter_identificador(entidade)) == str(identificador):
                return entidade

        return None

    def incluir(self):
        try:
            dados = self._tela.pega_dados_entidade()
            entidade = self._criar_entidade(dados)
            self._entidades.append(entidade)
            self._dao.salvar(self._entidades)
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
            # self._dao.salvar(self._entidades)
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
            # self._dao.salvar(self._entidades)
            self._tela.mostra_sucesso("Entidade editada com sucesso!")
        except ListaVaziaException as e:
            self._tela.mostra_erro(str(e))
        except EntidadeNaoEncontradaException as e:
            self._tela.mostra_erro(str(e))
        except Exception as e:
            self._tela.mostra_erro(f"Erro ao editar: {str(e)}")
