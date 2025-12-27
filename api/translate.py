# api/translate.py
import asyncio
import json
from googletrans import Translator
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

async def translate_async(text, src='auto', dest='en'):
    """Async wrapper for googletrans"""
    translator = Translator()
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, 
        lambda: translator.translate(text, src=src, dest=dest)
    )
    return result.text

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse URL and query parameters
            parsed_path = urlparse(self.path)
            query_params = parse_qs(parsed_path.query)
            
            text = query_params.get('text', [''])[0]
            src = query_params.get('src', ['auto'])[0]
            dest = query_params.get('dest', ['en'])[0]
            
            if not text:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'No text provided'}).encode())
                return
            
            # Run async translation
            translated_text = asyncio.run(translate_async(text, src, dest))
            
            # Return success response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'text': translated_text}).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def do_POST(self):
        self.do_GET()
