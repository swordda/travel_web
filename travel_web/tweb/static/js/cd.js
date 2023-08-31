window.onload = function () {
  const mail = localStorage.getItem('mail');
  const pwd = localStorage.getItem('pwd');
  if (mail && pwd) {
    fetch('http://127.0.0.1:8000/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ content: mail, password: pwd })
    }).then(response => response.json())
      .then(data => {
        console.log(data.message);
        if (data.message == "1") {
          const username = localStorage.getItem('username');
          document.getElementById('username').innerText = username;
          localStorage.setItem("username", username.innerText);
          return;
        }
        else {
          alert("1");
          localStorage.removeItem("mail");
          localStorage.removeItem("pwd");
          window.location.href = 'http://127.0.0.1:8000/login/';
        }
      })
      .catch(error => console.error(error));
  }
  else {
    alert("4");
    window.location.href = 'http://127.0.0.1:8000/login/';
  }
}
