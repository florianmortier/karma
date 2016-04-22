import logging
import re
from karma import KarmaHandler
logger = logging.getLogger(__name__)


class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer):
        self.clients = slack_clients
        self.msg_writer = msg_writer
        self.karma = KarmaHandler(self.msg_writer)

    def handle(self, event):

        if 'type' in event:
            self._handle_by_type(event['type'], event)

    def _handle_by_type(self, event_type, event):
        # See https://api.slack.com/rtm for a full list of events
        if event_type == 'error':
            # error
            self.msg_writer.write_error(event['channel'], json.dumps(event))
        elif event_type == 'message':
            # message was sent to channel
            self._handle_message(event)
        elif event_type == 'channel_joined':
            # you joined a channel
            self.msg_writer.write_help_message(event['channel'])
        elif event_type == 'group_joined':
            # you joined a private group
            self.msg_writer.write_help_message(event['channel'])
        else:
            pass
    
    def _handle_message(self, event):
        # Filter out messages from the bot itself
        if not self.clients.is_message_from_me(event['user']):

            msg_txt = event['text']

            #if self.clients.is_bot_mention(msg_txt):
                # add bot response here!"
            #else:
                # if karma change
            if self.karma.is_karma(msg_txt):
                self.karma.handle(event['channel'], msg_txt)
            if msg_txt.startswith("!"):
                # bot command stating by '!'
                command = msg_txt.split(" ")[0][1:]
                if command == "karma":
                    name = msg_txt.split(" ")[1]
                    self.msg_writer.write_text(event['channel'], self.karma.get_karma(name))
                if command == "help":
                    self.msg_writer.write_text(event['channel'], self.karma.help())
