from models import Pessoa
from models.exceptions import (
    PessoaJaCadastradaException,
    PessoaNaoEncontradaException,
    ListaVaziaException,
    OpcaoInvalidaException,
)
from views import TelaPessoa


class ControladorPessoa:
    def __init__(self, controlador_principal):
        self.__controlador_principal = controlador_principal
        self.__tela_pessoa = TelaPessoa()
        self.__participantes = []

    def incluir_pessoa(self):
        try:
            dados_pessoa = self.__tela_pessoa.pega_dados_pessoa()

            for participante in self.__participantes:
                if participante.identificacao() == dados_pessoa["identificacao"]:
                    raise PessoaJaCadastradaException(
                        "Pessoa com essa identificação já cadastrada."
                    )

            pessoa = Pessoa(
                dados_pessoa["nome"],
                dados_pessoa["celular"],
                dados_pessoa["identificacao"],
                dados_pessoa["idade"],
            )

            self.__participantes.append(pessoa)
            self.__tela_pessoa.mostra_mensagem("Pessoa incluída com sucesso!")

        except PessoaJaCadastradaException as e:
            self.__tela_pessoa.mostra_mensagem(f"ERRO: {e}")

    def listar_pessoas(self):
        try:
            if not self.__participantes:
                raise ListaVaziaException("Nenhuma pessoa cadastrada.")

            for pessoa in self.__participantes:
                dados_pessoa = {
                    "nome": pessoa.nome,
                    "celular": pessoa.celular,
                    "identificacao": pessoa.identificacao,
                    "idade": pessoa.idade,
                }

                self.__tela_pessoa.mostra_pessoa(dados_pessoa)

        except ListaVaziaException as e:
            self.__tela_pessoa.mostra_mensagem(str(e))

    def excluir_pessoa(self):
        try:
            self.listar_pessoas()
            if not self.__participantes:
                return

            identificacao = self.__tela_pessoa.seleciona_pessoa()

            pessoa_encontrada = None
            for pessoa in self.__participantes:
                if pessoa.identificacao == identificacao:
                    pessoa_encontrada = pessoa
                    break

            if not pessoa_encontrada:
                raise PessoaNaoEncontradaException("Pessoa não encontrada.")

            self.__participantes.remove(pessoa_encontrada)
            self.__tela_pessoa.mostra_mensagem("Pessoa removida com sucesso!")

        except PessoaNaoEncontradaException as e:
            self.__tela_pessoa.mostra_mensagem(f"ERRO: {e}")

    def editar_pessoa(self):
        try:
            self.listar_pessoas()
            if not self.__participantes:
                return

            identificacao = self.__tela_pessoa.seleciona_pessoa()
            pessoa_encontrada = None
            for pessoa in self.__participantes:
                if pessoa.identificacao == identificacao:
                    pessoa_encontrada = pessoa
                    break

            if not pessoa_encontrada:
                raise PessoaNaoEncontradaException("Pessoa não encontrada.")

            dados_pessoa = self.__tela_pessoa.pega_dados_pessoa()
            pessoa_encontrada.nome = dados_pessoa["nome"]
            pessoa_encontrada.celular = dados_pessoa["celular"]
            pessoa_encontrada.identificacao = dados_pessoa["identificacao"]
            pessoa_encontrada.idade = dados_pessoa["idade"]
            self.__tela_pessoa.mostra_mensagem("Pessoa editada com sucesso!")

        except PessoaNaoEncontradaException as e:
            self.__tela_pessoa.mostra_mensagem(f"ERRO: {e}")

    def retornar(self):
        self.__controlador_principal.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
            1: self.incluir_pessoa,
            2: self.listar_pessoas,
            3: self.excluir_pessoa,
            0: self.retornar,
        }

        while True:
            try:
                opcao_escolhida = self.__tela_pessoa.tela_opcoes()

                funcao_escolhida = lista_opcoes.get(opcao_escolhida)
                if not funcao_escolhida:
                    raise OpcaoInvalidaException("Opção inválida!")

                funcao_escolhida()

            except OpcaoInvalidaException as e:
                self.__tela_pessoa.mostra_mensagem(str(e))
