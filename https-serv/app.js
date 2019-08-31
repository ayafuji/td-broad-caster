var fs = require('fs');
var https = require('https');
var options = {
	  key:  fs.readFileSync('/etc/letsencrypt/live/test2.ayafuji.com/privkey.pem'),
	  cert: fs.readFileSync('/etc/letsencrypt/live/test2.ayafuji.com/cert.pem')
};
server = https.createServer(options);
var index;

fs.readFile('./index.html', function (err, html) {
	index = html;
	console.log("finished to load inidex.html file");
});

server.on('request',function(req,res) {
	fs.readFile("." + req.url, (err, data) => {
		if (!err) {
			res.writeHead(200, {"Content-Type": "text/html"});
			res.end(data);
		}
	});
})

x = server.listeners('request');
server.listen(3000);
