// Adiciona event listener ao formulário para prevenir o envio padrão e usar AJAX
document.querySelector('#pdf-upload-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Previne o reload da página

    const formData = new FormData(this);
    console.log(formData);

    // Envia os dados do formulário via AJAX usando Fetch API
    fetch('upload.php', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json()) // Converte a resposta para JSON
    .then(data => {
        const resultDiv = document.querySelector('#upload-result');
        if (data.status === 'success') {
            resultDiv.innerHTML = `<h3>Dados processados:</h3><pre>${JSON.stringify(data.data, null, 2)}</pre>`;
        } else {
            resultDiv.innerHTML = `<p>Erro: ${data.message}</p>`;
        }
    })
    .catch(error => console.error('Erro:', error));
});
