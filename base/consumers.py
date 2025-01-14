import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Tank

class UpdateTank(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "room"
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        t1 = await sync_to_async(Tank.objects.get)(user_address="tank_1")
        t2 = await sync_to_async(Tank.objects.get)(user_address="tank_2")
        await self.channel_layer.group_send(
            self.room_group_name,
                {
                    "type": "sync",
                    "tank_1": t1.water_level,
                    "tank_2": t2.water_level,
                    "t_1_active": t1.is_active,
                    "t_2_active": t2.is_active,
                }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        handler = text_data_json["type"]
        
        # check to see if data is coming frontend
        if handler == "update_active_1":
            t_1_active = text_data_json["t_1_active"]

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": handler,
                    "t_1_active": t_1_active,
                },
            )
            t1 = await sync_to_async(Tank.objects.get)(user_address="tank_1")
            t1.is_active = t_1_active
            await sync_to_async(t1.save)()

        if handler == "update_active_2":
            t_2_active = text_data_json["t_2_active"]

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": handler,
                    "t_2_active": t_2_active,
                },
            )
            t2 = await sync_to_async(Tank.objects.get)(user_address="tank_2")
            t2.is_active = t_2_active
            await sync_to_async(t2.save)()

        if handler == "stream":
            tank_1 = text_data_json["tank_1"]
            tank_2 = text_data_json["tank_2"]
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": handler,
                "tank_1": tank_1,
                "tank_2": tank_2,
            })
            t1 = await sync_to_async(Tank.objects.get)(user_address="tank_1")
            t2 = await sync_to_async(Tank.objects.get)(user_address="tank_2")
            t1.water_level = tank_1
            t2.water_level = tank_2

            await sync_to_async(t1.save)()
            await sync_to_async(t2.save)()

    async def stream(self, event):

        await self.send(
            text_data=json.dumps(
                {
                    "type": "stream",
                    "tank_1": event["tank_1"],
                    "tank_2": event["tank_2"],
                }
            )
        )

    async def update_active_1(self, event):

        await self.send(
            text_data=json.dumps(
                {
                    "type": "update_active_1",
                    "t_1_active": event["t_1_active"],
                }
            )
        )

    async def update_active_2(self, event):

        await self.send(
            text_data=json.dumps(
                {
                    "type": "update_active_2",
                    "t_2_active": event["t_2_active"],
                }
            )
        )
    # sync frontend and esp32 on connect with data from the database
    async def sync(self, event):

        await self.send(
            text_data=json.dumps(
                {
                    "type": "sync",
                    "tank_1": event["tank_1"],
                    "tank_2": event["tank_2"],
                    "t_1_active": event["t_1_active"],
                    "t_2_active": event["t_2_active"],
                }
            )
        )
