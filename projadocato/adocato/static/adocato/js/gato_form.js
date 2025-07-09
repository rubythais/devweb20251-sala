    // Preview da imagem selecionada e atualizar nome do arquivo
    document.getElementById('id_foto').addEventListener('change', function(e) {
        const file = e.target.files[0];
        const fileName = document.getElementById('file-name');
        
        if (file) {
            fileName.textContent = file.name;
            
            // Preview da imagem
            const reader = new FileReader();
            reader.onload = function(e) {
                // Remove preview anterior se existir
                const existingPreview = document.getElementById('foto-preview');
                if (existingPreview) {
                    existingPreview.remove();
                }
                
                // Cria novo preview
                const preview = document.createElement('div');
                preview.id = 'foto-preview';
                preview.className = 'mt-2';
                preview.innerHTML = `
                    <p class="help">Preview:</p>
                    <figure class="image is-96x96">
                        <img src="${e.target.result}" alt="Preview" class="is-rounded">
                    </figure>
                `;
                
                // Adiciona o preview após o campo de arquivo
                e.target.closest('.field').appendChild(preview);
            };
            reader.readAsDataURL(file);
        } else {
            fileName.textContent = 'Nenhum arquivo selecionado';
        }
    });