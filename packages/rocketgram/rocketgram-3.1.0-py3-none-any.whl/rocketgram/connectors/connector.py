# Copyright (C) 2015-2021 by Vd.
# This file is part of Rocketgram, the modern Telegram bot framework.
# Rocketgram is released under the MIT License (see LICENSE).


import logging

from ..api import Request, Response
from ..version import version

logger = logging.getLogger('rocketgram.connectors.connector')

USER_AGENT = f'Rocketgram/{version()}'
HEADERS = {'Content-Type': 'application/json', 'User-Agent': USER_AGENT}


class Connector:
    async def init(self):
        raise NotImplementedError

    async def shutdown(self):
        raise NotImplementedError

    async def send(self, token: str, request: Request) -> Response:
        raise NotImplementedError

    def resolve_file_url(self, token: str, file_path: str) -> str:
        raise NotImplementedError
