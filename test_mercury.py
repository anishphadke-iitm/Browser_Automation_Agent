from mercury_llm import get_actions_from_instruction

instruction = "Go to example.com and extract the heading"

actions = get_actions_from_instruction(instruction)

print(actions)