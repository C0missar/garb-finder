from main import db,User,Item,Climate

db.drop_all()
db.create_all()
db.session.commit()

# Add users
new=User('Stan','Ward')
db.session.add(new)

new=User('Fred','Flintstone')
db.session.add(new)

db.session.commit()

# Add Climates
new=Climate('subarctic')
db.session.add(new)

new=Climate('arctic')
db.session.add(new)

db.session.commit()

# Add Items
new=Item('shirt',1)
#,'viking','subartic','male','clothing',1500,1599,'Its a shirt')
db.session.add(new)

new = Item('pants',1)
#,'viking','subartic','male','clothing',1500,1599,"Pants!")
db.session.add(new)

db.session.commit()
