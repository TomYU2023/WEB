function validateForm() {
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    // 验证用户名长度
    if (username.length < 3) {
        alert("用户名必须至少包含 3 个字符！");
        return false;
    }

    // 验证密码长度
    if (password.length < 6) {
        alert("密码必须至少包含 6 个字符！");
        return false;
    }

    // 验证电子邮件格式
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        alert("请输入有效的电子邮件地址！");
        return false;
    }

    return true;
}