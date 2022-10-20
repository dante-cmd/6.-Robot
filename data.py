import re

data = [
    {
        "name": "quantity",
        "pattern": re.compile(r"(\w+|\d+)(?=\scaj\w*|pa[qk]\w*)"),
        "name_file":"data_number.json"
    },
    {
        "name": "container",
        "pattern": re.compile(r"(caj\w*|pa[qk]\w*)(?=\sde)"),
        "name_file":"data_container.json"
    },
    {
        "name":
        "name_product",
        "pattern":
        re.compile(r"\w+\s(?:caj\w*|pa[qk]\w*)[.,:; ]{1}de[.,:; ]{1}(.+)"),
        "name_file":"data_product.json"
    }
]
