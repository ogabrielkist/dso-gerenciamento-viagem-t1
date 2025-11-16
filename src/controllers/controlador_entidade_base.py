import FreeSimpleGUI as sg
from abc import abstractmethod
from controllers.controlador_base import ControladorBase
from models.exceptions import (
    EntidadeJaExisteException,
    ListaVaziaException,
    EntidadeNaoEncontradaException,
)


class ControladorEntidadeBase(ControladorBase):

    def __init__(self, controlador_principal):
        super().__init__(controlador_principal)
        self._dao = None
        self._entidades = []
        self._tela = None

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

    def abre_tela(self):
        while True:
            event = self._tela.le_opcao()
            
            if event == '-INCLUIR-':
                self.incluir()
            elif event == '-LISTAR-':
                self.listar()
            elif event == '-EDITAR-':
                self.editar()
            elif event == '-EXCLUIR-':
                self.excluir()
            elif event == '-VOLTAR-' or event == sg.WIN_CLOSED:
                break

    def incluir(self):
        try:
            dados = self._tela.pega_dados_entidade()
            
            if dados:
                entidade = self._criar_entidade(dados)
                self._entidades.append(entidade)
                self._dao.salvar(self._entidades)

                self._tela.mostra_sucesso("Entidade incluída com sucesso!")

        except (EntidadeJaExisteException, ValueError) as e:
            self._tela.mostra_erro(str(e))
        except Exception as e:
            self._tela.mostra_erro(f"Erro inesperado ao incluir: {str(e)}")

    def listar(self):
        try:
            if not self._entidades:
                raise ListaVaziaException("Nenhuma entidade cadastrada.")

            dados_lista = [self._entidade_para_dict(e) for e in self._entidades]
            
            self._tela.mostra_lista_entidades(dados_lista)

        except ListaVaziaException as e:
            self._tela.mostra_mensagem("Aviso", str(e))

    def excluir(self):
        try:
            if not self._entidades:
                raise ListaVaziaException("Nenhuma entidade cadastrada.")

            dados_lista = [self._entidade_para_dict(e) for e in self._entidades]
            id_selecionado = self._tela.seleciona_entidade(dados_lista, "Excluir Entidade")

            if id_selecionado:
                entidade_encontrada = self._buscar_entidade(id_selecionado)
                
                if not entidade_encontrada:
                    raise EntidadeNaoEncontradaException("Entidade não encontrada.")

                self._entidades.remove(entidade_encontrada)
                self._dao.salvar(self._entidades)
                self._tela.mostra_sucesso("Entidade removida com sucesso!")

        except (ListaVaziaException, EntidadeNaoEncontradaException) as e:
            self._tela.mostra_erro(str(e))
        except Exception as e:
            self._tela.mostra_erro(f"Erro ao excluir: {str(e)}")

    def editar(self):
        try:
            if not self._entidades:
                raise ListaVaziaException("Nenhuma entidade cadastrada.")

            dados_lista = [self._entidade_para_dict(e) for e in self._entidades]
            id_selecionado = self._tela.seleciona_entidade(dados_lista, "Editar Entidade")

            if id_selecionado:
                entidade_encontrada = self._buscar_entidade(id_selecionado)
                
                if not entidade_encontrada:
                    raise EntidadeNaoEncontradaException("Entidade não encontrada.")

                dados_atuais = self._entidade_para_dict(entidade_encontrada)
                novos_dados = self._tela.pega_dados_entidade(dados_atuais)

                if novos_dados:
                    self._atualizar_entidade(entidade_encontrada, novos_dados)
                    self._dao.salvar(self._entidades)
                    self._tela.mostra_sucesso("Entidade editada com sucesso!")

        except (ListaVaziaException, EntidadeNaoEncontradaException, ValueError) as e:
            self._tela.mostra_erro(str(e))
        except Exception as e:
            self._tela.mostra_erro(f"Erro ao editar: {str(e)}")

    def get_entidades(self) -> list:
        """
        Retorna a lista de entidades gerenciadas (ex: países, pessoas).
        Usado por outras telas para preencher dropdowns.
        """
        return self._entidades