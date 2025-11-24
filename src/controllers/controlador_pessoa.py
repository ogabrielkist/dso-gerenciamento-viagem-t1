from models.pessoa import Pessoa
from models.exceptions import (
    CPFInvalidoException,
    EntidadeJaExisteException,
    EntidadeNaoEncontradaException,
    IdadeInvalidaException,
    PessoaJaCadastradaException,
    PessoaNaoEncontradaException,
    TelefoneInvalidoException,
)
from models.utils.validadores import normaliza_cpf, normaliza_telefone

from views.tela_pessoa_gui import TelaPessoaGUI
from controllers.controlador_entidade_base import ControladorEntidadeBase
from dao.dao_pessoa import DAOPessoa


class ControladorPessoa(ControladorEntidadeBase):
    def __init__(self, controlador_principal):
        super().__init__(controlador_principal)

        self._tela = TelaPessoaGUI()
        self._dao = DAOPessoa()
        self._entidades = self._dao.carregar()

    def _normalizar_documentos(self, dados):
        try:
            cpf = normaliza_cpf(dados["identificacao"])
        except ValueError as err:
            raise CPFInvalidoException(str(err))

        try:
            celular = normaliza_telefone(dados["celular"])
        except ValueError as err:
            raise TelefoneInvalidoException(str(err))

        return cpf, celular

    def _criar_entidade(self, dados):
        for participante in self._entidades:
            if participante.identificacao == dados["identificacao"]:
                raise EntidadeJaExisteException(
                    "Pessoa com essa identificação já cadastrada."
                )

        if dados["idade"] < 18:
            raise IdadeInvalidaException("Pessoa deve ter mais de 18 anos.")

        cpf, celular = self._normalizar_documentos(dados)

        return Pessoa(
            dados["nome"],
            celular,
            cpf,
            dados["idade"],
        )

    def _atualizar_entidade(self, pessoa, dados):
        if dados["idade"] < 18:
            raise IdadeInvalidaException("Pessoa deve ter mais de 18 anos.")

        cpf, celular = self._normalizar_documentos(dados)

        pessoa.nome = dados["nome"]
        pessoa.celular = celular
        pessoa.identificacao = cpf
        pessoa.idade = dados["idade"]

    def _entidade_para_dict(self, pessoa):
        return {
            "id": pessoa.id,
            "nome": pessoa.nome,
            "celular": pessoa.celular,
            "identificacao": pessoa.identificacao,
            "idade": pessoa.idade,
        }
