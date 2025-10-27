"""
Minimal, dependency-free MCP server for PromptToProduct repository integration.
Provides:
 - GET /health => simple healthcheck
 - GET /mcp => basic MCP info JSON with repository details
 - POST /github-webhook => receives GitHub webhook payloads from PromptToProduct repo

Run with: python -m mcp_server.main
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
from . import github
from .config import get_config

class MCPHandler(BaseHTTPRequestHandler):
    def _set_json(self, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        config = get_config()
        
        if self.path == '/health':
            self._set_json()
            health_data = {
                'status': 'ok',
                'repo': config['repo']['full_name'],
                'webhook_secret_configured': bool(config.get('github_webhook_secret'))
            }
            self.wfile.write(json.dumps(health_data).encode('utf-8'))
            return
            
        if self.path == '/mcp':
            self._set_json()
            info = {
                'name': 'prompt-to-product-mcp',
                'version': '0.1.0',
                'repository': config['repo'],
                'endpoints': ['/health', '/mcp', '/github-webhook'],
                'webhook_configured': bool(config.get('github_webhook_secret'))
            }
            self.wfile.write(json.dumps(info).encode('utf-8'))
            return
            
        self.send_error(404, 'Not found')

    def do_POST(self):
        if self.path == '/github-webhook':
            length = int(self.headers.get('Content-Length', '0'))
            raw = self.rfile.read(length) if length else b''
            try:
                payload = json.loads(raw.decode('utf-8')) if raw else {}
            except Exception:
                payload = {'_raw': raw.decode('utf-8', errors='replace')}

            # Delegate to github handler
            result = github.handle_github_event(dict(self.headers), payload, raw)

            # Enhanced logging for PromptToProduct events
            config = get_config()
            if config.get('debug'):
                print(f'GitHub webhook received: {json.dumps(result, indent=2)}')
            else:
                print(f'GitHub webhook: {result.get("event")} from {result.get("repo")} - {result.get("action")} (processed: {result.get("processed")})')
            
            if result.get('error'):
                print(f'Webhook error: {result["error"]}')
                self._set_json(400)
                self.wfile.write(json.dumps({'error': result['error']}).encode('utf-8'))
                return

            self._set_json(200)
            response = {
                'received': True, 
                'event': result.get('event'),
                'repo': result.get('repo'),
                'processed': result.get('processed', False)
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            return
        self.send_error(404, 'Not found')


def run(host=None, port=None):
    config = get_config()
    host = host or config['host']
    port = port or config['port']
    
    server = HTTPServer((host, port), MCPHandler)
    print(f'PromptToProduct MCP server listening on {host}:{port}')
    print(f'Configured for repository: {config["repo"]["full_name"]}')
    print(f'Webhook secret configured: {bool(config.get("github_webhook_secret"))}')
    print(f'Debug mode: {config.get("debug", False)}')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down')
    finally:
        server.server_close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='PromptToProduct MCP Server')
    parser.add_argument('--host', help='Host to bind to (default from MCP_HOST env or 0.0.0.0)')
    parser.add_argument('--port', type=int, help='Port to bind to (default from MCP_PORT env or 8080)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    
    # Override config with command line args if provided
    import os
    if args.debug:
        os.environ['DEBUG'] = 'true'
    
    run(args.host, args.port)
