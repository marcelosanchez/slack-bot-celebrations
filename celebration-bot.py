import os
import asyncio
from datetime import datetime

from slack_integration import Slack
from members import Member

channel = os.environ['BOT_CHANNEL']


async def celebration_alerts():
    slack = Slack()
    TIEMPO_ESPERA = 90000  # segundos
    while True:
        bday_member = Member.validate_birthdays()
        print("[" + str(datetime.now()) + "] ** Buscando homenajeados")
        if bday_member:
            slack.send_messange_to_slack_channel(channel_name=channel, message="", json_block_msg=bday_member.dict_to_json_block())
        print("[" + str(datetime.now()) + "] ** Fin de la busqueda")
        await asyncio.sleep(TIEMPO_ESPERA)  # Tiempo de espera

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(celebration_alerts())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Finalizando Loop")
    loop.close()
