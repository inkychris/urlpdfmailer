from http.server import BaseHTTPRequestHandler, HTTPServer
import os, logging


class TextFileHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logger = logging.getLogger(__name__)
        logger.debug("Sending HTTP 200 response")
        self.send_response(200)
        logger.debug("Sending HTTP header")
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        try:
            logger.debug("Sending HTML response to client")
            self.wfile.write(self.server.http_get_response())
        except Exception:
            logger.exception("Failed to sent HTML response to client")


class HttpTextFileServer:
    def __init__(self, address, port, text_file):
        self.server = HTTPServer((address, port), TextFileHandler)
        self.text_file = text_file
        self.server.http_get_response = self.http_get_response

    def formatted_response(self, text):
        logger = logging.getLogger(__name__)
        logger.debug("Formatting file into HTML response")
        try:
            with open(os.path.join(os.path.dirname(__file__), 'response.html'), 'r') as html:
                html_response = html.read()
            html_response = html_response.replace('{{page-title}}', os.path.basename(self.text_file))
            body = '<p>'
            for line in text.readlines():
                body += line + '<br>'
            body += '</p>'
            html_response = html_response.replace('{{body}}', body)
            return html_response
        except Exception:
            logger.exception("Failed to format HTML response")
            return

    def  http_get_response(self):
        logger = logging.getLogger(__name__)
        try:
            with open(self.text_file, 'r') as text_file_content:
                return self.formatted_response(text_file_content).encode()
        except Exception:
            logger.exception("Failed to load file to serve to client")

    def run(self):
        self.server.serve_forever()


if __name__ == '__main__':
    import argparse, sys
    parser = argparse.ArgumentParser(description='A simple http server to view the contents of a single text file')
    parser.add_argument('host_address', type=str, help='Host address of the server')
    parser.add_argument('host_port', type=int, help='Host server port')
    parser.add_argument('file', type=str, help='File to serve')
    args = parser.parse_args()

    logging.basicConfig(stream=sys.stdout, format='%(asctime)s [%(levelname)s] %(name)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG

    logger.debug("Creating server instance")
    server = HttpTextFileServer(args.host_address, args.host_port, args.file)
    logger.debug("Starting server at '{}' on port '{}' for file '{}'".format(args.host_address, args.host_port, args.file))
    server.run()
