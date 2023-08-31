window.onload = function () {
  const mail = localStorage.getItem('mail');
  const pwd = localStorage.getItem('pwd');
  console.log(mail);
  console.log('123');
  console.log(pwd)
  if (mail && pwd) {
    const url = 'http://127.0.0.1:8000/index/?content=' + mail + '&password=' + pwd;
    fetch('http://127.0.0.1:8000/index/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ content: mail, password: pwd })
    }).then(response => response.text())
      .then(data => {
        console.log(data);
        if (data == "{\"message\": \"3\"}") {
          alert('密码错误');
          return;
        }
        if (data == "{\"message\": \"2\"}") {
          alert('未注册的账号');
          return;
        }
        if (data == "{\"message\": \"2\"}") {
          alert('服务器出现异常，请刷新页面后重试');
          return;
        }
        console.log(data);
        if (data != "{\"message\": \"2\"}") {
          localStorage.setItem("mail", mail);
          localStorage.setItem("pwd", pwd);
          window.location.href = url;
        }
      })
      .catch(error => console.error(error));
  }
}

function login() {
  const mail = document.getElementById('input_email').value;
  const pwd = document.getElementById('input_password').value;
  if (mail == '' || pwd == '') {
    alert("请输入完整的登录信息");
    return;
  }
  if (pwd.length < 6 || pwd.length > 16) {
    alert('密码需要在6-16位之间');
    return;
  }
  const url = 'http://127.0.0.1:8000/index/?content=' + mail + '&password=' + pwd;
  fetch('http://127.0.0.1:8000/index/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ content: mail, password: pwd })
  }).then(response => response.text())
    .then(data => {
      console.log(data);
      if (data == "{\"message\": \"3\"}") {
        alert('密码错误');
        return;
      }
      if (data == "{\"message\": \"2\"}") {
        alert('未注册的账号');
        return;
      }
      if (data == "{\"message\": \"2\"}") {
        alert('服务器出现异常，请刷新页面后重试');
        return;
      }
      console.log(data);
      if (data != "{\"message\": \"2\"}") {
        localStorage.setItem("mail", mail);
        localStorage.setItem("pwd", pwd);
        window.location.href = url;
      }
    })
    .catch(error => console.error(error));
}

$("#login").click(function (e) {
  console.log("sub");
  login();
})