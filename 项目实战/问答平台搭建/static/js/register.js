function bindEmailCaptchaClick(){
    // 这是“事件绑定”，不是递归执行函数！
    $("#captcha-btn").click(function (event){
        var $this = $(this);
        event.preventDefault();

        var email = $("#email").val();

        // 立即开始倒计时
        var countdown = 5;
        $this.off("click");  // 取消点击
        $this.prop("disabled", true);
        var timer = setInterval(function(){
            $this.text(countdown + " 秒后重试");
            countdown -= 1;
            if (countdown < 0){
                clearInterval(timer);
                $this.text("获取验证码");
                $this.prop("disabled", false);
                bindEmailCaptchaClick();
            }
        }, 1000);

        // 同时发起请求
        $.ajax({
            url: "/auth/captcha/email?email=" + email,
            method: "GET",
            success: function(result){
                var code = result['code'];
                if (code !== 200){
                    alert("验证码发送失败：" + result.message);
                }
            },
            error: function(error){
                console.log("请求失败:", error);
                alert("发送失败，请稍后重试");
            }
        });
    });
}

// 整个网页都加载完毕后执行
$(function (){
    bindEmailCaptchaClick();
});