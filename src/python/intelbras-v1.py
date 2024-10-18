import tabula
import pandas as pd
import json
import sys

# Função principal para processar o PDF
def process_pdf(pdf_path):
    try:
        # Extraindo todas as tabelas do PDF
        tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)

        # Definir o cabeçalho personalizado
        custom_header = ["ID Nome", "Bloco", "Apto", "Dispositivo", "Saída", 
                         "Recurso", "Status do Recurso", "Data de registro"]

        # Lista para armazenar todas as tabelas processadas
        processed_tables = []

        # Iterar sobre todas as tabelas extraídas
        for table in tables:
            # Definir o cabeçalho personalizado para cada tabela
            table.columns = custom_header

            # Remover as linhas com índices de 0 a 3
            table = table.drop(table.index[0:4])

            # Adicionar a tabela processada à lista
            processed_tables.append(table)

        # Concatenar todas as tabelas em um único DataFrame
        final_table = pd.concat(processed_tables, ignore_index=True)

        # Substituir NaN por None (que será convertido para null no JSON)
        final_table = final_table.where(pd.notnull(final_table), None)

        # Converte o DataFrame para uma lista de dicionários (JSON)
        json_data = final_table.to_dict(orient='records')

        # Processar os dados para combinar as linhas onde "ID Nome" está vazio
        processed_data = json_data

        # Exportar os dados processados para um arquivo JSON
        with open('json/output.json', 'w', encoding='utf-8') as json_file:
            json.dump(processed_data, json_file, indent=4, ensure_ascii=False)

        # Retornar o JSON processado como string
        return json.dumps(processed_data, indent=4, ensure_ascii=False)

    except Exception as e:
        # Redirecionar a mensagem de erro para o stderr
        sys.stderr.write(f"Erro ao processar o PDF: {str(e)}\n")
        return None

# Receber o caminho do PDF como argumento
if __name__ == "__main__":
    pdf_path = sys.argv[1]
    result = process_pdf(pdf_path)

    if result:
        # Se o JSON foi gerado com sucesso, exibir no stdout
        print(result)
    else:
        # Se houve erro, retornar uma mensagem clara
        sys.stderr.write("Erro ao processar o JSON.\n")
