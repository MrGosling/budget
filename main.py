import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from budget import Budget
import request_handlers as logic


class BudgetHandler(BaseHTTPRequestHandler):
    budget = Budget()

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        output = json.dumps(data if isinstance(data, (dict, list)) else {"message": data}, ensure_ascii=False)
        self.wfile.write(output.encode('utf-8'))

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/':
            return logic.handle_root(self)

        if path == '/api/v1/healthcheck':
            return logic.handle_healthcheck(self)

        if path == '/api/v1/help':
            return logic.handle_help(self)

        m = re.match(r'^/api/v1/expenses/max_category/(\d{1,2})$', path)
        if m:
            return logic.handle_max_category(self, m.group(1))

        m = re.match(r'^/api/v1/expenses/([^/]+)/max/(\d{1,2})$', path)
        if m:
            return logic.handle_max_purchase(self, m.group(1), m.group(2))

        self.send_error(404, "Not Found")

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/api/v1/expenses':
            return logic.handle_add_expense(self)

        self.send_error(404, "Not Found")


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8000
    server = ThreadingHTTPServer((host, port), BudgetHandler)
    print(f"Server running at http://{host}:{port}")
    server.serve_forever()
