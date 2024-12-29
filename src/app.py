from inaSpeechSegmenter_api_models import (
    GetSegmentsResponse,
    GetSegmentsRequest,
    SegmentItem,
)

from inaSpeechSegmenter.segmenter import Segmenter

import base64
import logging

from os import remove, environ
from typing import List, Tuple

from fastapi import FastAPI

log_level = environ.get("INA_SPEECH_SEGMENTER_API_LOG_LEVEL", "DEBUG")

logger = logging.Logger(
    name=__name__,
    level=getattr(logging, log_level),
)

app = FastAPI()

@app.post(
    path=GetSegmentsRequest.get_endpoint(),
    response_model=GetSegmentsResponse,
)
async def get_segments(
    request: GetSegmentsRequest,
) -> GetSegmentsResponse:
    logger.debug(f"Received request for analyzing file `{request.filename}`")

    audio_bytes: bytes = base64.b64decode(request.audio_bytes_base64)

    segmenter = Segmenter()

    audio_path: str = f"{request.filename}"

    with open(audio_path, "wb") as file:
        file.write(audio_bytes)

    logger.debug(f"Begin analyzing file `{request.filename}`")

    segments: List[Tuple[str, float, float]] = segmenter(audio_path)

    logger.debug(f"Finished analyzing file `{request.filename}`")

    remove(audio_path)

    segments_response: List[SegmentItem] = [
        SegmentItem(
            label=label,
            start_time=start_time,
            end_time=end_time,
        )
        for label, start_time, end_time in segments
    ]

    response = GetSegmentsResponse(
        segments=segments_response,
    )

    logger.debug(f"Responding to request of `{request.filename}` with:\n{response}")

    return response
