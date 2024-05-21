from flask import Flask, render_template, request, redirect, send_file, url_for
from helper import client, accounts

app = Flask(__name__)

serverDir = {}
username = ''

showingFilesFrom = "public"

@app.route('/')
def index():
    return redirect('/login')
    # return render_template("index.html")


@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        global username
        username = request.form['username']
        password = request.form['password']
        if {"username": username, "password": password} in accounts.accounts:
            return redirect('/home')
        return render_template("login.html", invalidCredentials=True)


    return render_template("login.html", invalidCredentials=False)

@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if {"username": username, "password": password} in accounts.accounts:
            return render_template("register.html", usernameTaken=True)
        accounts.accounts.append({"username": username, "password": password})
        return redirect('/login')

    return render_template("register.html")

@app.route('/home', methods=['POST', 'GET'])
def home():

    global serverDir
    global username

    if request.method == 'POST':

        if 'search' in request.form:
            filename = request.form['search_file_name']
            return redirect(url_for('.explore', filename=filename))
            # client.getDir(username, filename)
            # client.saveToFile('public', filename)

        elif 'explore' in request.form:
            serverDir = {}
            # serverDir = client.getDir(username)
            return redirect('/explore')
        
        elif 'upload' in request.form:
            return redirect('/upload')
        
        elif 'login' in request.form:
            username = ''
            return redirect('/login')

        return render_template("home.html", username=username)
    else:
        return render_template("home.html", username=username)
    
@app.route('/explore', methods=['POST', 'GET'])
def explore():

    global serverDir
    global showingFilesFrom
    global username

    # print(request.args)
    if 'filename' in request.args: serverDir = {}

    if request.method == 'POST':

        if 'explore' in request.form:
            serverDir = {}
            # serverDir = client.getDir(username)
            return redirect('/explore')
        
        elif 'upload' in request.form:
            return redirect('/upload')
        
        elif 'login' in request.form:
            username = ''
            return redirect('/login')

    filetableheaders = [
        {"header": "Name", "value": "name"},
        {"header": "Size", "value": "size"},
        {"header": "Last Modified", "value": "last_modified"},
        {"header": "Type", "value": "type"},
    ]

    if 'public' not in serverDir: serverDir = client.getDir(username, request.args['filename'] if 'filename' in request.args else None)

    if 'downloadfile' in request.args:
        file_index = int(request.args['downloadfile']) - 1
        return send_file(serverDir[showingFilesFrom][file_index]['downloadpath'], as_attachment=True)

    files = serverDir['public']
    showingFilesFrom = 'public'

    if username in request.args: 
        showingFilesFrom = username
        files = serverDir[username]
        if files == None: files = []
    # print(files)
    return render_template('explore.html', tableheaders=filetableheaders, folders=serverDir.keys(), files=files, username=username)

@app.route('/upload', methods=['POST', 'GET'])
def upload():

    global serverDir
    global username

    if request.method == 'POST':
        if 'explore' in request.form:
            serverDir = {}
            # serverDir = client.getDir(username)
            return redirect('/explore')
        
        elif 'upload' in request.form:
            return redirect('/upload')
        
        elif 'login' in request.form:
            username = ''
            return redirect('/login')
        else:
            for file in request.files:
                file = request.files[file]
                if 'upload_public' in request.form: client.uploadFile('', file)
                elif 'upload_user' in request.form: client.uploadFile(username, file)
        return render_template('upload.html', username=username, uploadSuccess=True)

    return render_template('upload.html', username=username)

if __name__ == "__main__":
    app.run(debug=True)