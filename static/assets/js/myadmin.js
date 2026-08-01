//Show Counter
document.addEventListener('DOMContentLoaded', function () {
    const inputs = document.querySelectorAll('input[type="text"], input[type="password"], textarea');

    inputs.forEach(function (input) {
        if (input.id !== 'searchbar') {
            const counter = document.createElement('div');
            counter.classList.add('char-word-counter');
            input.parentNode.insertBefore(counter, input.nextSibling);

            const updateCounter = () => {
                const value = input.value;
                const charCount = value.length;
                const wordCount = value.trim().split(/\s+/).filter(Boolean).length;
                counter.textContent = `Words : ${wordCount} Characters : ${charCount}`;
            };

            updateCounter();

            input.addEventListener('input', updateCounter);
        }
    });
});



// Show Image
document.addEventListener('DOMContentLoaded', function () {
    const fileInputs = document.querySelectorAll('input[type="file"]');

    fileInputs.forEach(function (fileInput) {
        const imagePreview = document.createElement('img');
        imagePreview.classList.add('image-preview');
        fileInput.parentNode.insertBefore(imagePreview, fileInput.nextSibling);

        const updatePreview = () => {
            const file = fileInput.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    imagePreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            } else {
                imagePreview.src = '';
            }
        };

        updatePreview();

        fileInput.addEventListener('change', updatePreview);
    });
});

// DATE
document.addEventListener('DOMContentLoaded', function() {
    const dateInputs = document.querySelectorAll('.vDateField');
    
    dateInputs.forEach(function(input) {
        // Change input type to date
        input.setAttribute('type', 'date');
        
        // Remove the <span> tag containing the calendar icon
        const span = input.parentNode.querySelector('.datetimeshortcuts');
        if (span) {
            span.parentNode.removeChild(span);
        }
        
        // Remove the <div> elements with the class "char-word-counter"
        const counterDiv = input.parentNode.querySelector('.char-word-counter');
        if (counterDiv) {
            counterDiv.parentNode.removeChild(counterDiv);
        }
    });
});

// Password
(document).ready(function() {
    // Target the password input elements and add a class
    $('input[type="password"]').addClass('vTextField');
});
