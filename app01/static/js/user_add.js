function handleUsernameLogin() {
    'use strict';
    var form = document.getElementById('username-login-form'); // 获取您的表单元素，确保它有 id="profile-form"

    if (!form.checkValidity()) {
        // 表单验证不通过
        form.classList.add('was-validated'); // Bootstrap 4 的验证样式
        return; // 不提交表单
    }
    console.log("handleUsernameLogin called");
    var username = document.getElementById('login-username').value;
    var password = document.getElementById('login-passwd').value;

    fetch('/user/add/', {
        method: 'POST',
        body: JSON.stringify({
            action: 'username_login',
            username: username,
            password: password
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error)
                // 处理错误
            } else {
                window.location.href = data.message; // 登录成功，重定向
            }
        })
        .catch(error => console.error('Error:', error));
}


function handlePhoneLogin() {
    'use strict';
    var form = document.getElementById('phone-login-form'); // 获取您的表单元素，确保它有 id="profile-form"

    if (!form.checkValidity()) {
        // 表单验证不通过
        form.classList.add('was-validated'); // Bootstrap 4 的验证样式
        return; // 不提交表单
    }

    var phone = document.getElementById('login-phone').value;
    var code = document.getElementById('login-code').value;

    var url = '/user/add/'; // 修改为实际的 URL

    fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            action: 'phone_login',
            phone: phone,
            code: code
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Server responded with status ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                // 显示错误消息
                console.log(data.error);
            } else {
                // 处理登录成功的情况
                window.location.href = data.message; // 重定向到其他页面
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function handleRegistration() {
    'use strict';
    var form = document.getElementById('register-form'); // 获取您的表单元素，确保它有 id="profile-form"

    if (!form.checkValidity()) {
        // 表单验证不通过
        form.classList.add('was-validated'); // Bootstrap 4 的验证样式
        return; // 不提交表单
    }
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var phone = document.getElementById('register-phone').value;
    var code = document.getElementById('register-code').value;

    var url = '/user/add/'; // 修改为实际的 URL

    fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            action: 'register',
            username: username,
            password: password,
            phone: phone,
            code: code
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                // 在验证码输入框旁边显示错误消息
                document.getElementById('code-error').innerText = data.error;
            } else {

                // 处理注册成功的情况
                window.location.href = data.message; // 重定向到其他页面
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}


function sendCode() {
    var phone = document.getElementById('login-phone').value; // 确保 ID 是正确的
    // 手机号格式验证
    if (!/^1[0-9]{10}$/.test(phone)) {
        alert('手机号格式有误');
        return; // 不发送请求，直接返回
    }
    var url = '/user/add/'; // 修改为实际的 URL
    fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            action: 'send_code_login',
            phone: phone
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie2('csrftoken')
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Server response wasn\'t OK');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                console.log(data.message); // 输出返回的消息
                startCountdown2(); // 开始倒计时
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });

}

function startCountdown2() {
    var button = document.getElementById('get-code');
    button.disabled = true;
    var counter = 60;
    button.innerText = `重新发送 (${counter}s)`;

    var interval = setInterval(function () {
        counter--;
        if (counter <= 0) {
            clearInterval(interval);
            button.innerText = '发送验证码';
            button.disabled = false;
        } else {
            button.innerText = `重新发送 (${counter}s)`;
        }
    }, 1000);
}

// 获取 CSRF token 的辅助函数
function getCookie2(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showLoginForm() {
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('phone-form').style.display = 'none';
}

function showPhoneForm() {
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('phone-form').style.display = 'block';
}


// 发送验证码的逻辑
function sendCodeReg() {
    var phone = document.getElementById('register-phone').value; // 获取用户输入的手机号
    if (!/^1[0-9]{10}$/.test(phone)) {
        alert('手机号格式有误');
        return; // 不发送请求，直接返回
    }
    var url = '/user/add/'; // 修改为实际的 URL
    console.log(phone); // 这应该打印出输入的手机号码
    fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            action: 'send_code_reg',
            phone: phone
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // 获取 CSRF token
        }
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message); // 输出返回的消息
            startCountdown(); // 开始倒计时
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function startCountdown() {
    var button = document.getElementById('get-code-reg');
    button.disabled = true;
    var counter = 60;
    button.innerText = `重新发送 (${counter}s)`;

    var interval = setInterval(function () {
        counter--;
        if (counter <= 0) {
            clearInterval(interval);
            button.innerText = '发送验证码';
            button.disabled = false;
        } else {
            button.innerText = `重新发送 (${counter}s)`;
        }
    }, 1000);
}

// 获取 CSRF token 的辅助函数
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
