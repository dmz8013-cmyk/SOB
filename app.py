import os
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)

# Mail config
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sob-dev-key-change-in-prod')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME', '')
app.config['CONTACT_EMAIL'] = 'dmz8013@gmail.com'

mail = Mail(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.form
        company = data.get('company', '')
        name = data.get('name', '')
        phone = data.get('phone', '')
        email = data.get('email', '')
        inquiry_type = data.get('inquiry_type', '')
        content = data.get('content', '')

        # Send email notification
        try:
            msg = Message(
                subject=f'[SOB Production] 새 문의: {inquiry_type} - {company}',
                recipients=[app.config['CONTACT_EMAIL']],
                html=f"""
                <div style="font-family:'Apple SD Gothic Neo',sans-serif;max-width:600px;margin:0 auto;">
                    <div style="background:#1A1A2E;padding:24px;text-align:center;">
                        <h1 style="color:#C87941;margin:0;font-size:22px;">SOB Production 문의</h1>
                    </div>
                    <div style="padding:24px;background:#f9f9f9;">
                        <table style="width:100%;border-collapse:collapse;">
                            <tr><td style="padding:10px;font-weight:700;border-bottom:1px solid #ddd;width:120px;">문의 유형</td><td style="padding:10px;border-bottom:1px solid #ddd;">{inquiry_type}</td></tr>
                            <tr><td style="padding:10px;font-weight:700;border-bottom:1px solid #ddd;">회사명</td><td style="padding:10px;border-bottom:1px solid #ddd;">{company}</td></tr>
                            <tr><td style="padding:10px;font-weight:700;border-bottom:1px solid #ddd;">담당자명</td><td style="padding:10px;border-bottom:1px solid #ddd;">{name}</td></tr>
                            <tr><td style="padding:10px;font-weight:700;border-bottom:1px solid #ddd;">연락처</td><td style="padding:10px;border-bottom:1px solid #ddd;">{phone}</td></tr>
                            <tr><td style="padding:10px;font-weight:700;border-bottom:1px solid #ddd;">이메일</td><td style="padding:10px;border-bottom:1px solid #ddd;">{email}</td></tr>
                            <tr><td style="padding:10px;font-weight:700;vertical-align:top;">문의 내용</td><td style="padding:10px;">{content}</td></tr>
                        </table>
                    </div>
                    <div style="background:#1A1A2E;padding:16px;text-align:center;">
                        <p style="color:#888;margin:0;font-size:12px;">SOB Production 자동 알림</p>
                    </div>
                </div>
                """
            )
            mail.send(msg)
        except Exception as e:
            print(f"Email send error: {e}")

        return jsonify({'success': True, 'message': '문의가 접수되었습니다. 빠른 시일 내 연락드리겠습니다.'})
    except Exception as e:
        print(f"Submit error: {e}")
        return jsonify({'success': False, 'message': '오류가 발생했습니다. 이메일로 직접 문의해주세요.'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5002)
