import sys
from user import User
from post import Post

current_user = User(username="xela888", password="GPIOpython_")
posts = []


def display_posts():
    for post in posts:
        post.display_post()


help_message = """get help => Gives this help message
help => Same action as "get help"
add post => Allows you to make a post up to 40 characters long
make post => Same action as "add post"
create post => Same action as "add post"
read posts => Displays all of the posts of all users
show posts => Same action as "read posts"
"""


while True:
    user_input = input('%s > ' % current_user.username).lower()
    if user_input == 'get help' or user_input == 'help':
        print(help_message)
    elif user_input == 'add post' or user_input == 'make post' or user_input == 'create post':
        content = input("What are you thinking of? Use 1-40 characters: ")
        try:
            posts.append(Post(current_user, content))
        except AssertionError:
            print("Hmm... Your post doesn't seem valid. Make sure it isn't longest than 40 characters!")
    elif user_input == 'read posts' or user_input == 'show posts':
        display_posts()
    elif user_input == '':
        print("Ahem. What did you want to say?")
    else:
        print("I didn't understand that command. If you want a list of commands, type HELP.")
    print()
