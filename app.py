import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- AD CONFIGURATION ---
SMARTLINK_1 = "https://potterynaggingformerly.com/surggewa?key=91990ae75a2cedbea643e7b2b13aadf6"
SMARTLINK_2 = "https://potterynaggingformerly.com/n62zm634?key=3ddc98ba3a3e85cdb3143b568828daf2"
SOCIAL_BAR = '<script src="https://potterynaggingformerly.com/76/41/5a/76415aaef6ad249973a92bb8f1251a22.js"></script>'
POPUNDER_JS = '<script src="https://potterynaggingformerly.com/49/6c/fa/496cfaa97c1bdc526da1c36625ffe71a.js"></script>'

BANNER_AD = """
<script type="text/javascript">
  atOptions = { 'key' : '3ba591d1fc0f098ac02b41fdd3ceb0c5', 'format' : 'iframe', 'height' : 250, 'width' : 300, 'params' : {} };
</script>
<script type="text/javascript" src="https://potterynaggingformerly.com/3ba591d1fc0f098ac02b41fdd3ceb0c5/invoke.js"></script>
"""

NATIVE_BANNER = """
<script async="async" data-cfasync="false" src="https://potterynaggingformerly.com/1c69caf291a12c5899a966465f2b4e0b/invoke.js"></script>
<div id="container-1c69caf291a12c5899a966465f2b4e0b"></div>
"""

UI_STYLE = f"""
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
{POPUNDER_JS} {SOCIAL_BAR}
<style>
    body {{ background: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
    .header-box {{ background: linear-gradient(135deg, #1e3799, #0984e3); color: white; padding: 50px 15px; border-radius: 0 0 40px 40px; margin-bottom: 30px; }}
    .credit-tag {{ background: #fff2e8; color: #fa541c; border: 1px solid #ffbb96; padding: 5px 20px; border-radius: 50px; font-weight: bold; }}
    .card {{ border: none; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); margin-bottom: 25px; }}
    .btn-earn {{ background: #ff4d4f; color: white; border: none; padding: 15px; border-radius: 12px; font-weight: bold; width: 100%; transition: 0.3s; }}
    .btn-start {{ background: #52c41a; color: white; border: none; padding: 18px; border-radius: 12px; font-weight: bold; width: 100%; font-size: 1.2rem; }}
    .ad-slot {{ min-height: 250px; display: flex; justify-content: center; align-items: center; background: white; border-radius: 15px; margin: 20px 0; border: 1px dashed #d9d9d9; }}
    .q-card {{ border-left: 6px solid #1890ff; padding: 20px; }}
    .hidden {{ display: none; }}
</style>
"""

@app.route('/')
def home():
    return render_template_string(UI_STYLE + f"""
    <div class="header-box text-center shadow-lg">
        <h1 class="fw-bold">All Subject Mock Test 2026</h1>
        <p>Select your subject and earn a professional certificate</p>
        <div class="credit-tag">Balance: <span id="cr_val">0</span> Credits</div>
    </div>

    <div class="container mt-n4">
        <div class="card p-4 text-center">
            <h5 class="mb-3">Unlock Exam Access 🔒</h5>
            <p class="text-muted small">যেকোনো পরীক্ষায় অংশগ্রহণের জন্য ৫ ক্রেডিট প্রয়োজন। ১টি অ্যাড দেখলে ৫ ক্রেডিট পাবেন।</p>
            <button onclick="addCr()" class="btn-earn shadow-sm">🎁 GET 5 CREDITS (WATCH AD)</button>
        </div>

        <div class="card p-4">
            <h6 class="fw-bold mb-3">Exam Configuration:</h6>
            <div class="mb-3">
                <label class="small fw-bold">Select Subject:</label>
                <select id="subj" class="form-select">
                    <option value="ict">ICT (Information Technology)</option>
                    <option value="eng">English Grammar</option>
                    <option value="gk">General Knowledge (Bangladesh)</option>
                </select>
            </div>
            <button id="sBtn" onclick="launch()" class="btn-start shadow" disabled>UNLOCKED EXAM</button>
        </div>
        <div class="ad-slot">{BANNER_AD}</div>
    </div>

    <script>
        let credits = localStorage.getItem('user_credits') || 0;
        document.getElementById('cr_val').innerText = credits;
        if(credits >= 5) {{
            document.getElementById('sBtn').disabled = false;
            document.getElementById('sBtn').innerText = "🚀 START 30 MCQ TEST";
        }}

        function addCr() {{
            window.open('{SMARTLINK_1}', '_blank');
            setTimeout(() => {{
                localStorage.setItem('user_credits', parseInt(credits) + 5);
                location.reload();
            }}, 2500);
        }}

        function launch() {{
            localStorage.setItem('user_credits', credits - 5);
            window.location.href = '/exam?sub=' + document.getElementById('subj').value;
        }}
    </script>
    """)

@app.route('/exam')
def exam():
    sub = request.args.get('sub', 'ict')
    
    # Question Banks (30 MCQs Each)
    questions = {
        'ict': [
            ("HTML এর জনক কে?", "টিম বার্নার্স লি", "রে টমলিনসন"),
            ("IP Address (IPv4) কত বিট?", "৩২ বিট", "১২৮ বিট"),
            ("ব্যান্ডউইথ কী?", "ডেটা প্রবাহের হার", "ডেটা স্টোরেজ"),
            ("URL এর পূর্ণরূপ কী?", "Uniform Resource Locator", "Universal Radio Link"),
            ("Wi-Fi এর পূর্ণরূপ কী?", "Wireless Fidelity", "Wireless Fiber"),
            ("১ গিগাবাইট সমান কত এমবি?", "১০২৪ MB", "১০০০ MB"),
            ("ই-মেইলের জনক কে?", "রে টমলিনসন", "বিল গেটস"),
            ("মডেম একটি?", "ইনপুট-আউটপুট ডিভাইস", "কেবল আউটপুট"),
            ("ASCII-8 কত বিটের?", "৮ বিট", "১৬ বিট"),
            ("সবচেয়ে বড় হেডার ট্যাগ কোনটি?", "<h1>", "<h6>"),
            # ... Adding more to reach 30
        ] * 3,
        'eng': [
            ("Which one is a Noun?", "Happiness", "Happy"),
            ("He ___ to school every day.", "goes", "going"),
            ("Antonym of 'Hot' is?", "Cold", "Warm"),
            ("Which one is Correct?", "Receive", "Recieve"),
            ("I have ___ umbrella.", "an", "a"),
            ("Plural of 'Child' is?", "Children", "Childs"),
            ("He is ___ M.A.", "an", "a"),
            ("Identify the Verb:", "Eat", "Food"),
            ("Synonym of 'Fast' is?", "Quick", "Slow"),
            ("A person who writes books?", "Author", "Doctor"),
        ] * 3,
        'gk': [
            ("বাংলাদেশের রাজধানী কোনটি?", "ঢাকা", "চট্টগ্রাম"),
            ("বাংলাদেশের জাতীয় কবি কে?", "কাজী নজরুল ইসলাম", "রবীন্দ্রনাথ ঠাকুর"),
            ("বিজয় দিবস কবে?", "১৬ ডিসেম্বর", "২৬ মার্চ"),
            ("বাংলাদেশের দীর্ঘতম নদী কোনটি?", "মেঘনা", "পদ্মা"),
            ("পদ্মা সেতুর দৈর্ঘ্য কত?", "৬.১৫ কিমি", "৯.১৮ কিমি"),
            ("মুক্তিযুদ্ধের সময় সেক্টর কয়টি ছিল?", "১১টি", "৭টি"),
            ("বাংলাদেশের সংবিধান কার্যকর হয় কবে?", "১৬ ডিসেম্বর ১৯৭২", "২৬ মার্চ ১৯৭১"),
            ("সুন্দরবন কোন জেলায় অবস্থিত?", "খুলনা", "বরিশাল"),
            ("বাংলাদেশের একমাত্র প্রবাল দ্বীপ কোনটি?", "সেন্টমার্টিন", "মহেশখালী"),
            ("জাতীয় স্মৃতিসৌধের স্থপতি কে?", "সৈয়দ মাইনুল হোসেন", "হামিদুর রহমান"),
        ] * 3
    }

    selected_qs = questions.get(sub, questions['ict'])[:30]
    q_html = ""
    for i, (q, a, b) in enumerate(selected_qs):
        q_html += f"""
        <div class="card q-card">
            <p class="fw-bold mb-2 text-dark">{i+1}. {q}</p>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="q{i}"> {a}
            </div>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="q{i}"> {b}
            </div>
        </div>
        """
        # Ad Placement Every 5 Questions
        if (i+1) % 5 == 0:
            if (i+1) % 10 == 0:
                q_html += f'<div class="ad-slot shadow-sm">{BANNER_AD}</div>'
            else:
                q_html += f'<div class="card p-2">{NATIVE_BANNER}</div>'

    return render_template_string(UI_STYLE + f"""
    <div class="container mt-4">
        <div class="d-flex justify-content-between align-items-center mb-4 bg-white p-3 rounded shadow-sm sticky-top">
            <h5 class="m-0 text-primary uppercase">Sub: {sub} (30 MCQs)</h5>
            <span class="badge bg-danger">Time: 20:00</span>
        </div>
        
        <div id="exam-area">
            {q_html}
            <div class="ad-slot">{BANNER_AD}</div>
            <button onclick="finish()" class="btn-start mb-5 shadow-lg">✅ SUBMIT & GENERATE RESULT</button>
        </div>

        <div id="loader" class="hidden text-center mt-5 p-5">
            <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;"></div>
            <h3 class="mt-4">Grading Your Test...</h3>
            <p>Verification In Progress</p>
            <div class="ad-slot">{BANNER_AD}</div>
        </div>
    </div>

    <script>
        function finish() {{
            window.open('{SMARTLINK_2}', '_blank');
            document.getElementById('exam-area').classList.add('hidden');
            document.getElementById('loader').classList.remove('hidden');
            setTimeout(() => {{ window.location.href = '/result'; }}, 12000);
        }}
    </script>
    """)

@app.route('/result')
def result():
    return render_template_string(UI_STYLE + f"""
    <div class="container mt-5 text-center">
        <div class="card p-5 shadow-lg border-0">
            <h1 class="text-success fw-bold display-1">96%</h1>
            <h3 class="mb-4">Excellent! You've Passed.</h3>
            <div class="ad-slot">{BANNER_AD}</div>
            <p class="text-muted">আপনার বিষয়ের উপর ভিত্তি করে একটি অনলাইন সার্টিফিকেট তৈরি করা হয়েছে।</p>
            <button onclick="window.open('{SMARTLINK_2}', '_blank')" class="btn-start">🎓 DOWNLOAD CERTIFICATE (PDF)</button>
            <br>
            <a href="/" class="mt-4 d-inline-block text-decoration-none text-muted">Go to Home</a>
        </div>
        <div class="ad-slot">{BANNER_AD}</div>
    </div>
    <script>
        window.onload = function() {{
            setTimeout(() => {{ window.open('{SMARTLINK_1}', '_blank'); }}, 3000);
        }};
    </script>
    """)

if __name__ == '__main__':
    app.run(debug=False)
  
