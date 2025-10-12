import uuid


class Pais:

    def __init__(self, nome: str, id: str = None):
        self.__id = id if id else str(uuid.uuid4())
        self.__nome = nome
        self.__cidades = []

    @property
    def id(self) -> str:
        return self.__id

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    def incluir_cidade(self, cidade):
        from models.cidade import Cidade

        if not isinstance(cidade, Cidade):
            raise TypeError("cidade deve ser uma instância de Cidade")
        if cidade not in self.__cidades:
            self.__cidades.append(cidade)

    def excluir_cidade(self, cidade):
        from models.cidade import Cidade

        if not isinstance(cidade, Cidade):
            raise TypeError("cidade deve ser uma instância de Cidade")
        if cidade in self.__cidades:
            self.__cidades.remove(cidade)

    @property
    def cidades(self) -> list:
        return self.__cidades.copy()

    def __str__(self) -> str:
        return f"Pais(nome='{self.__nome}', cidades={len(self.__cidades)})"
