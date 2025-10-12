from models.passagem import Passagem
from models.exceptions import EntidadeJaExisteException, EntidadeNaoEncontradaException
from views.tela_passagem import TelaPassagem
from controllers.controlador_base import ControladorBase
from dao.dao_passagem import DAOPassagem


class ControladorPassagem(ControladorBase):
    def __init__(self, controlador_principal, controlador_pessoa, controlador_trecho):
        super().__init__(controlador_principal)
        self._tela = TelaPassagem()
        self._tela.set_controlador_pessoa(controlador_pessoa)
        self._tela.set_controlador_trecho(controlador_trecho)
        self._dao = DAOPassagem()
        self._entidades = self._dao.carregar()
        self._mapa_opcoes = {
            1: self.incluir,
            2: self.listar,
            3: self.excluir,
            4: self.editar,
            5: self.confirmar_compra,
        }

    def _criar_entidade(self, dados):
        for passagem in self._entidades:
            if (
                passagem.passageiro.id == dados["passageiro"].id
                and passagem.trecho.id == dados["trecho"].id
            ):
                raise EntidadeJaExisteException(
                    "Passagem para esse passageiro nesse trecho já cadastrada."
                )

        return Passagem(
            dados["passageiro"],
            dados["trecho"],
            dados["responsavel_compra"],
        )

    def _atualizar_entidade(self, passagem, dados):
        for p in self._entidades:
            if (
                p != passagem
                and p.passageiro.id == dados["passageiro"].id
                and p.trecho.id == dados["trecho"].id
            ):
                raise EntidadeJaExisteException(
                    "Passagem para esse passageiro nesse trecho já cadastrada."
                )

        passagem.passageiro = dados["passageiro"]
        passagem.trecho = dados["trecho"]
        passagem.responsavel_compra = dados["responsavel_compra"]

    def _entidade_para_dict(self, passagem):
        return {
            "compra_efetuada": passagem.compra_efetuada,
            "passageiro": passagem.passageiro,
            "trecho": passagem.trecho,
            "responsavel_compra": passagem.responsavel_compra,
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

    def confirmar_compra(self):
        try:
            self.listar()
            if not self._entidades:
                return

            id_passagem = self._tela.seleciona_entidade()
            passagem_encontrada = None
            for passagem in self._entidades:
                if passagem.id == id_passagem:
                    passagem_encontrada = passagem
                    break

            if not passagem_encontrada:
                raise EntidadeNaoEncontradaException("Passagem não encontrada.")

            if passagem_encontrada.compra_efetuada:
                self._tela.mostra_erro("Passagem já foi comprada.")
                return

            passagem_encontrada.compra_efetuada = True
            self._dao.salvar(self._entidades)
            self._tela.mostra_sucesso("Compra da passagem confirmada!")

        except EntidadeNaoEncontradaException as e:
            self._tela.mostra_erro(str(e))
        except Exception as e:
            self._tela.mostra_erro(str(e))
