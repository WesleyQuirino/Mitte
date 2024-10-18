<?php
namespace App;

class FileUploader{
    private $uploadDir;

    public function __construct($uploadDir = 'uploads/'){
        $this->uploadDir = $uploadDir;
        if (!is_dir($this->uploadDir)) {
            mkdir($this->uploadDir, 0755, true);
        }
    }

    public function uploadFile($file){
        $uploadedFile = "C:/Users/Wesley/Desktop/Mitte/public/uploads/" . basename($file['name']);
        if (move_uploaded_file($file['tmp_name'], $uploadedFile)) {
            return $uploadedFile;
        }
        return false;
    }
}