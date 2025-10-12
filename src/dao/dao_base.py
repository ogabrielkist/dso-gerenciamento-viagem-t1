import json
import os
from abc import ABC, abstractmethod


class DAOBase(ABC):
    def __init__(self, arquivo):
        self.__arquivo = f"database/{arquivo}"
        self._criar_diretorio_se_nao_existir()

    def _criar_diretorio_se_nao_existir(self):
        diretorio = os.path.dirname(self.__arquivo)
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)

    def carregar(self):
        try:
            if os.path.exists(self.__arquivo):
                with open(self.__arquivo, "r", encoding="utf-8") as arquivo:
                    dados = json.load(arquivo)
                    return [self._deserializar_entidade(item) for item in dados]
            return []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def salvar(self, entidades):
        try:
            dados = [self._serializar_entidade(entidade) for entidade in entidades]
            with open(self.__arquivo, "w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False, indent=2)
        except Exception as e:
            raise Exception(f"Erro ao salvar dados: {str(e)}")

    @abstractmethod
    def _serializar_entidade(self, entidade):
        pass

    @abstractmethod
    def _deserializar_entidade(self, dados):
        pass
