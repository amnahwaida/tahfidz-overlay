import http.server
import socketserver
import json
import socket
import webbrowser
import threading
import os
import queue

PORT = 8000
STATE_FILE = "data/last_state.json"

# List untuk menyimpan koneksi SSE klien
clients = []

class ThreadingSimpleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

def load_initial_state():
    default_state = {
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
            "lineHeight": 2.0,
            "overlayWidth": 85,
            "overlayPadding": 30,
            "maxWords": 0,
            "textAlign": "center",
            "verticalAlign": "center",
            "transLang": "id",
            "transDisplay": "block",
            "highlightColor": "#FFD166",
            "wrongColor": "#ff595e",
            "verseColor": "#ffffff",
            "surahColor": "#ffffff",
            "transColor": "#ffffff"
        },
        "t": 1
    }
    
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                saved_state = json.load(f)
                import time
                saved_state['t'] = int(time.time() * 1000)
                default_state.update(saved_state)
                print("💾 Berhasil memuat state sebelumnya.")
        except Exception as e:
            print(f"⚠️ Gagal memuat state sebelumnya: {e}")
            
    return default_state

def save_state(state):
    try:
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f)
    except Exception as e:
        print(f"⚠️ Gagal menyimpan state: {e}")

class SyncHandler(http.server.SimpleHTTPRequestHandler):
    shared_state = load_initial_state()

    def do_POST(self):
        if self.path.startswith('/sync'):
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            new_state = json.loads(post_data.decode('utf-8'))
            SyncHandler.shared_state.update(new_state)
            
            save_state(SyncHandler.shared_state)
            
            s = new_state.get('s','?')
            a = new_state.get('a','?')
            print(f"📡 Update: Surah {s} Ayah {a}")

            # Broadcast ke semua client SSE
            state_json = json.dumps(SyncHandler.shared_state)
            for c in list(clients):
                try:
                    c.put_nowait(state_json)
                except Exception:
                    pass

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        # Endpoint khusus untuk Server-Sent Events (SSE)
        if self.path == '/events':
            self.send_response(200)
            self.send_header('Content-type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.send_header('Connection', 'keep-alive')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            client_queue = queue.Queue()
            clients.append(client_queue)
            
            try:
                # Kirim state pertama kali saat konek
                initial_data = json.dumps(SyncHandler.shared_state)
                self.wfile.write(f"data: {initial_data}\n\n".encode('utf-8'))
                self.wfile.flush()
                
                # Terus hidup dan tunggu update
                while True:
                    msg = client_queue.get()
                    self.wfile.write(f"data: {msg}\n\n".encode('utf-8'))
                    self.wfile.flush()
            except Exception:
                pass # Client disconnect
            finally:
                if client_queue in clients:
                    clients.remove(client_queue)
            return

        # Endpoint polling jadul (untuk load awal)
        if self.path.startswith('/sync'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.end_headers()
            self.wfile.write(json.dumps(SyncHandler.shared_state).encode('utf-8'))
            return
            
        return super().do_GET()

    def end_headers(self):
        if self.path != '/sync' and self.path != '/events':
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        try:
            super().end_headers()
        except Exception:
            pass

if __name__ == '__main__':
    with ThreadingSimpleServer(("", PORT), SyncHandler) as httpd:
        hostname = socket.gethostname()
        try:
            local_ip = socket.gethostbyname(hostname)
        except:
            local_ip = "127.0.0.1"
            
        print(f"✅ Server Tahfidz Overlay berjalan di port {PORT}")
        print(f"📡 Sistem: Real-Time SSE (Server-Sent Events) AKTIF")
        print(f"📺 VIEW (untuk OBS): http://localhost:{PORT}/")
        print(f"🎮 CONTROL (untuk HP/Laptop): http://localhost:{PORT}/control.html")
        print(f"📱 Akses Jaringan: http://{local_ip}:{PORT}/control.html")
        print("Tekan Ctrl+C untuk menghentikan.")
        
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
