import http.server
import socketserver
# import json
import secrets

HOST = "127.0.0.1"
PORT = 5000

usuarios_logados = []


class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # def do_GET(self):
    #     self.send_response(200)
    #     response = json.dumps({"logged_users": usuarios_logados})
    #     response = bytes(response, 'utf-8')
    #     self.wfile.write(response)

    def do_POST(self):
        if (self.path.endswith("/")):
            token = secrets.token_hex(16)
            usuarios_logados.append(token)
            self.send_response(200, token)
            self.end_headers()

        elif (self.path.endswith("/verify")):
            self.data_string = self.rfile.read(
                int(self.headers['Content-Length']))

            if (str(self.data_string).replace("b'", "").replace("'", "") in usuarios_logados):
                self.send_response(200, True)
                self.end_headers()

            else:
                self.send_response(404, False)
                self.end_headers()

    def do_DELETE(self):
        self.data_string = self.rfile.read(
            int(self.headers['Content-Length']))

        usuarios_logados.remove(
            str(self.data_string).replace("b'", "").replace("'", ""))


httpd = socketserver.TCPServer((HOST, PORT), SimpleHTTPRequestHandler)
print(f"Servindo em {HOST} na porta: {PORT}.")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("\nServidor parado.")
