from datetime import datetime
from models.trecho_viagem import TrechoViagem
from models.meio_transporte import MeioTransporte
from .dao_base import DAOBase
from .dao_meio_transporte import DAOMeioTransporte


class DAOTrechoViagem(DAOBase):
    def __init__(self):
        super().__init__("trechos_viagem.json")
        self.__dao_meio_transporte = DAOMeioTransporte()

    def _serializar_entidade(self, trecho):
        return {
            "id": trecho.id,
            "data": trecho.data.isoformat(),
            "local_origem": trecho.local_origem,
            "local_destino": trecho.local_destino,
            "meio_transporte_id": trecho.meio_transporte.id,
        }

    def _deserializar_entidade(self, dados):
        meios_transporte = self.__dao_meio_transporte.carregar()
        meio_transporte = next(
            (m for m in meios_transporte if m.id == dados["meio_transporte_id"]), None
        )
        if not meio_transporte:
            raise ValueError(
                f"Meio de transporte com ID {dados['meio_transporte_id']} não encontrado"
            )
        return TrechoViagem(
            datetime.fromisoformat(dados["data"]),
            dados["local_origem"],
            dados["local_destino"],
            meio_transporte,
            dados.get("id"),
        )
