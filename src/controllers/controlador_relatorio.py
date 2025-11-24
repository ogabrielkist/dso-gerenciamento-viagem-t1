from collections import Counter, defaultdict
import FreeSimpleGUI as sg
from dao.dao_viagem import DAOViagem
from dao.dao_itinerario_viagem import DAOItinerarioViagem
from dao.dao_passeio_turistico import DAOPasseioTuristico
from models.exceptions import ListaVaziaException
from views import TelaRelatorioGUI
from controllers.controlador_base import ControladorBase


class ControladorRelatorio(ControladorBase):
    def __init__(self, controlador_principal):
        super().__init__(controlador_principal)
        self._tela = TelaRelatorioGUI()
        self._dao_viagem = DAOViagem()
        self._dao_itinerario = DAOItinerarioViagem()
        self._dao_passeio = DAOPasseioTuristico()

        self._mapa_opcoes = {
            1: self.relatorio_destinos_populares,
            "-DESTINOS_POPULARES-": self.relatorio_destinos_populares,
            2: self.relatorio_destinos_por_preco,
            "-DESTINOS_PRECO-": self.relatorio_destinos_por_preco,
            3: self.relatorio_passeios_populares,
            "-PASSEIOS_POPULARES-": self.relatorio_passeios_populares,
            4: self.relatorio_passeios_por_preco,
            "-PASSEIOS_PRECO-": self.relatorio_passeios_por_preco,
        }

    def abre_tela(self):
        while True:
            event = self._tela.le_opcao()
            if event in ("-VOLTAR-", sg.WIN_CLOSED, 0):
                break

            handler = self._mapa_opcoes.get(event)
            if handler:
                handler()
            else:
                self._tela.mostra_erro("Relatório não encontrado.")

    def _coletar_viagens(self):
        viagens = self._dao_viagem.carregar()
        if not viagens:
            raise ListaVaziaException("Cadastre viagens para gerar relatórios.")
        return viagens

    def relatorio_destinos_populares(self):
        try:
            viagens = self._coletar_viagens()
            contador_cidades = Counter()

            for viagem in viagens:
                for itinerario in viagem.itinerarios:
                    for passeio in itinerario.passeios:
                        chave = f"{passeio.cidade.nome}/{passeio.cidade.pais.nome}"
                        contador_cidades[chave] += 1

            destinos_populares = contador_cidades.most_common()
            if not destinos_populares:
                raise ListaVaziaException(
                    "Nenhum destino associado a itinerários foi encontrado."
                )

            self._tela.mostra_relatorio_destinos(destinos_populares)
        except (ListaVaziaException, Exception) as e:
            self._tela.mostra_erro(str(e))

    def relatorio_destinos_por_preco(self):
        try:
            passeios = self._dao_passeio.carregar()
            if not passeios:
                raise ListaVaziaException("Cadastre passeios para calcular valores.")

            acumulado = defaultdict(list)
            for passeio in passeios:
                chave = (passeio.cidade.nome, passeio.cidade.pais.nome)
                acumulado[chave].append(passeio.valor)

            medias = []
            for (cidade, pais), valores in acumulado.items():
                media = sum(valores) / len(valores)
                medias.append((cidade, pais, media))

            medias.sort(key=lambda item: item[2], reverse=True)
            caros = medias[:5]
            baratos = list(reversed(medias[-5:]))
            self._tela.mostra_relatorio_destinos_preco(caros, baratos)
        except (ListaVaziaException, Exception) as e:
            self._tela.mostra_erro(str(e))

    def relatorio_passeios_populares(self):
        try:
            itinerarios = self._dao_itinerario.carregar()
            if not itinerarios:
                raise ListaVaziaException("Cadastre itinerários para gerar este relatório.")

            contador = Counter()
            for itinerario in itinerarios:
                for passeio in itinerario.passeios:
                    chave = (passeio.atracao_turistica, passeio.cidade.nome)
                    contador[chave] += 1

            populares = [
                (atracao, cidade, qtd) for (atracao, cidade), qtd in contador.most_common()
            ]
            if not populares:
                raise ListaVaziaException("Nenhum passeio associado a itinerários foi encontrado.")

            self._tela.mostra_relatorio_passeios_populares(populares)
        except (ListaVaziaException, Exception) as e:
            self._tela.mostra_erro(str(e))

    def relatorio_passeios_por_preco(self):
        try:
            passeios = self._dao_passeio.carregar()
            if not passeios:
                raise ListaVaziaException("Cadastre passeios turísticos para este relatório.")

            ordenado = sorted(
                [(p.atracao_turistica, p.cidade.nome, p.valor) for p in passeios],
                key=lambda item: item[2],
                reverse=True,
            )
            caros = ordenado[:5]
            baratos = list(reversed(ordenado[-5:]))
            self._tela.mostra_relatorio_passeios_preco(caros, baratos)
        except (ListaVaziaException, Exception) as e:
            self._tela.mostra_erro(str(e))
