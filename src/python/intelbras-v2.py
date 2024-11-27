import flet as ft
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    DataTable,
    DataColumn,
    DataRow,
    DataCell,
    Container,
    Column,
    icons,
)
import tabula
import pandas as pd
import json
import os
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from datetime import datetime
import mysql.connector  # Importando o conector MySQL
from mysql.connector import Error
import sys

# Função para processar o PDF e gerar JSON e Excel
def process_pdf(pdf_path):
    try:
        # Extrair o nome do arquivo PDF sem a extensão
        file_name = os.path.splitext(os.path.basename(pdf_path))[0]

        # Extrair todas as tabelas do PDF
        tables = tabula.read_pdf(
            pdf_path,
            pages="all",
            multiple_tables=True,
            relative_area=True,
            relative_columns=True,
            area=[12, 0, 90, 100],
            columns=[10, 30.5, 37, 45, 53, 60, 70, 80, 100]
        )

        if not tables or len(tables) == 0:
            raise ValueError("Nenhuma tabela foi extraída do PDF.")

        custom_header = ["ID", "Nome", "Bloco", "Apto", "Dispositivo", "Saída", "Recurso", "Status do Recurso", "Data de registro"]
        processed_tables = []

        for table in tables:
            table.columns = custom_header
            table = table.drop(table.index[0:2])
            processed_tables.append(table)

        final_table = pd.concat(processed_tables, ignore_index=True)
        final_table = final_table.where(pd.notnull(final_table), None)
        json_data = final_table.to_dict(orient="records")

        processed_data = []
        previous_item = {}

        for i in range(len(json_data)):
            if not json_data[i].get("ID"):
                for json_data_key, json_data_value in json_data[i].items():
                    if json_data_value:
                        if previous_item.get(json_data_key):
                            if json_data_value not in previous_item[json_data_key]:
                                previous_item[json_data_key] += " " + json_data_value
                        else:
                            previous_item[json_data_key] = json_data_value
                processed_data[-1] = previous_item
            else:
                previous_item = json_data[i]
                processed_data.append(previous_item)

        for i in range(len(processed_data)):
            data_registro = processed_data[i]["Data de registro"]
            data, hora = data_registro.split(" ")
            processed_data[i]["ID"] = int(processed_data[i]["ID"])
            if processed_data[i]["Apto"] != None:
                processed_data[i]["Apto"] = int(processed_data[i]["Apto"])
            processed_data[i]["Data"] = data
            processed_data[i]["Hora"] = hora
            del processed_data[i]["Data de registro"]

        # Atualizar as datas e horas para o formato correto
        for i in range(len(processed_data)):
            processed_data[i]["Data"] = datetime.strptime(processed_data[i]["Data"], "%d/%m/%Y")
            processed_data[i]["Hora"] = datetime.strptime(processed_data[i]["Hora"], "%H:%M:%S")

        return processed_data  # Retorna os dados processados
    except Exception as e:
        sys.stderr.write(f"Erro ao processar o PDF: {str(e)}\n")
        return None

# Função para inserir dados no MySQL
def insert_data_to_mysql(data):
    try:
        # Configurações de conexão com o banco de dados
        connection = mysql.connector.connect(
            host='193.203.175.55',      # Endereço do servidor MySQL
            user='u307536401_auto',    # Nome do usuário do MySQL
            password='autoAuto123321',  # Senha do MySQL
            database='u307536401_Automatizacoes'   # Nome do banco de dados
        )
        
        if connection.is_connected():
            cursor = connection.cursor()

            # Query para verificar se o registro já existe
            check_query = """
                SELECT COUNT(*) FROM clientes_acesso WHERE ID_imovel = %s AND Nome = %s AND Dispositivo = %s AND Saida = %s AND Recurso = %s AND Data = %s AND Hora = %s;
                """
            # Inserindo os dados na tabela
            insert_query = """
            INSERT INTO clientes_acesso (
                ID_imovel, Nome, Bloco, Apto, Dispositivo, Saida, Recurso, Status_recurso, Data, Hora
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            
            for item in data:
                if isinstance(item["Data"], str):
                    item["Data"] = datetime.strptime(item["Data"], "%d/%m/%Y")
                if isinstance(item["Hora"], str):
                    item["Hora"] = datetime.strptime(item["Hora"], "%H:%M:%S")
                # Verificar se o registro já existe
                cursor.execute(check_query, (
                    item["ID"],
                    item["Nome"],
                    item["Dispositivo"],
                    item["Saída"],
                    item["Recurso"],
                    item["Data"].strftime("%Y-%m-%d"),
                    item["Hora"].strftime("%H:%M:%S")
                ))
                exists = cursor.fetchone()[0]

                if not exists:
                    cursor.execute(insert_query, (
                        item["ID"],
                        item["Nome"],
                        item["Bloco"],
                        item["Apto"],
                        item["Dispositivo"],
                        item["Saída"],
                        item["Recurso"],
                        item["Status do Recurso"],
                        item["Data"].strftime("%Y-%m-%d"),
                        item["Hora"].strftime("%H:%M:%S")
                    ))
                else:
                    print(f"Registro já existe para: {item['Nome']} - {item['ID']}")

            connection.commit()
            print("Dados inseridos com sucesso no MySQL.")

    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Interface com Flet
def main(page: Page):
    def pick_files_result(e: FilePickerResultEvent):
        if e.files:
            pdf_file = e.files[0].path
            selected_files.value = f"Arquivo selecionado: {e.files[0].name}"
            selected_files.update()

            # Processa o PDF
            processed_data = process_pdf(pdf_file)
            if processed_data:
                download_excel_link.value = "Arquivo Excel criado com sucesso."
                download_excel_link.update()
                
                Mysql_process_message.controls = [ft.Icon(name=ft.icons.ARROW_CIRCLE_UP, color=ft.colors.BLUE, size=24),ft.Text("Processando e enviando para o Banco de dados...")]
                Mysql_process_message.update()

                # Atualizar a tabela com os dados processados
                table_rows = []
                for item in processed_data:
                    item["Data"] = item["Data"].strftime("%d/%m/%Y") if item["Data"] else ""
                    item["Hora"] = item["Hora"].strftime("%H:%M:%S") if item["Hora"] else ""
                    
                    table_rows.append(DataRow(cells=[DataCell(Text(str(item[col]))) for col in item]))

                table.rows = table_rows
                table.update()

                # Enviar os dados processados para o MySQL
                insert_data_to_mysql(processed_data)
                Mysql_process_message.controls = [ft.Icon(name=ft.icons.CHECK_CIRCLE_OUTLINE, color=ft.colors.BLUE, size=24),ft.Text("Dados processados com sucesso")]
                Mysql_process_message.update()
            else:
                selected_files.value = "Erro ao processar o PDF"
                selected_files.update()

    pick_files_dialog = FilePicker(on_result=pick_files_result)
    selected_files = Text()
    download_excel_link = Text(value="")
    Mysql_process_message = ft.Row(controls=[ft.Text(value="")],)

    table = DataTable(
        columns=[DataColumn(Text("ID")), DataColumn(Text("Nome")), DataColumn(Text("Bloco")),
                 DataColumn(Text("Apto")), DataColumn(Text("Dispositivo")), DataColumn(Text("Saída")),
                 DataColumn(Text("Recurso")), DataColumn(Text("Status do Recurso")),
                 DataColumn(Text("Data")), DataColumn(Text("Hora"))],
        rows=[]
    )

    table_container = Container(
        content=Column([table], scroll="auto"),
        width="100%",
        height=600
    )

    page.overlay.append(pick_files_dialog)

    page.add(
        Row(
            [
                ElevatedButton(
                    "Selecionar PDF",
                    icon=icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=False),
                ),
                selected_files,
            ]
        ),
        Row([download_excel_link, Mysql_process_message]),
        table_container,
    )

ft.app(target=main)
