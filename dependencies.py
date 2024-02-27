"""FastAPI dependencies."""

from typing import Annotated

import deepsearch as ds
from deepsearch.core.client.settings import ProfileSettings
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic(
    description="Provide the email and api_key for connecting to Deep Search."
)


async def get_deepsearch_api(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    """Initialize the Deep Search Toolkit with the default env settings"""

    settings = ProfileSettings(
        username=credentials.username,
        api_key=credentials.password,
        host="https://sds.app.accelerate.science/",
        verify_ssl=True,
    )
    api = ds.CpsApi.from_settings(settings=settings)

    return api