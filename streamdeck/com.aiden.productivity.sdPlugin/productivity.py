
import asyncio
import subprocess
from typing import Callable

from lib.button import Button
from lib.stream_deck import Event, Interface


log_path = '/Users/aidenstorey/dotfiles/data/_elgato_plugin_log'


def create_command_handler(
    command: str,
    *args: list[str],
) -> Callable[[Button], None]:
    async def __command_handler(_: Button) -> None:
        log(f'running command: {command}')

        try:
            subprocess.run(
                [
                    '/bin/zsh', '-l', '-c',
                    command,
                    *args,
                ],
            )
        except Exception as error:
            log(f'error running command: {error}')

    return __command_handler


async def handle_event(event: Event) -> None:
    if event.type == event.WILL_APPEAR:
        button: Button = event.instance

        for command in ['edit', 'shopify', 'start']:
            if event.action == command:
                button.set_short_press_handler(
                    create_command_handler(command)
                )

                break



def log(*parts) -> None:
    with open(log_path, 'a') as out_file:
        print('[productivity]', *parts, file=out_file)


async def main() -> None:
    async with Interface() as interface:
        async for event in interface:
            log(event)

            await handle_event(event)


if __name__ == '__main__':
    log('starting')
    try:
        asyncio.run(main())
    except Exception as error:
        log(f'uncaught error: {error}')
