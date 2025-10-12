from datetime import datetime
from models.trecho_viagem import TrechoViagem
from models.exceptions import EntidadeJaExisteException, EntidadeNaoEncontradaException
from views.tela_trecho_viagem import TelaTrechoViagem
from controllers.controlador_base import ControladorBase
from dao.dao_trecho_viagem import DAOTrechoViagem


class ControladorTrechoViagem(ControladorBase):
    def __init__(self, controlador_principal, controlador_meio_transporte):
        super().__init__(controlador_principal)
        self._tela = TelaTrechoViagem()
        self._tela.set_controlador_meio_transporte(controlador_meio_transporte)
        self._dao = DAOTrechoViagem()
        self._entidades = self._dao.carregar()
        self._mapa_opcoes = {
            1: self.incluir,
            2: self.listar,
            3: self.excluir,
            4: self.editar,
        }

    def _criar_entidade(self, dados):
        for trecho in self._entidades:
            if (
                trecho.data == dados["data"]
                and trecho.local_origem.lower() == dados["local_origem"].lower()
                and trecho.local_destino.lower() == dados["local_destino"].lower()
                and trecho.meio_transporte.id == dados["meio_transporte"].id
            ):
                raise EntidadeJaExisteException(
                    "Trecho de viagem com essas características já cadastrado."
                )

        return TrechoViagem(
            dados["data"],
            dados["local_origem"],
            dados["local_destino"],
            dados["meio_transporte"],
        )

    def _atualizar_entidade(self, trecho, dados):
        for t in self._entidades:
            if (
                t != trecho
                and t.data == dados["data"]
                and t.local_origem.lower() == dados["local_origem"].lower()
                and t.local_destino.lower() == dados["local_destino"].lower()
                and t.meio_transporte.id == dados["meio_transporte"].id
            ):
                raise EntidadeJaExisteException(
                    "Trecho de viagem com essas características já cadastrado."
                )

        trecho.data = dados["data"]
        trecho.local_origem = dados["local_origem"]
        trecho.local_destino = dados["local_destino"]
        trecho.meio_transporte = dados["meio_transporte"]

    def _entidade_para_dict(self, trecho):
        return {
            "data": trecho.data,
            "local_origem": trecho.local_origem,
            "local_destino": trecho.local_destino,
            "meio_transporte": trecho.meio_transporte,
        }

    def incluir(self):
        try:
            super().incluir()
            self._dao.salvar(self._entidades)
        except Exception as e:
            self._tela.mostra_erro(str(e))

    def excluir(self):
        try:
            self.listar()
            if not self._entidades:
                return

            identificador = self._tela.seleciona_entidade()
            data_str, origem, destino = identificador.split("|")
            data = datetime.fromisoformat(data_str)

            entidade_encontrada = None
            for entidade in self._entidades:
                if (
                    entidade.data == data
                    and entidade.local_origem.lower() == origem.lower()
                    and entidade.local_destino.lower() == destino.lower()
                ):
                    entidade_encontrada = entidade
                    break

            if not entidade_encontrada:
                raise EntidadeNaoEncontradaException("Trecho de viagem não encontrado.")

            self._entidades.remove(entidade_encontrada)
            self._dao.salvar(self._entidades)
            self._tela.mostra_sucesso("Trecho de viagem removido com sucesso!")
        except Exception as e:
            self._tela.mostra_erro(str(e))

    def editar(self):
        try:
            self.listar()
            if not self._entidades:
                return

            identificador = self._tela.seleciona_entidade()
            data_str, origem, destino = identificador.split("|")
            data = datetime.fromisoformat(data_str)

            entidade_encontrada = None
            for entidade in self._entidades:
                if (
                    entidade.data == data
                    and entidade.local_origem.lower() == origem.lower()
                    and entidade.local_destino.lower() == destino.lower()
                ):
                    entidade_encontrada = entidade
                    break

            if not entidade_encontrada:
                raise EntidadeNaoEncontradaException("Trecho de viagem não encontrado.")

            dados_novos = self._tela.pega_dados_entidade()
            self._atualizar_entidade(entidade_encontrada, dados_novos)
            self._dao.salvar(self._entidades)
            self._tela.mostra_sucesso("Trecho de viagem editado com sucesso!")
        except Exception as e:
            self._tela.mostra_erro(str(e))
