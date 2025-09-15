from datetime import date


class Pessoa:

    def __init__(self, nome: str, celular: str, identificacao: str, idade: int):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser uma string")
        if not isinstance(celular, str):
            raise TypeError("celular deve ser uma string")
        if not isinstance(identificacao, str):
            raise TypeError("identificacao deve ser uma string")
        if not isinstance(idade, int):
            raise TypeError("idade deve ser um inteiro")
        if idade < 0:
            raise ValueError("idade não pode ser negativa")

        self.__nome = nome
        self.__celular = celular
        self.__identificacao = identificacao
        self.__idade = idade

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if not isinstance(nome, str):
            raise TypeError("nome deve ser uma string")
        self.__nome = nome

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, celular: str):
        if not isinstance(celular, str):
            raise TypeError("celular deve ser uma string")
        self.__celular = celular

    @property
    def identificacao(self) -> str:
        return self.__identificacao

    @identificacao.setter
    def identificacao(self, identificacao: str):
        if not isinstance(identificacao, str):
            raise TypeError("identificacao deve ser uma string")
        self.__identificacao = identificacao

    @property
    def idade(self) -> int:
        return self.__idade

    @idade.setter
    def idade(self, idade: int):
        if not isinstance(idade, int):
            raise TypeError("idade deve ser um inteiro")
        if idade < 0:
            raise ValueError("idade não pode ser negativa")
        self.__idade = idade

    def pode_participar_viagem(self) -> bool:
        return self.__idade >= 18

    def __str__(self) -> str:
        return f"Pessoa(nome='{self.__nome}', idade={self.__idade}, pode_participar={self.pode_participar_viagem()})"
