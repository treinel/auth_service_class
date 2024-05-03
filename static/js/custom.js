(function() {

    'use strict';

    var elToggle = document.querySelector('.js-password-show-toggle'),
        passwordInput = document.getElementById('password');

        elToggle.addEventListener('click', (e) => {
            e.preventDefault();

            if ( elToggle.classList.contains('active') ) {
                passwordInput.setAttribute('type', 'password');
                elToggle.classList.remove('active');
            } else {
                passwordInput.setAttribute('type', 'text');
                elToggle.classList.add('active');
            }
        })

})();


document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signupForm');
    const loginForm = document.getElementById('loginForm');

    if (signupForm) {
        signupForm.addEventListener('submit', function(event) {
            handleSignupSubmit(event);
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            handleLoginSubmit(event);
        });
    }
});

function handleSignupSubmit(event) {
    event.preventDefault();
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        username: document.getElementById('username').value,
        role: document.getElementById('role').value,
        cel: document.getElementById('tel').value,
    };
    // Enviar los datos como JSON
    fetch('http://127.0.0.1:8000/users/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (response.ok) {
            return response.json(); 
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
}

function handleLoginSubmit(event) {
    event.preventDefault();
    const formData = {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value
    };
    // Enviar los datos como JSON
    fetch('http://127.0.0.1:8000/auth/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (response.ok) {
            return response.json(); 
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
}