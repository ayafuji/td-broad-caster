var socket = null;

function bootstrap() {
  socket = new WebSocket('ws://test2.ayafuji.com:8082');
  console.log("websocket connection is established...")
  socket.binaryType = 'arraybuffer';
  //socket.onopen = function() {
  //  send(ctx);
  //}
  socket.onmessage = handleReceive;
};


function handleReceive(message) {

  var c = resultCanvas = document.getElementById('result');
  var ctx = c.getContext('2d');
  var imageData = ctx.createImageData(300, 300);
  var pixels = imageData.data;
  var buffer = new Uint8Array(message.data);

  var idx = 0;
  for (var i=0; i < pixels.length; i+=4) {
    pixels[i] = buffer[idx];
    pixels[i+1] = buffer[idx+1];
    pixels[i+2] = buffer[idx+2];
    pixels[i+3] = 255;
    idx += 3;
  }
  ctx.putImageData(imageData, 0, 0);
}
