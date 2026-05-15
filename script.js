// EmailJS Initialization
(function() {
    emailjs.init("Qj4dDgU6UZu9c6Vvx"); // Public Key
})();

const activateBtn = document.getElementById('activate-btn');
const introScreen = document.getElementById('intro-screen');
const mainContainer = document.getElementById('main-container');
const formsWrapper = document.querySelector('.forms-wrapper');

const whooshSound = document.getElementById('whoosh-sfx');
const hoverSound = document.getElementById('hover-sfx');
const clickSound = document.getElementById('click-sfx');

let tempUserData = null;
let currentSentCode = "";

// Intro Animation & Sound
window.onload = () => {
    setTimeout(() => { 
        if(whooshSound) {
            whooshSound.volume = 0.5; 
            whooshSound.play().catch(()=>{}); 
        }
    }, 500);
};

// Activate System
activateBtn.onclick = () => {
    if(clickSound) clickSound.play();
    introScreen.style.opacity = "0";
    setTimeout(() => { 
        introScreen.style.display = "none"; 
        mainContainer.style.display = "block"; 
    }, 800);
};

// Switch Forms
document.getElementById('to-reg-link').onclick = (e) => {
    e.preventDefault(); 
    if(clickSound) clickSound.play(); 
    formsWrapper.style.transform = "translateX(-50%)";
};

document.getElementById('to-login-link').onclick = (e) => {
    e.preventDefault(); 
    if(clickSound) clickSound.play(); 
    formsWrapper.style.transform = "translateX(0)";
};

// --- REGISTRATSIYA ---
const regForm = document.getElementById('reg-form');
regForm.onsubmit = (e) => {
    e.preventDefault();
    const username = document.getElementById('reg-username').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    const errorMsg = document.getElementById('reg-error-msg');

    let users = JSON.parse(localStorage.getItem('users')) || [];
    if (users.some(u => u.username === username)) {
        errorMsg.innerText = "Bu foydalanuvchi nomi band!";
        return;
    }
    if (password.length !== 8) {
        errorMsg.innerText = "Parol kam yoki ko'p, 8 ta kiriting";
        return;
    }

    // 5 xonali kod yaratish
    currentSentCode = Math.floor(10000 + Math.random() * 90000).toString();

    const templateParams = {
        to_email: email,
        user_name: username,
        auth_code: currentSentCode
    };

    emailjs.send('service_cqi9bt6', 'template_cit74ko', templateParams)
        .then(() => {
            tempUserData = { username, email, password };
            document.getElementById('verify-modal').style.display = "flex";
            errorMsg.innerText = "";
            alert("Emailingizni tekshiring, kod yuborildi!");
        }, (err) => {
            errorMsg.innerText = "Email yuborishda xato!";
            console.error("EmailJS Error:", err);
        });
};

// --- TASDIQLASH ---
document.getElementById('verify-confirm-btn').onclick = () => {
    const codeInput = document.getElementById('verify-code-input').value;
    const verifyError = document.getElementById('verify-error');

    if (codeInput === currentSentCode) {
        let users = JSON.parse(localStorage.getItem('users')) || [];
        users.push(tempUserData);
        localStorage.setItem('users', JSON.stringify(users));

        alert("Muvaffaqiyatli ro'yxatdan o'tdingiz!");
        document.getElementById('verify-modal').style.display = "none";
        formsWrapper.style.transform = "translateX(0)"; 
        regForm.reset();
    } else {
        verifyError.innerText = "Kod xato!";
    }
};

// --- KIRISH ---
const loginForm = document.getElementById('login-form');
loginForm.onsubmit = (e) => {
    e.preventDefault();
    const user = document.getElementById('login-username').value;
    const pass = document.getElementById('login-password').value;
    const errorMsg = document.getElementById('login-error-msg');

    let users = JSON.parse(localStorage.getItem('users')) || [];
    const foundUser = users.find(u => u.username === user);

    if (!foundUser) {
        errorMsg.innerText = "Foydalanuvchi topilmadi!";
    } else if (foundUser.password !== pass) {
        errorMsg.innerText = "Noto'g'ri parol!";
    } else {
        errorMsg.style.color = "#00ff00";
        errorMsg.innerText = "Muvaffaqiyatli kirildi!";
        setTimeout(() => alert("Xush kelibsiz!"), 500);
    }
};