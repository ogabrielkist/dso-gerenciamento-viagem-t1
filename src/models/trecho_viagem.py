import uuid
from datetime import datetime
from models.meio_transporte import MeioTransporte


class TrechoViagem:

    def __init__(
        self,
        data: datetime,
        origem: str,
        destino: str,
        transporte: MeioTransporte,
        id: str = None,
    ):
        if not isinstance(data, datetime):
            raise TypeError("data deve ser uma instância de datetime")
        if not isinstance(origem, str):
            raise TypeError("origem deve ser uma string")
        if not isinstance(destino, str):
            raise TypeError("destino deve ser uma string")
        if not isinstance(transporte, MeioTransporte):
            raise TypeError("transporte deve ser uma instância de MeioTransporte")

        self.__id = id if id else str(uuid.uuid4())
        self.__data = data
        self.__local_origem = origem
        self.__local_destino = destino
        self.__meio_transporte = transporte

    @property
    def id(self) -> str:
        return self.__id

    @property
    def data(self) -> datetime:
        return self.__data

    @data.setter
    def data(self, data: datetime):
        if not isinstance(data, datetime):
            raise TypeError("data deve ser uma instância de datetime")
        self.__data = data

    @property
    def local_origem(self) -> str:
        return self.__local_origem

    @local_origem.setter
    def local_origem(self, origem: str):
        if not isinstance(origem, str):
            raise TypeError("origem deve ser uma string")
        self.__local_origem = origem

    @property
    def local_destino(self) -> str:
        return self.__local_destino

    @local_destino.setter
    def local_destino(self, destino: str):
        if not isinstance(destino, str):
            raise TypeError("destino deve ser uma string")
        self.__local_destino = destino

    @property
    def meio_transporte(self) -> MeioTransporte:
        return self.__meio_transporte

    @meio_transporte.setter
    def meio_transporte(self, transporte: MeioTransporte):
        if not isinstance(transporte, MeioTransporte):
            raise TypeError("transporte deve ser uma instância de MeioTransporte")
        self.__meio_transporte = transporte

    def __str__(self) -> str:
        return f"TrechoViagem({self.__local_origem} -> {self.__local_destino}, {self.__data.strftime('%d/%m/%Y %H:%M')})"
