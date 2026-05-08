from flask import Flask, render_template_string, request, redirect, url_for, session
import smtplib, random

app = Flask(__name__)
app.secret_key = "pixel_ultra_final_v5"

# --- CONFIG (Apnar Info) ---
SENDER_EMAIL = "applegadget07@gmail.com"
SENDER_PASS = "qesd sqzt zpou cccc" 

products = [{'name': 'Pixel Pen', 'price': '150', 'image': 'https://img.icons8.com/pixel-line/100/pencil.png'}]

@app.route('/')
def home():
    user_status = f"HI, {session['user'].split('@')[0]}" if session.get('user') else '<a href="/login">LOGIN</a>'
    return render_template_string(f"""
    <body style="font-family:sans-serif; background:#fdfae6; padding:20px;">
        <div style="background:#000; color:#fff; padding:10px;">PIXEL SHOP | {user_status}</div>
        <h3>ITEMS</h3>
        <div>{products[0]['name']} - {products[0]['price']} BDT</div>
    </body>
    """)

@app.route('/login')
def login():
    return render_template_string("""
    <form action="/send_otp" method="post" style="padding:20px;">
        <input name="email" type="email" placeholder="Gmail" required>
        <button type="submit">SEND OTP</button>
    </form>
    """)

@app.route('/send_otp', methods=['POST'])
def send_otp():
    email = request.form['email']
    otp = str(random.randint(1111, 9999))
    session['temp_email'], session['temp_otp'] = email, otp
    try:
        # SMTP Setup
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        server.set_debuglevel(1)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASS)
        msg = f"Subject: PixelShop OTP\\n\\nYour code: {otp}"
        server.sendmail(SENDER_EMAIL, email, msg)
        server.quit()
        return render_template_string(f'OTP Sent to {email}! <form action="/verify" method="post"><input name="otp"><button>OK</button></form>')
    except Exception as e:
        # Mail na gele screen-e Error dekhabe
        return f"<h3>MAIL ERROR:</h3> <p>{str(e)}</p> <p>Testing OTP: {otp}</p> <a href='/login'>Try Again</a>"

@app.route('/verify', methods=['POST'])
def verify():
    if request.form['otp'] == session.get('temp_otp'):
        session['user'] = session['temp_email']
        return redirect('/')
    return "Wrong OTP!"

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
