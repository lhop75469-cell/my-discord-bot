from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# قائمة لتخزين العمليات الشغالة
processes = {}

@app.route('/')
def home():
    return "سيرفر استضافة البوتات يعمل بنجاح 24/7!"

@app.route('/deploy', methods=['POST'])
def deploy():
    data = request.json
    token = data.get('token')
    bot_id = data.get('bot_id')

    if not token or not bot_id:
        return jsonify({"status": "error", "message": "بيانات ناقصة!"}), 400

    if bot_id in processes:
        return jsonify({"status": "error", "message": "هذا البوت شغال فعلاً!"}), 400

    # تشغيل ملف bot_template.py وتمرير التوكن له
    p = subprocess.Popen(['python', 'bot_template.py', token])
    processes[bot_id] = p

    return jsonify({"status": "success", "message": f"تم تشغيل البوت {bot_id} بنجاح!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
