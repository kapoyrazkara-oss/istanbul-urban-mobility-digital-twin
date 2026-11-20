from __future__ import annotations

import http.server
import socketserver
import threading
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"[final3d] {self.address_string()} - {fmt % args}")


def main() -> None:
    handler = lambda *args, **kwargs: QuietHandler(*args, directory=str(ROOT), **kwargs)
    with socketserver.TCPServer(("127.0.0.1", 0), handler) as server:
        port = server.server_address[1]
        url = f"http://127.0.0.1:{port}/viewer.html"
        print(f"[final3d] Viewer: {url}")
        print("[final3d] Bu pencereyi kapatmayın; çıkmak için Ctrl+C kullanın.")
        threading.Timer(0.7, lambda: webbrowser.open(url)).start()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n[final3d] Server kapatıldı.")

if __name__ == "__main__":
    main()
