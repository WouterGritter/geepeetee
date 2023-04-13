import re

import openai

from event import Event, GPTEvent


class Session:
    def __init__(self, goals: list[str]):
        self.goals: list[str] = goals
        self.short_term_events: list[Event] = []
        self.long_term_summary: str = 'No long term summary.'

    def generate_next_event(self):
        prompt = self.stringify()
        print('PROMPT:')
        print(prompt)

        res = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=256,
            temperature=0.7,
            top_p=1,
            n=1,
        )

        completion = res.choices[0].text
        print('COMPLETION:')
        print(completion)

        regex = r'THOUGHT: (?P<thought>[^\n]+)\nREASONING: (?P<reasoning>[^\n]+)\nPLAN: (?P<plan>[^\n]+)\nSPEAK: (?P<speak>[^\n]+)\n?'
        matches = re.search(regex, completion)

        event = GPTEvent(
            thought=matches.group('thought'),
            reasoning=matches.group('reasoning'),
            plan=matches.group('plan'),
            speak=matches.group('speak'),
        )

        self.short_term_events.append(event)

        self.clean_up_short_term_memory()

    def clean_up_short_term_memory(self):
        if len(self.short_term_events) < 10:
            return

        last_event = self.short_term_events[len(self.short_term_events) - 1]

        prompt = f'The following is a GPT-system that\'s capable of thought, reasoning and planning. Summarize it\'s short-term memory, and summarize it\'s previous long-term memory even shorter in the total summary.\n' \
                 f'Previous long-term memory summary:\n' \
                 f'{self.long_term_summary}\n' \
                 f'\n' \
                 f'Short-term memory:\n' \
                 f'{self.stringify_short_term_memory()}' \
                 f'\n' \
                 f'Write a summary of this chain of thought and events, in the perspective of the GPT system (the THOUGHT/REASONING/PLAN/SPEAK sections). Write it in the perspective of the GPT agent (eg. "I remember ...", "I wanted ..."). Make sure to note any specific things you don\'t want to forget.\n'

        print('SUMMARIZE-PROMPT:')
        print(prompt)

        res = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=256,
            temperature=0.7,
            top_p=1,
            n=1,
        )

        completion = res.choices[0].text
        self.long_term_summary = completion
        self.short_term_events = [last_event]

        print('SUMMARY:')
        print(completion)

    def stringify_goals(self) -> str:
        goals_stringified = 'No goals.\n' if len(self.goals) == 0 else ''

        for goal in self.goals:
            goals_stringified += f'- {goal}\n'

        return goals_stringified

    def stringify_short_term_memory(self) -> str:
        events_stringified = 'No short term events.\n' if len(self.short_term_events) == 0 else ''

        for event in self.short_term_events:
            events_stringified += f'{event.stringify()}\n'

        return events_stringified

    def stringify(self) -> str:
        return f'You are an autonomous GPT agent, capable of thought and reasoning. You are executed every timestep with your immediate short-term memory, and summarized long-term memory.\n' \
               f'Goals:\n' \
               f'{self.stringify_goals()}' \
               f'\n' \
               f'Summarized long-term memory:\n' \
               f'{self.long_term_summary}\n' \
               f'\n' \
               f'Your short-term memory of the past events:\n' \
               f'{self.stringify_short_term_memory()}' \
               f'\n' \
               f'Please note that other entities (such as SYSTEM) can only see and hear what you\'re saying in the SPEAK field.\n' \
               f'Respond with the following format:\n' \
               f'THOUGHT: <your thought>\n' \
               f'REASONING: <your reasoning behind your thought>\n' \
               f'PLAN: <your plan>\n' \
               f'SPEAK: <something you wish to say if anything>\n' \
               f'\n'
