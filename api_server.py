from fastapi import FastAPI
from pydantic import BaseModel

from mercury_llm import get_actions_from_instruction
from action_executor import execute_actions


app = FastAPI()


class InstructionRequest(BaseModel):
    instruction: str


@app.post("/run-agent")

def run_agent(request: InstructionRequest):

    instruction = request.instruction

    print("\nReceived instruction:")
    print(instruction)

    plan = get_actions_from_instruction(
        instruction
    )

    print("\nGenerated plan:")
    print(plan)

    execute_actions(plan)

    return {
        "status": "success",
        "message": "Agent executed instruction"
    }