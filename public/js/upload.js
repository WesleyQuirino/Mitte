document.querySelector('#pdf-upload-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Previne o reload da página

    const formData = new FormData(this);
    const resultDiv = document.querySelector('#upload-result');

    // Exibe o GIF de carregamento
    resultDiv.innerHTML = `
        <div class="d-flex justify-content-center">
            <div class="spinner-border text-primary" role="status">
                <span class="sr-only">Loading...</span>
            </div>
        </div>`;

    // Envia os dados do formulário via AJAX usando Fetch API
    fetch('upload.php', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json()) // Converte a resposta para JSON
    .then(data => {
        console.log("data:",data);
        
        if (data.status === 'success') {
            return fetch('components/tableXlsx.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)  // Envia os dados recebidos para o componente PHP
            });
        } else {
            // Exibe mensagem de erro caso o status seja 'error'
            resultDiv.innerHTML = `<p>Erro: ${data.message}</p>`;
            throw new Error(data.message);
        }
    })
    .then(response => response.text()) // Obtém a resposta do componente PHP como texto (HTML)
    .then(html => {
        // Exibe o HTML retornado do componente PHP
        resultDiv.innerHTML = html;
    })
    .catch(error => {
        console.error('Erro:', error);
        resultDiv.innerHTML = `<p>Ocorreu um erro: ${error.message}</p>`;
    });
});