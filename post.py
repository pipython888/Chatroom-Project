from datetime import datetime


class Post:
    def __init__(self, user, content, time=None):
        assert len(content) <= 300
        self.user = user
        self.content = content
        if not time:
            self.time = datetime.now().strftime('%A, %b. %d %Y, %I:%M%p')
        else:
            self.time = time

    def display_post(self):
        print('By %s at %s:\n%s' % (self.user.username, self.time, self.content))

    def convert_to_dict(self):
        return {
            'user': self.user.convert_to_dict(),
            'content': self.content,
            'time': self.time
        }
