import http.server
import socketserver
import json
import socket
import webbrowser
import threading
import os

PORT = 8000

class ThreadingSimpleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

class SyncHandler(http.server.SimpleHTTPRequestHandler):
    # Global state untuk sinkronisasi antar browser
    # State awal aplikasi
    shared_state = {
        "s": 1, 
        "a": 1, 
        "p": 0, 
        "v": False, 
        "wi": -1, 
        "st": "correct",
        "settings": {
            "verseSize": 64,
            "surahSize": 24,
            "transSize": 24,
            "lineHeight": 1.6,
            "overlayWidth": 85,
            "overlayPadding": 30,
            "maxWords": 0,
            "textAlign": "center",
            "verticalAlign": "center",
            "transLang": "id",
            "transDisplay": "block",
            "highlightColor": "#FFD166"
        },
        "t": 1
    }

    def do_POST(self):
        if self.path.startswith('/sync'):
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            new_state = json.loads(post_data.decode('utf-8'))
            SyncHandler.shared_state.update(new_state)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path.startswith('/sync'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.end_headers()
            self.wfile.write(json.dumps(SyncHandler.shared_state).encode('utf-8'))
        else:
            # Matikan cache untuk file statis agar selalu fresh
            super().do_GET()
            
    def end_headers(self):
        if self.path != '/sync':
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        super().end_headers()

if __name__ == '__main__':
    with ThreadingSimpleServer(("", PORT), SyncHandler) as httpd:
        hostname = socket.gethostname()
        try:
            local_ip = socket.gethostbyname(hostname)
        except:
            local_ip = "127.0.0.1"
            
        print(f"✅ Server Tahfidz Overlay berjalan di port {PORT}")
        print(f"📺 VIEW (untuk OBS): http://localhost:{PORT}/")
        print(f"🎮 CONTROL (untuk HP/Laptop): http://localhost:{PORT}/control.html")
        print(f"📱 Akses Jaringan: http://{local_ip}:{PORT}/control.html")
        print("Tekan Ctrl+C untuk menghentikan.")
        
        # Buka browser otomatis ke panel kontrol
        def open_browser():
            import time
            time.sleep(1)
            try:
                webbrowser.open(f"http://localhost:{PORT}/control.html")
            except:
                pass
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer dihentikan.")
