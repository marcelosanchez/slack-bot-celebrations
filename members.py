import json

import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, date
from datetime import timedelta

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Member:
    def __init__(self):
        self.id = None
        self.name = None
        self.avatar_img = None
        self.bday = None

    @classmethod
    def validate_birthdays(cls):
        json_file = open('bdays.json')
        json_string = json_file.read()
        jdata = json.loads(json_string)
        for value in jdata['members']:
            if cls.is_your_bday(bday=value['birthday']):
                profile_info = cls.get_member_info(value['user_id'])
                member = Member()
                member.id = value['user_id']
                member.name = profile_info['name']
                member.avatar_img = profile_info['avatar']
                member.bday = value['birthday']
                return member
        return None

    @classmethod
    def is_your_bday(cls, bday):
        # gets todays date
        today = date.today()
        # Validate bday
        checker = datetime.strptime(bday, "%Y-%m-%d").date()
        if checker.month == today.month and checker.day == today.day:
            print(True)
            return True
        print(False)
        return False

    @classmethod
    def get_member_info(cls, user_id):
        token = os.environ['SLACK_BOT_TOKEN']
        client = slack.WebClient(token=token)
        profile_resp = client.users_profile_get(user=user_id)
        if profile_resp.get('ok') and profile_resp.get('ok') is True:
            profile = profile_resp.get('profile')
            profile_info = {
                "name": profile.get('real_name'),
                "avatar": profile.get('image_512'),
            }
            return profile_info

    def dict_to_json_block(self):

        json_block = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Alguien esta cumpliendo años en tu equipo hoy :partying_face:"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":birthday: " + self.name + "\n _" + Member.get_today_display() + "_  \n\n Muchas felicidades <@" + self.id + ">!"
                },
                "accessory": {
                    "type": "image",
                    "image_url": "" + self.avatar_img + "",
                    "alt_text": "avatar"
                }
            }
        ]
        return json_block

    @classmethod
    def get_today_display(cls):
        today = date.today()
        date_time_obj = datetime.strptime(str(today), '%Y-%m-%d')
        date_time_obj = date_time_obj  # Para convertirlo al GMT-05
        date_str = date_time_obj.strftime("%d %b")
        return date_str
