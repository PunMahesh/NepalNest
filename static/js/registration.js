const usernameField = document.getElementById('username-field');
const usernameError = document.querySelector('.username-error');

const firstnameField = document.getElementById('firstname-field');
const firstnameError = document.querySelector('.firstname-error');

const lastnameField = document.getElementById('lastname-field');
const lastnameError = document.querySelector('.lastname-error');

const emailField = document.getElementById('email-field');
const emailError = document.querySelector('.email-error');

const addressField = document.getElementById('address-field');
const addressError = document.querySelector('.address-error');

const contactField = document.getElementById('contact-field');
const contactError = document.querySelector('.contact-error');

const password1Field = document.getElementById('password1-field');
const password1Error = document.querySelector('.password1-error');

const password2Field = document.getElementById('password2-field');
const password2Error = document.querySelector('.password2-error');

const submitBtn = document.querySelector('#submit-btn');
const registerForm = document.querySelector('form');

let usernameIsValid, firstnameIsValid, lastnameIsValid, emailIsValid, addressIsValid, contactIsValid, password1IsValid, password2IsValid;

// function to check is string contains @
function checkForAtSign(string) {
    return string.includes('@');
}

function validateUsername() {
    usernameIsValid = false;
    if (usernameField.value === '') {
        usernameError.textContent = 'Username is required';
        submitBtn.setAttribute('disabled', '');
        return;
    }
    if(checkForAtSign(usernameField.value)) {
        usernameError.textContent = 'Username cannot contain @';
        submitBtn.setAttribute('disabled', '');
        return;
    }

    usernameError.textContent = '';
    usernameIsValid = true;
    if (firstnameIsValid && lastnameIsValid && emailIsValid && addressIsValid && contactIsValid && password1IsValid && password2IsValid) {
        submitBtn.removeAttribute('disabled');
    }
    return;
}
usernameField.addEventListener('input', () => {
    validateUsername();
});

function validateFullname() {
    firstnameIsValid = false;
    if (firstnameField.value === '') {
        firstnameError.textContent = 'Name is required';
        submitBtn.setAttribute('disabled', '');
        return;
    }

    firstnameError.textContent = '';
    firstnameIsValid = true;
    if (usernameIsValid && lastnameIsValid && emailIsValid && addressIsValid && contactIsValid && password1IsValid && password2IsValid) {
        submitBtn.removeAttribute('disabled');
    }
    return;
}
firstnameField.addEventListener('input', () => {
    validateFirstname();
});

function validateLastname() {
    lastnameIsValid = false;
    if (lastnameField.value === '') {
        lastnameError.textContent = 'Lastname is required';
        submitBtn.setAttribute('disabled', '');
        return;
    }

    lastnameError.textContent = '';
    lastnameIsValid = true;
    if (usernameIsValid && firstnameIsValid && emailIsValid && addressIsValid && contactIsValid && password1IsValid && password2IsValid) {
        submitBtn.removeAttribute('disabled');
    }
    return;
}
lastnameField.addEventListener('input', () => {
    validateLastname();
});

// regex to check valid email format
let emailRegex = new RegExp('[a-z0-9]+@[a-z]+\.[a-z]{2,3}');
// function to check if email is valid
function validateEmail(email) {
    return emailRegex.test(email);
}

function validateEmail() {
    emailIsValid = false;
    if (emailField.value === '') {
        emailError.textContent = 'Email is required';
        submitBtn.setAttribute('disabled', '');
        return;
    }
    // if(!validateEmail(emailField.value)) {
    //     emailError.textContent = 'Invalid Email';
    //     submitBtn.setAttribute('disabled', '');
    //     return;
    // }

    emailError.textContent = '';
    emailIsValid = true;
    if (usernameIsValid && firstnameIsValid && lastnameIsValid && addressIsValid && contactIsValid && password1IsValid && password2IsValid) {
        submitBtn.removeAttribute('disabled');
    }
    return;
}
emailField.addEventListener('input', () => {
    validateEmail();
});

function validateAddress() {
    addressIsValid = false;
    if (addressField.value === '') {
        addressError.textContent = 'Address is required';
        submitBtn.setAttribute('disabled', '');
        return;
    }

    addressError.textContent = '';
    addressIsValid = true;
    if (usernameIsValid && firstnameIsValid && lastnameIsValid && emailIsValid && contactIsValid && password1IsValid && password2IsValid) {
        submitBtn.removeAttribute('disabled');
    }
    return;
}
addressField.addEventListener('input', () => {
    validateAddress();
});

function validateContact() {
    contactIsValid = false;
    if (contactField.value === '') {
        contactError.textContent = 'Contact is required';
        submitBtn.setAttribute('disabled', '');
        return;
    }
    if (isNaN(contactField.value)) {
        contactError.textContent = 'Contact must be a number';
        submitBtn.setAttribute('disabled', '');
        return;
    }
    if (contactField.value[0] !== '9' && contactField.value[1] !== '8') {
        contactError.textContent = 'Contact must start with 98';
        submitBtn.setAttribute('disabled', '');
        return;
    }
    if (contactField.value.length !== 10) {
        contactError.textContent = 'Contact must be 10 digits';
        submitBtn.setAttribute('disabled', '');
        return;
    }

    contactError.textContent = '';
    contactIsValid = true;
    if (usernameIsValid && firstnameIsValid && lastnameIsValid && emailIsValid && addressIsValid && password1IsValid && password2IsValid) {
        submitBtn.removeAttribute('disabled');
    }
    return;
}
contactField.addEventListener('input', () => {
    validateContact();
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

function validatePassword1() {
    password1IsValid = false;
    if (password1Field.value === '') {
        password1Error.textContent = 'Password is required';
        submitBtn.setAttribute('disabled', '');
        return;
    }
    if(password1Field.value.length < 8) {
        password1Error.textContent = 'Password must be at least 8 characters';
        submitBtn.setAttribute('disabled', '');
        return;
    }
    if(!checkPasswordForUppercase(password1Field.value)) {
        password1Error.textContent = 'Password must contain at least one uppercase letter';
        submitBtn.setAttribute('disabled', '');
        return;
    }
    if(!checkPasswordForNumber(password1Field.value)) {
        password1Error.textContent = 'Password must contain at least a number';
        submitBtn.setAttribute('disabled', '');
        return;
    }
    // if(!checkPasswordForSpecialCharacter(password1Field.value)) {
    //     password1Error.textContent = 'Password must contain at least a special character';
    //     submitBtn.setAttribute('disabled', '');
    //     return;
    // }
    password1Error.textContent = '';
    password1IsValid = true;
    if (usernameIsValid && firstnameIsValid && lastnameIsValid && emailIsValid && addressIsValid && contactIsValid && password2IsValid) {
        submitBtn.removeAttribute('disabled');
    }
    return;
}
password1Field.addEventListener('input', () => {
    validatePassword1();
});

function validatePassword2() {
    password2IsValid = false;
    if (password2Field.value === '') {
        password2Error.textContent = 'Confirm Password is required';
        submitBtn.setAttribute('disabled', '');
        return;
    }
    if(password2Field.value !== password1Field.value) {
        password2Error.textContent = 'Password does not match';
        submitBtn.setAttribute('disabled', '');
        return;
    }
    password2Error.textContent = '';
    password2IsValid = true;
    if (usernameIsValid && firstnameIsValid && lastnameIsValid && emailIsValid && addressIsValid && contactIsValid && password1IsValid) {
        submitBtn.removeAttribute('disabled');
    }
    return;
}
password2Field.addEventListener('input', () => {
    validatePassword2();
});

const validateRegisterForm = () => {
    validateUsername();
    validateFirstname();
    validateLastname();
    validateEmail();
    validateAddress();
    validateContact();
    validatePassword1();
    validatePassword2();
};

registerForm.addEventListener('submit', (e) => {
    e.preventDefault();
    validateRegisterForm();
    if (usernameIsValid && firstnameIsValid && lastnameIsValid && emailIsValid && addressIsValid && contactIsValid && password1IsValid && password2IsValid) {
        registerForm.submit();
    }
});