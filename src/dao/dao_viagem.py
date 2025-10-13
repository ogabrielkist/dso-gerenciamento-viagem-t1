from datetime import date
from models.viagem import Viagem
from .dao_base import DAOBase
from .dao_itinerario_viagem import DAOItinerarioViagem


class DAOViagem(DAOBase):
    def __init__(self):
        super().__init__("viagens.json")
        self.__dao_itinerario = DAOItinerarioViagem()

    def _serializar_entidade(self, viagem):
        return {
            "id": viagem.id,
            "data_inicio": viagem.data_inicio.isoformat(),
            "data_fim": viagem.data_fim.isoformat(),
            "valor_total_pacote": viagem.valor_total_pacote,
        }

    def _deserializar_entidade(self, dados):
        viagem = Viagem(
            date.fromisoformat(dados["data_inicio"]),
            date.fromisoformat(dados["data_fim"]),
            dados["valor_total_pacote"],
            dados.get("id"),
        )

        itinerarios = self.__dao_itinerario.carregar()
        for itinerario in itinerarios:
            if self._itinerario_pertence_a_viagem(itinerario, viagem):
                viagem.incluir_itinerario(itinerario)

        return viagem

    def _itinerario_pertence_a_viagem(self, itinerario, viagem):
        return viagem.data_inicio <= itinerario.data <= viagem.data_fim
