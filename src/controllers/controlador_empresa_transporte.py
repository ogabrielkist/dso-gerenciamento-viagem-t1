from models.empresa_transporte import EmpresaTransporte
from models.exceptions import EntidadeJaExisteException, EntidadeNaoEncontradaException
from views.tela_empresa_transporte_gui import TelaEmpresaTransporteGUI
from controllers.controlador_entidade_base import ControladorEntidadeBase
from dao.dao_empresa_transporte import DAOEmpresaTransporte


class ControladorEmpresaTransporte(ControladorEntidadeBase):
    def __init__(self, controlador_principal):
        super().__init__(controlador_principal)
        self._tela = TelaEmpresaTransporteGUI()
        self._dao = DAOEmpresaTransporte()
        self._entidades = self._dao.carregar()

    def _criar_entidade(self, dados):
        for empresa in self._entidades:
            if empresa.cnpj == dados["cnpj"]:
                raise EntidadeJaExisteException("Empresa com esse CNPJ já cadastrada.")

        return EmpresaTransporte(
            dados["nome"],
            dados["cnpj"],
            dados["telefone"],
        )

    def _atualizar_entidade(self, empresa, dados):
        for e in self._entidades:
            if e != empresa and e.cnpj == dados["cnpj"]:
                raise EntidadeJaExisteException("Empresa com esse CNPJ já cadastrada.")

        empresa.nome = dados["nome"]
        empresa.cnpj = dados["cnpj"]
        empresa.telefone = dados["telefone"]

    def _entidade_para_dict(self, empresa):
        return {
            "id": empresa.id,
            "nome": empresa.nome,
            "cnpj": empresa.cnpj,
            "telefone": empresa.telefone,
        }
