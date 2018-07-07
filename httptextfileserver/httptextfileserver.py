from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class TextFileHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(self.server.http_get_response)


class HttpTextFileServer:
    def formatted_response(self, text):
        with open(os.path.join(os.path.dirname(__file__), 'response.html'), 'r') as html:
            html_response = html.read()
        html_response = html_response.replace('{{page-title}}', os.path.basename(self.text_file))
        body = '<p>'
        for line in text.readlines():
            body += line + '<br>'
        body += '</p>'
        html_response = html_response.replace('{{body}}', body)
        return html_response

    def __init__(self, address, port, text_file):
        self.server = HTTPServer((address, port), TextFileHandler)
        self.text_file = text_file
        with open(text_file, 'r') as text_file_content:
            self.server.http_get_response = self.formatted_response(text_file_content).encode()

    def run(self):
        self.server.serve_forever()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='A simple http server to view the contents of a single text file')
    parser.add_argument('host_address', type=str, help='Host address of the server')
    parser.add_argument('host_port', type=int, help='Host server port')
    parser.add_argument('file', type=str, help='File to serve')
    args = parser.parse_args()

    server = HttpTextFileServer(args.host_address, args.host_port, args.file)
    server.run()
