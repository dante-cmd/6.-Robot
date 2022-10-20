from utils import *
from data import data
from pymongo import MongoClient

client =MongoClient('mongodb://localhost:27017')

db = client.robot
collection = db.products

def fetch_one_product(name_product):
    document = collection.find_one({"name_product":name_product})
    return document


def predict_class(text):
    results = {}
    pattern = pattern_search(text=text)
    
    for item in data:
        
        name_file = item.get('name_file')
        name = item.get('name')
        text_input = pattern.group(name)
        # pattern = item.get('pattern')
        
        
        frame, cat = get_frame(name_file)
        
        nb = fit_model(frame)
        predict = predict_naive_bayes(
            text=text_input, 
            model=nb
            )
        if predict:
            if isinstance(predict.get('index'), np.int8):
                index = predict.get('index')
                results[name] = str(cat.categories[index])
                # print(cat.categories[index], index)
            else:
                results[name] = str(predict.get('value'))
                # print(predict.get('value'))
        else :
            results['container'] = None
    

    name_product = results['name_product']
    # connect with MongoDB
    product_doc = fetch_one_product(name_product)
    # print(product_doc, results)
    if not results.get('container'):
        results['container'] = product_doc.get("container")

    results['price'] = product_doc.get("price")
    results['amount'] = float(results['price'])*float(results['quantity'])
    results['amount'] = str(results['amount'])
    return results

if __name__ == "__main__":
    print(predict_class("una caja de pilsen chica"))