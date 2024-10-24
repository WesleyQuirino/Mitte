<?php
// Obtém o JSON enviado pelo fetch
$inputData = file_get_contents('php://input');

// Decodifica o JSON para um array associativo em PHP
$data = json_decode($inputData, true);

// Verifica se a decodificação foi bem-sucedida
if ($data !== null) {
    // Agora você pode acessar os dados enviados
    // Por exemplo, se o JSON tem uma chave 'status', você pode fazer:
    $status = $data['status'];
    $processedData = $data['data'];
    $fileName = pathinfo($data['file_name'], PATHINFO_FILENAME) . '.xlsx';
    // Processa os dados conforme necessário?>
    <a href="excel/<?php echo $fileName; ?>" download class="btn btn-success mb-3">Baixar o arquivo</a>
    <table class="table table-striped table-bordered" style="width: 100%;">
        <thead class="thead-dark">
            <tr><?php 
                foreach ($processedData[0] as $key => $value) { ?>
                    <th scope="col"><?php echo $key; ?></th><?php
                }?>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($processedData as $acesso) { ?>
                <tr>
                    <?php foreach ($acesso as $key => $value) { ?>
                        <td><?php echo $value; ?></td><?php
                    }?>
                </tr>
            <?php } ?>
        </tbody>
    </table><?php
} else {
    // Envia uma resposta de erro se o JSON não pôde ser processado
    echo json_encode([
        'status' => 'error',
        'message' => 'Erro ao decodificar JSON'
    ]);
}