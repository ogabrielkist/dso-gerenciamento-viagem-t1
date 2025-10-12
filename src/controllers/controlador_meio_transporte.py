from models.meio_transporte import MeioTransporte
from models.exceptions import EntidadeJaExisteException, EntidadeNaoEncontradaException
from views.tela_meio_transporte import TelaMeioTransporte
from controllers.controlador_base import ControladorBase
from dao.dao_meio_transporte import DAOMeioTransporte


class ControladorMeioTransporte(ControladorBase):
    def __init__(self, controlador_principal, controlador_empresa):
        super().__init__(controlador_principal)
        self._tela = TelaMeioTransporte()
        self._tela.set_controlador_empresa(controlador_empresa)
        self._dao = DAOMeioTransporte()
        self._entidades = self._dao.carregar()
        self._mapa_opcoes = {
            1: self.incluir,
            2: self.listar,
            3: self.excluir,
            4: self.editar,
        }

    def _criar_entidade(self, dados):
        for meio in self._entidades:
            if (
                meio.tipo == dados["tipo"]
                and meio.empresa.cnpj == dados["empresa"].cnpj
            ):
                raise EntidadeJaExisteException(
                    "Meio de transporte com esse tipo e empresa já cadastrado."
                )

        return MeioTransporte(dados["tipo"], dados["empresa"])

    def _atualizar_entidade(self, meio_transporte, dados):
        for m in self._entidades:
            if (
                m != meio_transporte
                and m.tipo == dados["tipo"]
                and m.empresa.cnpj == dados["empresa"].cnpj
            ):
                raise EntidadeJaExisteException(
                    "Meio de transporte com esse tipo e empresa já cadastrado."
                )

        meio_transporte.tipo = dados["tipo"]
        meio_transporte.empresa = dados["empresa"]

    def _entidade_para_dict(self, meio_transporte):
        return {
            "id": meio_transporte.id,
            "tipo": meio_transporte.tipo,
            "empresa": meio_transporte.empresa,
        }

    def incluir(self):
        try:
            super().incluir()
            self._dao.salvar(self._entidades)
        except Exception as e:
            self._tela.mostra_erro(str(e))

    def excluir(self):
        try:
            super().excluir()
            self._dao.salvar(self._entidades)
        except Exception as e:
            self._tela.mostra_erro(str(e))

    def editar(self):
        try:
            super().editar()
            self._dao.salvar(self._entidades)
        except Exception as e:
            self._tela.mostra_erro(str(e))
