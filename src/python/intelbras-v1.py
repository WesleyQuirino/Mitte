import tabula
import pandas as pd
from datetime import datetime
import json
import sys
import os  # Para trabalhar com o nome do arquivo

def process_pdf(pdf_path):
    try:
        # Extrair o nome do arquivo PDF sem a extensão
        file_name = os.path.splitext(os.path.basename(pdf_path))[0]

        # Extraindo todas as tabelas do PDF
        tables = tabula.read_pdf(pdf_path, 
            pages="all", 
            multiple_tables=True, 
            relative_area=True, 
            relative_columns=True, 
            area=[12,0,90,100], 
            columns=[10, 30.5, 37, 45, 53, 60, 70, 80, 100]
        )

        if not tables or len(tables) == 0:
            raise ValueError("Nenhuma tabela foi extraída do PDF.")

        # Definir o cabeçalho personalizado
        custom_header = ["ID", "Nome", "Bloco", "Apto", "Dispositivo", "Saída", "Recurso", "Status do Recurso", "Data de registro"]

        # Lista para armazenar todas as tabelas processadas
        processed_tables = []

        # Iterar sobre todas as tabelas extraídas
        for table in tables:
            # Definir o cabeçalho personalizado para cada tabela
            table.columns = custom_header

            # Remover as linhas com índices de 0 a 1
            table = table.drop(table.index[0:2])

            # Adicionar a tabela processada à lista
            processed_tables.append(table)

        # Concatenar todas as tabelas em um único DataFrame
        final_table = pd.concat(processed_tables, ignore_index=True)

        # Substituir NaN por None (que será convertido para null no JSON)
        final_table = final_table.where(pd.notnull(final_table), None)

        # Converte o DataFrame para uma lista de dicionários (JSON)
        json_data = final_table.to_dict(orient='records')

        # Processar os dados como no exemplo anterior
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

        csv_data = processed_data
        
        for i in range(len(processed_data)):
            data_registro = processed_data[i]["Data de registro"]
            
            # Divide a data e a hora
            data, hora = data_registro.split(' ')
            
            # Atualiza o objeto com as novas chaves "Data" e "Hora" como objetos datetime
            processed_data[i]["Data"] = data
            processed_data[i]["Hora"] = hora
            
            # Remove a chave original "Data de registro"
            del processed_data[i]["Data de registro"]

        # Converte a lista final para JSON formatado
        json_string = json.dumps(processed_data, ensure_ascii=False, indent=4)

        # Criar o nome do arquivo JSON e CSV usando o nome do PDF
        json_output_path = f'./json/{file_name}.json'
        csv_output_path = f'./csv/{file_name}.csv'

        # Exportar os dados processados para um arquivo JSON
        with open(json_output_path, 'w', encoding='utf-8') as json_file:
            json_file.write(json_string)

        # Converter o processed_data para um DataFrame e exportar para CSV
        processed_df = pd.DataFrame(processed_data)
        processed_df.to_csv(csv_output_path, index=False, encoding='utf-8-sig')

        # Retornar o JSON processado como string
        return json_string
    except Exception as e:
        # Redirecionar a mensagem de erro para o stderr
        sys.stderr.write(f"Erro ao processar o PDF: {str(e)}\n")
        return None
# Receber o caminho do PDF como argumento
if __name__ == "__main__":
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        result = process_pdf(pdf_path)

        if result:
            # Se o JSON foi gerado com sucesso, exibir no stdout
            print(result)
        else:
            # Se houve erro, retornar uma mensagem clara
            sys.stderr.write("Erro ao processar o JSON.\n")
    else:
        sys.stderr.write("Por favor, forneça o caminho para o arquivo PDF como argumento.\n")