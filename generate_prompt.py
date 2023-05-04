### generate prompt

import openai
import re

openai.api_key = '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'
model_id = "gpt-3.5-turbo"
IG = 'instagram'


def get_information(info):
    """
    get the informative data from Do and Don't
    """
    prompt = """
           Please provide the top 5 most informative points from the list of Do's and Don'ts provided respectively, 
           which must include the use of FTC disclosure and relevant hashtags. 
            """.format(info)
    completion = openai.ChatCompletion.create(model=model_id, messages=[{"role": "user", "content": prompt}])
    return completion["choices"][0]["message"]["content"]


def generate_prompts(brief, network_type, constraint):
    # prompt = '''
    #         write a one high-quality prompt for generating an {} image post based on the given {} and {}.
    #         The prompt should be no more than 200 words long and should effectively guide the generative model to generate a post
    #          that accurately represents the given the above text and constraints.
    #         '''.format(network_type, brief, constraint)
    prompt = '''
    I want to get a prompt that starts with "please write a prompt ~" to chatgpt to generate the post text.
    Please write a prompt for generating an {} post based on the given this text {} and this info {}, 
    the required hashtags from info must be included and no more than 200 words! 
    '''.format(network_type, brief, constraint)

    completion = openai.ChatCompletion.create(model=model_id, messages=[{"role": "user", "content": prompt}])

    return completion["choices"][0]["message"]["content"]

def generate_post_text(input_prompt, network_type, post_type):
    prompt_for_test_generation = '''Please write realistic {} {} text with required hashtags based on this information {}. 
    no more than 100 words!'''.format(network_type, post_type, input_prompt)

    completion = openai.ChatCompletion.create(model=model_id, messages=[{"role": "user", "content": prompt_for_test_generation}])

    return completion["choices"][0]["message"]["content"]


if __name__ == "__main__":
    brief = '''
    Brand Overview: Do More With Viator. The more you do, the more memories you make. After staying at home for a while, people need inspiration to get out there and make new, amazing memories. Viator has over 300,000 travel experiences and something for everyone.
    Viator's Mission is to bring more wonder into the world. To bring extraordinary, unexpected, and forever-memorable experiences to more people, more often, wherever they’re traveling, wherever they are.
    Influencer Concept: Inspire your followers to seize adventures available at their fingertips through Viator. From river cruises to night life in the city, highlight exciting summer adventures both near and far. Content will focus on three key messaging pillars: wonder & spontaneity, flexible options, and five star choices.
    '''

    info = '''
    Do: 
    
    DO ensure all excursions featured are currently bookable 
    DO ensure locations/bookings are open for US Residents 
    DO ensure content is travel, culture, and destination forward not overly sexy, fashion, or style-focused
    DO showcase landmarks where applicable (i.e. the Statue of Liberty)
    DO include the names of Viator experiences in your concepts for confirmation of legal watch-outs
    DO only include people who have given express permission to be featured in your content/advertising for Viator
    DO ensure activities are family friendly if anyone under 18 will be involved in your travels
    DO tag brand handle (i.e. @viatortravel) in all captions and videos using the branded content / collaborator tools within the platforms 
    DO include FTC disclosure hashtag (#ad or #sponsored) in all captions and videos
    DO include program hashtags (i.e. #DoMoreWithViator and #Viatortravel) in in all captions and videos
    
    Don't
    
    DON'T mention the tour company as Viator should be the focus
    DON'T feature the color orange when possible
    DON'T mention or show any brand names/logos within all content including, clothing/fashion logos, copyrighted characters, restuarant/store logos, foods, beverages, tech logos, etc.
    DON'T show any graffiti or murals 
    DON'T show alcohol (i.e. wineries or brewery tours), high risk tours (i.e. helicopters), or anything involving animals, sustainability, or "volun-tourism"
    DON'T use the language "visit the link in my bio"
    DON’T go live prior to review and approval from the Linqia team.
    DON’T reference violence, politics, explicit content, profanity, or specific religious holidays within all content.
    '''
    #
    # most_top_five_do_and_dont = get_information(info)
    # print(most_top_five_do_and_dont)

    prompt_result_from_gpt = generate_prompts(brief, IG, info)
    print('#################################################Prompt for chat gpt#######################################')
    print(prompt_result_from_gpt)
    print('#################################################post text#################################################')
    print(generate_post_text('post', IG, prompt_result_from_gpt))
