function generateCode() {
  // 生成一个四位数的随机数
  var code = Math.floor(Math.random() * 9000) + 1000;
  return code;
}

function drawCodeImage(canvasId) {
  var canvas = document.getElementById(canvasId);
  var context = canvas.getContext("2d");
  var code = generateCode().toString();

  // 绘制背景色
  context.fillStyle = "#ffffff";
  context.fillRect(0, 0, canvas.width, canvas.height);

  // 绘制范围横线
  context.strokeStyle = "#000000";
  context.lineWidth = 2;
  context.moveTo(10, canvas.height / 2);
  context.lineTo(canvas.width - 10, canvas.height / 2);
  context.stroke();

  // 绘制验证码数字
  context.font = "bold 48px sans-serif";
  context.fillStyle = "#000000";
  context.textAlign = "center";
  context.textBaseline = "middle";
  context.fillText(code, canvas.width / 2, canvas.height / 2);

  // 将画布转换为图片并插入到DOM
  var img = new Image();
  img.src = canvas.toDataURL("image/png");
  document.getElementById("code-image").appendChild(img);
}
