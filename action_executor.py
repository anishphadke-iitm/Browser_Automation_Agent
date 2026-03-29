from browser_controller import BrowserController


def execute_actions(plan):

    browser = BrowserController()

    url = plan.get("url")

    if url:
        browser.navigate(url)

    actions = plan.get("actions", [])

    for action in actions:

        action_type = action.get("type")

        if action_type == "click":
            browser.click(action["selector"])

        elif action_type == "fill":
            browser.fill(
                action["selector"],
                action["text"]
            )

        elif action_type == "extract":
            browser.extract(
                action["selector"]
            )

        elif action_type == "wait":
            browser.wait(
                action.get("seconds", 2)
            )

    browser.wait(5)
    browser.close()