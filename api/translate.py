# api/translate.py
import asyncio
from flask import Flask, request, jsonify
from googletrans import Translator

app = Flask(__name__)

async def translate_async(text, src='auto', dest='en'):
    """Async wrapper for googletrans"""
    translator = Translator()
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, 
        lambda: translator.translate(text, src=src, dest=dest)
    )
    return result.text

@app.route('/api/translate', methods=['GET', 'POST'])
def translate():
    try:
        # Get text from query parameter or JSON body
        if request.method == 'GET':
            text = request.args.get('text', '')
            src = request.args.get('src', 'auto')
            dest = request.args.get('dest', 'en')
        else:
            data = request.get_json()
            text = data.get('text', '')
            src = data.get('src', 'auto')
            dest = data.get('dest', 'en')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Run async translation
        translated_text = asyncio.run(translate_async(text, src, dest))
        
        # Return only the translated text
        return jsonify({'text': translated_text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# For local testing
if __name__ == '__main__':
    app.run(debug=True)