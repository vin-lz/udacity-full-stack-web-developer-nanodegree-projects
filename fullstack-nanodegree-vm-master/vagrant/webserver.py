#!/usr/local/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

## import CRUD Operations from Lesson 1 ##
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Make a New Restaurant Here</a>"
                output += "</br>"
                output += "</br>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a>" % str(restaurant.id)
                    output += "</br>"
                    output += "<a href='/restaurants/%s/delete'>Delete</a>" % str(restaurant.id)
                    output += "</br>"
                    output += "</br>"
                output += "</body></html>"
                print(output)
                self.wfile.write(output.encode())
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'restaurant_name' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                print(output)
                self.wfile.write(output.encode())
                return

            if self.path.endswith("/edit"):
                restaurant_id_path = self.path.split("/")[2]
                restaurant_query = session.query(Restaurant).filter_by(id = restaurant_id_path).one()
                if restaurant_query != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>%s</h1>" % restaurant_query.name
                    output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/edit'>" % str(restaurant_id_path)
                    output += "<input name = 'restaurant_name' type = 'text' placeholder = '%s' > " % restaurant_query.name
                    output += "<input type='submit' value='Rename'>"
                    output += "</form></body></html>"
                    print(output)
                    self.wfile.write(output.encode())
                return
                
            if self.path.endswith("/delete"):
                restaurant_id_path = self.path.split("/")[2]
                restaurant_query = session.query(Restaurant).filter_by(id = restaurant_id_path).one()
                if restaurant_query != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete %s</h1>" % restaurant_query.name
                    output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/delete'>" % str(restaurant_id_path)
                    output += "<input type='submit' value='Delete'>"
                    output += "</form></body></html>"
                    print(output)
                    self.wfile.write(output.encode())
                return


            # if self.path.endswith("/hello"):
            #     self.send_response(200)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_headers()
            #     message = ""
            #     message += "<html><body>Hello!"
            #     message += """<form method='POST' enctype='multipart/form-data' action='/hello'>
            #         <h2>What would you like me to say?</h2><input name='message' type='text'>
            #         <input type='submit' value='Submit'></form>"""
            #     message += "</body></html>"
            #     self.wfile.write(message.encode())
            #     print(message)
            #     return

            # if self.path.endswith("/hola"):
            #     self.send_response(200)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_headers()
            #     message = ""
            #     message += "<html><body>&#161Hola <a href = '/hello'>Back to Hello</a>"
            #     message += """<form method='POST' enctype='multipart/form-data' action='/hello'>
            #         <h2>What would you like me to say?</h2><input name='message' type='text'>
            #         <input type='submit' value='Submit'></form>"""
            #     message += "</body></html>"
            #     self.wfile.write(message.encode())
            #     print(message)
            #     return
        
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):

        print("==============I'm doing POST=================")
        try:
            print("================I'm trying================")
            # if self.path.endswith("/hello"):
            #     self.send_response(301)
            #     self.end_headers()

            #     ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            #     pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            #     if ctype == 'multipart/form-data':
            #         fields = cgi.parse_multipart(self.rfile, pdict)
            #         messagecontent = fields.get('message')

            #     output = ""
            #     output += "<html><body>"
            #     output += "  <h2>Okay, how about this: </h2>"
            #     output += "  <h1> %s </h1>" % messagecontent[0].decode()
            #     output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
            #         <h2>What would you like me to say?</h2><input name='message' type='text'>
            #         <input type='submit' value='Submit'></form>"""
            #     output += "</body></html>"
            #     self.wfile.write(output.encode())
            #     print(output)
            #     return
            
            if self.path.endswith("/restaurants/new"):
                print("==============Right page!!!=================")
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant_name')
                    print(messagecontent[0])

                    #Create new Restaurant class
                    new_restaurant = Restaurant(name=messagecontent[0].decode())
                    session.add(new_restaurant)
                    session.commit()
                
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/edit"):
                print("==============Edit page!!!=================")
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant_name')
                    print(messagecontent[0])

                    #Edit restaurant name
                    restaurant_id_path = self.path.split("/")[2]
                    restaurant_query = session.query(Restaurant).filter_by(id = restaurant_id_path).one()
                    if restaurant_query != []:
                        restaurant_query.name = messagecontent[0].decode()
                        session.add(restaurant_query)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/delete"):
                print("==============Delete page!!!=================")
                restaurant_id_path = self.path.split("/")[2]
                restaurant_query = session.query(Restaurant).filter_by(id = restaurant_id_path).one()
                if restaurant_query != []:
                    session.delete(restaurant_query)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except:
            pass
            


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