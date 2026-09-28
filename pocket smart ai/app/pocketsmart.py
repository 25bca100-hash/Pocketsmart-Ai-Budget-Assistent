def generate_recommendation(category, budget):
    budget = float(budget)

    if category.lower() == "home":
        return (
            f"Your home planning budget is ₹{budget:.2f}. "
            "Consider allocating 50% for essential items, "
            "30% for decoration and 20% as a reserve."
        )

    if category.lower() == "party":
        return (
            f"Your party budget is ₹{budget:.2f}. "
            "Consider allocating 40% for food, 25% for decoration, "
            "20% for entertainment and 15% for emergency expenses."
        )

    if category.lower() == "jewelry":
        return (
            f"Your jewelry budget is ₹{budget:.2f}. "
            "Compare prices from different sellers and keep "
            "a portion of your budget as a reserve."
        )

    return (
        f"Your available budget is ₹{budget:.2f}. "
        "Prioritize essential expenses and keep some money "
        "as savings or emergency funds."
    )
