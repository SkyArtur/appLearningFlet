from flet_core import Page, DataTable, DataColumn, Text, DataRow, DataCell
from functions import get_data_table_profiles



def table_profiles(page: Page):
    _table = DataTable(
        columns=[
            DataColumn(Text('ID')),
            DataColumn(Text('Nome')),
            DataColumn(Text('Sobrenome')),
            DataColumn(Text('Nascimento')),
        ],
        rows=[]
    )
    get_data_table_profiles(page, _table)
    page.update()
    return _table