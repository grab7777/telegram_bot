import openai
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI()


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
