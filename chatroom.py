import sys
from user import User
from post import Post

users = []
posts = []

current_user = None


def display_posts():
    for post in posts:
        post.display_post()


def create_user():
    username = input("What do you want your username to be? Be creative; you won't be able to change this later! ")
    password = input("What do you want your password to be? ")
    name = input("What's your full name? (This is optional) ")
    email = input("What's your email you would like to share? (Also optional) ")

    user_info = {
        'username': username,
        'password': password
    }
    if name:
        user_info['name'] = name
    if email:
        user_info['email'] = email

    print("Creating account...")
    try:
        user = User(**user_info)
    except AssertionError:
        print("ERROR: There was something wrong with your information you passed in. Make sure that:\n"
              "- Your username contains only letters, numbers, the underscore (_) and the hyphen (-)\n"
              "- Your username is more than 3 and less than 15 characters long\n"
              "- Your password is greater than 5 characters and less than 14 characters\n"
              "- Your email is a real valid email\n"
              "- You include both your first and last name (middle name is optional)")
    else:
        users.append(user)
        print("Creation complete! You may log in (using the command LOG IN) now.")


help_message = """get help => Gives this help message
help => Same action as "get help"
add post => Allows you to make a post up to 40 characters long
make post => Same action as "add post"
create post => Same action as "add post"
read posts => Displays all of the posts of all users
show posts => Same action as "read posts"
create user => Lets you creat an account
sign up => Same effect as "create user"
create account => Same effect as "create user"
log in => Logs you in. You must be logged out to do this
sign in => Same action as "log in"
log out => Logs you out so the computer doesn't know who you are. You must do this to sign into another account!
sign out => Same effect as "log out"
"""

while True:
    try:
        user_input = input('@%s > ' % current_user.username).lower()
    except AttributeError:
        user_input = input('> ').lower()
    if current_user == None:
        if user_input == 'create user' or user_input == 'sign up' or user_input == 'create account':
            create_user()
        elif user_input == 'log in' or user_input == 'sign in':
            username = input("What's your username? ")
            password = input("What's your password? ")

            found = False
            for user in users:
                if user.is_user(username, password):
                    found = True
                    print("Account found! Signing in...")
                    current_user = user
            if not found:
                print("Sorry, that account doesn't exist. Either your password is wrong or the user doesn't exist.")
        elif user_input == 'log out' or user_input == 'sign out':
            print("Dude, your already signed out!")
        elif user_input == 'exit' or user_input == 'quit':
            print("Saving information...")
            print("Completed saving! Bye!")
            sys.exit(0)
        else:
            print("Hmm... Either you entered an invalid command or I don't know who you are. "
                  "To create an account, you can type CREATE USER.")
    else:
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
        elif user_input == 'create user' or user_input == 'sign up' or user_input == 'create account':
            print("You must be signed out to do that!")
        elif user_input == 'sign in' or user_input == 'log in':
            print("You must be signed out to do that!")
        elif user_input == 'log out' or user_input == 'sign out':
            print("Logging out...")
            current_user = None
            print("Logging out complete!")
        elif user_input == '':
            print("Ahem. What did you want to say?")
        else:
            print("I didn't understand that command. If you want a list of commands, type HELP.")
    print()
