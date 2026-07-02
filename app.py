from flask import Flask , render_template , redirect , request , url_for,flash
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from datetime import datetime,timezone


app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app,db)
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200),nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<post {self.id} {self.title!r}>"
    
class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    author = db.Column(db.String(100),nullable=False)
    body = db.Column(db.Text,nullable=False)
    created_at=db.Column(db.DateTime,nullable=False,default=datetime.now(timezone.utc))
    
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'),nullable=False)
    post = db.relationship('Post',backref=db.backref('comments',cascade='all,delete-orphan',lazy='dynamic'))
    
    def __repr__(self):
        return f"Comment {self.id} on Post {self.post_id!r}"

@app.route("/")
def home():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("index.html",posts=posts)


@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    comments = post.comments.order_by(Comment.created_at.desc()).all()
    return render_template("post_detail.html",post=post,comments=comments)

@app.route("/post/<int:post_id>/comment", methods=["POST"])
def create_comment(post_id):
    post = Post.query.get_or_404(post_id)

    author = request.form.get("author","").strip()
    body = request.form.get("body","").strip()

    if not author or not body:
        flash("Name and comment are required")
        return redirect(url_for("post_detail",post_id=post.id))
    
    comment = Comment(author=author, body = body , post=post)
    db.session.add(comment)
    db.session.commit()
    flash("Comment added")

    return redirect(url_for("post_detail",post_id=post.id))


    





@app.route("/post/new",methods=["GET","POST"])
def new_post():
    if request.method=="POST":
        title=request.form.get("title","").strip()
        body = request.form.get("body","").strip()

        if not title or not body:
            flash("title and body are required")
            return redirect(url_for("new_post"))
        
        post = Post(title=title,body=body)
        db.session.add(post)
        db.session.commit()
        flash("created post")
        return redirect(url_for('home'))
    

    return render_template("new_post.html")













if __name__ == "__main__":
    app.run(debug=True)