from datetime import date, time
from models.itinerario_viagem import ItinerarioViagem
from models.passeio_turistico import PasseioTuristico
from .dao_base import DAOBase
from .dao_passeio_turistico import DAOPasseioTuristico


class DAOItinerarioViagem(DAOBase):
    def __init__(self):
        super().__init__("itinerarios_viagem.json")
        self.__dao_passeio = DAOPasseioTuristico()

    def _serializar_entidade(self, itinerario):
        return {
            "id": itinerario.id,
            "data": itinerario.data.isoformat(),
            "passeios_ids": [p.id for p in itinerario.passeios],
        }

    def _deserializar_entidade(self, dados):
        itinerario = ItinerarioViagem(
            date.fromisoformat(dados["data"]),
            dados.get("id"),
        )

        passeios = self.__dao_passeio.carregar()
        for passeio_id in dados.get("passeios_ids", []):
            passeio = next((p for p in passeios if p.id == passeio_id), None)
            if passeio:
                itinerario.incluir_passeio(passeio)

        return itinerario
