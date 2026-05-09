import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- AD CONFIGURATION ---
SMARTLINK_1 = "https://potterynaggingformerly.com/surggewa?key=91990ae75a2cedbea643e7b2b13aadf6"
SMARTLINK_2 = "https://potterynaggingformerly.com/n62zm634?key=3ddc98ba3a3e85cdb3143b568828daf2"

# এখানে আপনার অ্যাড কোডগুলো সরাসরি ডিফাইন করা হলো
POPUNDER_SCRIPT = '<script src="https://potterynaggingformerly.com/49/6c/fa/496cfaa97c1bdc526da1c36625ffe71a.js"></script>'
SOCIAL_BAR_SCRIPT = '<script src="https://potterynaggingformerly.com/76/41/5a/76415aaef6ad249973a92bb8f1251a22.js"></script>'

BANNER_AD = """
<script type="text/javascript">
  atOptions = { 'key' : '3ba591d1fc0f098ac02b41fdd3ceb0c5', 'format' : 'iframe', 'height' : 250, 'width' : 300, 'params' : {} };
</script>
<script type="text/javascript" src="https://potterynaggingformerly.com/3ba591d1fc0f098ac02b41fdd3ceb0c5/invoke.js"></script>
"""

NATIVE_AD = """
<script async="async" data-cfasync="false" src="https://potterynaggingformerly.com/1c69caf291a12c5899a966465f2b4e0b/invoke.js"></script>
<div id="container-1c69caf291a12c5899a966465f2b4e0b"></div>
"""

@app.route('/')
def home():
    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>All Subject Exam Portal</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        {POPUNDER_SCRIPT}
        {SOCIAL_BAR_SCRIPT}
        <style>
            body {{ background: #f4f7f6; font-family: 'Segoe UI', sans-serif; }}
            .header {{ background: #1e3799; color: white; padding: 40px 10px; border-radius: 0 0 30px 30px; text-align: center; }}
            .card {{ border: none; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: -30px; }}
            .btn-earn {{ background: #ff4d4f; color: white; border: none; padding: 15px; width: 100%; border-radius: 10px; font-weight: bold; margin-bottom: 20px; }}
            .btn-start {{ background: #27ae60; color: white; border: none; padding: 15px; width: 100%; border-radius: 10px; font-weight: bold; font-size: 1.1rem; }}
            .ad-box {{ text-align: center; margin: 20px 0; background: #fff; padding: 10px; border-radius: 10px; }}
        </style>
    </head>
    <body>
        <div class="header shadow-lg">
            <h1>HSC Multi-Subject Mock Test</h1>
            <p>Earn Credits to Unlock Exams</p>
            <div class="badge bg-warning text-dark p-2 mt-2">Credits: <span id="c_val">0</span></div>
        </div>

        <div class="container">
            <div class="card p-4 mt-3">
                <button onclick="earnCr()" class="btn-earn shadow">💎 WATCH AD & GET 5 CREDITS</button>
                
                <h5 class="mb-3">Select Your Subject:</h5>
                <select id="subj" class="form-select mb-4">
                    <option value="ict">ICT (Information & Tech)</option>
                    <option value="eng">English Grammar</option>
                    <option value="gk">General Knowledge</option>
                </select>

                <button id="s_btn" onclick="start()" class="btn-start shadow" disabled>LOCKED (5 Credits Required)</button>
            </div>

            <div class="ad-box shadow-sm">
                {BANNER_AD}
            </div>
        </div>

        <script>
            let cr = localStorage.getItem('my_credits') || 0;
            document.getElementById('c_val').innerText = cr;
            if(cr >= 5) {{
                document.getElementById('s_btn').disabled = false;
                document.getElementById('s_btn').innerText = "🚀 START 30 MCQ TEST";
            }}

            function earnCr() {{
                window.open('{SMARTLINK_1}', '_blank');
                setTimeout(() => {{
                    localStorage.setItem('my_credits', parseInt(cr) + 5);
                    location.reload();
                }}, 2000);
            }}

            function start() {{
                localStorage.setItem('my_credits', cr - 5);
                window.location.href = '/exam?sub=' + document.getElementById('subj').value;
            }}
        </script>
    </body>
    </html>
    """)

@app.route('/exam')
def exam():
    sub = request.args.get('sub', 'ict')
    
    # প্রশ্ন ব্যাংক (৩০টি করে প্রশ্ন)
    questions_ict = [("HTML এর জনক কে?", "টিম বার্নার্স লি", "রে টমলিনসন"), ("IP Address কত বিটের?", "৩২ বিট", "১২৮ বিট"), ("মডেম কী?", "I/O ডিভাইস", "আউটপুট")] * 10
    questions_eng = [("Which one is a noun?", "Water", "Beautiful"), ("Identify Verb:", "Go", "Good"), ("Antonym of Big?", "Small", "Large")] * 10
    questions_gk = [("বাংলাদেশের রাজধানী?", "ঢাকা", "চট্টগ্রাম"), ("জাতীয় কবি কে?", "নজরুল", "রবীন্দ্রনাথ"), ("বিজয় দিবস কবে?", "১৬ ডিসে", "২৬ মার্চ")] * 10

    if sub == 'eng': current_qs = questions_eng
    elif sub == 'gk': current_qs = questions_gk
    else: current_qs = questions_ict

    q_html = ""
    for i, (q, a, b) in enumerate(current_qs):
        q_html += f"""
        <div class="card p-3 mb-3" style="border-left: 5px solid #1e3799;">
            <p class="fw-bold">{i+1}. {q}</p>
            <label class="d-block"><input type="radio" name="q{i}"> {a}</label>
            <label class="d-block"><input type="radio" name="q{i}"> {b}</label>
        </div>
        """
        # প্রতি ৫টি প্রশ্নের পর ব্যানার বা নেটিভ অ্যাড
        if (i+1) % 5 == 0:
            if (i+1) % 10 == 0: q_html += f'<div class="ad-box">{BANNER_AD}</div>'
            else: q_html += f'<div class="ad-box">{NATIVE_AD}</div>'

    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        {POPUNDER_SCRIPT}
        {SOCIAL_BAR_SCRIPT}
    </head>
    <body style="background:#f4f7f6;">
        <div class="container mt-4">
            <h4 class="text-center p-3 bg-white shadow-sm rounded">Subject: {sub.upper()}</h4>
            {q_html}
            <div class="ad-box">{BANNER_AD}</div>
            <button onclick="finish()" class="btn btn-success w-100 p-3 shadow mb-5">✅ SUBMIT & GET RESULT</button>
        </div>

        <div id="loading" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:9999; text-align:center; padding-top:100px;">
            <h3>Analyzing Score...</h3>
            <div class="ad-box">{BANNER_AD}</div>
        </div>

        <script>
            function finish() {{
                window.open('{SMARTLINK_2}', '_blank');
                document.getElementById('loading').style.display = 'block';
                setTimeout(() => {{ window.location.href = '/result'; }}, 10000);
            }}
        </script>
    </body>
    </html>
    """)

@app.route('/result')
def result():
    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        {POPUNDER_SCRIPT}
        {SOCIAL_BAR_SCRIPT}
    </head>
    <body class="bg-light text-center">
        <div class="container mt-5">
            <div class="card p-5 shadow">
                <h1 class="text-success fw-bold">RESULT: 92%</h1>
                <p>Grade: A+ (Excellent)</p>
                <div class="ad-box">{BANNER_AD}</div>
                <button onclick="window.open('{SMARTLINK_2}', '_blank')" class="btn btn-primary w-100 p-3 mt-3">⬇️ DOWNLOAD CERTIFICATE</button>
                <a href="/" class="d-block mt-4 text-muted">Go Back</a>
            </div>
            <div class="ad-box">{NATIVE_AD}</div>
        </div>
        <script>
            window.onload = function() {{
                setTimeout(() => {{ window.open('{SMARTLINK_1}', '_blank'); }}, 3000);
            }};
        </script>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=False)
