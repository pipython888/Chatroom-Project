from datetime import datetime


class Post:
    def __init__(self, user, content, time=None):
        assert len(content) < 40
        self.user = user
        self.content = content
        if not time:
            self.time = datetime.now().strftime('%A, %b. %d %Y, %I:%M%p')
        else:
            self.time = time


    def display_post(self):
        print('@%s: %s\t\t%s' % (self.user.username, self.content, self.time))

    def convert_to_dict(self):
        return {
            'user': self.user.convert_to_dict(),
            'content': self.content,
            'time': self.time
        }
