document.getElementById('image-input').addEventListener('change', function (event) {
    const file = event.target.files[0];
    const imagePreview = document.getElementById('image-preview');

    if (file) {
        const fileURL = URL.createObjectURL(file);
        imagePreview.src = fileURL;
        imagePreview.style.display = 'block';
    }
});

document.getElementById('previous-button').addEventListener('click', function () {
    alert("Bouton 'Précédent' cliqué !");
});

document.getElementById('analyze-button').addEventListener('click', async function () {
    const fileInput = document.getElementById('image-input');
    const resultDiv = document.getElementById('result');

    // Vérifie si un fichier a été sélectionné
    if (!fileInput.files[0]) {
        resultDiv.textContent = "Veuillez sélectionner une image avant d'analyser.";
        return;
    }

    // Prépare les données à envoyer (FormData pour inclure le fichier)
    const formData = new FormData();
    formData.append('image', fileInput.files[0]);

    try {
		resultDiv.textContent ="Patientez s'il vous plaît!";
		
        // Effectue une requête POST vers l'API Flask
        const response = await fetch('http://127.0.0.1:5000/api/cancer_prostate/predict',{
            method: 'POST',
            body: formData,
        });

        // Vérifie si la réponse est correcte
		if (response.ok) {
			const data = await response.json();
			
            if (data.cancer_prostate) {
                resultDiv.textContent = `Cancer détecté : ${data.cancer_prostate}`;
            } else {
                resultDiv.textContent  = "Aucun cancer de prostate détecté.";
            }
        } else {
            const errorData = await response.json();
            resultDiv.textContent = `Erreur : ${errorData.error}`;
        }
 
    } catch (error) {
        // Gestion des erreurs réseau ou autres
        resultDiv.textContent = `Erreur lors de la communication avec le serveur : ${error.message}`;
    }
});

