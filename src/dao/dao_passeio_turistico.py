from datetime import time
from models.passeio_turistico import PasseioTuristico
from models.cidade import Cidade
from .dao_base import DAOBase
from .dao_cidade import DAOCidade


class DAOPasseioTuristico(DAOBase):
    def __init__(self):
        super().__init__("passeios_turisticos.json")
        self.__dao_cidade = DAOCidade()

    def _serializar_entidade(self, passeio):
        return {
            "id": passeio.id,
            "atracao_turistica": passeio.atracao_turistica,
            "horario_inicio": passeio.horario_inicio.isoformat(),
            "horario_fim": passeio.horario_fim.isoformat(),
            "valor": passeio.valor,
            "cidade_id": passeio.cidade.id,
            "participantes": [p.id for p in passeio.participantes_passeio],
        }

    def _deserializar_entidade(self, dados):
        cidades = self.__dao_cidade.carregar()
        cidade = next((c for c in cidades if c.id == dados["cidade_id"]), None)
        if not cidade:
            raise ValueError(f"Cidade com ID {dados['cidade_id']} não encontrada")

        passeio = PasseioTuristico(
            dados["atracao_turistica"],
            time.fromisoformat(dados["horario_inicio"]),
            time.fromisoformat(dados["horario_fim"]),
            dados["valor"],
            cidade,
            dados.get("id"),
        )

        return passeio
