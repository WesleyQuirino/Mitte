<?php
    namespace App;
    require_once '../src/FileUploader.php';
    require_once '../src/PdfProcessor.php';

    if (isset($_FILES['pdf_file']) && isset($_POST['pdf_model'])) {
        $pdf_model = $_POST['pdf_model'];
        $uploader = new FileUploader('uploads/');

        // Realiza o upload do arquivo PDF
        $uploaded_file = $uploader->uploadFile($_FILES['pdf_file']);

        if ($uploaded_file) {
            // Inicializa o processador de PDF com base no modelo selecionado
            $processor = new PdfProcessor($uploaded_file, $pdf_model);

            // Processa o PDF e retorna os dados processados
            $json_data = $processor->process();

            if ($json_data) {
                // Envia resposta de sucesso com os dados
                echo json_encode(['status' => 'success', 'data' => $json_data, 'file_name' => $_FILES['pdf_file']['name']]);
            } else {
                echo json_encode(['status' => 'error', 'message' => 'Erro ao processar o arquivo JSON.']);
            }
        } else {
            echo json_encode(['status' => 'error', 'message' => 'Erro ao enviar o arquivo.']);
        }
    }