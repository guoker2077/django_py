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
    // var form = document.getElementById('modifyinfo'); // 获取您的表单元素，确保它有 id="profile-form"

    // var id = document.getElementById('userid').value;
    var content = document.getElementById('content').value;
    console.log("search_content；"+content);
    // console.log(id, balance);

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
    //     .then(data => {
    //     if (data.error) {
    //         alert(data.error);
    //         // 处理错误
    //     } else if (Array.isArray(data.user_infos)) {  // Check if user_infos is an array
    //         // 获取表格的 tbody 元素
    //         var tbody = document.getElementById('dataList').getElementsByTagName('tbody')[0];
    //
    //         // 清空当前表格内容
    //         tbody.innerHTML = '';
    //
    //         // 处理用户信息
    //         var userInfos = data.user_infos;
    //         console.log('userInfos',userInfos);
    //         userInfos.forEach(userInfo => {
    //             // 创建新的表格行
    //             var row = tbody.insertRow();
    //
    //             // 插入单元格并赋值
    //             var cellId = row.insertCell(0);
    //             cellId.innerHTML = userInfo.id;
    //
    //
    //             var celluserName = row.insertCell(1);
    //             celluserName.innerHTML = userInfo.name;
    //
    //             var cellName = row.insertCell(2);
    //             cellName.innerHTML = userInfo.name;
    //
    //             // 插入其他单元格...
    //         });
    //
    //         // 进行其他前端处理...
    //     } else {
    //         console.error('Invalid user_infos data:', data.user_infos);
    //     }
    // })
    // .catch(error => console.error('Error:', error));



}