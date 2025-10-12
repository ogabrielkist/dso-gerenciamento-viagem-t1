import uuid


class EmpresaTransporte:

    def __init__(self, nome: str, cnpj: str, telefone: str, id: str = None):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser uma string")
        if not isinstance(cnpj, str):
            raise TypeError("cnpj deve ser uma string")
        if not isinstance(telefone, str):
            raise TypeError("telefone deve ser uma string")

        self.__id = id if id else str(uuid.uuid4())
        self.__nome = nome
        self.__cnpj = cnpj
        self.__telefone = telefone

    @property
    def id(self) -> str:
        return self.__id

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser uma string")
        self.__nome = nome

    @property
    def cnpj(self) -> str:
        return self.__cnpj

    @cnpj.setter
    def cnpj(self, cnpj: str):
        if not isinstance(cnpj, str):
            raise TypeError("cnpj deve ser uma string")
        self.__cnpj = cnpj

    @property
    def telefone(self) -> str:
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone: str):
        if not isinstance(telefone, str):
            raise TypeError("telefone deve ser uma string")
        self.__telefone = telefone

    def __str__(self) -> str:
        return f"EmpresaTransporte(nome='{self.__nome}', cnpj='{self.__cnpj}')"
