import re


def email_addresses_validator(value):
    """Validator for validating e-mail addresses.
    `value` is a string of carriage-return-seperated bulk of e-mail addresses.
    Returns `True` if all addresses are valid, otherwise `False`.
    """

    expr = re.compile(r"^(\w&.%#$&'\*+-/=?^_`{}|~]+!)*[\w&.%#$&'\*+-/=" +
                      r"?^_`{}|~]+@(([0-9a-z]([0-9a-z-]*[0-9a-z])?" +
                      r"\.)+[a-z]{2,6}|([0-9]{1,3}\.){3}[0-9]{1,3})$",
                      re.IGNORECASE)

    if value is None:
        # empty field is ok
        return True

    addresses = value.strip().split('\n')
    for addr in addresses:
        addr = addr.strip()
        if not expr.match(addr):
            return False
    return True
