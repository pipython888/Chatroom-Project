import sys
from user import User
from post import Post

current_user = User(username="xela888", password="GPIOpython_")
posts = []


def display_posts():
    for post in posts:
        post.display_post()


while True:
    user_input = input('%s> ' % current_user.username)
    if user_input == 'add post':
        content = input("What are you thinking of? Use 1-40 characters: ")
        posts.append(Post(current_user, content))
    elif user_input == 'read posts':
        display_posts()
