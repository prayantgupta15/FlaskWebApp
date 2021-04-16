from flask import Flask,render_template,request,redirect,flash,url_for,abort,session,jsonify
import os.path
import json
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = 'gm21emfmvovoee' 
@app.route('/')
def home():
    return render_template('home.html',codes= session.keys())


@app.route('/your-url', methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls={}
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
        if request.form['code'] in urls.keys():
            flash("Code already used. Try with new code.")
            return redirect('/')

        if 'url' in request.form.keys():
            urls[request.form['code']]={"url":request.form['url']}
        else:
            f=request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)    
            f.save('/root/Desktop/url-shortner/static/user_files/' + full_name)
            urls[request.form['code']]={"file":full_name}


        with open('urls.json','w') as url_file:
            json.dump(urls,url_file)
            session[request.form['code']]=True

        # GET: return render_template('your-url.html',code = request.args['code'])      
        return render_template('your-url.html',code = request.form['code'])
    
    
    else:
        return redirect('/')

@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                     return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static',filename='user_files/' + urls[code]['file']
                    ));
    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
     return render_template('page_not_found.html'),404  
     
@app.route('/api')
def json_api():
    return jsonify(list(session.keys()))