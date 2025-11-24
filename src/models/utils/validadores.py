import re

CPF_DIGITS = 11
CNPJ_DIGITS = 14
TELEFONE_MIN = 10
TELEFONE_MAX = 11


def _apenas_digitos(valor: str) -> str:
    if valor is None:
        return ""
    return re.sub(r"\D", "", valor)


def normaliza_cpf(valor: str) -> str:
    digitos = _apenas_digitos(valor)
    if len(digitos) != CPF_DIGITS:
        raise ValueError("CPF deve conter 11 dígitos numéricos.")
    if len(set(digitos)) == 1:
        raise ValueError("CPF não pode possuir todos os dígitos iguais.")
    return digitos


def normaliza_cnpj(valor: str) -> str:
    digitos = _apenas_digitos(valor)
    if len(digitos) != CNPJ_DIGITS:
        raise ValueError("CNPJ deve conter 14 dígitos numéricos.")
    if len(set(digitos)) == 1:
        raise ValueError("CNPJ não pode possuir todos os dígitos iguais.")
    return digitos


def normaliza_telefone(valor: str) -> str:
    digitos = _apenas_digitos(valor)
    if len(digitos) < TELEFONE_MIN or len(digitos) > TELEFONE_MAX:
        raise ValueError("Telefone deve conter 10 ou 11 dígitos, incluindo DDD.")
    return digitos


def formata_cpf(valor: str) -> str:
    digitos = _apenas_digitos(valor)
    if len(digitos) != CPF_DIGITS:
        return valor
    return f"{digitos[:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}"


def formata_cnpj(valor: str) -> str:
    digitos = _apenas_digitos(valor)
    if len(digitos) != CNPJ_DIGITS:
        return valor
    return (
        f"{digitos[:2]}.{digitos[2:5]}.{digitos[5:8]}/"
        f"{digitos[8:12]}-{digitos[12:]}"
    )


def formata_telefone(valor: str) -> str:
    digitos = _apenas_digitos(valor)
    if len(digitos) == 11:
        return f"({digitos[:2]}) {digitos[2:7]}-{digitos[7:]}"
    if len(digitos) == 10:
        return f"({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}"
    return valor
