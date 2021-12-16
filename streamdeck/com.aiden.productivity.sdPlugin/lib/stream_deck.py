#!/usr/bin/env python3

import argparse
import json
from typing import ForwardRef

import websockets

from lib.button import Button


__ALL__ = ['Interface', 'Event']


class Event(dict):
    KEY_DOWN: str = 'keyDown'
    KEY_UP: str = 'keyUp'
    WILL_APPEAR: str = 'willAppear'
    WILL_DISAPPEAR: str = 'willDisappear'


    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Interface:
    __port: int = 8000
    __plugin_uuid: str = ""
    __register_event: str = "registerPlugin"
    __info: dict = {}
    __web_socket: websockets.WebSocketCommonProtocol = None

    __buttons: dict[str, Button] = {}


    # Lifecycle methods

    async def __aenter__(
        self,
    ) -> ForwardRef('Interface'):
        self.__parse_args()

        self.__web_socket = await websockets.connect(
            f'ws://127.0.0.1:{self.__port}',
        )

        await self.__send_payload({
            'event': self.__register_event,
            'uuid': self.__plugin_uuid,
        })

        return self


    async def __aexit__(
        self,
        _exc_type,
        _exc_value,
        _exc_traceback,
    ) -> None:
        self.__web_socket.close()


    def __aiter__(
        self,
    ) -> ForwardRef('Interface'):
        return self


    async def __anext__(
        self,
    ) -> Event:
        response: str = await self.__web_socket.recv()
        data: dict = json.loads(response)

        data['type'] = data['event']
        del data['event']

        if 'action' in data:
            data['action'] = data['action'].rsplit('.', 1)[-1]

        event = Event(data)

        if event.type == Event.WILL_APPEAR:
            button = Button(
                self,
                event.action,
                event.context,
                event.device,
                event.payload['settings'],
            )

            self.__buttons[event.context] = button
            event.instance = self.__buttons[event.context]

        if event.type == Event.WILL_DISAPPEAR:
            event.instance = self.__buttons[event.context]
            del self.__buttons[event.context]

        if event.type == Event.KEY_DOWN:
            await self.__buttons[event.context].key_down()
            event.instance = self.__buttons[event.context]

        if event.type == Event.KEY_UP:
            await self.__buttons[event.context].key_up()
            event.instance = self.__buttons[event.context]

        return event


    # Public methods

    async def get_global_settings(
        self,
        context: str,
    ) -> None:
        await self.__send_payload({
            "event": "getGlobalSettings",
            "context": context,
        })


    async def get_settings(
        self,
        context: str,
    ) -> None:
        await self.__send_payload({
            "event": "getSettings",
            "context": context,
        })


    async def log_message(
        self,
        message: str,
    ) -> None:
        await self.__send_payload({
            "event": "logMessage",
            "payload": {
                "message": message,
            },
        })


    async def open_url(
        self,
        url: str,
    ) -> None:
        await self.__send_payload({
            "event": "openUrl",
            "payload": {
                "url": url,
            },
        })


    async def send_to_property_inspector(
        self,
        context: str,
        payload: dict,
    ) -> None:
        await self.__send_payload({
            "event": "sendToProperyInspector",
            'context': context,
            'payload': payload,
        })


    async def set_global_settings(
        self,
        context: str,
        payload: dict,
    ) -> None:
        await self.__send_payload({
            "event": "setGlobalSettings",
            "context": context,
            "payload": payload,
        })


    async def set_image(
        self,
        context: str,
        image: str,
        target: int = None,
        state: int = None,
    ) -> None:
        await self.__send_payload({
            "event": "setImage",
            "context": context,
            "payload": {
                "image": image,
                "target": target,
                "state": state,
            },
        })


    async def set_settings(
        self,
        context: str,
        payload: dict,
    ) -> None:
        await self.__send_payload({
            "event": "setSettings",
            "context": context,
            "payload": payload,
        })


    async def set_state(
        self,
        context: str,
        state: int,
    ) -> None:
        await self.__send_payload({
            "event": "setState",
            "context": context,
            "payload": {
                "state": state,
            },
        })


    async def set_title(
        self,
        context: str,
        title: str,
        target: int = None,
        state: int = None,
    ) -> None:
        await self.__send_payload({
            "event": "setTitle",
            "context": context,
            "payload": {
                "title": title,
                "target": target,
                "state": state,
            },
        })


    async def show_alert(
        self,
        context: str,
    ) -> None:
        await self.__send_payload({
            "event": "showAlert",
            "context": context,
        })


    async def show_ok(
        self,
        context: str,
    ) -> None:
        await self.__send_payload({
            "event": "showOk",
            "context": context,
        })


    async def switch_to_profile(
        self,
        context: str,
        device: str,
        profile_name: str,
    ) -> None:
        await self.__send_payload({
            "event": "switchToProfile",
            "context": context,
            "device": device,
            "payload": {
                "profile": profile_name,
            },
        })


    # Private methods

    def __parse_args(
        self,
    ) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-port',
            type=int,
            required=True,
        )
        parser.add_argument(
            '-pluginUUID',
            type=str,
            required=True,
            dest='plugin_uuid',
        )
        parser.add_argument(
            '-registerEvent',
            type=str,
            required=True,
            dest='register_event',
        )
        parser.add_argument(
            '-info',
            type=str,
            required=True,
        )

        args = parser.parse_args()

        self.__port = args.port
        self.__plugin_uuid = args.plugin_uuid
        self.__register_event = args.register_event
        self.__info = args.info


    async def __send_payload(
        self,
        payload: dict,
    ) -> None:
        json_string: str = json.dumps(payload)
        await self.__web_socket.send(json_string)
