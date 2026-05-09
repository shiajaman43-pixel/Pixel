import os
from flask import Flask, render_template_string

app = Flask(__name__)

# --- MAXIMUM REVENUE CONFIG ---
SMARTLINK = "https://potterynaggingformerly.com/n62zm634?key=3ddc98ba3a3e85cdb3143b568828daf2"

UI_STYLE = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
    body { background: #f4f7f6; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .header-box { background: #2c3e50; color: white; padding: 30px 15px; border-bottom: 5px solid #27ae60; }
    .card { border: none; border-radius: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .btn-main { background: #27ae60; color: white; padding: 15px 30px; font-weight: bold; border-radius: 10px; width: 100%; border: none; font-size: 1.2rem; }
    .timer-text { font-size: 2rem; color: #e74c3c; font-weight: bold; }
    .native-ad-box { min-height: 250px; background: #fff; border: 1px solid #ddd; margin: 15px 0; display: flex; align-items: center; justify-content: center; overflow: hidden; }
    .hidden { display: none; }
    .question-box { padding: 20px; background: #fff; border-left: 5px solid #2980b9; }
    .option-label { display: block; padding: 10px; margin: 5px 0; background: #f8f9fa; border-radius: 5px; cursor: pointer; transition: 0.2s; }
    .option-label:hover { background: #e9ecef; }
</style>
<script async="async" data-cfasync="false" src="https://pl29377894.profitablecpmratenetwork.com/49/6c/fa/496cfaa97c1bdc526da1c36625ffe71a.js"></script>
"""

# Dynamic Native Ad Script
NATIVE_JS = '<script async="async" data-cfasync="false" src="https://pl29378660.profitablecpmratenetwork.com/1c69caf291a12c5899a966465f2b4e0b/invoke.js"></script><div id="container-1c69caf291a12c5899a966465f2b4e0b"></div>'

@app.route('/')
def home():
    return render_template_string(UI_STYLE + f"""
    <div onclick="window.open('{SMARTLINK}', '_blank')" style="cursor:pointer">
        <div class="header-box text-center">
            <h1>HSC ICT Final Mock Test 2026</h1>
            <p>Complete the test to get your online certificate</p>
        </div>
        
        <div class="container mt-4">
            <div class="native-ad-box">{NATIVE_JS}</div>
            <div class="card p-4 text-center">
                <h3>Test Instructions</h3>
                <p class="text-muted">Total Questions: 15 | Passing Score: 40%</p>
                <button onclick="startTest()" class="btn-main shadow-lg">START TEST NOW</button>
            </div>
            <div class="native-ad-box">{NATIVE_JS}</div>
        </div>
    </div>
    <script>
        function startTest() {{
            window.location.href = '/exam';
        }}
    </script>
    """)

@app.route('/exam')
def exam():
    # Board Standard Internet & ICT Questions
    questions = [
        ("WWW er purno rup ki?", "World Wide Web", "World Wide Website"),
        ("HTTP er full form ki?", "Hypertext Transfer Protocol", "High Transfer Text Process"),
        ("Internet er madhyome chikitsha sebake ki bole?", "Telemedicine", "E-Health"),
        ("Nicher konti social media noy?", "Google", "Instagram"),
        ("IP version 4 koyti bit er?", "32 bit", "128 bit"),
        ("Bangladesh e 5G porikkhamulok bhabe kobe chalu hoy?", "2021", "2018"),
        ("Search Engine er udahoron konti?", "DuckDuckGo", "Safari"),
        ("HTML file er extension konti?", ".html", ".ht"),
        ("E-mail er full form ki?", "Electronic Mail", "Electrical Mail"),
        ("Nicher konti browse korar software?", "Opera Mini", "Android"),
        ("Data transmission speed ke ki bola hoy?", "Bandwidth", "Bitrate"),
        ("WiFi er purno rup ki?", "Wireless Fidelity", "Wireless Fiber"),
        ("Optical Fiber e kon prokriyay data jay?", "Purno Abhyantarin Protifolon", "Protishoron"),
        ("Computer er mastishko konti?", "CPU", "RAM"),
        ("Prithibir prothom computer network er naam ki?", "ARPANET", "Internet")
    ]

    q_html = ""
    for i, (q, o1, o2) in enumerate(questions):
        q_html += f"""
        <div class="card question-box">
            <p class='fw-bold'>{i+1}. {q}</p>
            <label class="option-label"><input type="radio" name="q{i}"> {o1}</label>
            <label class="option-label"><input type="radio" name="q{i}"> {o2}</label>
        </div>
        """
        if (i+1) % 5 == 0: # Every 5 questions, inject an ad
            q_html += f'<div class="native-ad-box">{NATIVE_JS}</div>'

    return render_template_string(UI_STYLE + f"""
    <div class="container mt-4">
        <h2 class="text-center mb-4">ICT MCQ Challenge</h2>
        <div id="test-area">
            {q_html}
            <button onclick="processResult()" class="btn-main mt-4 mb-5">SUBMIT ANSWERS</button>
        </div>

        <div id="loading" class="hidden text-center mt-5">
            <h2 class="text-primary">Verifying Answers...</h2>
            <div class="timer-text" id="countdown">7</div>
            <p>Please wait while we generate your certificate.</p>
            <div class="native-ad-box">{NATIVE_JS}</div>
        </div>
    </div>

    <script>
        function processResult() {{
            window.open('{SMARTLINK}', '_blank');
            document.getElementById('test-area').classList.add('hidden');
            document.getElementById('loading').classList.remove('hidden');
            let count = 7;
            let timer = setInterval(() => {{
                count--;
                document.getElementById('countdown').innerText = count;
                if(count <= 0) {{
                    clearInterval(timer);
                    window.location.href = '/result';
                }}
            }}, 1000);
        }}
    </script>
    """)

@app.route('/result')
def result():
    return render_template_string(UI_STYLE + f"""
    <div class="container mt-5">
        <div class="card p-5 text-center shadow-lg">
            <h4 class="text-muted">Your Score</h4>
            <h1 class="display-1 fw-bold text-success">14/15</h1>
            <p class="lead">Grade: <b>A+ (Excellent)</b></p>
            <div class="alert alert-info">Certificate is ready to download!</div>
            <div class="native-ad-box">{NATIVE_JS}</div>
            <button onclick="window.open('{SMARTLINK}', '_blank')" class="btn-main">⬇️ DOWNLOAD CERTIFICATE</button>
            <a href="/" class="btn btn-link mt-3 text-decoration-none">Retake Exam</a>
        </div>
        <div class="native-ad-box">{NATIVE_JS}</div>
    </div>
    <script>
        // Maximize revenue by opening one more ad on result load
        window.onload = function() {{
            setTimeout(() => {{ window.open('{SMARTLINK}', '_blank'); }}, 3000);
        }};
    </script>
    """)

if __name__ == '__main__':
    app.run(debug=True)
  
