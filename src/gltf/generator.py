"""
A GLTF 2.0 Generator
"""


class Generator:
    """
    key:    POSITION,   NORMAL,     TEXTURE,    COLOR
    value:  3 Floats,   3 Floats,   2 Floats,   3 Floats
    """

    __slots__ = ["__attributes", "__attribute_order", "__indices", "__json", ]

    # Attribute type names and their floats
    __attribute_types = {
        "POSITION": 3,
        "NORMAL": 3,
        "TEXTURE": 2,
        "COLOR": 3
    }

    # Asset information
    __asset_information = {
        "asset": {
            "version": 2.0,
            "generator": "BigWorldDreams",
        }
    }

    def __init__(self, attribute_order={"POSITION"}):

        # Set up Variables
        self.__attributes = []
        self.__indices = []
        self.__json = {}

        # Validate our passed in attribute order.
        for attribute_type in attribute_order:
            if attribute_type not in self.__attribute_types.keys():
                raise ValueError(
                    f"Attribute types must be {self.__attribute_types.keys()}."
                )

        # Set attribute order
        self.__attribute_order = attribute_order

    def __str__(self):
        """
        Returns the GLTF Json in its current state.
        """
        return f"{self.__json} {self.__indices} {self.__attributes}"

    def add_attribute_sequence(self, attribute_values):
        """
        Adds a sequence of attribute values, based on
        the order of attributes we have.  This is handled
        in a single iteration of the order.
        For example, if you have POSITION, NORMAL in your order
        this method expects 6 Floats and won't go farther.
        """
        if type(attribute_values) not in (list, tuple):
            raise ValueError('Expected attribute values to be list or tuple.')

        # Current attribute value
        current = 0

        # Attribute Dict, we build to compare
        # against existing dicts.
        attribute_dict = {}

        # We iterate our attribute order
        for attribute_type in self.__attribute_order:

            # Create an attribute_type entry
            attribute_dict[attribute_type] = []

            # How many floats we expecting?
            floats_expected = self.__attribute_types[attribute_type]

            # Expected attribute values end
            end = current + floats_expected

            # We have enough floats?
            if end > len(attribute_values):
                raise ValueError("Not enough Floats for attributes!")

            # Iterate our range
            for position in range(current, end):
                attribute_value = attribute_values[position]
                attribute_dict[attribute_type].append(attribute_value)

        # This attribute dict not already exist?
        if attribute_dict not in self.__attributes:
            self.__attributes.append(attribute_dict)
            self.__indices.append(len(self.__indices))
        else:
            self.__indices.append(self.__attributes.index(attribute_dict))
