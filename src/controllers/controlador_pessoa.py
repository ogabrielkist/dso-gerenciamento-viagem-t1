from models import Pessoa
from models.exceptions import (
    PessoaJaCadastradaException,
    PessoaNaoEncontradaException,
    EntidadeJaExisteException,
    EntidadeNaoEncontradaException,
)
from views import TelaPessoa
from controllers.controlador_entidade_base import ControladorEntidadeBase
from dao.dao_pessoa import DAOPessoa


class ControladorPessoa(ControladorEntidadeBase):
    def __init__(self, controlador_principal):
        super().__init__(controlador_principal)
        self._tela = TelaPessoa()
        self._dao = DAOPessoa()
        self._entidades = self._dao.carregar()
        self._mapa_opcoes = {
            1: self.incluir,
            2: self.listar,
            3: self.excluir,
            4: self.editar,
        }

    def _criar_entidade(self, dados):
        for participante in self._entidades:
            if participante.identificacao == dados["identificacao"]:
                raise EntidadeJaExisteException(
                    "Pessoa com essa identificação já cadastrada."
                )

        if dados["idade"] < 18:
            raise ValueError(
                "Pessoa deve ter mais de 18 anos para participar da viagem."
            )

        return Pessoa(
            dados["nome"],
            dados["celular"],
            dados["identificacao"],
            dados["idade"],
        )

    def _atualizar_entidade(self, pessoa, dados):
        if dados["idade"] < 18:
            raise ValueError(
                "Pessoa deve ter mais de 18 anos para participar da viagem."
            )

        pessoa.nome = dados["nome"]
        pessoa.celular = dados["celular"]
        pessoa.identificacao = dados["identificacao"]
        pessoa.idade = dados["idade"]

    def _entidade_para_dict(self, pessoa):
        return {
            "id": pessoa.id,
            "nome": pessoa.nome,
            "celular": pessoa.celular,
            "identificacao": pessoa.identificacao,
            "idade": pessoa.idade,
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
