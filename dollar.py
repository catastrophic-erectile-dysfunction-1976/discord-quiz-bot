def usd(value: str):
    if value[0] == "-":
        new_value = "-" + "$" + f"{int(value[1:]):,}"
    else:
        new_value = "$" + f"{int(value):,}"

    return new_value