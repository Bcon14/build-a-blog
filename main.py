from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:mypassword@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog', methods=['POST', 'GET'])
def index():
    blogs = Blog.query.all()
    blog_id = request.args.get('id')
    if not blog_id:
        return render_template('blog.html',blogs = blogs)
    else:
        blog = Blog.query.get(blog_id)
        blog_title = blog.title
        blog_body = blog.body
        return render_template('/blog_post.html', title=blog_title, body=blog_body)


@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    return render_template('add_blog_form.html')


@app.route('/blog_post', methods=['POST'])
def blog_post():
   
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        if blog_title == '' or blog_body == '':
            return redirect('/newpost')
        else:
            new_blog = Blog(blog_title , blog_body)
            db.session.add(new_blog)
            db.session.commit()
            return render_template('/blog_post.html', title=blog_title, body=blog_body)
        
    


if __name__ == '__main__':
    app.run()