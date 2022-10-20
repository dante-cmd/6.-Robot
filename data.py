import re

data = [{
    "name": "quantity",
    "pattern": re.compile(r"(\w+|\d+)(?=\scaj\w*|pa[qk]\w*)"),
    "name_file": "data_number.json"
}, {
    "name": "container",
    "pattern": re.compile(r"(caj\w*|pa[qk]\w*)(?=\sde)"),
    "name_file": "data_container.json"
}, {
    "name":
    "name_product",
    "pattern":
    re.compile(r"\w+\s(?:caj\w*|pa[qk]\w*)[.,:; ]{1}de[.,:; ]{1}(.+)"),
    "name_file":
    "data_product.json"
}]

if __name__ == "__main__":
    print('dd')
#     import motor.motor_asyncio

# client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

# db = client.robot
# collection = db.products


# async def fetch_one_product(name_product):
#     document = await collection.find_one({"name_product": name_product})
#     return document
#     loop = client.get_io_loop()
#     product_doc = loop.run_until_complete(
#         fetch_one_product("Inca Kola 1lt. x12 vidrio"))
#     pprint(product_doc.get("price"))
