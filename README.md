# Flask Translation API

This is a simple REST API built with Flask that translates text using the `googletrans` library.

## Features

- Translate text between languages
- Automatic source language detection (`src='auto'`)
- Supports both GET and POST requests
- Returns JSON responses

## Requirements

- Python 3.8+
- Flask
- googletrans (version 4.0.0-rc1 recommended)

Install dependencies:

```
pip install flask googletrans==4.0.0-rc1
```

## Running the App

From the project root directory:

```
python api/translate.py
```

The server will run at:

```
http://127.0.0.1:5000
```

## API Endpoint

```
/api/translate
```

## GET Request Example

```
http://127.0.0.1:5000/api/translate?text=Hola&src=es&dest=en
```

Response:

```json
{
  "text": "Hello"
}
```

## POST Request Example

```
POST /api/translate
Content-Type: application/json
```

Request body:

```json
{
  "text": "Bonjour",
  "src": "fr",
  "dest": "en"
}
```

Response:

```json
{
  "text": "Hello"
}
```

## Parameters

- `text` (required): Text to translate  
- `src` (optional): Source language code (default: auto)  
- `dest` (optional): Destination language code (default: en)  

## Notes

- Returns `400` if no text is provided.
- Returns `500` if an internal error occurs.
- `googletrans` is an unofficial API and may break if Google changes their endpoints.
