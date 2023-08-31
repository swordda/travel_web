function sendemail() {
  const mail = document.getElementById('input_email').value;
  if (mail == '') {
    alert("邮箱不能为空");
    return;
  }
  fetch('http://127.0.0.1:8000/signmail/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ content: mail })
  }).then(response => response.json())
    .then(data => {
      if (data.message == "1") {
        alert('验证码已发送');
      }
      if (data.message == "2") {
        alert('请输入正确的邮箱');
      }
      if (data.message == "3") {
        alert('服务器异常，请刷新页面后重试');
      }
      console.log(data)
    })
}

function formsubmit() {
  const mail = document.getElementById('input_email').value;
  const pwd = document.getElementById('input_password').value;
  const pwd2 = document.getElementById('input_password2').value;
  const check_num = document.getElementById('input_check').value;
  if (mail == '' || pwd == '' || pwd2 == '' || check_num == '') {
    alert('请输入完整的信息');
    return;
  }
  if (pwd != pwd2) {
    alert('两次密码不一致，请重新输入');
    return;
  }
  if (pwd.length < 6 || pwd.length > 16) {
    alert('密码需要在6-16位之间');
    return;
  }
  fetch('http://127.0.0.1:8000/signup/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ content: mail, password: pwd, check: check_num })
  }).then(response => response.json())
    .then(data => {
      if (data.message == "1") {
        alert('注册成功');
        window.location.href = "http://127.0.0.1:8000/login/"
      }
      if (data.message == "2") {
        alert('验证码错误(超时)');
      }
      if (data.message == "3") {
        alert('服务器异常，请刷新页面后重试');
      }
      if (data.message == "4") {
        alert('该邮箱已经注册过')
      }
    })
}

$("#sendemail").click(function (e) {
  console.log("sub");
  sendemail();
})

$("#formsubmit").click(function (e) {
  console.log("sub");
  formsubmit();
})