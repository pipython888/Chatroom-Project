from datetime import datetime
import string
import re


def is_valid_email(email):
    try:
        match_object = re.match(r'[a-zA-Z0-9+_]+@[a-zA-Z0-9-.]+', email)
        return match_object.span()[0] == 0 and match_object.span()[1] == len(email)
    except:
        return False


def is_valid_name(name):
    try:
        match_object = re.match(r'[a-zA-Z]+\s([a-zA-Z.]+)?\s?[a-zA-Z]+', name)
        return match_object.span()[0] == 0 and match_object.span()[1] == len(name)
    except:
        return False


class User:
    def __init__(self, username, password, email=None, name=None, bio="No bio for this user"):
        # Check to make sure the username doesn't contain strange characters
        contains_valid_chars = True
        for char in username:
            if char not in (string.ascii_letters + "_-0123456789"):
                contains_valid_chars = False

        assert (type(username) == str or username == None) and contains_valid_chars
        assert type(password) == str and len(password) > 5 and len(password) < 14
        assert is_valid_email(email) or email == None
        assert is_valid_name(name) or name == None
        assert len(username) > 3 and len(username) < 15

        self.username = username
        self.password = password
        self.email = email
        self.name = name

        self.bio = ''
        # Add a newline after each 72 characters
        i = 1
        for char in bio:
            if char == '\n':
                i = 1
            if i > 72:
                i = 1
                self.bio += '\n'
            self.bio += char
            i += 1

        self.time_joined = datetime.now().strftime('%A, %b. %d %Y, %I:%M%p')

    def display_profile(self):
        lines = ['Joined at: ' + self.time_joined]
        if self.name:
            lines.append('Name: ' + self.name)
        if self.email:
            lines.append('Email: <%s>' % self.email)
        lines.extend(self.bio.split('\n'))

        # Get the longest line on the profile view
        longest_line_length = max([len(x) for x in lines])

        extra_spaces = 0
        if len(self.username) > 15:
            extra_spaces = 8
        elif len(self.username) > 10:
            extra_spaces = 5
        elif len(self.username) > 5:
            extra_spaces = 3

        # Print username
        print(' ' * (longest_line_length // 2 - len(self.username) + extra_spaces) + self.username)
        print('-' * longest_line_length)

        # Print email & name
        if self.name:
            print('Name:', self.name)
        if self.email:
            print('Email: <%s>' % self.email)
        print('Joined at:', self.time_joined)
        print('-' * longest_line_length)

        # Print bio
        print(self.bio)
        print('-' * longest_line_length)

    def get_username(self):
        return self.username

    def is_user(self, username, password):
        assert type(username) == str and type(password) == str
        return self.username == username and self.password == password

    def convert_to_dict(self):
        dict_ = {
            'username': self.username,
            'password': self.password,  # Check this to be safer
        }
        if self.name:
            dict_['name'] = self.name
        if self.email:
            dict_['email'] = self.email
        if self.bio:
            dict_['bio'] = self.bio
        return dict_
