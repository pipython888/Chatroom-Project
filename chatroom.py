from user import User
from post import Post

alex = User(username="xela888",
            password="GPIOpython_",
            email="alexdavison888@gmail.com",
            name="Alexander J. Davison",
            bio="""A Python developer that is very interested in Game development!
Enjoys Python, Ruby, JS, Python's PyGame and Unity.
Also likes playing/watching tennis, playing board games and playing the
trumpet! :D""")

post = Post(user=alex, content="Hello world! My first post.")
post.display_post()