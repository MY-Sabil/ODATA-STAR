import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename


import main_v2

app = Flask(__name__)

g_file = ""
is_tstd = False
# history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/basic')
def basic():
    global is_tstd
    is_tstd = False

    return render_template('basic.html')

@app.route('/tstd')
def tstd():
    global is_tstd
    is_tstd = True

    return render_template('tstd.html')

# upload a file to the 'data' folder
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('basic'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('basic'))
    
    if file:
        file_name = secure_filename(file.filename)
        file_uri = os.path.join('data', file_name)
        file.save(file_uri)

        global g_file
        g_file = file_uri

        try:
            with open(file_uri, 'r', encoding='utf-8') as f:
                content = f.read()

            return render_template('basic.html', content=content, file_uri=g_file)
        
        except UnicodeDecodeError:
            content = 'Error: Unable to decode file content'
            return render_template('basic.html', content=content, file_uri=g_file)


# return an answer based on the uploaded document
@app.route('/answer', methods=['POST'])
def answer():
    prompt = request.form.get('prompt')
    temp = 0.7

    if prompt and g_file != '':
        answer = main_v2.Basic(prompt, temp)

        return render_template('basic.html', prompt=prompt, answer=answer, file_uri=g_file)
    
    return render_template('basic.html')


# return the file preview
@app.route('/preview/<filename>')
def preview_file(filename):
    try:
        return send_file(filename, as_attachment=False)
    
    except FileNotFoundError:
        print("File Not Found")
        return redirect(url_for('/'))
    
# delete the file using filename
@app.route('/delete/<filename>', methods=['POST'])
def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

        if(not is_tstd):
            return redirect(url_for('basic'))
        return redirect(url_for('tstd'))

    if(not is_tstd):
        return redirect(url_for('basic'))
    return redirect(url_for('tstd'))

# delete all files in the 'data' folder
@app.route('/deleteall', methods=['POST'])
def remove_all_files():
        folder_path = 'data/'
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print("Error deleting file: " + e)

        global history
        history = []

        return redirect(url_for('tstd'))


# upload multiple files
@app.route('/uploadfiles', methods=['POST'])
def uploadfiles():
        if 'file' not in request.files:
            return redirect(url_for('tstd'))
        
        file = request.files['file']
        if file.filename == '':
            return redirect(url_for('tstd'))
        
        if file:
            file_name = secure_filename(file.filename)
            file_uri = os.path.join('data', file_name)
            file.save(file_uri)
            
            file_list = os.listdir('data')
        
        global g_file
        g_file = file_uri

        try:
            with open(file_uri, 'r', encoding='utf-8') as f:
                content = f.read()
                return render_template('tstd.html', content=content, file_uri=g_file)

        except UnicodeDecodeError:
            content = 'Error: Unable to decode file content'
            return render_template('tstd.html', content=content, file_uri=g_file)

# analyze technical standard files
@app.route('/analyze', methods=['POST'])
def analyze():

    section_no = request.form.get('section')

    # global history
    temp = 0.7
    result = main_v2.TechSTD(section_no, temp)

    file_list = os.listdir('data')

    return render_template('tstd.html', result=result, file_list=file_list, file_uri=g_file)


if __name__ == '__main__':
    app.run(debug=True)
