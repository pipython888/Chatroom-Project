from datetime import datetime


class Post:
    def __init__(self, user, content):
        assert len(content) < 40
        self.user = user
        self.content = content
        self.time = datetime.now().strftime('%A, %b. %d %Y, %I:%M%p')

    def display_post(self):
        print('@%s: %s\t\t%s' % (self.user.username, self.content, self.time))