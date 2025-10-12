from models.meio_transporte import MeioTransporte, TipoTransporte
from models.empresa_transporte import EmpresaTransporte
from .dao_base import DAOBase
from .dao_empresa_transporte import DAOEmpresaTransporte


class DAOMeioTransporte(DAOBase):
    def __init__(self):
        super().__init__("meios_transporte.json")
        self.__dao_empresa = DAOEmpresaTransporte()

    def _serializar_entidade(self, meio_transporte):
        return {
            "id": meio_transporte.id,
            "tipo": meio_transporte.tipo.value,
            "empresa_id": meio_transporte.empresa.id,
        }

    def _deserializar_entidade(self, dados):
        empresas = self.__dao_empresa.carregar()
        empresa = next((e for e in empresas if e.id == dados["empresa_id"]), None)
        if not empresa:
            raise ValueError(f"Empresa com ID {dados['empresa_id']} não encontrada")
        tipo = TipoTransporte(dados["tipo"])
        return MeioTransporte(tipo, empresa, dados.get("id"))
