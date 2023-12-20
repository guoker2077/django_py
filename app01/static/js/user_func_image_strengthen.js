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

// 确保在用户选择图片后可以在页面上预览
function previewFile() {
    var preview = document.getElementById('avatar-preview');
    var file = document.getElementById('avatar').files[0];
    var reader = new FileReader();

    reader.onloadend = function () {
        if (file) {
            preview.src = reader.result;
            preview.style.display = 'block'; // 显示预览
        } else {
            preview.style.display = 'none'; // 隐藏预览
        }
    }

    if (file) {
        reader.readAsDataURL(file);
    } else {
        preview.style.display = 'none'; // 如果没有文件，隐藏预览
    }
}

function ProFile() {
    'use strict';
    var form = document.getElementById('profile-form'); // 获取您的表单元素，确保它有 id="profile-form"

    if (!form.checkValidity()) {
        // 表单验证不通过
        form.classList.add('was-validated'); // Bootstrap 4 的验证样式
        return; // 不提交表单
    }
    var formData = new FormData();
    formData.append('avatar', document.getElementById('avatar').files[0]); // 添加文件
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
            if(data.error) {
                alert(data.error)
            }
            else {
                update_new(data.message)
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function update_new(imageUrl) {
    // 获取图片和下载链接的元素
    var outputImage = document.getElementById('outputImage');
    var downloadLink = document.getElementById('downloadLink');

    // 设置图片源并显示图片
    outputImage.src = imageUrl;
    outputImage.style.display = 'block';

    // 设置下载链接并显示链接
    downloadLink.href = imageUrl;
    downloadLink.style.display = 'block';
}