import typer, yaml, json
from tabulate import tabulate
#from nlu import extract_order
from openAPI import extract_order
from pydantic import ValidationError
from order import OrderMerge
from db import save_order, init_db

app = typer.Typer()


def load_menu():
    with open("menu.yaml") as f:
        return yaml.safe_load(f)

def price_cart(menu, draft):
    total = 0.0
    lines = []
    for it in draft.items:
        # validate
        cat = it.category
        assert cat in ("pizza","side","drink")
        m = menu["pizzas" if cat=="pizza" else ("sides" if cat=="side" else "drinks")]
        assert it.name in m, f"Unknown item {it.name}"
        # size
        if it.size not in m[it.name]:
            raise AssertionError(f"Size missing/invalid for {it.name}. Options: {list(m[it.name])}")
        base = float(m[it.name][it.size])
        toppings_cost = sum(float(menu["toppings"].get(t, 0)) for t in it.toppings) if cat=="pizza" else 0.0
        line_total = (base + toppings_cost) * it.qty
        total += line_total
        lines.append([it.qty, f"{it.size} {it.name}", ", ".join(it.toppings) or "-", f"{line_total:.2f}"])
    return lines, total


@app.command()
def chat():
    init_db()
    menu = load_menu()
    menu_text = json.dumps(menu)  # compact for prompt
    typer.echo("👋 Welcome to Local Order Bot! Type 'quit' to exit.\n")
    cart = None
    while True:
        user = typer.prompt("You")
        if user.strip().lower() in {"quit","exit"}:
            break
        try:
            draft = extract_order(user, menu_text)
        except (ValidationError, AssertionError, json.JSONDecodeError) as e:
            typer.echo(f"🤖 Sorry, I couldn't parse that. Please rephrase. ({e})")
            continue
        # Merge into cart (simple replace for MVP)
        cart = draft if cart is None else OrderMerge.merge(cart, draft)  # implement simple merge or just replace
        # Show current cart & ask for missing slots
        try:
            lines, total = price_cart(menu, cart)
            typer.echo(tabulate(lines, headers=["qty","item","toppings","$"], tablefmt="github"))
            if cart.service not in ("pickup","delivery"):
                cart.service = typer.prompt("Pickup or delivery?", default="pickup")
            if cart.service=="delivery" and not cart.address:
                cart.address = typer.prompt("Delivery address")
            confirm = typer.confirm(f"Confirm order (total ${total:.2f})?")
            if confirm:
                payload = cart.model_dump()
                save_order(json.dumps(payload), total)
                typer.echo("✅ Order placed. Thank you!")
                break
        except AssertionError as e:
            typer.echo(f"🤖 {e}")

if __name__ == "__main__":
    app()
