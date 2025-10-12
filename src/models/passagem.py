import uuid
from models.pessoa import Pessoa
from models.trecho_viagem import TrechoViagem


class Passagem:

    def __init__(
        self,
        passageiro: Pessoa,
        trecho: TrechoViagem,
        responsavel: Pessoa,
        id: str = None,
    ):
        if not isinstance(passageiro, Pessoa):
            raise TypeError("passageiro deve ser uma instância de Pessoa")
        if not isinstance(trecho, TrechoViagem):
            raise TypeError("trecho deve ser uma instância de TrechoViagem")
        if not isinstance(responsavel, Pessoa):
            raise TypeError("responsavel deve ser uma instância de Pessoa")

        self.__id = id if id else str(uuid.uuid4())
        self.__compra_efetuada = False
        self.__passageiro = passageiro
        self.__trecho = trecho
        self.__responsavel_compra = responsavel

    @property
    def id(self) -> str:
        return self.__id

    @property
    def compra_efetuada(self) -> bool:
        return self.__compra_efetuada

    @compra_efetuada.setter
    def compra_efetuada(self, status: bool):
        if not isinstance(status, bool):
            raise TypeError("status deve ser um booleano")
        self.__compra_efetuada = status

    @property
    def passageiro(self) -> Pessoa:
        return self.__passageiro

    @passageiro.setter
    def passageiro(self, pessoa: Pessoa):
        if not isinstance(pessoa, Pessoa):
            raise TypeError("pessoa deve ser uma instância de Pessoa")
        self.__passageiro = pessoa

    @property
    def trecho(self) -> TrechoViagem:
        return self.__trecho

    @trecho.setter
    def trecho(self, trecho: TrechoViagem):
        if not isinstance(trecho, TrechoViagem):
            raise TypeError("trecho deve ser uma instância de TrechoViagem")
        self.__trecho = trecho

    @property
    def responsavel_compra(self) -> Pessoa:
        return self.__responsavel_compra

    @responsavel_compra.setter
    def responsavel_compra(self, pessoa: Pessoa):
        if not isinstance(pessoa, Pessoa):
            raise TypeError("pessoa deve ser uma instância de Pessoa")
        self.__responsavel_compra = pessoa

    def __str__(self) -> str:
        status = "Comprada" if self.__compra_efetuada else "Pendente"
        return f"Passagem(passageiro='{self.__passageiro.nome}', status={status}, responsavel='{self.__responsavel_compra.nome}')"
