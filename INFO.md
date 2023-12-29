<img src="https://github.com/Hassassistant/openai_response/blob/main/misc/ChatGPT_image.PNG?raw=true"
     width="20%"
     align="right"
     style="float: right; margin: 10px 0px 20px 20px;" />

# Home Assistant OpenAI Response Sensor

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

This custom component for Home Assistant allows you to generate text responses using Bing's OpenAI's GPT-4 model.

Head to **[This Link](https://www.bing.com/chat)** to get you cookie from Bing Chat. 


## Installation
**1.** Copy the **bing_response** folder to your Home Assistant's custom_components directory. If you don't have a **custom_components** directory, create one in the same directory as your **configuration.yaml** file.

**2.** Add the following lines to your Home Assistant **configuration.yaml** file:

```yaml
sensor:
  - platform: BingChatAI
    name: Bing_response # Optional, Defaults to "BingChatAI"
    input_name: "gpt_prompt" # Optional, defaults to "bing_text"
    input_name2: "gpt_prompt2" # Optional, defaults to "bing_text2"
    style: "precise" # Optional, defaults to "precise"
```
**3.** Restart Home Assistant.

## Usage
Create an **input_text.gpt_input** entity in Home Assistant to serve as the input for the GPT-3 model. Add the following lines to your configuration.yaml file:

```yaml
input_text:
  gpt_input:
    name: GPT-3 Input
```
Note you can also create this input_text via the device helpers page!

If you are creating via YAML, you will need to restart again to activate the new entity,

To generate a response from Bing, update the **input_text.gpt_text** and **input_text.bing_text2** (if the line is greater than 255) entity with the text you want to send to the model. The generated response will be available as an attribute of the **sensor.Bing_response** entity.

## Example
To display the Bing input and response in your Home Assistant frontend, add the following to your **ui-lovelace.yaml** file or create a card in the Lovelace UI:

```yaml
type: grid
square: false
columns: 1
cards:
  - type: entities
    entities:
      - entity: input_text.Bing_text
      - entity: input_text.Bing_text
  - type: markdown
    content: '{{ state_attr(''sensor.Bing_response'', ''response_text'') }}'
    title: ChatGPT Response
```
Now you can type your text in the Bing Input field, and the generated response will be displayed in the response card.


**Disclaimer:** This project is not affiliated with or endorsed by OpenAI or Bing. Use Bing at your own risk, and be aware of cookie expiry and connection timeout.
