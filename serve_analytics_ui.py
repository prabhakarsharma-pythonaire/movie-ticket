#!/usr/bin/env python3
"""
Simple HTTP server to serve the Analytics UI
"""

import http.server
import socketserver
import os
import webbrowser
from urllib.parse import urlparse

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def main():
    PORT = 8080
    
    # Change to the directory containing the HTML file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create server
    with socketserver.TCPServer(("", PORT), CORSHTTPRequestHandler) as httpd:
        print(f"🎬 Analytics UI Server Started!")
        print(f"📊 Dashboard URL: http://localhost:{PORT}/analytics_ui.html")
        print(f"🔗 API Server: http://localhost:8000")
        print(f"📋 Make sure your FastAPI server is running on port 8000")
        print(f"🚀 Opening dashboard in browser...")
        print(f"⏹️  Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Open browser
        webbrowser.open(f'http://localhost:{PORT}/analytics_ui.html')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n🛑 Server stopped by user")
            httpd.shutdown()

if __name__ == "__main__":
    main()
