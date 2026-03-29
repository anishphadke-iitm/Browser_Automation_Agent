from playwright.sync_api import sync_playwright
from mercury_llm import get_actions_from_instruction

def run_agent(instruction):

    llm_response = get_actions_from_instruction(instruction)

    print("LLM Response:")
    print(llm_response)

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # For now — manual example action
        page.goto("https://example.com")

        heading = page.text_content("h1")

        print("Extracted:", heading)

        page.wait_for_timeout(5000)

        browser.close()


if __name__ == "__main__":

    instruction = input("Enter instruction: ")

    run_agent(instruction)