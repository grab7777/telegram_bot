import openai
from dotenv import dotenv_values

config = dotenv_values(".env")
OPENAI_API_KEY = config.get("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)


def get_dalle_image(prompt, debug=False):
    """
    Generate an image using OpenAI's DALL-E model based on the provided prompt.
    """
    try:
        print(f"Generating image for prompt: {prompt}")
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
        )
        if debug:
            print("Response from OpenAI API:")
            print(response)
        image_url = response.data[0].url
        revised_prompt = response.data[0].revised_prompt
        return image_url, revised_prompt
    except Exception as e:
        print(f"Error generating image: {e}")
        return None


instruction = """Instruction: Please answer the prompt, which follows in the next message. Format your answer in the Telegram Markdown syntax:
*bold text*
_italic text_
[inline URL](http://www.example.com/)
[inline mention of a user](tg://user?id=123456789)
`inline fixed-width code`
```
pre-formatted fixed-width code block
```
```python
pre-formatted fixed-width code block written in the Python programming language
```
"""


def get_chatgpt_response(prompt, debug=False):
    """
    Generate a response using OpenAI's ChatGPT model based on the provided prompt.
    """

    try:
        print(f"Generating response for prompt: {prompt}")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": instruction},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            temperature=0.7,
        )
        if debug:
            print("Response from OpenAI API:")
            print(response)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {e}")
        return None
