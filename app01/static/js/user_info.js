function ProFile() {
    'use strict';
    var form = document.getElementById('profile-form'); // 获取您的表单元素，确保它有 id="profile-form"

    if (!form.checkValidity()) {
        // 表单验证不通过
        form.classList.add('was-validated'); // Bootstrap 4 的验证样式
        return; // 不提交表单
    }
    var formData = new FormData();
    formData.append('username', document.getElementById('username').value);
    formData.append('nickname', document.getElementById('nickname').value);
    formData.append('age', document.getElementById('age').value);
    formData.append('gender', document.getElementById('gender').value);
    formData.append('avatar', document.getElementById('avatar').files[0]); // 添加文件
    formData.append('user_id', document.getElementById('user_id').getAttribute('data-info-user_id'));
    formData.append('action', 'profile');
    var infoUrl = document.getElementById('url-container').getAttribute('data-info-url');

    fetch(infoUrl, {
        method: 'POST',
        body: formData,  // 使用 FormData
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            // 处理修改成功的情况
            window.location.href = data.message; // 重定向到其他页面
            alert("修改成功！")
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}


// 确保在用户选择图片后可以在页面上预览
function previewFile() {
    var preview = document.getElementById('avatar-preview');
    var file = document.getElementById('avatar').files[0];
    var reader = new FileReader();

    reader.onloadend = function () {
        preview.style.backgroundImage = 'url("' + reader.result + '")';
    }

    if (file) {
        reader.readAsDataURL(file);
    } else {
        preview.style.backgroundImage = "url('default-avatar.png')";
    }
}

function SubmitChangPasswordVerfi() {
    'use strict';
    var form = document.getElementById('verifyPhoneModal1-form'); // 获取您的表单元素，确保它有 id="profile-form"

    if (!form.checkValidity()) {
        // 表单验证不通过
        form.classList.add('was-validated'); // Bootstrap 4 的验证样式
        return; // 不提交表单
    }
    var currentModal = document.querySelector('#verifyPhoneModal1');
    var newModal = document.querySelector('#newPasswordModal');
    var formData = new FormData();
    var phone = document.getElementById('phone1').value;
    if (!/^1[0-9]{10}$/.test(phone)) {
        alert('手机号格式有误');
        return; // 不发送请求，直接返回
    }
    formData.append('phone', document.getElementById('phone1').value);
    formData.append('code', document.getElementById('code1').value);
    formData.append('user_id', document.getElementById('user_id').getAttribute('data-info-user_id'));
    formData.append('action', 'verifyPhoneModal1-form');
    var infoUrl = document.getElementById('url-container').getAttribute('data-info-url');
    fetch(infoUrl, {
        method: 'POST',
        body: formData,  // 使用 FormData
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                // 在验证码输入框旁边显示错误消息
                alert(data.errors);
            } else {
                // 关闭当前模态框
                $(currentModal).modal('hide');

                // 打开另一个模态框
                $(newModal).modal('show');

            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });

}

function SubmitChangPhoneVerfi() {
    'use strict';
    var form = document.getElementById('verifyPhoneModal2-form'); // 获取您的表单元素，确保它有 id="profile-form"

    if (!form.checkValidity()) {
        // 表单验证不通过
        form.classList.add('was-validated'); // Bootstrap 4 的验证样式
        return; // 不提交表单
    }
    var currentModal = document.querySelector('#verifyPhoneModal2');
    var newModal = document.querySelector('#changePhoneModal');
    var formData = new FormData();
    var phone = document.getElementById('phone2').value;
    if (!/^1[0-9]{10}$/.test(phone)) {
        alert('手机号格式有误');
        return; // 不发送请求，直接返回
    }
    formData.append('phone', document.getElementById('phone2').value);
    formData.append('code', document.getElementById('code2').value);
    formData.append('user_id', document.getElementById('user_id').getAttribute('data-info-user_id'));
    formData.append('action', 'verifyPhoneModal2-form');
    var infoUrl = document.getElementById('url-container').getAttribute('data-info-url');
    fetch(infoUrl, {
        method: 'POST',
        body: formData,  // 使用 FormData
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                // 在验证码输入框旁边显示错误消息
                alert(data.error);
            } else {
                // 关闭当前模态框
                $(currentModal).modal('hide');

                // 打开另一个模态框
                $(newModal).modal('show');

            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });

}

function changePassword() {
    'use strict';
    var form = document.getElementById('newPasswordModal-form'); // 获取您的表单元素，确保它有 id="profile-form"

    if (!form.checkValidity()) {
        // 表单验证不通过
        form.classList.add('was-validated'); // Bootstrap 4 的验证样式
        return; // 不提交表单
    }
    var formData = new FormData();
    // 从输入字段获取数据
    var newPassword = document.getElementById('new-password-input').value;
    var confirmPassword = document.getElementById('confirm-password-input').value;
    formData.append('new-password', document.getElementById('new-password-input').value);
    formData.append('user_id', document.getElementById('user_id').getAttribute('data-info-user_id'));
    formData.append('action', 'newPasswordModal-form');
    var infoUrl = document.getElementById('url-container').getAttribute('data-info-url');
    // 确保两次输入的密码相同
    if (newPassword !== confirmPassword) {
        alert('两次输入的密码不一致');
        return;
    }

    // 发送请求到后端验证验证码并更新密码
    // 使用 AJAX 或其他方式

    fetch(infoUrl, {
        method: 'POST',
        body: formData,  // 使用 FormData
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                window.location.href = '/user/add'; // 重定向到其他页面
                alert("修改成功！")
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function changePhone() {
    'use strict';
    var form = document.getElementById('changePhoneModal-form'); // 获取您的表单元素，确保它有 id="profile-form"

    if (!form.checkValidity()) {
        // 表单验证不通过
        form.classList.add('was-validated'); // Bootstrap 4 的验证样式
        return; // 不提交表单
    }
    // 从输入字段获取数据
    var formData = new FormData();
    // 从输入字段获取数据
    var phone = document.getElementById('new-phone-input').value;
    if (!/^1[0-9]{10}$/.test(phone)) {
        alert('手机号格式有误');
        return; // 不发送请求，直接返回
    }
    formData.append('new-phone', document.getElementById('new-phone-input').value);
    formData.append('user_id', document.getElementById('user_id').getAttribute('data-info-user_id'));
    formData.append('action', 'changePhoneModal-form');
    var infoUrl = document.getElementById('url-container').getAttribute('data-info-url');

    // 发送请求到后端验证验证码并更新密码
    // 使用 AJAX 或其他方式

    fetch(infoUrl, {
        method: 'POST',
        body: formData,  // 使用 FormData
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                window.location.href = '/user/add'; // 重定向到其他页面
                alert("修改成功！")
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });

}


// 发送验证码的逻辑
function sendCodeReg1() {
    var phone = document.getElementById('phone1').value;
    if (!/^1[0-9]{10}$/.test(phone)) {
        alert('手机号格式有误');
        return; // 不发送请求，直接返回
    }
    var formData = new FormData();
    formData.append('phone', document.getElementById('phone1').value);
    formData.append('user_id', document.getElementById('user_id').getAttribute('data-info-user_id'));
    formData.append('action', 'send_code1');
    var infoUrl = document.getElementById('url-container').getAttribute('data-info-url');
    fetch(infoUrl, {
        method: 'POST',
        body: formData,  // 使用 FormData
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                // 显示错误消息
                alert(data.error);
            } else {
                console.log(data.message); // 输出返回的消息
                startCountdown1(); // 开始倒计时
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function startCountdown1() {
    var button = document.getElementById('get-code-reg1');
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

// 发送验证码的逻辑
function sendCodeReg2() {
    var phone = document.getElementById('phone2').value;
    if (!/^1[0-9]{10}$/.test(phone)) {
        alert('手机号格式有误');
        return; // 不发送请求，直接返回
    }
    var formData = new FormData();
    formData.append('phone', document.getElementById('phone2').value);
    formData.append('user_id', document.getElementById('user_id').getAttribute('data-info-user_id'));
    formData.append('action', 'send_code2');
    var infoUrl = document.getElementById('url-container').getAttribute('data-info-url');
    fetch(infoUrl, {
        method: 'POST',
        body: formData,  // 使用 FormData
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                // 显示错误消息
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
    var button = document.getElementById('get-code-reg2');
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