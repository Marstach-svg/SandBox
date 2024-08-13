from sandbox_system import db
from sandbox_system.models import User

db.drop_all()
db.create_all()

user1 = User(username='Marstach.', email='ryoken.102388@gmail.com', password='Maruko880325', administrator='1')

db.session.add(user1)
db.session.commit()