from models.cidade import Cidade
from models.exceptions import EntidadeJaExisteException, EntidadeNaoEncontradaException
from views.tela_cidade import TelaCidade
from controllers.controlador_entidade_base import ControladorEntidadeBase
from dao.dao_cidade import DAOCidade


class ControladorCidade(ControladorEntidadeBase):
    def __init__(self, controlador_principal, controlador_pais):
        super().__init__(controlador_principal)
        self._tela = TelaCidade()
        self._tela.set_controlador_pais(controlador_pais)
        self._dao = DAOCidade()
        self._entidades = self._dao.carregar()
        self._mapa_opcoes = {
            1: self.incluir,
            2: self.listar,
            3: self.excluir,
            4: self.editar,
        }

    def _criar_entidade(self, dados):
        for cidade in self._entidades:
            if (
                cidade.nome.lower() == dados["nome"].lower()
                and cidade.pais.nome.lower() == dados["pais"].nome.lower()
            ):
                raise EntidadeJaExisteException(
                    "Cidade com esse nome já cadastrada neste país."
                )

        return Cidade(dados["nome"], dados["pais"])

    def _atualizar_entidade(self, cidade, dados):
        for c in self._entidades:
            if (
                c != cidade
                and c.nome.lower() == dados["nome"].lower()
                and c.pais.nome.lower() == dados["pais"].nome.lower()
            ):
                raise EntidadeJaExisteException(
                    "Cidade com esse nome já cadastrada neste país."
                )

        cidade.nome = dados["nome"]
        cidade.pais = dados["pais"]

    def _entidade_para_dict(self, cidade):
        return {
            "id": cidade.id,
            "nome": cidade.nome,
            "pais": cidade.pais,
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
