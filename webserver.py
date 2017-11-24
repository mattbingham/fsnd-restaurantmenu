#!/usr/bin/env python3.5

from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import sqlite3


class WebServerHandler(BaseHTTPRequestHandler):
    form_html = \
        '''
        <form method='POST' enctype='multipart/form-data' action='/hello'>
        <h2>What would you like me to say?</h2>
        <input name="message" type="text"><input type="submit" value="Submit" >
        </form>
         '''
    open_tags = "<html><body>"
    close_tags = "</html></body>"

    def do_GET(self):

        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = self.open_tags
                output += "Hello!<br>" + self.form_html
                output += self.close_tags
                self.wfile.write(output.encode())
                print(output)

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = self.open_tags
                output += "&#161;Hola! <br>"
                output += self.form_html
                output += "<a href='/hello'>Back Home</a>"
                output += self.close_tags
                self.wfile.write(output.encode())
                print(output)

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # Call restaurant names from database
                conn = sqlite3.connect('restaurantmenu.db')
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM restaurant")
                results = cursor.fetchall()
                cursor.close()
                conn.close()
                
                output = self.open_tags + "<h1>Restaurants</h1>"
                # Print restaurant names from database
                for r in results:
                    r = str(r)
                    r = r[2:-3]
                    output += "<h2>{}</h2>".format(r)
                output += self.close_tags
                self.wfile.write(output.encode())
                print(output)


        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            ctype, pdict = cgi.parse_header(
                self.headers['content-type'])

            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> {} </h1>".format(messagecontent[0].decode())
            output += self.form_html
            output += "</body></html>"
            self.wfile.write(output.encode())
            print(output)

        except:
            raise


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web server is running on port {}".format(port))
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")

    finally:
        if server:
            server.socket.close()


if __name__ == '__main__':
    main()