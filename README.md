
<img src="https://github.com/Hassassistant/OpenMindsAI/blob/main/misc/openmindsai.png?raw=true"
     width="20%"
     align="right"
     style="float: right; margin: 10px 0px 20px 20px;" />

# Home Assistant Bing Response Sensor 
# (No API Key Needed)

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

This custom component for Home Assistant allows you to generate text responses using Bing at no expense.<BR>
This Integration was forked from HassAssistants MindDB integration. https://github.com/Hassassistant/OpenMindsAI/


## Get Cookie from Bing Chat

**1.** Login to Bing Chat.

**2.** Request a question 

**3.** Open the developer tab and go to the cookies 

**4.** Copy the cookie into cookie.txt in the integration folder


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
    name: "Bing_response"
## Optional. Defaults to Bing_response
    input_name: "gpt_prompt"
    input_name2 "gpt2_prompt"
## Optional. Defaults to gpt_prompt. This is your input_text name
    style: "Precise"
## Optional. This is the search Style
```
**3.** Restart Home Assistant.

## Usage
To generate a response from GPT-3, update the **input_text.gpt_prompt** and **input_text.gpt_prompt2** (if the string is greater than 255) entity with the text you want to send to the model. The generated response will be available as an attribute of the **sensor.bing_response** entity.

## Example
To display the GPT-3 input and response in your Home Assistant frontend, add the following to your **ui-lovelace.yaml** file or create a card in the Lovelace UI:

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
