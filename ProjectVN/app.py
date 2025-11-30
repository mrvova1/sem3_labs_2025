from flask import Flask, render_template, request, send_file, make_response
import io, json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/export', methods=['POST'])
def export_project():
    data = request.get_json()
    # Minimal validation
    if not data:
        return {"error":"No JSON"}, 400
    # Attach exportedAt
    data['exportedAt'] = datetime.utcnow().isoformat() + 'Z'
    text = json.dumps(data, ensure_ascii=False, indent=2)
    buf = io.BytesIO()
    buf.write(text.encode('utf-8'))
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name=(data.get('name','vnred_project') + '_vnred_export.txt'), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)