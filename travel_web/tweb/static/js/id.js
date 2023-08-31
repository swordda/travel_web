var imageArray = [
  "https://youimg1.c-ctrip.com/target/0106m120004eks4oyF624_C_1180_462.jpg",
  "https://youimg1.c-ctrip.com/target/0103l1200080zklhd01B9_C_1180_462.jpg",
  "https://wsxar.cn/cyber/img/1681199570136.jpg",
  "https://wsxar.cn/cyber/img/1681199570140.jpg"
];

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
          var username = document.getElementById();
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

function preloadImages() {
  for (var i = 0; i < imageArray.length; i++) {
    var img = new Image();
    img.src = imageArray[i];
  }
}

preloadImages();

function logout() {
  localStorage.removeItem("mail");
  localStorage.removeItem("pwd");
  window.location.href = "http://127.0.0.1:8000/login/";
}

function search() {
  input = document.getElementById('input_city').value;
  if (input == '') {
    alert('请输入需要查找的城市');
  }
  window.location.href = 'http://127.0.0.1:8000/city/?city=' + input;
}

$("#logout").click(function (e) {
  console.log("sub");
  logout();
})

$("#search").click(function (e) {
  console.log("sub");
  search();
})

var background = document.getElementById("background");
background.style.backgroundImage = "url(" + imageArray[0] + ")";

var index = 0;
setInterval(function () {
  index = (index + 1) % imageArray.length;
  var imageUrl = "url(" + imageArray[index] + ")";
  fadeToImage(imageUrl);
}, 8000);

function fadeToImage(imageUrl) {
  var tempBackground = document.createElement("div");
  tempBackground.style.backgroundImage = imageUrl;
  tempBackground.style.opacity = 0;
  tempBackground.className = "temp-background";
  background.appendChild(tempBackground);

  setTimeout(function () {
    tempBackground.style.opacity = 1;
    background.style.backgroundImage = imageUrl;
  }, 1000);

  setTimeout(function () {
    var oldBackground = document.getElementsByClassName("temp-background")[0];
    background.removeChild(oldBackground);
  }, 1000);
}