from flask import Flask, render_template, request, send_file, jsonify
import subprocess
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def invert_pdf(input_pdf, output_pdf, text_color=(0.8, 0.8, 0.8), bg_color=(0.2, 0.2, 0.2)):
    bg_r, bg_g, bg_b = bg_color
    text_r, text_g, text_b = text_color
    scale_r = bg_r - text_r
    offset_r = text_r
    scale_g = bg_g - text_g
    offset_g = text_g
    scale_b = bg_b - text_b
    offset_b = text_b
    transfer_func = f"""
    {{ {scale_r} mul {offset_r} add }} settransfer
    {{ {scale_g} mul {offset_g} add }} settransfer
    {{ {scale_b} mul {offset_b} add }} settransfer
    """
    gs_command = [
        "gswin64c.exe",  # 替换为 Ghostscript 的完整路径如果需要
        "-sOutputFile=" + output_pdf,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dNOPAUSE",
        "-dBATCH",
        "-dAutoRotatePages=/None",
        "-c", transfer_func,
        "-f", input_pdf
    ]
    subprocess.run(gs_command, check=True)

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16)/255.0 for i in range(0, lv, lv // 3))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        bg_color_hex = request.form.get('bg_color', '#333333')
        text_color_hex = request.form.get('text_color', '#CCCCCC')
        try:
            bg_color = hex_to_rgb(bg_color_hex)
            text_color = hex_to_rgb(text_color_hex)
        except ValueError:
            return jsonify({'error': '颜色值无效，请返回重新输入。'}), 400
        if 'pdf_file' not in request.files:
            return jsonify({'error': '未找到文件部分。'}), 400
        file = request.files['pdf_file']
        if file.filename == '':
            return jsonify({'error': '未选择文件。'}), 400
        if file and file.filename.lower().endswith('.pdf'):
            filename = secure_filename(file.filename)
            unique_filename = str(uuid.uuid4()) + "_" + filename
            input_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(input_pdf_path)
            output_filename = 'processed_' + unique_filename
            output_pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            try:
                invert_pdf(input_pdf_path, output_pdf_path, text_color=text_color, bg_color=bg_color)
            except Exception as e:
                return jsonify({'error': f'处理PDF时出错: {str(e)}'}), 500
            return send_file(output_pdf_path, as_attachment=True, download_name='processed.pdf', mimetype='application/pdf')
        else:
            return jsonify({'error': '请上传有效的PDF文件。'}), 400
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
