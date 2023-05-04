import openai
openai.api_key = "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"

def create_image_prompt(product_name: str, visual_features: str, prompt_number=3) -> str:
    """create prompts for Midjourney
    Args:
        product_name (str): name for the content breif
        visual_features (str): visual features in content brief
    Returns:
        str: Description 1... Description 2... 
    """
    if prompt_number > 5:
        print("prompt number cannot be larger than 5.")
    prompt = "I am promoting a product called {}. I need to have these visual features in my pictures: {}. \
                Can you give me {} example descriptions of images that would fit those visual features? \
                Please format the response as \"Description 1: ...; Description 2:...\"".format(product_name, visual_features, prompt_number)
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}], temperature=0.2)
    response = completion["choices"][0]["message"]["content"]
    return response