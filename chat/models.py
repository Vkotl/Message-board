from django.db import models
from django.contrib.auth.models import User


class Message (models.Model):

    sender = models.ForeignKey(User, related_name='Sender')
    mess_receiver = models.ForeignKey(User, related_name='Receiver')
    content = models.CharField('Message', max_length=500)
    pub_date = models.DateTimeField('Date sent')

    def __str__(self):
        temp = 'Sent from: ' + self.sender.username + '\n' + 'Sent to: ' + self.mess_receiver.username + '\n'
        temp += self.content + '\n' + 'Sent on: ' + '{0}:{1}'.format(self.pub_date.hour, self.pub_date.minute)

        return temp