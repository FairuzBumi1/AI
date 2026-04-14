from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

# Konfigurasi folder templates agar terbaca oleh Vercel
app = Flask(__name__, template_folder='../templates')

# Ambil API Key dari environment variable Vercel
API_KEY = os.getenv("GEMINI_API_KEY")

try:
    genai.configure(api_key=API_KEY)
    # Pakai model versi 3 sesuai kemauan kamu
    model = genai.GenerativeModel('gemini-3-flash-preview')
except Exception as e:
    print(f"Error Konfigurasi: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get("message")
    
    if not API_KEY:
        return jsonify({"error": "API Key belum disetting di Vercel!"}), 500

    if not user_message:
        return jsonify({"error": "Pesan kosong!"}), 400

    try:
        response = model.generate_content(user_message)
        if response and response.text:
            return jsonify({"response": response.text})
        else:
            return jsonify({"response": "Maaf, Aletha AI tidak bisa merespon."})
    except Exception as e:
        return jsonify({"error": f"Error dari Gemini API: {str(e)}"}), 500

if __name__ == '__main__':
    app.run()
