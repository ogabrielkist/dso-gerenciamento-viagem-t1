from models.pessoa import Pessoa
from models.exceptions import (
    EntidadeJaExisteException,
    PessoaJaCadastradaException,
    PessoaNaoEncontradaException,
    EntidadeNaoEncontradaException,
)

from views.tela_pessoa_gui import TelaPessoaGUI
from controllers.controlador_entidade_base import ControladorEntidadeBase
from dao.dao_pessoa import DAOPessoa


class ControladorPessoa(ControladorEntidadeBase):
    def __init__(self, controlador_principal):
        super().__init__(controlador_principal)

        self._tela = TelaPessoaGUI()
        self._dao = DAOPessoa()
        self._entidades = self._dao.carregar()

    def _criar_entidade(self, dados):
        for participante in self._entidades:
            if participante.identificacao == dados["identificacao"]:
                raise EntidadeJaExisteException("Pessoa com essa identificação já cadastrada.")

        if dados["idade"] < 18:
            raise ValueError("Pessoa deve ter mais de 18 anos.")

        return Pessoa(
            dados["nome"],
            dados["celular"],
            dados["identificacao"],
            dados["idade"],
        )

    def _atualizar_entidade(self, pessoa, dados):
        if dados["idade"] < 18:
            raise ValueError("Pessoa deve ter mais de 18 anos.")

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
