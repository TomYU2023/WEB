// 等待页面完全加载后再执行脚本
document.addEventListener('DOMContentLoaded', function () {
    // 查找按钮
    const button = document.getElementById('click-me');

    // 给按钮绑定点击事件
    if (button) {
        button.addEventListener('click', function () {
            alert('你点击了按钮！'); // 弹出提示框
        });
    } else {
        console.error('未找到按钮，请检查 HTML 代码！');
    }
});
