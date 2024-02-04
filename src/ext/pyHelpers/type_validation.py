"""
type_validation.py
"""


def type_validation(vars, types):
    """
    List or Var
    List or Type

    We can pass in a List and a single Type
        [1, "hey"]
        string

    We can pass in a List and a List
        [1, "hey"]
        [int, string]

    We can pass a List of Lists
        [1, "hey"]
        [[int, float], string]
    """

    def __comparitor(v, t):
        if not isinstance(v, t):
            raise ValueError(f"{type(v)} must be of type {t}")

    # Two Lists Passed in
    if isinstance(vars, list) and isinstance(types, list):
        if len(vars) != len(types):
            raise ValueError(
                "Type Validation requires vars and types to be the same length."
            )
        else:
            for i in range(len(vars)):
                type_validation(vars[i], types[i])

    # Vars is a list, Types is not
    elif isinstance(vars, list):
        for var in vars:
            __comparitor(var, types)

    # Types is a list, Vars is not
    elif isinstance(types, list):
        __comparitor(vars, tuple(types))

    # Neither are a list
    elif not isinstance(vars, list) and not isinstance(types, list):
        __comparitor(vars, types)

    # Something went wrong
    else:
        raise ValueError("Error validating.")
