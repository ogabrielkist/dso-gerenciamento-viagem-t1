from models.empresa_transporte import EmpresaTransporte
from .dao_base import DAOBase


class DAOEmpresaTransporte(DAOBase):
    def __init__(self):
        super().__init__("empresas_transporte.json")

    def _serializar_entidade(self, empresa):
        return {
            "id": empresa.id,
            "nome": empresa.nome,
            "cnpj": empresa.cnpj,
            "telefone": empresa.telefone,
        }

    def _deserializar_entidade(self, dados):
        return EmpresaTransporte(
            dados["nome"],
            dados["cnpj"],
            dados["telefone"],
            dados.get("id"),
        )
