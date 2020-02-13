var domains = {
    "google.com": 1,
    "facebook.com": 1,
    "github.com": 1,
	"youtube.com": 1,
	"wikipedia.org":1,
};
 
var server = "192.168.1.120";

var socks5_port = "1090";
var socks5_s = "SOCKS5 "+server+":"+socks5_port+"; ";

var http_port = "41091"
var http_s = "PROXY "+server+":"+http_port+"; ";

var proxy = socks5_s + http_s + "DIRECT;";
 
var direct = 'DIRECT;';
 
function FindProxyForURL(url, host) {
    var lastPos;
    do {
        if (domains.hasOwnProperty(host)) {
            return proxy;
        }
        lastPos = host.indexOf('.') + 1;
        host = host.slice(lastPos);
    } while (lastPos >= 1);
    return direct;
}

