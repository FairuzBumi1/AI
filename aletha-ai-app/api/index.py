from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

# Karena folder api/ sejajar dengan folder templates/
app = Flask(__name__, template_folder='../templates')

# Mengambil API Key yang aman dari Environment Variable Vercel
API_KEY = os.getenv("GEMINI_API_KEY")

# Konfigurasi Gemini (Pastikan model name-nya sudah tepat)
try:
    genai.configure(api_key=API_KEY)
    # Ganti baris model kamu jadi ini:
model = genai.GenerativeModel('gemini-3-flash-preview')
except Exception as e:
    print(f"Error Konfigurasi Gemini: {e}")

@app.route('/')
def home():
    # Menampilkan halaman utama dari templates/index.html
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get("message")
    
    # Cek apakah API_KEY kosong (lupa disetting di Vercel)
    if not API_KEY:
        return jsonify({"error": "API Key belum disetting di Vercel!"}), 500

    if not user_message:
        return jsonify({"error": "Pesan kosong!"}), 400

    try:
        # Kirim pesan user ke model Gemini
        response = model.generate_content(user_message)
        
        # Ambil teks jawaban dari respon Gemini
        if response and response.text:
            return jsonify({"response": response.text})
        else:
            return jsonify({"response": "Maaf, Aletha AI tidak bisa memberikan respon saat ini."})
            
    except Exception as e:
        return jsonify({"error": f"Error dari Gemini API: {str(e)}"}), 500

# Wajib ada agar Vercel bisa menjalankan Flask
if __name__ == '__main__':
    app.run()
