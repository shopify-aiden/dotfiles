import asyncio
import base64
from typing import Any, Callable, ForwardRef


class Button:
    action: str = ""
    context: str = ""
    device: str = ""
    settings: dict[str, Any] = {}

    __interface: ForwardRef("Interface") = None

    __handler_long_press: Callable[[ForwardRef('Button')], None] = None
    __handler_short_press: Callable[[ForwardRef('Button')], None] = None

    __key_press: asyncio.Task = None


    # Lifecycle methods

    def __init__(
        self,
        interface: ForwardRef('Interface'),
        action: str,
        context: str,
        device: str,
        settings: dict[str, Any],
    ) -> None:
        self.__interface = interface

        self.action = action
        self.context = context
        self.device = device
        self.settings = settings


    # Public methods

    async def key_down(
        self,
    ) -> None:
        if self.__key_press != None:
            self.__key_press.cancel()

        self.__key_press = asyncio.create_task(self.__key_down())


    async def key_up(
        self,
    ) -> None:
        if self.__key_press == None:
            return

        self.__key_press.cancel()

        if self.__handler_short_press != None:
            await self.__handler_short_press(self)


    async def set_image(
        self,
        image: str,
    ) -> None:
        await self.__interface.set_image(
            self.context,
            image
        )


    async def set_image_from_file(
        self,
        file_path: str,
    ) -> None:
        with open(file_path, 'rb') as in_file:
            image = base64.b64encode(in_file.read()).decode('utf-8')
            image = f'data:image/jpg;base64,{image}'

            await self.__interface.set_image(
                self.context,
                image,
            )


    def set_long_press_handler(
        self,
        handler: Callable[[ForwardRef('Button')], None]
    ) -> None:
        self.__handler_long_press = handler


    def set_short_press_handler(
        self,
        handler: Callable[[ForwardRef('Button')], None]
    ) -> None:
        self.__handler_short_press = handler


    async def set_settings(
        self,
        settings: dict[str, Any],
    ) -> None:
        self.settings = settings

        self.__interface.set_settings(
            self.context,
            settings
        )


    async def set_title(
        self,
        title: str,
    ) -> None:
        await self.__interface.set_title(
            self.context,
            title,
        )

    async def update(
        self,
        image: str,
        title: str,
        settings: dict[str, Any],
    ) -> None:
        if image == '' or image.startswith('data:image/'):
            await self.set_image(image)
        else:
            await self.set_image_from_file(image)

        await self.set_title(title)
        await self.set_settings(settings)


    # Private methods

    async def __key_down(
        self,
    ) -> None:
        await asyncio.sleep(0.5)

        if self.__handler_long_press != None:
            await self.__handler_long_press(self)

        self.__key_press = None
