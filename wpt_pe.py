#!/usr/bin/python
import tornado.ioloop
import tornado.web
import httplib,urllib

WPT_PVT_HOST='www.webpagetest.org'

MAIN_PAGE_HTML = """\
<html>
  <body>
  CPU
    <form action="/gen_cpu" method="post">
        URL to Test: <div><input type="url" size="50" name="url" value="http://"></div>
        <br/>
        <input type="submit" value="Get me CPU Impact!">
    </form>

Network
    <form action="/gen_net" method="post">
        URL to Test: <div><input type="url" size="50" name="url" value="http://"></div>
        <br/>
        <input type="submit" value="Get me Network Impact!">
    </form>

Latency

    <form action="/gen_lat" method="post">
        URL to Test: <div><input type="url" size="50" name="url" value="http://"></div>
        <br/>
        <input type="submit" value="Get me Latency Impact!">
    </form>
Browser
    <form action="/gen_bro" method="post">
        URL to Test: <div><input type="url" size="50" name="url" value="http://"></div>
        <br/>
        <input type="submit" value="Get me Browser Impact!">
    </form>


</body>
</html>
"""

class MainPage(tornado.web.RequestHandler):

    def get(self):
        self.write(MAIN_PAGE_HTML)

class LatInfo(tornado.web.RequestHandler):
    def post(self):
        url = self.get_argument('url')
        lats =  {
		'20ms' : 20,
                '40ms' : 40,
                '60ms' : 60,
                '80ms' : 80,
                '100ms' : 100,
                '120ms' : 120,
                '140ms' : 140,
                '160ms' : 160,
                '180ms' : 180,
                '200ms' : 200,
                '240ms' : 240,
                '270ms' : 270,
                '300ms' : 300
        }
        browser = 'Chrome'
        testids = []
        for lat in lats:
            form_fields = {
                "url": url,
                    "browser": browser,
                    "location": "gpu_wptdriver"+":"+browser+".Custom",
                    "ignoreSSL":1,
                    "runs": "3",
                    "latency" : lats[lat],
                    "bwDown" : 50000,
                    "bwUp" : 10000,
                    "fvonly": "1",
                    "video": "1",
                    "label": lat,
                    "keepua": 1
            }
            form_data = urllib.urlencode(form_fields)
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
            conn = httplib.HTTPConnection(WPT_PVT_HOST)
            conn.request("POST", "/runtest.php", form_data, headers)
            response = conn.getresponse()
            loc = response.getheader('location')
            testids.append(loc.split('=')[-1])
	redir = 'http://'+WPT_PVT_HOST+'/video/compare.php?tests='+",".join(testids)
	self.redirect(redir)


class NetInfo(tornado.web.RequestHandler):
    def post(self):
        url = self.get_argument('url')
        nets =  {
                '1Mbps' : 1000,
                '2Mbps' : 2000,
                '3Mbps' : 3000,
                '4Mbps' : 4000,
                '5Mbps' : 5000,
                '6Mbps' : 6000,
                '7Mbps' : 7000,
                '8Mbps' : 8000,
                '9Mbps' : 9000,
                '10Mbps' : 10000
        }
        browser = 'Chrome'
        testids = []
        for net in nets:
            form_fields = {
                    "url": url,
                    "browser": browser,
                    "location": "gpu_wptdriver"+":"+browser+".Custom",
                    "ignoreSSL":1,
                    "runs": "3",
                    "bwDown" : nets[net],
                    "bwUp" : 10000,
                    "latency" : 0,
                    "fvonly": "1",
                    "video": "1",
                    "label": net,
                    "keepua": 1
            }
            form_data = urllib.urlencode(form_fields)
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
            conn = httplib.HTTPConnection(WPT_PVT_HOST)
            conn.request("POST", "/runtest.php", form_data, headers)
            response = conn.getresponse()
            loc = response.getheader('location')
            testids.append(loc.split('=')[-1])
	redir = 'http://'+WPT_PVT_HOST+'/video/compare.php?tests='+",".join(testids)
	self.redirect(redir)

class CPUInfo(tornado.web.RequestHandler):
    def post(self):
        url = self.get_argument('url')
        # Process input URL list
        cpus =  {
		'cpu_1' : '1 vCPU',
                'cpu_2' : '2 vCPUs',
                'cpu_4' : '4 vCPUs',
                'cpu_8' : '8 vCPUs',
                'gpu' : 'GPU'
        }
        browser = 'Chrome'
        testids = []
        for cpu in cpus:
            form_fields = {
                "url": url,
                    "browser": browser,
                    "location": cpu +"_wptdriver"+":"+browser+".Native",
                    "ignoreSSL":1,
                    "runs": "3",
                    "fvonly": "1",
                    "video": "1",
                    "label": cpus[cpu],
                    "keepua": 1
            }
            form_data = urllib.urlencode(form_fields)
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
            conn = httplib.HTTPConnection(WPT_PVT_HOST)
            conn.request("POST", "/runtest.php", form_data, headers)
            response = conn.getresponse()
            loc = response.getheader('location')
            testids.append(loc.split('=')[-1])
	redir = 'http://'+WPT_PVT_HOST+'/video/compare.php?tests='+",".join(testids)
	self.redirect(redir)

class BroInfo(tornado.web.RequestHandler):
    def post(self):
        url = self.get_argument('url')
        browsers = ['Firefox', 'IE 11','Chrome']
        testids = []
        for browser in browsers:
            form_fields = {
                    "url": url,
                    "browser": browser,
                    "location": "gpu_wptdriver"+":"+browser+".Native",
                    "ignoreSSL":1,
                    "runs": "3",
                    "fvonly": "1",
                    "video": "1",
                    "label": browser,
                    "keepua": 1
            }
            form_data = urllib.urlencode(form_fields)
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
            conn = httplib.HTTPConnection(WPT_PVT_HOST)
            conn.request("POST", "/runtest.php", form_data, headers)
            response = conn.getresponse()
            loc = response.getheader('location')
            testids.append(loc.split('=')[-1])

        redir = 'http://'+WPT_PVT_HOST+'/video/compare.php?tests='+",".join(testids)
        self.redirect(redir)

application = tornado.web.Application([
    (r"/gen_cpu", CPUInfo),
    (r"/gen_net", NetInfo),
    (r"/gen_lat", LatInfo),
    (r"/gen_bro", BroInfo),
    ("/", MainPage),
], debug=True)

if __name__ == "__main__":
    application.listen(3000)
    tornado.ioloop.IOLoop.instance().start()
