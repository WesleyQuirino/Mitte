<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upload PDF</title>
        <script src="js/upload.js" defer></script>
    </head>
    <body>
        <h2>Envie o arquivo PDF</h2>

        <!-- Formulário para envio de PDF -->
        <form id="pdf-upload-form" enctype="multipart/form-data">
            Selecione o PDF:
            <input type="file" name="pdf_file" accept="application/pdf" required>
            
            <!-- Campo para selecionar o modelo de PDF -->
            <label for="pdf_model">Selecione o modelo de processamento:</label>
            <select name="pdf_model" id="pdf_model" required>
                <option value="intelbras-v1">Intelbras v.1</option>
                <option value="outro_modelo">Outro Modelo</option>
            </select>

            <input type="submit" value="Enviar PDF">
        </form>

        <div id="upload-result"></div> <!-- Onde serão exibidos os resultados -->
    </body>
</html>