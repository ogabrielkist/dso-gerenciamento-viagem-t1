from models.passeio_turistico import PasseioTuristico
from models.exceptions import EntidadeJaExisteException, EntidadeNaoEncontradaException
from views.tela_passeio_turistico import TelaPasseioTuristico
from controllers.controlador_entidade_base import ControladorEntidadeBase
from dao.dao_passeio_turistico import DAOPasseioTuristico


class ControladorPasseioTuristico(ControladorEntidadeBase):
    def __init__(self, controlador_principal, controlador_cidade, controlador_pessoa):
        super().__init__(controlador_principal)
        self._tela = TelaPasseioTuristico()
        self._tela.set_controlador_cidade(controlador_cidade)
        self._tela.set_controlador_pessoa(controlador_pessoa)
        self._dao = DAOPasseioTuristico()
        self._entidades = self._dao.carregar()
        self._mapa_opcoes.update(
            {
                1: self.incluir,
                2: self.listar,
                3: self.excluir,
                4: self.editar,
            }
        )

    def _criar_entidade(self, dados):
        for passeio in self._entidades:
            if (
                passeio.atracao_turistica.lower() == dados["atracao_turistica"].lower()
                and passeio.cidade.id == dados["cidade"].id
                and passeio.horario_inicio == dados["horario_inicio"]
            ):
                raise EntidadeJaExisteException(
                    "Passeio turístico com essas características já cadastrado."
                )

        return PasseioTuristico(
            dados["atracao_turistica"],
            dados["horario_inicio"],
            dados["horario_fim"],
            dados["valor"],
            dados["cidade"],
        )

    def _atualizar_entidade(self, passeio, dados):
        for p in self._entidades:
            if (
                p != passeio
                and p.atracao_turistica.lower() == dados["atracao_turistica"].lower()
                and p.cidade.id == dados["cidade"].id
                and p.horario_inicio == dados["horario_inicio"]
            ):
                raise EntidadeJaExisteException(
                    "Passeio turístico com essas características já cadastrado."
                )

        passeio.atracao_turistica = dados["atracao_turistica"]
        passeio.horario_inicio = dados["horario_inicio"]
        passeio.horario_fim = dados["horario_fim"]
        passeio.valor = dados["valor"]
        passeio.cidade = dados["cidade"]

    def _entidade_para_dict(self, passeio):
        return {
            "id": passeio.id,
            "atracao_turistica": passeio.atracao_turistica,
            "horario_inicio": passeio.horario_inicio,
            "horario_fim": passeio.horario_fim,
            "valor": passeio.valor,
            "cidade": passeio.cidade,
            "participantes_passeio": passeio.participantes_passeio,
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
