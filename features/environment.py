def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()


def after_step(context, step):
    if step.status == "failed":
        # Take a screenshot or perform some other error handling/logging
        context.driver.save_screenshot(f"screenshots/{step.name}.png")
