    const fileInput = document.getElementById('fileInput');
    const dropZone = document.getElementById('drop-zone');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultArea = document.getElementById('result-area');
    const predictionText = document.getElementById('prediction-text');

    dropZone.onclick = () => fileInput.click();

    fileInput.onchange = (e) => {
        const [file] = fileInput.files;
        if (file) {
            imagePreview.src = URL.createObjectURL(file);
            previewContainer.classList.remove('hidden');
            resultArea.classList.add('hidden');
            analyzeBtn.innerText = "Провести анализ";
        }
    };

    analyzeBtn.onclick = async () => {
        if (!fileInput.files[0]) return;

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        analyzeBtn.disabled = true;
        analyzeBtn.innerText = "Нейросеть думает...";

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            // Показываем результат
            resultArea.classList.remove('hidden');
            predictionText.innerText = data.prediction;

            // ВАЖНО: Обновляем картинку на ту, что с рамками детекции
            // Добавляем timestamp, чтобы браузер не брал старую версию из кэша
            imagePreview.src = data.image_url + "?t=" + new Date().getTime();

            analyzeBtn.innerText = "Готово!";
        } catch (error) {
            console.error(error);
            alert("Ошибка при связи с сервером");
            analyzeBtn.innerText = "Провести анализ";
        } finally {
            analyzeBtn.disabled = false;
        }
    };

    // Поддержка Drag-and-Drop
    dropZone.ondragover = (e) => { e.preventDefault(); dropZone.classList.add('border-blue-500'); };
    dropZone.ondragleave = () => dropZone.classList.remove('border-blue-500');
    dropZone.ondrop = (e) => {
        e.preventDefault();
        fileInput.files = e.dataTransfer.files;
        fileInput.onchange();
    };