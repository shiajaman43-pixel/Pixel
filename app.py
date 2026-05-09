import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- AD CONFIGURATION ---
SMARTLINK_1 = "https://potterynaggingformerly.com/surggewa?key=91990ae75a2cedbea643e7b2b13aadf6"
SMARTLINK_2 = "https://potterynaggingformerly.com/n62zm634?key=3ddc98ba3a3e85cdb3143b568828daf2"

# 300x250 Banner Script
BANNER_AD = """
<script type="text/javascript">
  atOptions = {
    'key' : '3ba591d1fc0f098ac02b41fdd3ceb0c5',
    'format' : 'iframe',
    'height' : 250,
    'width' : 300,
    'params' : {}
  };
</script>
<script type="text/javascript" src="https://potterynaggingformerly.com/3ba591d1fc0f098ac02b41fdd3ceb0c5/invoke.js"></script>
"""

# Native Banner Script
NATIVE_BANNER = """
<script async="async" data-cfasync="false" src="https://potterynaggingformerly.com/1c69caf291a12c5899a966465f2b4e0b/invoke.js"></script>
<div id="container-1c69caf291a12c5899a966465f2b4e0b"></div>
"""

# Pop-under Script
POPUNDER_JS = '<script src="https://potterynaggingformerly.com/49/6c/fa/496cfaa97c1bdc526da1c36625ffe71a.js"></script>'

UI_STYLE = f"""
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
{POPUNDER_JS}
<style>
    body {{ background: #f4f6f9; font-family: 'Poppins', sans-serif; }}
    .header-box {{ background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; padding: 45px 15px; border-radius: 0 0 30px 30px; }}
    .credit-status {{ background: #ffeaa7; color: #d35400; padding: 10px; border-radius: 10px; font-weight: bold; margin-bottom: 20px; }}
    .card {{ border: none; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px; overflow: hidden; }}
    .btn-earn {{ background: #ff4757; color: white; padding: 15px; width: 100%; border: none; border-radius: 10px; font-weight: bold; animation: pulse 2s infinite; }}
    .btn-start {{ background: #2ed573; color: white; padding: 15px; width: 100%; border: none; border-radius: 10px; font-weight: bold; font-size: 1.1rem; }}
    .ad-slot {{ background: #fff; margin: 15px 0; display: flex; justify-content: center; align-items: center; min-height: 250px; border: 1px solid #ddd; }}
    @keyframes pulse {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.02); }} 100% {{ transform: scale(1); }} }}
</style>
"""

@app.route('/')
def index():
    return render_template_string(UI_STYLE + f"""
    <div class="header-box text-center shadow-lg">
        <h1>ICT Mock Test Pro</h1>
        <p>Unlock your potential & get a certificate</p>
        <div class="credit-status d-inline-block">Credits: <span id="cr">0</span></div>
    </div>

    <div class="container mt-4">
        <!-- Banner Ad at Top -->
        <div class="ad-slot shadow-sm">{BANNER_AD}</div>

        <div class="card p-4 text-center">
            <h4><i class="fas fa-lock text-danger"></i> Exam is Locked!</h4>
            <p>পরীক্ষা দিতে হলে ৫ ক্রেডিট প্রয়োজন। ১টি অ্যাড দেখলে ৫ ক্রেডিট পাবেন।</p>
            <button onclick="earnCr()" class="btn-earn">🎁 EARN CREDITS (SMART AD)</button>
        </div>

        <div class="card p-4">
            <label class="fw-bold mb-2">Select Questions:</label>
            <select id="qc" class="form-select mb-3">
                <option value="10">10 Questions (Quick)</option>
                <option value="25">25 Questions (Standard)</option>
                <option value="50">50 Questions (Advanced)</option>
            </select>
            <button id="sbt" onclick="start()" class="btn-start shadow" disabled>🚀 UNLOCK & START</button>
        </div>

        <!-- Native Banner at Bottom -->
        <div class="card p-2">{NATIVE_BANNER}</div>
    </div>

    <script>
        let c = localStorage.getItem('ict_c') || 0;
        document.getElementById('cr').innerText = c;
        if(c >= 5) {{
            document.getElementById('sbt').disabled = false;
            document.getElementById('sbt').innerHTML = "🚀 START EXAM";
        }}

        function earnCr() {{
            window.open('{SMARTLINK_1}', '_blank');
            setTimeout(() => {{
                localStorage.setItem('ict_c', parseInt(c) + 5);
                location.reload();
            }}, 3000);
        }}

        function start() {{
            localStorage.setItem('ict_c', c - 5);
            window.location.href = '/exam?count=' + document.getElementById('qc').value;
        }}
    </script>
    """)

@app.route('/exam')
def exam():
    count = int(request.args.get('count', 10))
    # ICT Questions Database (Sample)
    qs = [
        ("HTML এর জনক কে?", "টিম বার্নার্স লি", "মার্ক জুকারবার্গ"),
        ("IP Address (IPv4) কত বিটের?", "৩২ বিট", "১২৮ বিট"),
        ("ই-মেইলের জনক কে?", "রে টমলিনসন", "বিল গেটস"),
        ("URL এর পূর্ণরূপ কী?", "Uniform Resource Locator", "Universal Radio Link"),
        ("Wi-Fi এর পূর্ণরূপ কী?", "Wireless Fidelity", "Wireless Fiber"),
        ("১ গিগাবাইট সমান কত মেগাবাইট?", "১০২৪ MB", "১০০০ MB"),
        ("C++ কোন ধরনের ল্যাঙ্গুয়েজ?", "High Level", "Machine Level"),
        ("ফেসবুকের প্রতিষ্ঠাতা কে?", "মার্ক জুকারবার্গ", "স্টিভ জবস"),
        ("Bluetooth কোন নেটওয়ার্কের উদাহরণ?", "PAN", "LAN"),
        ("১ বাইট সমান কত বিট?", "৮ বিট", "১৬ বিট")
    ] * 5 # Multiplying to handle 50 questions
    
    selected_qs = qs[:count]
    q_html = ""
    for i, (q, o1, o2) in enumerate(selected_qs):
        q_html += f"""
        <div class="card p-3 border-start border-primary border-5">
            <p class="fw-bold">{i+1}. {q}</p>
            <label class="d-block mb-1"><input type="radio" name="q{i}"> {o1}</label>
            <label class="d-block"><input type="radio" name="q{i}"> {o2}</label>
        </div>
        """
        # Inject Banner or Native Ad every 5 questions
        if (i+1) % 5 == 0:
            if (i+1) % 10 == 0:
                q_html += f'<div class="ad-slot">{BANNER_AD}</div>'
            else:
                q_html += f'<div class="card p-2">{NATIVE_BANNER}</div>'

    return render_template_string(UI_STYLE + f"""
    <div class="container mt-4">
        <h4 class="text-center mb-4 text-primary">Board Standard MCQ Exam</h4>
        {q_html}
        <div class="ad-slot">{BANNER_AD}</div>
        <button onclick="finish()" class="btn-start mb-5 shadow">✅ SUBMIT ANSWERS</button>
    </div>

    <div id="wait" class="hidden" style="position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:9999; text-align:center; padding-top:100px;">
        <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;"></div>
        <h3 class="mt-3">Analyzing Score...</h3>
        <p>Please wait for ad verification</p>
        <div class="ad-slot">{BANNER_AD}</div>
    </div>

    <script>
        function finish() {{
            window.open('{SMARTLINK_2}', '_blank');
            document.getElementById('wait').classList.remove('hidden');
            setTimeout(() => {{ window.location.href = '/result'; }}, 12000);
        }}
    </script>
    """)

@app.route('/result')
def result():
    return render_template_string(UI_STYLE + f"""
    <div class="container mt-5">
        <div class="card p-5 text-center shadow-lg border-0">
            <h1 class="text-success fw-bold">94% Score!</h1>
            <p class="lead">Grade: A+ (Excellent Performance)</p>
            <hr>
            <div class="ad-slot">{BANNER_AD}</div>
            <button onclick="window.open('{SMARTLINK_2}', '_blank')" class="btn-start">🎓 DOWNLOAD CERTIFICATE</button>
            <a href="/" class="mt-4 d-block text-decoration-none">Retake Test</a>
        </div>
        <div class="card p-2 mt-4">{NATIVE_BANNER}</div>
    </div>
    <script>
        window.onload = function() {{
            setTimeout(() => {{ window.open('{SMARTLINK_1}', '_blank'); }}, 3000);
        }};
    </script>
    """)

if __name__ == '__main__':
    app.run(debug=False)
  
