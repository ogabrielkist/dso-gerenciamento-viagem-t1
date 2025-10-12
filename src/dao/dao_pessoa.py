from models.pessoa import Pessoa
from .dao_base import DAOBase


class DAOPessoa(DAOBase):
    def __init__(self):
        super().__init__("pessoas.json")

    def _serializar_entidade(self, pessoa):
        return {
            "id": pessoa.id,
            "nome": pessoa.nome,
            "celular": pessoa.celular,
            "identificacao": pessoa.identificacao,
            "idade": pessoa.idade,
        }

    def _deserializar_entidade(self, dados):
        return Pessoa(
            dados["nome"],
            dados["celular"],
            dados["identificacao"],
            dados["idade"],
            dados.get("id"),
        )
