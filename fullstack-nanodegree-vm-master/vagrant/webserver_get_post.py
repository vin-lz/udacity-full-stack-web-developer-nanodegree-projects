from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = ""
                message += "<html><body>Hello!"
                message += """<form method='POST' enctype='multipart/form-data' action='/hello'>
                    <h2>What would you like me to say?</h2><input name='message' type='text'>
                    <input type='submit' value='Submit'></form>"""
                message += "</body></html>"
                self.wfile.write(message.encode())
                print(message)
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = ""
                message += "<html><body>&#161Hola <a href = '/hello'>Back to Hello</a>"
                message += """<form method='POST' enctype='multipart/form-data' action='/hello'>
                    <h2>What would you like me to say?</h2><input name='message' type='text'>
                    <input type='submit' value='Submit'></form>"""
                message += "</body></html>"
                self.wfile.write(message.encode())
                print(message)
                return
        
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):

            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += "  <h2>Okay, how about this: </h2>"
            output += "  <h1> %s </h1>" % messagecontent[0].decode()
            output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
                <h2>What would you like me to say?</h2><input name='message' type='text'>
                <input type='submit' value='Submit'></form>"""
            output += "</body></html>"
            self.wfile.write(output.encode())
            print(output)
            return
            


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()