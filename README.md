# GeePeeTee

A bootleg version of [Auto-GPT](https://github.com/Torantulino/Auto-GPT).

A quick and dirty script to give a GPT model (in this case gpt-3.5-turbo) the capability to have short-term
and long-term memory. Could be expanded to give the agent more functionality, e.g. by giving it
the ability to execute commands.

It works surprisingly well for such simple prompts. However, there are some issues, mainly that the short-term
memory is reset with a summary every 10 events. This should really happen gradually, because now the agent
becomes quite dumb every 10 events.
