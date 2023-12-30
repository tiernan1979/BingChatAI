
# Home Assistant Bing Response Sensor 
# (No API Key Needed)

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

This custom component for Home Assistant allows you to generate text responses using Bing at no expense.<BR>
This Integration was forked from HassAssistants MindDB integration. https://github.com/Hassassistant/OpenMindsAI/

This integration requires sydney-py https://github.com/vsakkas/sydney.py which connects to the Bing AI.<BR>
Which is installed when installing via hacs or Manually.<BR><BR>
Please note that the Cookie does expire every 2 weeks and also appears to timeout every 2 days.<BR>
<i> The current version i've locked this integration to of sydney.py might work without a cookie.</i><BR>
I currently have a window refreshing on a PC as a work around to this timeout.<BR>

## Get Cookie from Bing Chat

**1.** Login to Bing Chat. https://www.bing.com/chat/

**2.** Request a question 

**3.** Open the developer tab and go to the cookies. Find _U

**4.** Copy the cookie into cookie.txt in the integration folder (this is done so no restart of Home Assistant is required to replace the cookie)


## Home Assistant Integration
**1.** 
**(Manual)** Copy the **BingChatAI** folder to your Home Assistant's custom_components directory. If you don't have a **custom_components** directory, create one in the same directory as your **configuration.yaml** file.

**(HACS)** Add this repository to HACS. https://github.com/tiernan1979/BingChatAI/

**2.** Restart Home Assistant.

**2.** Add the following lines to your Home Assistant **configuration.yaml** file:

```yaml
input_text:
  gpt_prompt:
    initial: ""
    max: 255
  gpt_prompt2:
    initial: ""
    max: 255
## This is the input_text entity you'll use to send prompts.

sensor:
  - platform: BingChatAI
    name: "BingChatAI"
## Optional. Defaults to BingChatAI
    input_name: "bing_text"
    input_name2 "bing_text2"
## Optional. Defaults to bing_text. This is your input_text name
    style: "Precise"
## Optional. Defaults to Precise. This is the search Style
```
**3.** Restart Home Assistant.

## Usage
To generate a response from Bing, update the **input_text.gpt_prompt2** first (if over 255 characters) then **input_text.gpt_prompt** <BR>
entity with the text you want to send to the model. The generated response will be available as an attribute of the **sensor.bing_response** entity.

## Example
To display the Bing input and response in your Home Assistant frontend, add the following to your **ui-lovelace.yaml** file or create a card in the Lovelace UI:

```yaml
type: grid
square: false
columns: 1
cards:
  - type: entities
    entities:
      - entity: input_text.gpt_prompt
  - type: markdown
    content: '{{ state_attr(''sensor.bing_response'', ''response_text'') }}'
    title: OpenAI Response
```
Now you can type your text in the GPT Prompt Input field, and the generated response will be displayed in the response card.

**Disclaimer:** This project is not affiliated with or endorsed by OpenAI/Bing. Use the GPT-4 API at your own risk.
