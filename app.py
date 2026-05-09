import os
import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- AD SCRIPTS ---
POP_SCRIPTS = """
<script src="https://potterynaggingformerly.com/49/6c/fa/496cfaa97c1bdc526da1c36625ffe71a.js"></script>
<script src="https://potterynaggingformerly.com/76/41/5a/76415aaef6ad249973a92bb8f1251a22.js"></script>
"""
BANNER_AD = '<div class="ad-slot"><script type="text/javascript">atOptions = {"key" : "3ba591d1fc0f098ac02b41fdd3ceb0c5","format" : "iframe","height" : 250,"width" : 300,"params" : {}};</script><script type="text/javascript" src="https://potterynaggingformerly.com/3ba591d1fc0f098ac02b41fdd3ceb0c5/invoke.js"></script></div>'
NATIVE_AD = '<div class="ad-slot"><script async="async" data-cfasync="false" src="https://potterynaggingformerly.com/1c69caf291a12c5899a966465f2b4e0b/invoke.js"></script><div id="container-1c69caf291a12c5899a966465f2b4e0b"></div></div>'

SMARTLINK_1 = "https://potterynaggingformerly.com/surggewa?key=91990ae75a2cedbea643e7b2b13aadf6"
SMARTLINK_2 = "https://potterynaggingformerly.com/n62zm634?key=3ddc98ba3a3e85cdb3143b568828daf2"

# --- FULL QUESTION DATABASE (30 Questions per subject) ---
DB = {
    'ict': [
        ("HTML-এর পূর্ণরূপ কী?", "Hyper Text Markup Language", "High Tech Markup Language"),
        ("ইন্টারনেটের জনক কে?", "ভিন্ট কার্ফ", "মার্ক জুকারবার্গ"),
        ("IP Address (IPv4) কত বিটের?", "৩২ বিট", "১২৮ বিট"),
        ("১ গিগাবাইট সমান কত মেগাবাইট?", "১০২৪ MB", "১০০০ MB"),
        ("মডেম কোন ধরনের ডিভাইস?", "ইনপুট ও আউটপুট", "শুধুমাত্র ইনপুট"),
        ("ই-মেইলের জনক কে?", "রে টমলিনসন", "বিল গেটস"),
        ("Wi-Fi এর পূর্ণরূপ কী?", "Wireless Fidelity", "Wireless Fiber"),
        ("ব্যান্ডউইথ কিসের একক?", "ডেটা প্রবাহের হার", "ডেটা মেমোরি"),
        ("URL কিসের সংক্ষিপ্ত রূপ?", "Uniform Resource Locator", "Universal Radio Link"),
        ("সি ল্যাঙ্গুয়েজের জনক কে?", "ডেনিস রিচি", "জেমস গসলিং"),
        ("ফেসবুক কত সালে প্রতিষ্ঠিত হয়?", "২০০৪", "২০০৮"),
        ("১ বাইট সমান কত বিট?", "৮ বিট", "১৬ বিট"),
        ("Google কী ধরনের ওয়েবসাইট?", "সার্চ ইঞ্জিন", "সোশ্যাল মিডিয়া"),
        ("Bluetooth কোন নেটওয়ার্কের উদাহরণ?", "PAN", "LAN"),
        ("সবচেয়ে বড় হেডার ট্যাগ কোনটি?", "<h1>", "<h6>"),
        ("RAM এর কাজ কী?", "অস্থায়ী মেমোরি", "স্থায়ী মেমোরি"),
        ("CPU এর পূর্ণরূপ কী?", "Central Processing Unit", "Control Power Unit"),
        ("কম্পিউটারের মস্তিষ্ক কাকে বলা হয়?", "CPU", "Hard Disk"),
        ("PDF এর পূর্ণরূপ কী?", "Portable Document Format", "Public Data File"),
        ("Binary পদ্ধতিতে কয়টি অংক থাকে?", "২টি", "১০টি"),
        ("বাংলাদেশের ডোমেইন কোনটি?", ".bd", ".com"),
        ("Wi-Max কোন নেটওয়ার্কের অন্তর্ভুক্ত?", "MAN", "PAN"),
        ("ASCII-8 কত বিটের কোড?", "৮ বিট", "৭ বিট"),
        ("সফটওয়্যার কয় প্রকার?", "২ প্রকার", "৪ প্রকার"),
        ("Keyboard কী ধরনের ডিভাইস?", "ইনপুট", "আউটপুট"),
        ("১ মেগাবাইট সমান কত কিলোবাইট?", "১০২৪ KB", "৫১২ KB"),
        ("CSS এর পূর্ণরূপ কী?", "Cascading Style Sheets", "Classic Style Scripts"),
        ("Browser কোনটি?", "Chrome", "Excel"),
        ("Windows কী ধরনের সফটওয়্যার?", "অপারেটিং সিস্টেম", "এপ্লিকেশন"),
        ("আইসিটি-র পূর্ণরূপ কী?", "Information and Communication Technology", "Internal Communication Tech")
    ],
    'eng': [
        ("Noun of 'Strong' is?", "Strength", "Strongly"),
        ("Antonym of 'Beautiful'?", "Ugly", "Pretty"),
        ("He ___ to school daily.", "goes", "go"),
        ("Identity the Verb:", "Eat", "Apple"),
        ("Plural of 'Mouse'?", "Mice", "Mouses"),
        ("Which is a Proper Noun?", "Dhaka", "City"),
        ("Opposite of 'Hot'?", "Cold", "Warm"),
        ("An umbrella is ___ useful thing.", "a", "an"),
        ("Synonym of 'Fast'?", "Quick", "Slow"),
        ("He is ___ honest man.", "an", "a"),
        ("Correct Spelling?", "Receive", "Recieve"),
        ("Plural of 'Man'?", "Men", "Mans"),
        ("Identify Adjective:", "Big", "Run"),
        ("He is ___ M.A.", "an", "a"),
        ("Past form of 'Write'?", "Wrote", "Written"),
        ("Opposite of 'Boy'?", "Girl", "Man"),
        ("I ___ a student.", "am", "is"),
        ("The sun ___ in the East.", "rises", "rise"),
        ("Collective Noun example?", "Army", "Soldier"),
        ("Gender of 'Actor'?", "Masculine", "Feminine"),
        ("A person who writes books?", "Author", "Doctor"),
        ("Abstract Noun example?", "Love", "Book"),
        ("Who is the writer of 'Hamlet'?", "Shakespeare", "Milton"),
        ("Short form of 'Cannot'?", "Can't", "Cont"),
        ("Which one is a Pronoun?", "He", "Rahim"),
        ("Synonym of 'Happy'?", "Glad", "Sad"),
        ("Antonym of 'Rich'?", "Poor", "Good"),
        ("I have ___ inkpot.", "an", "a"),
        ("Past form of 'Go'?", "Went", "Gone"),
        ("Present Continuous form of 'Play'?", "Playing", "Player")
    ],
    'gk': [
        ("বাংলাদেশের রাজধানী কোনটি?", "ঢাকা", "চট্টগ্রাম"),
        ("বিজয় দিবস কবে?", "১৬ ডিসেম্বর", "২৬ মার্চ"),
        ("পদ্মা সেতুর দৈর্ঘ্য কত?", "৬.১৫ কিমি", "৯.১৮ কিমি"),
        ("জাতীয় কবি কে?", "নজরুল ইসলাম", "রবীন্দ্রনাথ"),
        ("মুক্তিযুদ্ধে সেক্টর কয়টি ছিল?", "১১টি", "৭টি"),
        ("বাংলাদেশের প্রথম রাষ্ট্রপতি কে?", "শেখ মুজিবুর রহমান", "সৈয়দ নজরুল ইসলাম"),
        ("সাত বীরশ্রেষ্ঠের মধ্যে প্রথম কে?", "মুন্সী আব্দুর রউফ", "মহিউদ্দিন জাহাঙ্গীর"),
        ("বাংলাদেশের জাতীয় ফল কোনটি?", "কাঁঠাল", "আম"),
        ("মুজিবনগর সরকার গঠিত হয় কবে?", "১০ এপ্রিল ১৯৭১", "১৬ ডিসেম্বর ১৯৭১"),
        ("জাতীয় স্মৃতিসৌধ কোথায় অবস্থিত?", "সাভার", "গাজীপুর"),
        ("বাংলাদেশের একমাত্র প্রবাল দ্বীপ?", "সেন্টমার্টিন", "সন্দ্বীপ"),
        ("বঙ্গবন্ধু কত সালে জন্মগ্রহণ করেন?", "১৯২০", "১৯২৫"),
        ("ঢাকা বিশ্ববিদ্যালয় কত সালে স্থাপিত হয়?", "১৯২১", "১৯০৫"),
        ("পদ্মা সেতু কোন দুটি জেলাকে যুক্ত করেছে?", "মুন্সিগঞ্জ ও শরীয়তপুর", "ঢাকা ও চাঁদপুর"),
        ("বাংলাদেশের জাতীয় খেলা কোনটি?", "হা-ডু-ডু", "ক্রিকেট"),
        ("সবচেয়ে বড় জেলা কোনটি?", "রাঙামাটি", "খুলনা"),
        ("বাংলাদেশের সংবিধান কার্যকর হয় কবে?", "১৬ ডিসেম্বর ১৯৭২", "১০ জানুয়ারি ১৯৭১"),
        ("জাতীয় সংসদ ভবনের স্থপতি কে?", "লুই আই কান", "হামিদুর রহমান"),
        ("বাংলাদেশের দীর্ঘতম নদী কোনটি?", "মেঘনা", "পদ্মা"),
        ("সুন্দরবন কোন কোন জেলায় অবস্থিত?", "খুলনা ও বাগেরহাট", "বরিশাল ও ভোলা"),
        ("শহীদ বুদ্ধিজীবী দিবস কবে?", "১৪ ডিসেম্বর", "১৫ আগস্ট"),
        ("বাংলাদেশের বৃহত্তম স্থলবন্দর কোনটি?", "বেনাপোল", "হিলি"),
        ("বাংলাদেশের টাকার নোট প্রথম কবে বের হয়?", "৪ মার্চ ১৯৭২", "১ জানুয়ারি ১৯৭৩"),
        ("বাংলাদেশের সমুদ্র সৈকতের দৈর্ঘ্য কত?", "১২০ কিমি", "৮০ কিমি"),
        ("মহাস্থানগড় কোথায় অবস্থিত?", "বগুড়া", "রাজশাহী"),
        ("বাংলাদেশের জাতীয় পতাকার ডিজাইনার কে?", "কামরুল হাসান", "শিবনারায়ণ দাশ"),
        ("বাংলা নববর্ষ পালিত হয় কবে?", "১৪ এপ্রিল", "১ জানুয়ারি"),
        ("জাতীয় সংগীতের রচয়িতা কে?", "রবীন্দ্রনাথ ঠাকুর", "কাজী নজরুল ইসলাম"),
        ("বাংলাদেশের প্রশস্ততম নদী কোনটি?", "যমুনা", "পদ্মা"),
        ("বাংলাদেশের প্রথম প্রধানমন্ত্রী কে?", "তাজউদ্দীন আহমদ", "শেখ মুজিব")
    ]
}

STYLE = f"""
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
{POP_SCRIPTS}
<style>
    body {{ background: #f0f4f8; font-family: 'Segoe UI', sans-serif; }}
    .glass {{ background: white; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); padding: 30px; }}
    .hero {{ background: linear-gradient(135deg, #4834d4, #686de0); color: white; padding: 40px 10px; border-radius: 0 0 40px 40px; text-align: center; }}
    .btn-custom {{ padding: 15px; border-radius: 12px; font-weight: bold; width: 100%; border: none; transition: 0.3s; }}
    .btn-earn {{ background: #eb4d4b; color: white; }}
    .btn-start {{ background: #6ab04c; color: white; }}
    .ad-slot {{ background: #fff; padding: 10px; border-radius: 15px; margin: 20px 0; border: 1px dashed #ccc; text-align: center; }}
    .q-card {{ background: white; border-radius: 15px; padding: 20px; margin-bottom: 20px; border-left: 6px solid #4834d4; }}
</style>
"""

@app.route('/')
def index():
    return render_template_string(STYLE + f"""
    <div class="hero">
        <h2 class="fw-bold">Multi-Subject Exam Portal 2026</h2>
        <p>Gain knowledge and earn rewards</p>
        <div class="badge bg-light text-dark p-2 rounded-pill">Credits: <span id="cr_val">0</span></div>
    </div>
    <div class="container" style="max-width: 550px; margin-top: -30px;">
        <div class="glass p-4">
            <button onclick="getCr()" class="btn-custom btn-earn shadow mb-4"><i class="fas fa-gem"></i> EARN 5 CREDITS (ADS)</button>
            <label class="fw-bold small text-muted mb-1">CHOOSE SUBJECT:</label>
            <select id="sub_sel" class="form-select form-select-lg mb-4">
                <option value="ict">ICT Mastery</option>
                <option value="eng">English Specialist</option>
                <option value="gk">General Knowledge</option>
            </select>
            <button id="st_btn" onclick="go()" class="btn-custom btn-start shadow" disabled>LOCKED 🔒</button>
        </div>
        {BANNER_AD}
    </div>
    <script>
        let credits = localStorage.getItem('user_cr') || 0;
        document.getElementById('cr_val').innerText = credits;
        if(credits >= 5) {{
            document.getElementById('st_btn').disabled = false;
            document.getElementById('st_btn').innerText = "🚀 START 30 QUESTIONS";
        }}
        function getCr() {{
            window.open('{SMARTLINK_1}', '_blank');
            setTimeout(() => {{
                localStorage.setItem('user_cr', parseInt(credits) + 5);
                location.reload();
            }}, 2000);
        }}
        function go() {{
            localStorage.setItem('user_cr', credits - 5);
            window.location.href = '/exam?sub=' + document.getElementById('sub_sel').value;
        }}
    </script>
    """)

@app.route('/exam')
def exam():
    sub = request.args.get('sub', 'ict')
    all_qs = DB.get(sub, DB['ict'])
    
    q_html = ""
    for i, (q, correct, wrong) in enumerate(all_qs):
        options = [correct, wrong]
        random.shuffle(options)
        q_html += f"""
        <div class="q-card shadow-sm">
            <p class="fw-bold mb-3">{i+1}. {q}</p>
            <div class="form-check mb-2">
                <input class="form-check-input q-input" type="radio" name="q{i}" value="{options[0]}" data-ans="{correct}"> {options[0]}
            </div>
            <div class="form-check">
                <input class="form-check-input q-input" type="radio" name="q{i}" value="{options[1]}" data-ans="{correct}"> {options[1]}
            </div>
        </div>
        """
        if (i+1) % 5 == 0:
            q_html += BANNER_AD if (i+1)%10==0 else NATIVE_AD

    return render_template_string(STYLE + f"""
    <div class="container mt-4" style="max-width: 700px;">
        <div class="sticky-top bg-white p-3 rounded shadow mb-4 d-flex justify-content-between">
            <h5 class="m-0 text-primary uppercase"><b>{sub}</b> Exam</h5>
            <span class="text-danger fw-bold"><i class="fas fa-clock"></i> 20:00</span>
        </div>
        {q_html}
        <button onclick="calc()" class="btn-custom btn-start mb-5 shadow-lg">✅ SUBMIT FINAL EXAM</button>
    </div>
    <div id="load" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:white; z-index:999; text-align:center; padding-top:150px;">
        <div class="spinner-grow text-primary"></div>
        <h3 class="mt-4">Grading Your Exam...</h3>
        {BANNER_AD}
    </div>
    <script>
        function calc() {{
            let c = 0, w = 0;
            document.querySelectorAll('.q-input:checked').forEach(inp => {{
                if(inp.value === inp.getAttribute('data-ans')) c++;
                else w++;
            }});
            localStorage.setItem('res_c', c);
            localStorage.setItem('res_w', 30 - c);
            window.open('{SMARTLINK_2}', '_blank');
            document.getElementById('load').style.display = 'block';
            setTimeout(() => {{ window.location.href = '/result'; }}, 8000);
        }}
    </script>
    """)

@app.route('/result')
def result():
    return render_template_string(STYLE + f"""
    <div class="container mt-5 text-center" style="max-width: 500px;">
        <div class="glass p-5">
            <h2 class="fw-bold mb-4">Exam Result</h2>
            <div class="row mb-4">
                <div class="col-6"><div class="p-3 bg-success bg-opacity-10 text-success rounded"><b>Correct:</b> <h3 id="rc">0</h3></div></div>
                <div class="col-6"><div class="p-3 bg-danger bg-opacity-10 text-danger rounded"><b>Wrong:</b> <h3 id="rw">0</h3></div></div>
            </div>
            <h1 class="display-3 fw-bold text-primary mb-4" id="per">0%</h1>
            {BANNER_AD}
            <button onclick="window.open('{SMARTLINK_2}', '_blank')" class="btn-custom btn-earn mb-3 shadow">🎓 DOWNLOAD CERTIFICATE</button>
            <a href="/" class="text-muted text-decoration-none">Back to Dashboard</a>
        </div>
    </div>
    <script>
        let correct = localStorage.getItem('res_c') || 0;
        let wrong = localStorage.getItem('res_w') || 0;
        let p = Math.round((correct / 30) * 100);
        document.getElementById('rc').innerText = correct;
        document.getElementById('rw').innerText = wrong;
        document.getElementById('per').innerText = p + "%";
        window.onload = function() {{
            setTimeout(() => {{ window.open('{SMARTLINK_1}', '_blank'); }}, 3000);
        }};
    </script>
    """)

if __name__ == '__main__':
    app.run(debug=False)
