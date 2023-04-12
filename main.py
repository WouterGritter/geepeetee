import os

import openai as openai
from dotenv import load_dotenv

from event import SystemEvent
from session import Session

load_dotenv()

if __name__ == '__main__':
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if openai_api_key is None:
        print('Please provide an OpenAI API key.')
        exit(-1)

    print(f'OpenAI API Key: {openai_api_key[:3]}-{openai_api_key[-4:]}')
    openai.api_key = openai_api_key

    print('Hello! I am a GPT agent capable of basic thought, reasoning and planning.')

    session = Session()
    while True:
        session.generate_next_event()

        msg = input('> ')

        if msg == 'q':
            exit()
        if len(msg) > 0:
            session.short_term_events.append(SystemEvent(msg))
