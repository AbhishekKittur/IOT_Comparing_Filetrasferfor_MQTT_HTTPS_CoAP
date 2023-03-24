#!/usr/bin/env python  
  
from http.server import BaseHTTPRequestHandler, HTTPServer  
import os  
  

class HTTPRequestHandler(BaseHTTPRequestHandler):  

  #handle GET command  
  def do_GET(self):  
    #rootdir = 'F:\new\server' #file location  
    try:  
        f = open(self.path,  'rb') #open requested file  
        #send code 200 response  
        self.send_response(200)    
        #send header first  
        self.send_header('Content-type', 'text/plain')  
        self.end_headers()  
        self.wfile.write(f.read())
        f.close()  
        return  

    except IOError:  
      self.send_error(404, 'file not found')  

def run():  
  print('http server is starting...')  
  
  #ip and port of servr  
  #by default http server port is 80  
  server_address = ('127.0.0.1', 8889)  
  httpd = HTTPServer(server_address, HTTPRequestHandler)  
  print('http server is running...')  
  httpd.serve_forever()  

if __name__ == '__main__':  
  run() 