const canvas = document.getElementById('pizarra');
const ctx = canvas.getContext('2d');
let isDrawing = false;

canvas.addEventListener('mousedown', (e) => {
  isDrawing = true;
  draw(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
});

canvas.addEventListener('mousemove', (e) => {
  if (isDrawing) {
    draw(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
  }
});

canvas.addEventListener('mouseup', () => {
  isDrawing = false;
});

function draw(x, y) {
  if (!isDrawing) return;
  ctx.lineWidth = 2;
  ctx.lineCap = 'round';
  ctx.strokeStyle = 'black';
  ctx.lineTo(x, y);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x, y);
}

function guardarDibujo() {
  const link = document.createElement('a');
  link.download = 'dibujo.png';
  link.href = canvas.toDataURL('image/png');
  link.click();
}
