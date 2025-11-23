from models.trecho_viagem import TrechoViagem
from models.exceptions import EntidadeJaExisteException
from views.tela_trecho_viagem import TelaTrechoViagem
from controllers.controlador_entidade_base import ControladorEntidadeBase
from dao.dao_trecho_viagem import DAOTrechoViagem


class ControladorTrechoViagem(ControladorEntidadeBase):
    def __init__(self, controlador_principal, controlador_meio_transporte):
        super().__init__(controlador_principal)
        self._tela = TelaTrechoViagem()
        self._tela.set_controlador_meio_transporte(controlador_meio_transporte)
        self._dao = DAOTrechoViagem()
        self._entidades = self._dao.carregar()
        self._mapa_opcoes.update(
            {
                1: self.incluir,
                2: self.listar,
                3: self.excluir,
                4: self.editar,
            }
        )

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
            "id": trecho.id,
            "data": trecho.data,
            "local_origem": trecho.local_origem,
            "local_destino": trecho.local_destino,
            "meio_transporte": trecho.meio_transporte,
        }
