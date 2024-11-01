<?php
namespace App;

class PdfProcessor {
    private $filePath;
    private $model;

    public function __construct($filePath, $model) {
        $this->filePath = $filePath;
        $this->model = $model;
    }

    public function process() {
        $pythonScript = '';

        // Extrair o nome do arquivo PDF sem a extensão
        $fileName = pathinfo($this->filePath, PATHINFO_FILENAME);

        // Escolhe o script Python com base no modelo
        switch ($this->model) {
            case 'intelbras-v1':
                $pythonScript =  __DIR__ . DIRECTORY_SEPARATOR .'.' . DIRECTORY_SEPARATOR .'python' . DIRECTORY_SEPARATOR . 'intelbras-v1.py';
                // Executa o script Python correspondente
                $command = escapeshellcmd("python $pythonScript " . escapeshellarg($this->filePath));
                shell_exec($command . " 2>&1"); // Executa o script Python

                // Verifica se o arquivo JSON foi gerado
                $jsonFile = __DIR__ . DIRECTORY_SEPARATOR .'..' . DIRECTORY_SEPARATOR . 'public' . DIRECTORY_SEPARATOR . 'json' . DIRECTORY_SEPARATOR . $fileName . '.json';
                if (!file_exists($jsonFile)) {
                    return ['status' => 'error', 'message' => 'Erro: arquivo JSON não foi gerado.'];
                }
                break;
            case 'outro_modelo':
                $pythonScript = 'outro_modelo.py';
                break;
            default:
                return null;
        }

        // Verifica se o arquivo JSON tem conteúdo
        $jsonContent = file_get_contents($jsonFile);
        if (empty($jsonContent)) {
            return ['status' => 'error', 'message' => 'Erro: arquivo JSON está vazio.'];
        }

        // Tenta decodificar o arquivo JSON
        $jsonData = json_decode($jsonContent, true);
        if ($jsonData === null && json_last_error() !== JSON_ERROR_NONE) {
            return ['status' => 'error', 'message' => 'Erro: JSON inválido.'];
        }

        return $jsonData; // Retorna o conteúdo do JSON
    }
}