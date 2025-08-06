document.addEventListener('DOMContentLoaded', () => {
            const toggleButton = document.getElementById('dark-mode-toggle');
            const body = document.body;
    
            toggleButton.addEventListener('click', () => {
                fetch("/adocato/toogle-dark-mode/")
                .then(response => response.json())
                .then(data => {
                    if (data.dark_mode) {
                        body.classList.add('dark-mode');
                        toggleButton.textContent = 'Modo Claro';
                    } else {
                        body.classList.remove('dark-mode');
                        toggleButton.textContent = 'Modo Escuro';
                    }
                });
            });
        });