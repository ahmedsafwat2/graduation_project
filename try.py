from flaskblog import app, db
from flaskblog.models import User, Post

with app.app_context():
    user=User.query.filter_by(username='omar').first()
    #db.session.delete(user)
    #db.session.commit()
    print(user)