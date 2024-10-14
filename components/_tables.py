from flet_core import Page, DataTable, DataColumn, Text, DataRow, DataCell
from functions import get_all_profile_not_users



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
    for profile in get_all_profile_not_users(page):
        _table.rows.append(
            DataRow(
                cells=[
                    DataCell(Text(str(profile['id']))),
                    DataCell(Text(str(profile['first_name']))),
                    DataCell(Text(str(profile['last_name']))),
                    DataCell(Text(str(profile['birth_date']))),
                ]
            )
        )
    return _table