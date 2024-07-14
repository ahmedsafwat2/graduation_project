from flaskblog import app, db, bcrypt

from flaskblog.models import User, Post

with app.app_context():
    hashed_password = bcrypt.generate_password_hash("123456").decode('utf-8')
    user1 = User(username='Omar Safwat', email='omarsafwat0161@gmail.com', password=hashed_password)
    user2 = User(username='Ahmed Saad', email='ahmedsaad01021639658@gmail.com', password=hashed_password)
    user3 = User(username='Basant Draz', email='basantdraz476@gmail.com', password=hashed_password)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()
    #user=User.query.filter_by(username='Ahmed Saad').first()
    #print(user)
    #db.session.delete(user)
    #db.session.commit()
    user=User.query.all()
    print(user)