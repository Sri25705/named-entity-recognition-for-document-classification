document.addEventListener('DOMContentLoaded', function () {

    // Handle form validation for login page
    const loginForm = document.querySelector('#loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // Basic validation for empty fields
            if (!email || !password) {
                alert("Please fill in both email and password!");
                event.preventDefault();  // Prevent form submission
            }
        });
    }

    // Handle form validation for register page
    const registerForm = document.querySelector('#registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function (event) {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;

            // Check if passwords match
            if (password !== confirmPassword) {
                alert("Passwords do not match!");
                event.preventDefault();  // Prevent form submission
            }

            // Basic validation for empty fields
            if (!email || !password || !confirmPassword) {
                alert("Please fill in all the fields!");
                event.preventDefault();  // Prevent form submission
            }
        });
    }

    // Handle file upload validation for document upload page
    const uploadForm = document.querySelector('#uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function (event) {
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];

            // Check if a file is selected
            if (!file) {
                alert("Please select a file to upload!");
                event.preventDefault();  // Prevent form submission
            }

            // Validate file type (accepts pdf, docx, txt files)
            const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
            if (!validTypes.includes(file.type)) {
                alert("Invalid file type! Only PDF, DOCX, and TXT files are allowed.");
                event.preventDefault();  // Prevent form submission
            }
        });
    }

    // Handle highlighting of entities on the highlight page
    const highlightButton = document.querySelector('#highlightButton');
    if (highlightButton) {
        highlightButton.addEventListener('click', function () {
            // Simulate highlighting of entities in text (this can be replaced with actual NER logic)
            const textArea = document.querySelector('#documentText');
            let text = textArea.value;

            // Example: Highlighting words like 'person' and 'organization' (basic example)
            const highlightedText = text.replace(/\b(person|organization)\b/gi, function (match) {
                return `<span style="background-color: yellow">${match}</span>`;
            });

            // Display the highlighted text
            document.querySelector('#highlightedText').innerHTML = highlightedText;
        });
    }

});
