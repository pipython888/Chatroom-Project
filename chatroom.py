from string import ascii_letters
from pprint import pprint
from os import system
import getpass
import json
import sys
import re

from vigenere import encode, decode
from user import User
from post import Post

KEY = 'NODf8dtlghmgf;hdfg0h[8fd79ertif&%$d90+ddf!~'


def display_posts():
    """Display all of the posts made by calling display_post() on each of the posts

    Returns a boolean"""

    for post in posts:
        post.display_post()


def username_exists(username, users):
    """Checks to see if a username exists or not

    username => The username you want to search if it exists. Type: String
    users => The list of users you want to search through. Type: List[User]

    Returns: boolean"""

    for user in users:
        if user.username == username:
            return True
    return False


def email_exists(email, users):
    """Checks to see if an email exists

    email => The email you want to search for. Type: String
    users => The list of users you want to search through. Type: List[User]

    Returns: boolean"""

    for user in users:
        if user.email == email:
            return True
    return False


def save_data(users, posts):
    """Saves all information, including users and posts, to the data.json file

    The passwords are kept "safe"!

    users => The list of users you want to save. Type: List[User]
    posts => The list of posts you want to save. Type: List[Post]

    Returns: None"""

    info_dict = {
        'users': [user.convert_to_dict() for user in users],
        'posts': [post.convert_to_dict() for post in posts]
    }

    for x in info_dict['users']:
        x['password'] = encode(x['password'], KEY)

    with open("data.json", 'w') as file_:
        json.dump(json.dumps(info_dict), file_)


def convert_to_user(dict_):
    """Converts a dictionary instance to a User instance.

    Since JSON files aren't allowed to hold instances, you must
    convert the instance to a dictionary. This converts the dictionary
    back to a User instance.

    dict_ => The dictionary you want to convert to a User

    Returns: A User instance"""

    dict_['password'] = decode(dict_['password'], KEY)
    return User(**dict_)


def convert_to_post(dict_):
    """Converts a dictionary to a Post instance.

    Since JSON files aren't allowed to hold instances, you must
    convert the instance to a dictionary. This converts the dictionary
    back to a Post instance.

    dict_ => The dictionary you want to convert to a Post

    Returns: A Post instance
    """

    dict_['user'] = convert_to_user(dict_['user'])
    return Post(**dict_)


def validate_username(username):
    """Makes sure that a username is okay to use.

    It checks these:

    - Makes sure that the username contains only letters, numbers, the - and the _ symbols
    - Make sure that it is longer than 3 characters and less than 15 characters

    username => The username you want to validate

    Returns: boolean"""

    # Checks if the username has valid characters.
    contains_valid_chars = True
    for char in username:
        if char not in (ascii_letters + "_-0123456789"):
            contains_valid_chars = False

    if not contains_valid_chars:
        print("ERROR: The username has invalid characters in it. Make sure you are are only using letters, numbers,"
              "the - character and the _ character.")
        return False
    # Checks if the username is longer than 3 but less than 5 characters.
    elif not (len(username) > 3 and len(username) < 15):
        print("ERROR: The length of the username must be GREATER than3 letters and LESS THEM 15 letters.")
        return False
    return True


def validate_password(password):
    """Makes sure the password is okay to use.

    Checks if the password is longer than 3 characters but less than 14.

    password => The password you want to validate

    Returns: boolean"""

    if len(password) > 3 and len(password) < 14:
        return True
    else:
        print("ERROR: Password is too short (or too long)")
        return False


def validate_email(email):
    """Makes sure that an email is okay to use.

    Checks to see if the email is valid in a RE expression.

    email => The email you want to check

    Returns: boolean"""

    try:
        match_object = re.match(r'[a-zA-Z0-9+_]+@[a-zA-Z0-9-.]+', email)
        return match_object.span()[0] == 0 and match_object.span()[1] == len(email)
    except:
        return False


def validate_name(name):
    """Makes sure that the name is okay to use.

    Uses a RE expression to check.

    Requires both a first and last name. Middle name is optinoal.

    name => The name you want to check on

    Returns: boolean"""

    try:
        match_object = re.match(r'[a-zA-Z]+\s([a-zA-Z.]+)?\s?[a-zA-Z]+', name)
        return match_object.span()[0] == 0 and match_object.span()[1] == len(name)
    except:
        return False


def create_user():
    """Makes a user.

    Asks the user for a lot of data, including:

    - Username (required)
    - Password (required)
    - Full name (optional, middle name is also optional)
    - Email (optional)
    - Bio (optional)

    All of these are checked to make sure they are valid.

    Returns: None"""

    # Print requirements
    print("Make sure that:")
    print("- Your username contains only letters, numbers, the underscore (_) and the hyphen (-)\n"
          "- Your username is more than 3 and less than 15 characters long\n"
          "- Your password is greater than 5 characters and less than 14 characters\n"
          "- Your email is a real valid email\n"
          "- You include both your first and last name (middle name is optional)")

    # Ask for and validates username
    username = input("What do you want your username to be? Be creative; you won't be able to change this later! ")
    if not validate_username(username) or username_exists(username, users):
        if username_exists(username, users):
            print("ERROR: Sorry, that username is already taken. Try something else!")
        return

    # Ask for and validates password
    password = getpass.getpass("What do you want your password to be? ")
    if not validate_password(password):
        return

    # Asks for the password to bew typed again
    confirm_password = getpass.getpass("Please type your password again: ")
    if password != confirm_password:
        print("ERROR: The two passwords don't match")
        return

    # Asks for and validates full name
    name = input("What's your full name? (This is optional) ")
    if name != '' and not (validate_name(name)):
        print("ERROR: Isn't a valid name.")
        return

    # Asks for and validates email
    email = input("What's your email you would like to share? (Also optional) ")
    if email != '' and not (validate_email(email)):
        print("ERROR: Isn't a valid email.")
        return
    if email_exists(email, users):
        print("That email is already used! You aren't allowed to make two accounts.")
        return

    # Asks for bio
    print("(Optional, press Ctrl+d to quit) Enter a little more about yourself... (Press Ctrl+d to confirm)")
    bio = sys.stdin.read().strip()

    # Store information as a dictionary
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

    # Convert dictionary to User and adds user to user list
    print("Creating account...")
    user = User(**user_info)
    users.append(user)
    print("Creation complete! You may log in (using the command LOG IN) now.")


def edit_profile(user, users):
    """A function that edits a profile.

    It can edit:

    - Passwords
    - Email
    - Bio

    user => The User you want to edit
    users => The list of Users"""

    # Ask the user what he/she would like to edit.
    # Asks repeatedly until the input is valid.
    to_edit = ''
    while to_edit not in ('password', 'email', 'bio', 'cancel'):
        to_edit = input("What do you want to edit? Enter PASSWORD, EMAIL, CANCEL (to cancel) or BIO: ").lower()
        if to_edit not in ('password', 'email', 'bio', 'cancel'):
            print("That's not one of the choices!")
        elif to_edit == 'cancel':
            # If the user enters "cancel", forget about editing their account
            return

    # Get the index of the User in the list of Users
    index_of_user = users.index(user)

    # Edit the part of the profile the user wants to edit
    if to_edit == 'password':
        users[index_of_user].set_password()
    elif to_edit == 'email':
        users[index_of_user].email = input("What's your new email? ")
    elif to_edit == 'bio':
        print("Enter your new bio (press Ctrl+d to confirm)...")
        users[index_of_user].bio = sys.stdin.read().strip()
    else:
        raise ValueError("Something went really wrong... the \"to_edit\" variable is a weird value of %s..." % to_edit)


try:
    file_ = open("data.json")
except FileNotFoundError:
    # If the data.json file doesn't exist, default the Users list and Posts list to be empty.
    users = []
    posts = []
else:
    # If the data.json file exists, great, load in the data.
    print("Information found! Loading in info...")
    data = json.loads(json.load(file_))
    users = [convert_to_user(user) for user in data['users']]
    posts = [convert_to_post(post) for post in data['posts']]
    print("Loading complete!\n")
    file_.close()

current_user = None

# Get help message
with open("help.txt") as help_file:
    help_message = help_file.read()

# ---- MAIN LOOP ----

print("Type HELP to get help.")
while True:
    # If the user is logged in, put the username in the prompt. Otherwise, don't.
    if current_user:
        user_input = input('@%s > ' % current_user.username).lower()
    else:
        user_input = input('> ').lower()

    # If the user is logged out, the user has separate commands
    if current_user is None:
        if user_input == 'create user' or user_input == 'sign up' or user_input == 'create account':
            create_user()
        elif user_input == 'log in' or user_input == 'sign in':
            username = input("What's your username? ")
            password = getpass.getpass("What's your password? ")

            # Search for user
            found = False
            for user in users:
                if user.is_user(username, password):
                    found = True
                    print("Account found! Signing in...")
                    current_user = user
            # If the user is not found, tell the user
            if not found:
                print("Sorry, that account doesn't exist. Either your password is wrong or the user doesn't exist.")
        elif user_input == 'users':
            for user in users:
                print(user.username())
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
                print("Hmm... Your post doesn't seem valid. Make sure it isn't longer than 40 characters!")
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

            # Look for the user
            found = False
            for user in users:
                if user.username == username:
                    # Tell the computer that the user was found
                    found = True
                    # Wait for the user to press the ENTER key, then clear the screen & show the profile.
                    input("Found! Press enter to view.")
                    system('clear')
                    user.display_profile()
                    # When viewing profile, wait for the user to press ENTER once again then clear screen.
                    input("Press enter to go back to the menu...")
                    system('clear')
            # If the user wasn't found, tell the user
            if not found:
                print("User not found. Did you make a typo?")
        elif user_input == 'delete account' or user_input == 'remove account':
            # Make sure that the user wants to really delete their profile
            check = input("Are you sure? [Ny] ")
            if check.lower() == 'y' or check.lower() == 'yes':
                # If the user is 100% sure, remove their profile & log out
                print('Removing account...')
                users.remove(current_user)
                print("Finished! Logging out...")
                current_user = None
                print("All complete!")
        elif user_input == 'users':
            for user in users:
                print(user.username)
        elif user_input == 'save':
            print("Saving information...")
            save_data(users, posts)
            print("Completed saving!")
        elif user_input == 'exit' or user_input == 'quit':
            print("Saving information...")
            save_data(users, posts)
            print("Completed saving! Bye %s!" % current_user.username)
            sys.exit(0)
        elif user_input == 'edit account' or user_input == 'edit profile':
            edit_profile(current_user, users)
        elif user_input == 'follow user' or user_input == 'follow account':
            person_to_follow = input("Who do you want to follow? (Enter username of person) ")
            found = False
            # Look for user
            for user in users:
                if user.username == person_to_follow and user.username != current_user.username:
                    # If the user was found, follow the user
                    user.followers.append(current_user.username)
                    current_user.following.append(current_user.username)
                    print("Followed %s!" % person_to_follow)
                    found = True
            # If the user wasn't found (or if the user was the current user), tell the user.
            if not found:
                print("Either that user doesn't exist or you are trying to follow yourself...")
        elif user_input == 'show json':
            with open('data.json') as file_:
                pprint(json.loads(json.load(file_)))
        elif user_input == '':
            print("Ahem. What did you want to say?")
        else:
            print("I didn't understand that command. If you want a list of commands, type HELP.")
    print()
