import re


def email_addresses_validator(values):
    """Validator for validating e-mail addresses.
    `value` is a string of carriage-return-seperated bulk of e-mail addresses.
    Returns `True` if all addresses are valid, otherwise `False`.
    """

    expr = re.compile(r"^(\w&.%#$&'\*+-/=?^_`{}|~]+!)*[\w&.%#$&'\*+-/=" +
                      r"?^_`{}|~]+@(([0-9a-z]([0-9a-z-]*[0-9a-z])?" +
                      r"\.)+[a-z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$",
                      re.IGNORECASE)

    if not values:
        # empty field is ok
        return True

    for addr in values:
        if not expr.match(addr.strip()):
            return False
    return True
