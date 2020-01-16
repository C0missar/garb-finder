from main import db,User,Item,Climate

db.drop_all()
db.create_all()
db.session.commit()

new=User('stan','pass1')
db.session.add(new)

new=User('Fred','Flintstone')
db.session.add(new)

db.session.commit()
