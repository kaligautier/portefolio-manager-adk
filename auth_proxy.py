#!/usr/bin/env python3
"""Simple authenticated proxy for Cloud Run service."""
import subprocess
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import json

SERVICE_URL = "https://porte-folio-manager-j6sw5ssaca-ew.a.run.app"
PORT = 8080

def get_identity_token():
    """Get identity token from gcloud."""
    result = subprocess.run(
        ["gcloud", "auth", "print-identity-token"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.proxy_request()

    def do_POST(self):
        self.proxy_request()

    def proxy_request(self):
        try:
            token = get_identity_token()
            url = SERVICE_URL + self.path

            # Prepare request
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": self.headers.get("Content-Type", "application/json")
            }

            # Read body for POST requests
            body = None
            if self.command == "POST":
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length)

            # Make request
            req = urllib.request.Request(url, data=body, headers=headers)
            with urllib.request.urlopen(req) as response:
                self.send_response(response.status)
                for header, value in response.headers.items():
                    if header.lower() not in ["transfer-encoding", "connection"]:
                        self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.read())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())

    def log_message(self, format, *args):
        print(f"[{self.command}] {args[0]} - {args[1]}")

if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), ProxyHandler)
    print(f"🚀 Proxy server running on http://localhost:{PORT}")
    print(f"📖 Access Swagger UI at: http://localhost:{PORT}/docs")
    print(f"🔗 Proxying to: {SERVICE_URL}")
    print("\nPress Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Stopping proxy server...")
        sys.exit(0)
