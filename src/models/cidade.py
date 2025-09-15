from models.pais import Pais


class Cidade:

    def __init__(self, nome: str, pais: Pais):
        if not isinstance(pais, Pais):
            raise TypeError("pais deve ser uma instância de Pais")
        self.__nome = nome
        self.__pais = pais
        pais.incluir_cidade(self)

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def pais(self) -> Pais:
        return self.__pais

    @pais.setter
    def pais(self, pais: Pais):
        if pais is not None and not isinstance(pais, Pais):
            raise TypeError("pais deve ser uma instância de Pais")
        if self.__pais:
            self.__pais.excluir_cidade(self)

        self.__pais = pais
        if pais:
            pais.incluir_cidade(self)

    def __str__(self) -> str:
        return f"Cidade(nome='{self.__nome}', pais='{self.__pais.nome if self.__pais else 'N/A'}')"
