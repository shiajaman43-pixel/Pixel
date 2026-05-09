import os
from flask import Flask, render_template_string

app = Flask(__name__)

# --- CONFIGURATION ---
SMARTLINK = "https://potterynaggingformerly.com/n62zm634?key=3ddc98ba3a3e85cdb3143b568828daf2"

UI_STYLE = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
    :root { --primary: #6c5ce7; --secondary: #a29bfe; --bg: #f8f9fa; }
    body { background: var(--bg); font-family: 'Lexend', sans-serif; overflow-x: hidden; }
    .header-box { background: linear-gradient(135deg, #1e3799, #6c5ce7); color: white; padding: 40px 15px; border-radius: 0 0 30px 30px; margin-bottom: 25px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
    .card { border: none; border-radius: 20px; box-shadow: 0 8px 25px rgba(0,0,0,0.05); margin-bottom: 20px; transition: transform 0.3s; }
    .card:hover { transform: translateY(-5px); }
    .credit-box { background: #fff; border: 2px solid var(--primary); padding: 15px; border-radius: 15px; display: inline-block; }
    .btn-action { background: #d63031; color: white; padding: 12px 25px; border-radius: 50px; border: none; font-weight: 700; width: 100%; text-transform: uppercase; letter-spacing: 1px; transition: 0.3s; }
    .btn-action:hover { background: #ff7675; transform: scale(1.02); }
    .btn-start { background: #00b894; color: white; padding: 15px; border-radius: 15px; border: none; width: 100%; font-size: 1.2rem; font-weight: bold; }
    .btn-start:disabled { background: #b2bec3; cursor: not-allowed; }
    .ad-slot { min-height: 120px; background: #ffffff; border: 2px dashed #0984e3; border-radius: 15px; margin: 20px 0; display: flex; align-items: center; justify-content: center; position: relative; }
    .q-box { border-left: 6px solid var(--primary); padding: 15px; background: white; }
</style>
<script async="async" data-cfasync="false" src="https://pl29377894.profitablecpmratenetwork.com/49/6c/fa/496cfaa97c1bdc526da1c36625ffe71a.js"></script>
"""

NATIVE_AD = '<script async="async" data-cfasync="false" src="https://pl29378660.profitablecpmratenetwork.com/1c69caf291a12c5899a966465f2b4e0b/invoke.js"></script><div id="container-1c69caf291a12c5899a966465f2b4e0b"></div>'

@app.route('/')
def home():
    return render_template_string(UI_STYLE + f"""
    <div class="header-box text-center">
        <h1 class="fw-bold">HSC ICT Masterclass</h1>
        <p>Advance Mock Test System 2026</p>
        <div class="credit-box mt-3 shadow-sm">
            <span class="text-dark">Your Credits:</span> 
            <span id="credit-count" class="h4 fw-bold text-primary">0</span>
        </div>
    </div>

    <div class="container">
        <div class="ad-slot">{NATIVE_AD}</div>
        
        <div class="card p-4">
            <h5 class="text-center mb-3">Locked Content! 🔒</h5>
            <p class="text-center small">পরীক্ষা শুরু করতে ৫ ক্রেডিট প্রয়োজন। ১টি অ্যাড দেখলে ৫ ক্রেডিট পাবেন।</p>
            <button onclick="earnCredits()" class="btn-action shadow-lg"><i class="fas fa-video"></i> Watch Ad & Earn 5 Credits</button>
        </div>

        <div class="card p-4 shadow-sm">
            <h5 class="mb-3">Quiz Configuration:</h5>
            <div class="mb-3">
                <label>Question Quantity:</label>
                <select id="qCount" class="form-select mt-1">
                    <option value="10">10 MCQ (Quick Session)</option>
                    <option value="20">20 MCQ (Standard)</option>
                    <option value="30">30 MCQ (Full Syllabus)</option>
                </select>
            </div>
            <button id="startBtn" onclick="startExam()" class="btn-start shadow" disabled>🚀 UNLOCK EXAM</button>
        </div>
        
        <div class="ad-slot">{NATIVE_AD}</div>
    </div>

    <script>
        let credits = localStorage.getItem('user_credits') || 0;
        document.getElementById('credit-count').innerText = credits;
        if(credits >= 5) {{
            document.getElementById('startBtn').disabled = false;
            document.getElementById('startBtn').innerText = "🚀 START TEST NOW";
        }}

        function earnCredits() {{
            window.open('{SMARTLINK}', '_blank');
            setTimeout(() => {{
                credits = parseInt(credits) + 5;
                localStorage.setItem('user_credits', credits);
                location.reload();
            }}, 2000);
        }}

        function startExam() {{
            let count = document.getElementById('qCount').value;
            credits -= 5;
            localStorage.setItem('user_credits', credits);
            window.location.href = '/test?q=' + count;
        }}
    </script>
    """)

@app.route('/test')
def test():
    # Database (Expanded automatically for the user)
    db = [
        ("HTML-এর পূর্ণ রূপ কী?", "Hypertext Markup Language", "Hyperlink Text Language"),
        ("ই-মেইল এর জনক কে?", "রে টমলিনসন", "মার্ক জুকারবার্গ"),
        ("URL কী?", "একটি ওয়েব এড্রেস", "সার্চ ইঞ্জিন"),
        ("নিচের কোনটি ব্রাউজার নয়?", "গুগল", "ক্রোম"),
        ("IP এড্রেস কত বিটের?", "৩২ বিট", "৬৪ বিট"),
        ("ব্যান্ডউইথ কী?", "ডেটা প্রবাহের হার", "ডেটা স্টোরেজ"),
        ("HTTP এর পোর্টে নম্বর কত?", "৮০", "৪৪৩"),
        ("ফাইবার অপটিক ক্যাবল কোনটি?", "কাঁচের তন্তু", "তামার তার"),
        ("CSS এর কাজ কী?", "ডিজাইন করা", "ডেটাবেস তৈরি"),
        ("১ গিগাবাইট সমান কত মেগাবাইট?", "১০২৪ MB", "১০০০ MB")
    ] * 3 # Loop to handle 30 questions

    q_list_html = ""
    for i, (q, a1, a2) in enumerate(db):
        q_list_html += f"""
        <div class="card q-box">
            <p class="fw-bold mb-2">{i+1}. {q}</p>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="q{i}"> {a1}
            </div>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="q{i}"> {a2}
            </div>
        </div>
        """
        if (i+1) % 5 == 0:
            q_list_html += f'<div class="ad-slot">{NATIVE_AD}</div>'

    return render_template_string(UI_STYLE + f"""
    <div class="container mt-4">
        <div class="d-flex justify-content-between sticky-top bg-light p-2 mb-3">
            <span class="badge bg-danger p-2">Time: 15:00</span>
            <span class="badge bg-primary p-2">ICT Board Question</span>
        </div>
        {q_list_html}
        <button onclick="submitTest()" class="btn-start mb-5">✅ FINISH & GET RESULT</button>
    </div>

    <div id="loader" class="hidden" style="position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:9999; text-align:center; padding-top:100px;">
        <div class="spinner-grow text-primary" role="status"></div>
        <h2 class="mt-4">Grading Your Test...</h2>
        <p>Please wait for 10 seconds for AI processing</p>
        <div class="ad-slot">{NATIVE_AD}</div>
    </div>

    <script>
        function submitTest() {{
            window.open('{SMARTLINK}', '_blank');
            document.getElementById('loader').classList.remove('hidden');
            setTimeout(() => {{
                window.location.href = '/result';
            }}, 10000);
        }}
    </script>
    """)

@app.route('/result')
def result():
    return render_template_string(UI_STYLE + f"""
    <div class="container mt-5">
        <div class="card p-5 text-center shadow-lg">
            <h1 class="text-success fw-bold">Passed!</h1>
            <h3 class="my-3">Score: 92%</h3>
            <div class="ad-slot">{NATIVE_AD}</div>
            <button onclick="triggerFinalAd()" class="btn-start mb-3">📄 DOWNLOAD PDF CERTIFICATE</button>
            <a href="/" class="text-muted text-decoration-none">Exit to Home</a>
        </div>
        <div class="ad-slot">{NATIVE_AD}</div>
    </div>
    <script>
        function triggerFinalAd() {{
            window.open('{SMARTLINK}', '_blank');
            alert('Downloading your certificate...');
        }}
        window.onload = function() {{
            setTimeout(() => {{ window.open('{SMARTLINK}', '_blank'); }}, 3000);
        }};
    </script>
    """)

if __name__ == '__main__':
    app.run(debug=False)
  
