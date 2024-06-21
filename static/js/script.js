document.getElementById('upload').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('result');
            const uploadButton = document.getElementById('upload');
            const modal = document.getElementById('modal');
            const yesButton = document.getElementById('yesButton');
            const noButton = document.getElementById('noButton');

            uploadButton.classList.add('hidden');

            if (data.face_detected) {
                modal.style.display = "block";

                yesButton.onclick = function() {
                    modal.style.display = "none";
                    fetch('/replace', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ image_url: data.image_url })
                    })
                    .then(response => response.json())
                    .then(data => {
                        resultDiv.innerHTML = `<p>Face replaced! Here is your modified photo:</p><img src="${data.image_url}" alt="Modified Photo">`;
                    });
                };

                noButton.onclick = function() {
                    modal.style.display = "none";
                    resultDiv.innerHTML = `<p>Here is your original photo:</p><img src="${data.image_url}" alt="Original Photo">`;
                };
            } else {
                resultDiv.innerHTML = `<p>No face detected. Here is your original photo:</p><img src="${data.image_url}" alt="Original Photo">`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});