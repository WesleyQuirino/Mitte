<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload PDF</title>
</head>
<body>
    <h2>Envie o arquivo PDF</h2>
    <form action="index.php" method="post" enctype="multipart/form-data">
        Selecione o PDF:
        <input type="file" name="pdf_file" accept="application/pdf" required>
        <input type="submit" name="submit" value="Enviar PDF">
    </form><?php

    if (isset($_FILES['pdf_file'])) {
        $upload_dir = 'uploads/';
        
        // Verifica se o diretório existe, caso contrário, cria
        if (!is_dir($upload_dir)) {
            mkdir($upload_dir, 0755, true);
        }

        $uploaded_file = $upload_dir . basename($_FILES['pdf_file']['name']);

        // Mover o arquivo para o diretório de uploads
        if (move_uploaded_file($_FILES['pdf_file']['tmp_name'], $uploaded_file)) {
            echo "<p>Arquivo PDF enviado com sucesso.</p>";

            // Testar se o arquivo foi enviado corretamente
            if (file_exists($uploaded_file)) {
                echo "<p>Arquivo disponível para processamento: $uploaded_file</p>";
            } else {
                echo "<p>Arquivo não foi encontrado no diretório de uploads.</p>";
            }

            // Chamar o script Python passando o caminho do arquivo
            $command = escapeshellcmd("python intelbras-v1.py " . escapeshellarg($uploaded_file));
            shell_exec($command . " 2>&1"); // Executa o script Python

            // Verificar se o arquivo JSON foi gerado
            $json_file = 'output.json'; // Arquivo JSON gerado pelo Python

            if (file_exists($json_file)) {
                // Ler e decodificar o arquivo JSON
                $json_data = json_decode(file_get_contents($json_file), true);
                $processed_data = array();
                $previous_item = array();

                for ($i = 0; $i < count($json_data); $i++) {
                    if (empty($json_data[$i]["ID Nome"])) {
                        foreach ($json_data[$i] as $json_data_key => $json_data_value) {
                            if (!empty($json_data_value)) {
                                if (!empty($previous_item[$json_data_key])) {
                                    if (strpos($previous_item[$json_data_key], $json_data_value) === false) {
                                        $previous_item[$json_data_key] .= " " . $json_data_value;
                                    }
                                } else {
                                    $previous_item[$json_data_key] = $json_data_value;
                                }
                            }
                        }
                        $processed_data[count($processed_data) - 1] = $previous_item;
                    } else {
                        $previous_item = $json_data[$i];
                        $processed_data[] = $previous_item;
                    }
                }

                if ($processed_data) {
                    echo "<h3>Dados processados:</h3>";
                    echo "<pre>" . json_encode($processed_data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "</pre>";
                } else {
                    echo "<p>Erro ao processar o arquivo JSON.</p>";
                }
            } else {
                echo "<p>Erro: arquivo JSON não encontrado.</p>";
            }
        } else {
            echo "<p>Erro ao enviar o arquivo.</p>";
        }
    }?>
</body>
</html>
