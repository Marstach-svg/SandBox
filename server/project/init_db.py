from sandbox_system import db
from sandbox_system.models import User, ChatChannel

#db.drop_all()
db.create_all()

user1 = User(username='Marstach.', email='ryoken.102388@gmail.com', introduce='よろしくお願いします', tech='Python, flask, その他基礎知識', job='大学生', image='', password='Maruko880325', administrator='1')

db.session.add(user1)
db.session.commit()

channel1 = ChatChannel(channelname='All')

db.session.add(channel1)
db.session.commit()