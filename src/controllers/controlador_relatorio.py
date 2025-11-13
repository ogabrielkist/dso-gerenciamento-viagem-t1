from collections import Counter
from dao.dao_viagem import DAOViagem
from models.exceptions import ListaVaziaException
from views import TelaRelatorio
from controllers.controlador_base import ControladorBase


class ControladorRelatorio(ControladorBase):
    def __init__(self, controlador_principal):
        super().__init__(controlador_principal)
        self._tela = TelaRelatorio()
        self._dao = DAOViagem()

        self._mapa_opcoes = {
            1: self.relatorio_destinos_populares,
        }

    def relatorio_destinos_populares(self):
        """
        Coleta os dados de viagens, processa o relatório de destinos
        e envia os dados formatados para a tela exibir.
        """
        try:
            viagens = self._dao.carregar()

            if not viagens:
                raise ListaVaziaException(
                    "Não há viagens cadastradas para gerar o relatório"
                )

            contador_cidades = Counter()

            for viagem in viagens:
                for itinerario in viagem.itinerarios:
                    for passeio in itinerario.passeios:
                        cidade_nome = passeio.cidade.nome
                        contador_cidades[cidade_nome] += 1

            destinos_populares = contador_cidades.most_common()

            if not destinos_populares:
                raise ListaVaziaException(
                    "Não há dados suficientes para gerar o relatório de destinos populares"
                )

            self._tela.mostra_relatorio_destinos(destinos_populares)

        except (ListaVaziaException, Exception) as e:
            self._tela.mostra_erro(str(e))
