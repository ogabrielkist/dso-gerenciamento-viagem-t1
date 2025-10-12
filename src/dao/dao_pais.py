from models.pais import Pais
from .dao_base import DAOBase


class DAOPais(DAOBase):
    def __init__(self):
        super().__init__("paises.json")

    def _serializar_entidade(self, pais):
        return {
            "id": pais.id,
            "nome": pais.nome,
        }

    def _deserializar_entidade(self, dados):
        return Pais(dados["nome"], dados.get("id"))
