from datetime import date
from models.viagem import Viagem
from models.exceptions import EntidadeJaExisteException, EntidadeNaoEncontradaException
from views.tela_viagem import TelaViagem
from controllers.controlador_base import ControladorBase
from dao.dao_viagem import DAOViagem


class ControladorViagem(ControladorBase):
    def __init__(self, controlador_principal):
        super().__init__(controlador_principal)
        self._tela = TelaViagem()
        self._dao = DAOViagem()
        self._entidades = self._dao.carregar()
        self._mapa_opcoes = {
            1: self.incluir,
            2: self.listar,
            3: self.excluir,
            4: self.editar,
        }

    def _criar_entidade(self, dados):
        for viagem in self._entidades:
            if viagem.data_inicio == dados["data_inicio"]:
                raise EntidadeJaExisteException(
                    "Viagem com essa data de início já cadastrada."
                )

        if dados["data_fim"] <= dados["data_inicio"]:
            raise ValueError("Data de fim deve ser posterior à data de início.")

        if dados["valor_total_pacote"] < 0:
            raise ValueError("Valor total do pacote não pode ser negativo.")

        return Viagem(
            dados["data_inicio"],
            dados["data_fim"],
            dados["valor_total_pacote"],
        )

    def _atualizar_entidade(self, viagem, dados):
        for v in self._entidades:
            if v != viagem and v.data_inicio == dados["data_inicio"]:
                raise EntidadeJaExisteException(
                    "Viagem com essa data de início já cadastrada."
                )

        if dados["data_fim"] <= dados["data_inicio"]:
            raise ValueError("Data de fim deve ser posterior à data de início.")

        if dados["valor_total_pacote"] < 0:
            raise ValueError("Valor total do pacote não pode ser negativo.")

        viagem.data_inicio = dados["data_inicio"]
        viagem.data_fim = dados["data_fim"]
        viagem.valor_total_pacote = dados["valor_total_pacote"]

    def _entidade_para_dict(self, viagem):
        return {
            "id": viagem.id,
            "data_inicio": viagem.data_inicio,
            "data_fim": viagem.data_fim,
            "valor_total_pacote": viagem.valor_total_pacote,
            "participantes": viagem.participantes,
            "destinos_visitados": viagem.destinos_visitados,
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
