import uuid
from datetime import time
from models.cidade import Cidade
from models.pessoa import Pessoa


class PasseioTuristico:

    def __init__(
        self,
        atracao: str,
        inicio: time,
        fim: time,
        valor: float,
        cidade: Cidade,
        id: str = None,
    ):
        if not isinstance(atracao, str):
            raise TypeError("atracao deve ser uma string")
        if not isinstance(inicio, time):
            raise TypeError("inicio deve ser uma instância de time")
        if not isinstance(fim, time):
            raise TypeError("fim deve ser uma instância de time")
        if not isinstance(valor, (int, float)):
            raise TypeError("valor deve ser um número")
        if valor < 0:
            raise ValueError("valor não pode ser negativo")
        if not isinstance(cidade, Cidade):
            raise TypeError("cidade deve ser uma instância de Cidade")

        self.__id = id if id else str(uuid.uuid4())
        self.__atracao_turistica = atracao
        self.__horario_inicio = inicio
        self.__horario_fim = fim
        self.__valor = valor
        self.__cidade = cidade
        self.__participantes_passeio = []

    @property
    def id(self) -> str:
        return self.__id

    @property
    def atracao_turistica(self) -> str:
        return self.__atracao_turistica

    @atracao_turistica.setter
    def atracao_turistica(self, atracao: str):
        if not isinstance(atracao, str):
            raise TypeError("atracao deve ser uma string")
        self.__atracao_turistica = atracao

    @property
    def horario_inicio(self) -> time:
        return self.__horario_inicio

    @horario_inicio.setter
    def horario_inicio(self, inicio: time):
        if not isinstance(inicio, time):
            raise TypeError("inicio deve ser uma instância de time")
        self.__horario_inicio = inicio

    @property
    def horario_fim(self) -> time:
        return self.__horario_fim

    @horario_fim.setter
    def horario_fim(self, fim: time):
        if not isinstance(fim, time):
            raise TypeError("fim deve ser uma instância de time")
        self.__horario_fim = fim

    @property
    def valor(self) -> float:
        return self.__valor

    @valor.setter
    def valor(self, valor: float):
        if not isinstance(valor, (int, float)):
            raise TypeError("valor deve ser um número")
        if valor < 0:
            raise ValueError("valor não pode ser negativo")
        self.__valor = valor

    @property
    def cidade(self) -> Cidade:
        return self.__cidade

    @cidade.setter
    def cidade(self, cidade: Cidade):
        if not isinstance(cidade, Cidade):
            raise TypeError("cidade deve ser uma instância de Cidade")
        self.__cidade = cidade

    def incluir_participante(self, pessoa: Pessoa):
        if not isinstance(pessoa, Pessoa):
            raise TypeError("pessoa deve ser uma instância de Pessoa")
        if pessoa not in self.__participantes_passeio:
            self.__participantes_passeio.append(pessoa)

    def excluir_participante(self, pessoa: Pessoa):
        if not isinstance(pessoa, Pessoa):
            raise TypeError("pessoa deve ser uma instância de Pessoa")
        if pessoa in self.__participantes_passeio:
            self.__participantes_passeio.remove(pessoa)

    @property
    def participantes_passeio(self) -> list:
        return self.__participantes_passeio.copy()

    def __str__(self) -> str:
        return f"PasseioTuristico(atracao='{self.__atracao_turistica}', cidade='{self.__cidade.nome}', valor=R$ {self.__valor:.2f})"
