import string
import json
import sys
import os
import re

from vigenere import encode, decode
from user import User
from post import Post

KEY = 'NODf8dtlghmgf;hdfg0h[8fd79ertif&%$d90+ddf!~'


def display_posts():
    for post in posts:
        post.display_post()


def username_exists(username, users):
    for user in users:
        if user.get_username() == username:
            return True
    return False


def save_data(users, posts):
    info_dict = {
        'users': [user.convert_to_dict() for user in users],
        'posts': [post.convert_to_dict() for post in posts]
    }
    for x in info_dict['users']:
        x['password'] = encode(x['password'], KEY)
        x['username'] = encode(x['username'], KEY)
        x['bio'] = encode(x['bio'], KEY)
    json.dump(json.dumps(info_dict), open("data.json", 'w'))


def convert_to_user(dict_):
    dict_['password'] = decode(dict_['password'], KEY)
    dict_['username'] = decode(dict_['username'], KEY)
    dict_['bio'] = decode(dict_['bio'], KEY)
    return User(**dict_)


def convert_to_post(dict_):
    dict_['user'] = convert_to_user(dict_['user'])
    return Post(**dict_)


def validate_username(username):
    contains_valid_chars = True
    for char in username:
        if char not in (string.ascii_letters + "_-0123456789"):
            contains_valid_chars = False
    if not contains_valid_chars:
        print("ERROR: The username has invalid characters in it. Make sure you are a=only using letters, numbers,"
              "the - character and the _ character.")
        return False
    elif not (len(username) > 3 and len(username) < 15):
        print("ERROR: The length of the username must be GREATER than3 letters and LESS THEM 15 letters.")
        return False
    return True


def validate_password(password):
    if len(password) > 3 and len(password) < 14:
        return True
    else:
        print("ERROR: Password is too short (or too long)")
        return False


def validate_email(email):
    try:
        match_object = re.match(r'[a-zA-Z0-9+_]+@[a-zA-Z0-9-.]+', email)
        return match_object.span()[0] == 0 and match_object.span()[1] == len(email)
    except:
        return False


def validate_name(name):
    try:
        match_object = re.match(r'[a-zA-Z]+\s([a-zA-Z.]+)?\s?[a-zA-Z]+', name)
        return match_object.span()[0] == 0 and match_object.span()[1] == len(name)
    except:
        return False


def create_user():
    print("Make sure that:")
    print("- Your username contains only letters, numbers, the underscore (_) and the hyphen (-)\n"
          "- Your username is more than 3 and less than 15 characters long\n"
          "- Your password is greater than 5 characters and less than 14 characters\n"
          "- Your email is a real valid email\n"
          "- You include both your first and last name (middle name is optional)")

    username = input("What do you want your username to be? Be creative; you won't be able to change this later! ")
    if not validate_username(username) or username_exists(username, users):
        if username_exists(username, users):
            print("ERROR: Sorry, that username is already taken. Try something else!")
        return

    password = input("What do you want your password to be? ")
    if not validate_password(password):
        return

    confirm_password = input("Please type your password again: ")
    if password != confirm_password:
        print("ERROR: The two passwords don't match")
        return

    name = input("What's your full name? (This is optional) ")
    if name != '' and not (validate_name(name)):
        print("ERROR: Isn't a valid name.")
        return

    email = input("What's your email you would like to share? (Also optional) ")
    if email != '' and not (validate_email(email)):
        print("ERROR: Isn't a valid email.")
        return

    print("(Optional, press Ctrl+d to quit) Enter a little more about yourself... (Press Ctrl+d to confirm)")
    bio = sys.stdin.read().strip()

    user_info = {
        'username': username,
        'password': password
    }
    if name:
        user_info['name'] = name
    if email:
        user_info['email'] = email
    if bio:
        user_info['bio'] = bio

    print("Creating account...")
    user = User(**user_info)
    users.append(user)
    print("Creation complete! You may log in (using the command LOG IN) now.")


try:
    file = open('data.json')
except FileNotFoundError:
    users = []
    posts = []
else:
    print("Information found! Loading in info...")
    data = json.loads(json.load(file))
    users = [convert_to_user(user) for user in data['users']]
    posts = [convert_to_post(post) for post in data['posts']]
    print("Loading complete!\n")

current_user = None


help_message = """get help => Gives this help message
help => Same action as "get help"

quit => Exits the application
exit => Same action as "quit"

add post => Allows you to make a post up to 40 characters long
make post => Same action as "add post"
create post => Same action as "add post"

read posts => Displays all of the posts of all users
show posts => Same action as "read posts"
view posts => Saem action as "read posts"
posts => Same action as "read posts"

create user => Lets you create an account
sign up => Same effect as "create user"
create account => Same effect as "create user"

log in => Logs you in. You must be logged out to do this
sign in => Same action as "log in"

log out => Logs you out so the computer doesn't know who you are. You must do this to sign into another account!
sign out => Same effect as "log out"

view profile => View a users's profile

users => Get a list of users

remove account => Removes your account and logs you out
delete account => Same effect as "remove account"
"""

print("Type HELP to get help.")

while True:
    if current_user:
        user_input = input('@%s > ' % current_user.username).lower()
    else:
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
        elif user_input == 'users':
            for user in users:
                print(user.get_username())
        elif user_input == 'log out' or user_input == 'sign out':
            print("Dude, your already signed out!")
        elif user_input == 'exit' or user_input == 'quit':
            print("Saving information...")
            save_data(users, posts)
            print("Completed saving! Bye!")
            sys.exit(0)
        elif user_input == 'help' or user_input == 'get help':
            print(help_message)
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
        elif user_input in ('read posts', 'show posts', 'view posts', 'posts'):
            display_posts()
        elif user_input == 'create user' or user_input == 'sign up' or user_input == 'create account':
            print("You must be signed out to do that!")
        elif user_input == 'sign in' or user_input == 'log in':
            print("You must be signed out to do that!")
        elif user_input == 'log out' or user_input == 'sign out':
            print("Logging out...")
            current_user = None
            print("Logging out complete!")
        elif user_input == 'view profile':
            username = input("Which user's profile would you like to see? Input the username of the user: ")

            found = False
            for user in users:
                if user.get_username() == username:
                    found = True
                    input("Found! Press enter to view.")
                    os.system('clear')
                    user.display_profile()
                    input("Press enter to go back to the menu...")
                    os.system('clear')
            if not found:
                print("User not found. Did you make a typo?")
        elif user_input == 'delete account' or user_input == 'remove account':
            check = input("Are you sure? [Ny] ")
            if check.lower() == 'y' or check.lower() == 'yes':
                print('Removing account...')
                users.remove(current_user)
                print("Finished! Logging out...")
                current_user = None
                print("All complete!")
        elif user_input == 'users':
            for user in users:
                print(user.get_username())
        elif user_input == 'exit' or user_input == 'quit':
            print("Saving information...")
            save_data(users, posts)
            print("Completed saving! Bye %s!" % current_user)
            sys.exit(0)
        elif user_input == 'show json':
            print(json.loads(json.load(open('data.json'))))
        elif user_input == '':
            print("Ahem. What did you want to say?")
        else:
            print("I didn't understand that command. If you want a list of commands, type HELP.")
    print()
