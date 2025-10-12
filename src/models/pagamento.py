import uuid
from abc import ABC, abstractmethod
from datetime import date
from models.pessoa import Pessoa


class Pagamento(ABC):

    def __init__(
        self, data: date, valor: float, pagador: Pessoa, viagem, id: str = None
    ):
        from models.viagem import Viagem

        if not isinstance(data, date):
            raise TypeError("data deve ser uma instância de date")
        if not isinstance(valor, (int, float)):
            raise TypeError("valor deve ser um número")
        if valor < 0:
            raise ValueError("valor não pode ser negativo")
        if not isinstance(pagador, Pessoa):
            raise TypeError("pagador deve ser uma instância de Pessoa")
        if not isinstance(viagem, Viagem):
            raise TypeError("viagem deve ser uma instância de Viagem")

        self.__id = id if id else str(uuid.uuid4())
        self.__data = data
        self.__valor_pago = valor
        self.__pagador = pagador
        self.__viagem = viagem

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

    @property
    def valor_pago(self) -> float:
        return self.__valor_pago

    @valor_pago.setter
    def valor_pago(self, valor: float):
        if not isinstance(valor, (int, float)):
            raise TypeError("valor deve ser um número")
        if valor < 0:
            raise ValueError("valor não pode ser negativo")
        self.__valor_pago = valor

    @property
    def pagador(self) -> Pessoa:
        return self.__pagador

    @pagador.setter
    def pagador(self, pessoa: Pessoa):
        if not isinstance(pessoa, Pessoa):
            raise TypeError("pessoa deve ser uma instância de Pessoa")
        self.__pagador = pessoa

    @property
    def viagem(self):
        return self.__viagem

    @viagem.setter
    def viagem(self, viagem):
        from models.viagem import Viagem

        if not isinstance(viagem, Viagem):
            raise TypeError("viagem deve ser uma instância de Viagem")
        self.__viagem = viagem

    def __str__(self) -> str:
        return f"Pagamento(data={self.__data}, valor=R$ {self.__valor_pago:.2f}, pagador='{self.__pagador.nome}')"


class PagamentoDinheiro(Pagamento):

    def __init__(
        self, data: date, valor: float, pagador: Pessoa, viagem, id: str = None
    ):
        super().__init__(data, valor, pagador, viagem, id)

    def __str__(self) -> str:
        return f"PagamentoDinheiro(data={self.data}, valor=R$ {self.valor_pago:.2f}, pagador='{self.pagador.nome}')"


class PagamentoPix(Pagamento):

    def __init__(
        self,
        data: date,
        valor: float,
        pagador: Pessoa,
        viagem,
        cpf: str,
        id: str = None,
    ):
        super().__init__(data, valor, pagador, viagem, id)
        if not isinstance(cpf, str):
            raise TypeError("cpf deve ser uma string")
        self.__cpf_pagador = cpf

    @property
    def cpf_pagador(self) -> str:
        return self.__cpf_pagador

    @cpf_pagador.setter
    def cpf_pagador(self, cpf: str):
        if not isinstance(cpf, str):
            raise TypeError("cpf deve ser uma string")
        self.__cpf_pagador = cpf

    def __str__(self) -> str:
        return f"PagamentoPix(data={self.data}, valor=R$ {self.valor_pago:.2f}, pagador='{self.pagador.nome}', cpf='{self.cpf_pagador}')"


class PagamentoCartao(Pagamento):

    def __init__(
        self,
        data: date,
        valor: float,
        pagador: Pessoa,
        viagem,
        numero: str,
        bandeira: str,
        id: str = None,
    ):
        super().__init__(data, valor, pagador, viagem, id)
        if not isinstance(numero, str):
            raise TypeError("numero deve ser uma string")
        if not isinstance(bandeira, str):
            raise TypeError("bandeira deve ser uma string")
        self.__numero_cartao = numero
        self.__bandeira = bandeira

    @property
    def numero_cartao(self) -> str:
        return self.__numero_cartao

    @numero_cartao.setter
    def numero_cartao(self, numero: str):
        if not isinstance(numero, str):
            raise TypeError("numero deve ser uma string")
        self.__numero_cartao = numero

    @property
    def bandeira(self) -> str:
        return self.__bandeira

    @bandeira.setter
    def bandeira(self, bandeira: str):
        if not isinstance(bandeira, str):
            raise TypeError("bandeira deve ser uma string")
        self.__bandeira = bandeira

    def __str__(self) -> str:
        return f"PagamentoCartao(data={self.data}, valor=R$ {self.valor_pago:.2f}, pagador='{self.pagador.nome}', bandeira='{self.bandeira}')"
