from datetime import datetime
import FreeSimpleGUI as sg
from views.tela_base_gui import TelaBaseGUI


class TelaPasseioTuristico(TelaBaseGUI):
    def __init__(self):
        super().__init__()
        self._controlador_cidade = None
        self._controlador_pessoa = None

    def set_controlador_cidade(self, controlador_cidade):
        self._controlador_cidade = controlador_cidade

    def set_controlador_pessoa(self, controlador_pessoa):
        self._controlador_pessoa = controlador_pessoa

    def le_opcao(self):
        layout = [
            [
                sg.Text(
                    "Passeios Turísticos",
                    font=("Helvetica", 18, "bold"),
                    justification="center",
                    expand_x=True,
                )
            ],
            [sg.Button("Incluir", key="-INCLUIR-", size=(25, 2))],
            [sg.Button("Listar", key="-LISTAR-", size=(25, 2))],
            [sg.Button("Editar", key="-EDITAR-", size=(25, 2))],
            [sg.Button("Excluir", key="-EXCLUIR-", size=(25, 2))],
            [sg.VPush()],
            [sg.Button("Voltar", key="-VOLTAR-", size=(25, 2))],
        ]
        window = sg.Window("Passeios Turísticos", layout, finalize=True)
        event, _ = window.read()
        window.close()
        if event in (sg.WIN_CLOSED, "-VOLTAR-"):
            return "-VOLTAR-"
        return event

    def pega_dados_entidade(self, dados_atuais=None):
        cidades = (
            self._controlador_cidade.get_entidades() if self._controlador_cidade else []
        )
        if not cidades:
            self.mostra_erro("Cadastre uma cidade antes de criar passeios.")
            return None

        mapa_cidades = {
            f"{cidade.nome} / {cidade.pais.nome}": cidade for cidade in cidades
        }
        cidade_default = (
            f"{dados_atuais['cidade'].nome} / {dados_atuais['cidade'].pais.nome}"
            if dados_atuais
            else next(iter(mapa_cidades.keys()))
        )

        atracao = dados_atuais["atracao_turistica"] if dados_atuais else ""
        inicio = (
            dados_atuais["horario_inicio"].strftime("%H:%M") if dados_atuais else ""
        )
        fim = dados_atuais["horario_fim"].strftime("%H:%M") if dados_atuais else ""
        valor = f"{dados_atuais['valor']:.2f}" if dados_atuais else ""

        titulo = "Editar Passeio" if dados_atuais else "Novo Passeio Turístico"
        layout = [
            [sg.Text(titulo, font=("Helvetica", 16))],
            [sg.Text("Atração:", size=(15, 1)), sg.Input(default_text=atracao, key="-ATRACAO-")],
            [
                sg.Text("Horário Início (HH:MM):", size=(15, 1)),
                sg.Input(default_text=inicio, key="-INICIO-"),
            ],
            [
                sg.Text("Horário Fim (HH:MM):", size=(15, 1)),
                sg.Input(default_text=fim, key="-FIM-"),
            ],
            [
                sg.Text("Valor (R$):", size=(15, 1)),
                sg.Input(default_text=valor, key="-VALOR-"),
            ],
            [
                sg.Text("Cidade:", size=(15, 1)),
                sg.Combo(
                    list(mapa_cidades.keys()),
                    default_value=cidade_default,
                    readonly=True,
                    key="-CIDADE-",
                ),
            ],
            [sg.Button("Salvar", key="-SALVAR-"), sg.Button("Cancelar", key="-CANCELAR-")],
        ]

        window = sg.Window(titulo, layout, finalize=True)
        dados = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "-CANCELAR-"):
                break
            if event == "-SALVAR-":
                try:
                    atracao = values["-ATRACAO-"].strip()
                    if not atracao:
                        raise ValueError("Informe a atração turística.")
                    horario_inicio = datetime.strptime(values["-INICIO-"], "%H:%M").time()
                    horario_fim = datetime.strptime(values["-FIM-"], "%H:%M").time()
                    valor = float(values["-VALOR-"])
                    dados = {
                        "atracao_turistica": atracao,
                        "horario_inicio": horario_inicio,
                        "horario_fim": horario_fim,
                        "valor": valor,
                        "cidade": mapa_cidades[values["-CIDADE-"]],
                    }
                    break
                except ValueError as err:
                    self.mostra_erro(str(err))

        window.close()
        return dados

    def mostra_lista_entidades(self, dados_lista):
        if not dados_lista:
            self.mostra_mensagem("Passeios", "Nenhum passeio cadastrado.")
            return

        headings = ["ID", "Atração", "Horário", "Valor", "Cidade"]
        data = [
            [
                d["id"],
                d["atracao_turistica"],
                f"{d['horario_inicio'].strftime('%H:%M')} - {d['horario_fim'].strftime('%H:%M')}",
                f"{d['valor']:.2f}",
                f"{d['cidade'].nome}/{d['cidade'].pais.nome}",
            ]
            for d in dados_lista
        ]
        self.mostra_lista("Passeios Turísticos", headings, data)

    def seleciona_entidade(self, dados_lista, titulo_janela):
        if not dados_lista:
            self.mostra_erro("Nenhum passeio cadastrado.")
            return None

        headings = ["ID", "Atração", "Cidade"]
        data = []
        id_lookup = []
        for d in dados_lista:
            data.append(
                [
                    d["id"],
                    d["atracao_turistica"],
                    f"{d['cidade'].nome}/{d['cidade'].pais.nome}",
                ]
            )
            id_lookup.append(d["id"])

        layout = [
            [sg.Text(titulo_janela, font=("Helvetica", 16))],
            [
                sg.Table(
                    values=data,
                    headings=headings,
                    auto_size_columns=True,
                    num_rows=min(15, len(data)),
                    select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                    key="-TABLE-",
                )
            ],
            [sg.Button("Selecionar", key="-OK-"), sg.Button("Cancelar", key="-CANCELAR-")],
        ]

        window = sg.Window(titulo_janela, layout, finalize=True)
        selecionado = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "-CANCELAR-"):
                break
            if event == "-OK-":
                if values["-TABLE-"]:
                    selecionado = id_lookup[values["-TABLE-"][0]]
                    break
                self.mostra_erro("Selecione um passeio.")

        window.close()
        return selecionado
