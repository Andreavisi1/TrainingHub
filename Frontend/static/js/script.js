document.addEventListener('DOMContentLoaded', () => {
    // Gestione caricamento file
    const fileInputs = document.querySelectorAll('.file-input');
    
    fileInputs.forEach(fileInput => {
        const fileChosen = fileInput.closest('.file-upload-wrapper').querySelector('.file-chosen');
        
        fileInput.addEventListener('change', function() {
            if (this.files && this.files.length > 0) {
                fileChosen.textContent = this.files[0].name;
                fileChosen.style.color = 'var(--primary-color)';
            } else {
                fileChosen.textContent = 'Nessun file selezionato';
                fileChosen.style.color = '';
            }
        });
    });

    // Gestione form di upload (se presente)
    const uploadForms = document.querySelectorAll('#upload-form');
    
    uploadForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const fileInput = form.querySelector('.file-input');
            const loadingOverlay = document.getElementById('loading-overlay');
            
            if (!fileInput.files.length) {
                e.preventDefault();
                alert('Seleziona un documento prima di procedere');
                return;
            }

            // Validazione dimensione file
            const fileSize = fileInput.files[0].size;
            const maxSize = 16 * 1024 * 1024; // 16 MB

            if (fileSize > maxSize) {
                e.preventDefault();
                alert('Il file è troppo grande. Dimensione massima: 16 MB');
                return;
            }

            // Mostra overlay di caricamento
            if (loadingOverlay) {
                loadingOverlay.style.display = 'flex';
            }
        });
    });

    // Gestione generazione quiz (nelle pagine dei risultati)
    const generateQuizBtns = document.querySelectorAll('#generate-quiz-btn');
    generateQuizBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            alert('Funzionalità di generazione quiz in sviluppo');
        });
    });

    // Gestione download report
    const downloadReportBtns = document.querySelectorAll('#download-report-btn');
    downloadReportBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            alert('Funzionalità di download report in sviluppo');
        });
    });
});


