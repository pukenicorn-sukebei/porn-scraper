import logging
from datetime import datetime, timedelta
from typing import Callable

from fastapi.routing import APIRoute
from starlette.background import BackgroundTask
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse


class LoggingRoute(APIRoute):
    logger = logging.getLogger('API')

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            start_time = datetime.now()
            req_body = await request.body()
            response = await original_route_handler(request)
            end_time = datetime.now()

            timing = end_time - start_time

            if isinstance(response, StreamingResponse):
                res_body = b''
                async for item in response.body_iterator:
                    res_body += item

                streaming_response = Response(
                    content=res_body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type,
                )

                streaming_response.background = BackgroundTask(
                    self.log_request,
                    request, streaming_response, timing
                )

                return streaming_response
            else:
                response.background = BackgroundTask(
                    self.log_request,
                    request, response, timing
                )
                return response

        return custom_route_handler

    def log_request(self, req: Request, res: Response, timing: timedelta):
        self.logger.info('[REQ][%s] %s %s', req.base_url, req.query_params, req.body())
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug('[RESP][%s] took $d, %s', req.base_url, timing, res.body)
        else:
            self.logger.info('[RESP][%s] took $d, length: %d', req.base_url, timing, len(res.body))
