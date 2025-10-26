from datetime import date
from datetime import datetime


def date_para_str(data: date) -> str:
    return data.strftime('%d/%m/%Y')  # formata uma data no formato 'date': para 'string'.


def str_para_date(data: str) -> date:
    return datetime.strptime(data, '%d/%m/%Y')  # formata uma data no formato 'string': para 'date'.


def formata_float_str_moeda(valor: float) -> str:
    return f'R$ {valor:,.2f}'



