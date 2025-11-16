from models.pais import Pais
from models.exceptions import EntidadeJaExisteException, EntidadeNaoEncontradaException
from views.tela_pais import TelaPais
from controllers.controlador_entidade_base import ControladorEntidadeBase
from dao.dao_pais import DAOPais


class ControladorPais(ControladorEntidadeBase):
    def __init__(self, controlador_principal):
        super().__init__(controlador_principal)
        self._tela = TelaPais()
        self._dao = DAOPais()
        self._entidades = self._dao.carregar()
        self._mapa_opcoes = {
            1: self.incluir,
            2: self.listar,
            3: self.excluir,
            4: self.editar,
        }

    def _criar_entidade(self, dados):
        for pais in self._entidades:
            if pais.nome.lower() == dados["nome"].lower():
                raise EntidadeJaExisteException("País com esse nome já cadastrado.")

        return Pais(dados["nome"])

    def _atualizar_entidade(self, pais, dados):
        for p in self._entidades:
            if p != pais and p.nome.lower() == dados["nome"].lower():
                raise EntidadeJaExisteException("País com esse nome já cadastrado.")

        pais.nome = dados["nome"]

    def _entidade_para_dict(self, pais):
        return {
            "id": pais.id,
            "nome": pais.nome,
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
