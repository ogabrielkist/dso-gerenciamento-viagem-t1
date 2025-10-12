from models.cidade import Cidade
from models.pais import Pais
from .dao_base import DAOBase
from .dao_pais import DAOPais


class DAOCidade(DAOBase):
    def __init__(self):
        super().__init__("cidades.json")
        self.__dao_pais = DAOPais()

    def _serializar_entidade(self, cidade):
        return {
            "id": cidade.id,
            "nome": cidade.nome,
            "pais_id": cidade.pais.id,
        }

    def _deserializar_entidade(self, dados):
        paises = self.__dao_pais.carregar()
        pais = next((p for p in paises if p.id == dados["pais_id"]), None)
        if not pais:
            raise ValueError(f"País com ID {dados['pais_id']} não encontrado")
        return Cidade(dados["nome"], pais, dados.get("id"))
