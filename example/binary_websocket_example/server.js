#!/usr/bin/env node
var WebSocketServer = require('websocket').server,
    http = require('http'),
    fs = require('fs');

var server = http.createServer(function(request, response) {
  var filePath;
  if (request.url == '/') {
    filePath = './index.html';
  } else {
    filePath = './client.js';
  }
  var data = fs.readFileSync(filePath, 'utf8');
  console.log((new Date()) + " Received request for " + request.url);
  response.end(data);
});

server.listen(8082, function() {
  console.log((new Date()) + " Server is listening on port 8082");
});

wsServer = new WebSocketServer({
  httpServer: server,
  // デフォルトでは65535byte以上受けつけないので
  // 値を増やしてみる
  maxReceivedFrameSize: 0x1000000,
  autoAcceptConnections: false
});

wsServer.on('request', function(request) {

  var connection = request.accept(null, request.origin);
  console.log((new Date()) + " Connection accepted.");
  connection.on('message', function(message) {
    if (message.type === 'utf8') {
      // NOP
    }
    else if (message.type === 'binary') {
      // バイナリデータを受信した場合
      console.log("Received Binary Message of " + message.binaryData.length + " bytes");
      console.log(message.binaryData);

      var data = message.binaryData;
      var len = data.length;

      // 受信したRAW画像をグレースケールにする
      var buf = new Buffer(len);
      var arr = new Uint32Array(buf);
      for (var i = 0; i < len; i+=4 ) {
        var r = data.readUInt8(i);
        var g = data.readUInt8(i+1);
        var b = data.readUInt8(i+2);
        var y = Math.floor((77*r + 28*g + 151*b)/255);

        // Canvasにそのまま投入するために
        // 4チャンネル8ビットのRGBAにする
        var v = y + (y << 8) + (y << 16) + (0xFF << 24);
        buf.writeInt32LE(v, i);
      }
      // グレースケールにした物をクライアントに送信する
      connection.sendBytes(buf);
    }
  });

  connection.on('close', function(reasonCode, description) {
    console.log((new Date()) + " Peer " + connection.remoteAddress + " disconnected.");
  });
});
