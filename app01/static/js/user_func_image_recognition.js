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

    console.log("dasfasf");
    var formData = new FormData();

    formData.append('avatar', document.getElementById('avatar').files[0]); // 添加文件
    formData.append('action', 'profile');
    var infoUrl = document.getElementById('url-container').getAttribute('data-info-url');
    console.log("dasfasf");
    fetch(infoUrl, {
        method: 'POST',
        body: formData,  // 使用 FormData
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.error){
                alert(data.error)
            }
            else {
                // 使用从后端获取的数据更新页面
                updateResults(data.results);  // 这里处理返回的结果
            }
    })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function updateResults(results) {
    var resultsContainer = document.getElementById('results-container');
    resultsContainer.innerHTML = '';  // 清空之前的结果
    // 假设返回的结果格式为: [(class_id, class_name_cn, probability), ...]
    results.forEach(function(result) {
        var listItem = document.createElement('li');
        listItem.textContent = result[1] + ": " + result[2].toFixed(2); // 格式化概率为两位小数
        resultsContainer.appendChild(listItem);
    });
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
