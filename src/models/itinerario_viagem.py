import uuid
from datetime import date
from models.passeio_turistico import PasseioTuristico


class ItinerarioViagem:

    def __init__(self, data: date, id: str = None):
        if not isinstance(data, date):
            raise TypeError("data deve ser uma instância de date")
        self.__id = id if id else str(uuid.uuid4())
        self.__data = data
        self.__passeios = []

    @property
    def id(self) -> str:
        return self.__id

    @property
    def data(self) -> date:
        return self.__data

    @data.setter
    def data(self, data: date):
        if not isinstance(data, date):
            raise TypeError("data deve ser uma instância de date")
        self.__data = data

    def incluir_passeio(self, passeio: PasseioTuristico):
        if not isinstance(passeio, PasseioTuristico):
            raise TypeError("passeio deve ser uma instância de PasseioTuristico")
        if passeio not in self.__passeios:
            self.__passeios.append(passeio)

    def excluir_passeio(self, passeio: PasseioTuristico):
        if not isinstance(passeio, PasseioTuristico):
            raise TypeError("passeio deve ser uma instância de PasseioTuristico")
        if passeio in self.__passeios:
            self.__passeios.remove(passeio)

    @property
    def passeios(self) -> list:
        return self.__passeios.copy()

    def __str__(self) -> str:
        return f"ItinerarioViagem(data={self.__data}, {len(self.__passeios)} passeios)"
