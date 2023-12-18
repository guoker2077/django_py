function updateClock() {
    var now = new Date();
    var hours = now.getHours();
    var minutes = now.getMinutes();
    var seconds = now.getSeconds();

    // 添加前导零
    hours = hours < 10 ? "0" + hours : hours;
    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;

    var timeString = hours + ":" + minutes + ":" + seconds;

    // 将时间字符串更新到页面中的元素
    var clockElement = document.getElementsByClassName("ml-clock")[0];
    if (clockElement) {
        clockElement.textContent = timeString;
    }
}

// 每隔一秒更新一次时间
setInterval(updateClock, 1000);

// 初始加载时先调用一次，避免页面加载后有短暂的空白时间
updateClock();