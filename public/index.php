<!DOCTYPE html>
<html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upload PDF</title>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="css/style.css">
        <script src="js/upload.js" defer></script>
    </head>
    <body>
        <div class="container mt-4">
            <h2>Envie o arquivo PDF</h2>
            <form id="pdf-upload-form" enctype="multipart/form-data">
                <div class="form-group">
                    <label for="pdf_file">Selecione o PDF:</label>
                    <input type="file" name="pdf_file" class="form-control-file" accept="application/pdf" required>
                </div>
                <div class="form-group">
                    <label for="pdf_model">Selecione o modelo do PDF:</label>
                    <select name="pdf_model" id="pdf_model" class="form-control" required>
                        <option value="">Selecione</option>
                        <option value="intelbras-v1" selected>Intelbras v.1</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary">Enviar PDF</button>
            </form>
            <div id="upload-result" class="mt-3"></div> <!-- Onde serão exibidos os resultados -->
        </div>
        
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
</html>