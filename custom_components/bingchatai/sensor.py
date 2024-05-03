import requests
import json
import yaml
import aiohttp
import logging
import asyncio
import os
import voluptuous as vol
import urllib.request
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_NAME
from sydney import SydneyClient

import homeassistant.helpers.config_validation as cv
from homeassistant.core import callback

from .const import (
    DOMAIN,
    INPUT_NAME1,
    INPUT_NAME2,
    NAME,
    CONF_STYLE,
    COOKIE,
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=NAME): cv.string,
    vol.Optional("input_name", default=INPUT_NAME1): cv.string,
    vol.Optional("input_name_2", default=INPUT_NAME2): cv.string,
    vol.Optional("cookie", default=COOKIE): cv.string,
    vol.Required("style", default=CONF_STYLE): cv.string,
})

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    name = config[CONF_NAME]
    input_name = config["input_name"]
    input_name_2 = config["input_name_2"]
    cookie = config["cookie"]
    style = config["style"]
    async_add_entities([BingChatResponseSensor(hass, name, input_name, input_name_2, cookie, style)], True)

async def clean_response(message):
    message = message.replace('[["','')
    message = message.replace('"]]','')
    message = message.replace("\n","\r\n")
    message = message.replace('"', '')
    message = message.replace("'", '')
    message = message.replace("**", '')
    message = message.replace("[^1^]", '')
    message = message.replace("[^2^]", '')
    message = message.replace("[^3^]", '')
    message = message.replace("[^4^]", '')
    message = message.replace("[^5^]", '')
    message = message.replace("[^6^]", '')
    message = message.replace("[^7^]", '')
    message = message.replace("[^8^]", '')
    message = message.replace("[^9^]", '')
    message = message.replace("[^10^]", '')

    return message


class BingChatResponseSensor(SensorEntity):
    def __init__(self, hass, name, input_name, input_name_2, cookie, style):
        self._hass = hass
        self._name = name
        self._input_name = input_name
        self._input_name_2 = input_name_2
        self._cookie = cookie
        self._style = style
        self._state = None
        self._response_text = ""

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return {"response_text": self._response_text}

    async def ask(self, prompt):
        _LOGGER.debug(f"Asking Bing")
        # Check if the prompt starts and ends with double quotes, if not, add them.
        if not prompt.startswith('"'):
            prompt = '"' + prompt
        if not prompt.endswith('"'):
            prompt = prompt + '"'

        cookie = ""
        #data = urllib.request.urlopen(self._cookieurl)
        fo = open("cookie.txt","r")
        cookie = fo.read()
        fo.close()

        # Replace all double quotes except for the ones at the start and end
        sanitized_prompt = '"' + prompt[1:-1].replace('"', '') + '"'
        query_response = ""

        cookie = cookie.replace("\n","")
        cookie = cookie.replace("#033[0m","")

        _LOGGER.info(f"Bing Cookie: {cookie}")

        # Set Cookie
        os.environ["BING_U_COOKIE"] = cookie
        os.environ["BING_COOKIES"] = cookie

        # Sydney Client

        try:
            async with SydneyClient(style=self._style) as sydney:

                async for response in sydney.ask_stream(sanitized_prompt):
                    query_response += response
            query_response = await clean_response(query_response)

        except Exception as inst:
            query_response = inst

        _LOGGER.info(f"Bing response: {query_response}")
        
        return query_response

    @callback

    async def async_ask(self, entity_id, old_state, new_state):
        new_query = new_state.state
        new_query2 = self._hass.states.get("input_text." + self._input_name_2)
        new_query = str(new_query) + str(new_query2.state)

        if len(new_query) > 5:
            self._state = "Query Starting"
            self._response_text = "Sending Request..." + new_query
            self.async_write_ha_state()
            response = await self.ask(new_query)
            self._response_text = response
            self._state = "Query Complete"
            self.async_write_ha_state()
            self._state = "Reset"
            self.async_write_ha_state()

    async def async_added_to_hass(self):
        self.async_on_remove(
            self._hass.helpers.event.async_track_state_change(
                f"input_text.{self._input_name}", self.async_ask
            )
        )

    async def async_update(self):
        pass

