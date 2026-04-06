import gradio as gr

# Table of dosage ranges
table = [
    (0, 11, "ask a doctor for appropriate dose"),
    (12, 17, "1 mL"),
    (18, 23, "1.5 mL"),
    (24, 35, "5 mL"),
    (36, 47, "7.5 mL"),
    (48, 59, "10 mL"),
    (60, 71, "12.5 mL"),
    (72, 95, "15 mL"),
]

# State
state = {
    "low": 0,
    "high": len(table)-1,
    "mid": None,
    "target": None,
    "done": False,
    "found": False  # To track if we actually found the correct range or just ran out of bounds
}

# Renders dosage table with color coding based on current state


def render_table():
    html = "<table border='1' style='border-collapse: collapse; width:100%; text-align:center;'>"
    html += "<tr><th>Weight Range</th><th>Dosage</th></tr>"

    for i, (low, high, dose) in enumerate(table):
        color = ""

        # Discarded (RED)
        if i < state["low"] or i > state["high"]:
            color = "background-color: #ffcccc;"

        # Current guess (YELLOW)
        if state["mid"] == i and not state["done"]:
            color = "background-color: #fff3cd;"

        # Correct (only if found) (GREEN)
        if state["done"] and state["found"] and state["mid"] == i:
            color = "background-color: #ccffcc;"

        # If done but NOT found (out-of-bounds) (RED)
        if state["done"] and not state["found"] and state["mid"] == i:
            color = "background-color: #ffcccc;"

        html += f"<tr style='{color}'><td>{low}-{high} lbs</td><td>{dose}</td></tr>"

    html += "</table>"
    return html


def start_game(weight):
    weight = int(weight)
    state["low"] = 0
    state["high"] = len(table)-1
    state["done"] = False
    state["found"] = False  # reset found status at the start of a new game
    state["target"] = weight
    state["mid"] = (state["low"] + state["high"]) // 2

    low, high, _ = table[state["mid"]]

    return (
        f"My current guess is {low}-{high} lbs.",
        gr.update(visible=True),
        gr.update(visible=True),
        gr.update(visible=True),
        render_table()
    )


def make_guess(direction):
    if state["done"]:
        return (
            "Game over! Refresh to play again.",
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            render_table()
        )

    mid_low, mid_high, mid_dose = table[state["mid"]]
    target = state["target"]

    # force DONE if already correct
    if mid_low <= target <= mid_high and direction != "DONE":
        return (
            f"You're already in the correct range {mid_low}-{mid_high} lbs!\nPress DONE.",
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(visible=True),
            render_table()
        )

    if direction == "LEFT":
        if target < mid_low:
            state["high"] = state["mid"] - 1
        else:
            return (
                f"Wrong! {target} ≥ {mid_low}, go RIGHT.",
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=True),
                render_table()
            )

    elif direction == "RIGHT":
        if target > mid_high:
            state["low"] = state["mid"] + 1
        else:
            return (
                f"Wrong! {target} ≤ {mid_high}, go LEFT.",
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=True),
                render_table()
            )

    elif direction == "DONE":
        if mid_low <= target <= mid_high:
            state["done"] = True
            state["found"] = True  # mark as actually found
            return (
                f"Correct! {target} lbs is in {mid_low}-{mid_high} lbs.\nDose: {mid_dose}",
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                render_table()
            )
        else:
            return (
                f"Not in this range. Try again.",
                gr.update(visible=True),
                gr.update(visible=True),
                gr.update(visible=True),
                render_table()
            )

    # Next step
    if state["low"] > state["high"]:
        state["done"] = True
        state["found"] = False  # out of bounds
        return (
            "The weight is out of bounds! No valid dosage range found.",
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            render_table()
        )

    state["mid"] = (state["low"] + state["high"]) // 2
    mid_low, mid_high, _ = table[state["mid"]]

    return (
        f"My current guess is {mid_low}-{mid_high} lbs.",
        gr.update(visible=True),
        gr.update(visible=True),
        gr.update(visible=True),
        render_table()
    )


# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# Child Tylenol Dosage Assistant (Binary Search Simulation)")
    gr.Markdown("## How it works")
    gr.Markdown("""When giving Tylenol to a child, the correct dosage depends on their weight, so instead of checking every possible range manually, this simulation lets you act as the decision-maker while the computer uses binary search to quickly narrow down the correct dosage range.
                
                1. Enter a child's weight (in pounds) to begin 
                2. The computer will guess a weight range
                3. Use:
                   - LEFT if the child's weight is less than the guessed range
                   - RIGHT if the child's weight is greater than the guessed range
                   - DONE if the guessed range is correct
                
                The table on the right visually represent the Binary Search Process: RED shows discarded ranges, YELLOW shows current guess, and GREEN shows the correct range once found.""")

    with gr.Row():
        # Left side: Inputs and feedback
        with gr.Column():
            weight_input = gr.Number(label="Enter weight (lbs)")
            start_btn = gr.Button("Start")
            output = gr.Textbox(label="Computer Says", interactive=False)

            left_btn = gr.Button("⬅ LEFT", visible=False)
            right_btn = gr.Button("➡ RIGHT", visible=False)
            done_btn = gr.Button("✔ DONE", visible=False)

        # Right side: Dosage Table
        with gr.Column():
            gr.Markdown(
                "<div style='text-align: center;'><h2>Dosage Table</h2></div>")
            table_display = gr.HTML(render_table())

# Gradio Buttons
    start_btn.click(start_game,
                    inputs=weight_input,
                    outputs=[output, left_btn, right_btn, done_btn, table_display])

    left_btn.click(make_guess,
                   inputs=gr.State("LEFT"),
                   outputs=[output, left_btn, right_btn, done_btn, table_display])

    right_btn.click(make_guess,
                    inputs=gr.State("RIGHT"),
                    outputs=[output, left_btn, right_btn, done_btn, table_display])

    done_btn.click(make_guess,
                   inputs=gr.State("DONE"),
                   outputs=[output, left_btn, right_btn, done_btn, table_display])

demo.launch()
