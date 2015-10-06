from flask import Flask, render_template_string
from flask.ext.upcdn import UPCDN

app = Flask(__name__)

app.config['CDN_DOMAIN'] = 'mycdnname.cloudfront.net'
app.config['CDN_DEBUG'] = True
app.config['CDN_HTTPS'] = True

UPCDN(app)


@app.route('/')
def index():
    template_str = """{{ url_for('static', filename="logo.png") }}"""
    return render_template_string(template_str)

if __name__ == '__main__':
    app.run(debug=True)
