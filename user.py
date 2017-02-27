from datetime import datetime
import string
import re


class User:
    def __init__(self, username, password, email=None, name=None, bio="No bio for this user"):
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

    def __str__(self):
        return self.username

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

    def get_email(self):
        return self.email

    def set_password(self):
        old_password = input("What's your current password? ")
        if old_password == self.password:
            new_password = input("What do you want your password to be? ")
            confirm_password = input("Please enter the new password again... ")
            if new_password == confirm_password:
                print("Resetting password...")
                self.password = new_password
            else:
                print("Those two passwords don't match!")
        else:
            print("That isn't your password...")

    def set_bio(self, new_bio):
        self.bio = new_bio

    def set_email(self, email):
        self.email = email

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
