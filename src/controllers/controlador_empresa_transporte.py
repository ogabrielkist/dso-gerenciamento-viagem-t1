from models.empresa_transporte import EmpresaTransporte
from models.exceptions import (
    CNPJInvalidoException,
    EntidadeJaExisteException,
    EntidadeNaoEncontradaException,
    TelefoneInvalidoException,
)
from models.utils.validadores import normaliza_cnpj, normaliza_telefone
from views.tela_empresa_transporte_gui import TelaEmpresaTransporteGUI
from controllers.controlador_entidade_base import ControladorEntidadeBase
from dao.dao_empresa_transporte import DAOEmpresaTransporte


class ControladorEmpresaTransporte(ControladorEntidadeBase):
    def __init__(self, controlador_principal):
        super().__init__(controlador_principal)
        self._tela = TelaEmpresaTransporteGUI()
        self._dao = DAOEmpresaTransporte()
        self._entidades = self._dao.carregar()

    def _normalizar_documentos(self, dados):
        try:
            cnpj = normaliza_cnpj(dados["cnpj"])
        except ValueError as err:
            raise CNPJInvalidoException(str(err))

        try:
            telefone = normaliza_telefone(dados["telefone"])
        except ValueError as err:
            raise TelefoneInvalidoException(str(err))

        return cnpj, telefone

    def _criar_entidade(self, dados):
        cnpj_normalizado, telefone_normalizado = self._normalizar_documentos(dados)

        for empresa in self._entidades:
            if empresa.cnpj == cnpj_normalizado:
                raise EntidadeJaExisteException("Empresa com esse CNPJ já cadastrada.")

        return EmpresaTransporte(
            dados["nome"],
            cnpj_normalizado,
            telefone_normalizado,
        )

    def _atualizar_entidade(self, empresa, dados):
        cnpj_normalizado, telefone_normalizado = self._normalizar_documentos(dados)

        for e in self._entidades:
            if e != empresa and e.cnpj == cnpj_normalizado:
                raise EntidadeJaExisteException("Empresa com esse CNPJ já cadastrada.")

        empresa.nome = dados["nome"]
        empresa.cnpj = cnpj_normalizado
        empresa.telefone = telefone_normalizado

    def _entidade_para_dict(self, empresa):
        return {
            "id": empresa.id,
            "nome": empresa.nome,
            "cnpj": empresa.cnpj,
            "telefone": empresa.telefone,
        }
