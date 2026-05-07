from typing import Any, Optional

from fastapi import Response

from app.entities.types.response_type import TypeResponses

class WebResponse():

    @staticmethod
    def response(
        type: TypeResponses,
        messsage: str,
        title: str,
        content: Optional[Any],
        http_code: int):

        return Response(
            status_code=http_code,
            content={
                "type": type,
                "message": messsage,
                "title": title,
                "data": content
            },
        )