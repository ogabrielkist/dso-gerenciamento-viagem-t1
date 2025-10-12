from datetime import date
from models.viagem import Viagem
from .dao_base import DAOBase


class DAOViagem(DAOBase):
    def __init__(self):
        super().__init__("viagens.json")

    def _serializar_entidade(self, viagem):
        return {
            "id": viagem.id,
            "data_inicio": viagem.data_inicio.isoformat(),
            "data_fim": viagem.data_fim.isoformat(),
            "valor_total_pacote": viagem.valor_total_pacote,
        }

    def _deserializar_entidade(self, dados):
        return Viagem(
            date.fromisoformat(dados["data_inicio"]),
            date.fromisoformat(dados["data_fim"]),
            dados["valor_total_pacote"],
            dados.get("id"),
        )
