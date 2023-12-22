function handlemodifyinfo(id) {
    'use strict';
    var form = document.getElementById('modifyinfo' + id); // 获取您的表单元素，确保它有 id="profile-form"

    if (!form.checkValidity()) {
        // 表单验证不通过
        form.classList.add('was-validated'); // Bootstrap 4 的验证样式
        console.log("handleUsernameLogin notcalled");
        return; // 不提交表单
    }
    // var id = document.getElementById('userid').value;
    var balance = document.getElementById('userbalance' + id).value;
    console.log("id,balance");
    console.log(id, balance);

    fetch('/admin/main/', {
        method: 'POST',
        body: JSON.stringify({
            action: 'modify_balance',
            id: id,
            balance: balance
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

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function handlesearch() {
    'use strict';
    var content = document.getElementById('content').value;
    console.log("search_content；"+content);

    fetch('/admin/main/', {
        method: 'POST',
        body: JSON.stringify({
            action: 'search_content',
            content: content,
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