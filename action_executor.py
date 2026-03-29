from browser_controller import BrowserController


def execute_actions(plan):

    browser = BrowserController()

    results = []

    try:

        url = plan.get("url")

        if url:
            browser.navigate(url)

        actions = plan.get("actions", [])

        for action in actions:

            action_type = action.get("type")

            if action_type == "click":

                browser.click(
                    action["selector"]
                )

            elif action_type == "fill":

                browser.fill(
                    action["selector"],
                    action["text"]
                )

            elif action_type == "extract":

                text = browser.extract(
                    action["selector"]
                )

                # Save extracted result
                results.append({
                    "selector": action["selector"],
                    "value": text
                })

            elif action_type == "wait":

                browser.wait(
                    action.get("seconds", 2)
                )

        browser.wait(5)

        return results

    finally:

        browser.close()