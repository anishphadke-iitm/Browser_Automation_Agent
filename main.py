from mercury_llm import get_actions_from_instruction
from action_executor import execute_actions


def main():

    instruction = input(
        "Enter your browser instruction:\n"
    )

    print("\nGetting plan from Mercury...\n")

    plan = get_actions_from_instruction(
        instruction
    )

    print("Generated Plan:")
    print(plan)

    print("\nExecuting actions...\n")

    execute_actions(plan)


if __name__ == "__main__":
    main()