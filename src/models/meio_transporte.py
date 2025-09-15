from enum import Enum
from models.empresa_transporte import EmpresaTransporte


class TipoTransporte(Enum):
    AVIAO = "Avião"
    CARRO = "Carro"
    TREM = "Trem"
    ONIBUS = "Ônibus"


class MeioTransporte:

    def __init__(self, tipo: TipoTransporte, empresa: EmpresaTransporte):
        if not isinstance(tipo, TipoTransporte):
            raise TypeError("tipo deve ser uma instância de TipoTransporte")
        if not isinstance(empresa, EmpresaTransporte):
            raise TypeError("empresa deve ser uma instância de EmpresaTransporte")

        self.__tipo = tipo
        self.__empresa = empresa

    @property
    def tipo(self) -> TipoTransporte:
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo: TipoTransporte):
        if not isinstance(tipo, TipoTransporte):
            raise TypeError("tipo deve ser uma instância de TipoTransporte")
        self.__tipo = tipo

    @property
    def empresa(self) -> EmpresaTransporte:
        return self.__empresa

    @empresa.setter
    def empresa(self, empresa: EmpresaTransporte):
        if not isinstance(empresa, EmpresaTransporte):
            raise TypeError("empresa deve ser uma instância de EmpresaTransporte")
        self.__empresa = empresa

    def __str__(self) -> str:
        return f"MeioTransporte(tipo={self.__tipo.value}, empresa='{self.__empresa.nome if self.__empresa else 'N/A'}')"
