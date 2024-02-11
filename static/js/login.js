const passwordVisibilityIcon = document.getElementById('show-icon');
const passwordInputField = document.getElementById('password-input-field');
const usernameInputField = document.getElementById('username-input-field');

const usernameError = document.querySelector('.username-error');
const passwordError = document.querySelector('.password-error');

const usernameLabel = document.querySelector('#username-label');
const submitBtn = document.querySelector('#submit-btn');

const loginForm = document.querySelector('form');

passwordVisibilityIcon.addEventListener('click', () => {
    if (passwordInputField.type === 'password') {
        passwordInputField.type = 'text';
        passwordVisibilityIcon.className = "view-hide";
    } else {
        passwordInputField.type = 'password';
        passwordVisibilityIcon.className = "view-show";
    }
});

let usernameIsValid, passwordIsValid;

// function to check is string contains @
function checkForAtSign(string) {
    return string.includes('@');
}

// regex to check valid email format
let emailRegex = new RegExp('[a-z0-9]+@[a-z]+\.[a-z]{2,3}');
// function to check if email is valid
function validateEmail(email) {
    return emailRegex.test(email);
}

function validateUsername() {
    usernameIsValid = false;
    usernameLabel.textContent = 'Username or Email';
    if (usernameInputField.value === '') {
        usernameError.textContent = 'Username or Email is required';
        submitBtn.setAttribute('disabled', '');
        return;
    }
    if (checkForAtSign(usernameInputField.value)) {
        usernameLabel.textContent = 'Email';
        if (!validateEmail(usernameInputField.value)) {
            usernameError.textContent = 'Invalid Email';
            submitBtn.setAttribute('disabled', '');
            return;
        }
    }
    usernameError.textContent = '';
    usernameIsValid = true;
    if (passwordIsValid) {
        submitBtn.removeAttribute('disabled');
    }
    return;
}
usernameInputField.addEventListener('input', () => {
    validateUsername();
    if (passwordInputField.value !== '') {
        validatePassword();
    };
});


// regex to check if string contains at least one uppercase letter
const uppercaseRegex = /[A-Z]/;
// function to check password for uppercase letter
function checkPasswordForUppercase(password) {
    return uppercaseRegex.test(password);
}

// regex to check if string contains at least a number
const numberRegex = /[0-9]/;
// function to check password for number
function checkPasswordForNumber(password) {
    return numberRegex.test(password);
}

// regex to check if string contains at least a special character
const specialCharacterRegex = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/;
// function to check password for special character
function checkPasswordForSpecialCharacter(password) {
    return specialCharacterRegex.test(password);
}

function validatePassword() {
    passwordIsValid = false;
    if (passwordInputField.value === '') {
        passwordError.textContent = 'Password is required';
        submitBtn.setAttribute('disabled', '');
        return;
    }
    // if(passwordInputField.value.length < 8) {
    //     passwordError.textContent = 'Password must be at least 8 characters';
    //     submitBtn.setAttribute('disabled', '');
    //     return;
    // }
    // if(!checkPasswordForUppercase(passwordInputField.value)) {
    //     passwordError.textContent = 'Password must contain at least one uppercase letter';
    //     submitBtn.setAttribute('disabled', '');
    //     return;
    // }
    // if(!checkPasswordForNumber(passwordInputField.value)) {
    //     passwordError.textContent = 'Password must contain at least a number';
    //     submitBtn.setAttribute('disabled', '');
    //     return;
    // }
    // if(!checkPasswordForSpecialCharacter(passwordInputField.value)) {
    //     passwordError.textContent = 'Password must contain at least a special character';
    //     submitBtn.setAttribute('disabled', '');
    //     return;
    // }
    passwordError.textContent = '';
    passwordIsValid = true;
    if (usernameIsValid) {
        submitBtn.removeAttribute('disabled');
    }
    passwordError.textContent = '';
    passwordIsValid = true;
    if (usernameIsValid) {
        submitBtn.removeAttribute('disabled');
    }
    return;
};
passwordInputField.addEventListener('input', () => {
    validatePassword();
    if (usernameInputField.value !== '') {
        validateUsername();
    };
});

const validateLogin = () => {
    validateUsername();
    validatePassword();
};

loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    validateLogin();
    if (usernameIsValid && passwordIsValid) {
        loginForm.submit();
    }
});