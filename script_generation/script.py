import random
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the keys
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None or openai_api_key.strip() == "":
    raise ValueError("OpenAI API key not found. Please ensure it is set in the .env file.")

# Set the OpenAI API key
openai.api_key = openai_api_key


def generate_script():

    # List of possible styles
    styles = [
        "David Goggins",
        "Tony Robbins",
        "Les Brown",
        "Eric Thomas",
        "Jim Rohn",
        "Zig Ziglar",
        "Mel Robbins",
        "Simon Sinek"
    ]

     # List of possible topics
    topics = [
        "overcoming fear",
        "discipline",
        "persistence",
        "self-belief",
        "embracing failure",
        "taking action",
        "goal setting",
        "mindset shift",
        "resilience",
        "personal growth"
    ]

    # Randomly select a style and topic
    style = random.choice(styles)
    topic = random.choice(topics)

    # Randomly select the number of sentences to vary the script length
    num_sentences = random.randint(2, 8)  # Adjust as needed for desired length

    # Randomly decide whether to include a call to action
    include_call_to_action = random.choice([True, False])

    # Base prompt
    prompt = (
        f"Write a powerful, {num_sentences}-sentence motivational message in paragraph form about {topic} in the style of {style}. The message should inspire the viewer to take immediate action and feel a sense of urgency. Use strong, direct language that challenges the viewer. "
    )

    # Append call to action if decided
    if include_call_to_action:
        prompt += " End with a compelling call to action to like and subscribe for more content."
    

    try:
        completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", 
             "content": "You are a motivational speaker creating content for social media videos. Only provide the requested sentences and no other text. Always make sure to make it sound natural, in terms of tone, speech, grammar, syntax, and structure."},
            {
                "role": "user",
                "content": prompt
            }
        ]
        )

        return (completion.choices[0].message.content)
    
    except Exception as e:
        print(f"An error occurred while generating the script: {e}")
        return None
    