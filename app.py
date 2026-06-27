from flask import Flask , render_template , redirect
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from datetime import datetime,timezone


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100),nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<post {self.id} {self.title!r}>"

@app.route("/")
def home():
    return render_template("index.html")













if __name__ == "__main__":
    app.run(debug=True)