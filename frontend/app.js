document.getElementById('register-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const mobileNumber = document.getElementById('mobile-number').value;
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ mobile_number: mobileNumber })
    }).then(response => response.json())
      .then(data => {
          alert(data.message);
          document.getElementById('verification-section').