from utils import *
from data import data

# import motor.motor_asyncio
from pymongo import MongoClient

client =MongoClient('mongodb://localhost:27017')

db = client.robot
collection = db.products

def fetch_one_product(name_product):
    document = collection.find_one({"name_product":name_product})
    return document


def predict_class(text):
    results = {}
    
    for item in data:
        
        name_file = item.get('name_file')
        pattern = item.get('pattern')
        name = item.get('name')
        
        frame, cat = get_frame(name_file)
        
        nb = fit_model(frame)
        predict = predict_naive_bayes(
            text=text, 
            model=nb, 
            regex=pattern
            )
        
        if isinstance(predict.get('index'), np.int8):
            index = predict.get('index')
            results[name] = str(cat.categories[index])
            # print(cat.categories[index], index)
        else:
            results[name] = str(predict.get('value'))
            # print(predict.get('value'))
    

    name_product = results['name_product']
    # connect with MongoDB
    product_doc = fetch_one_product(name_product)
    results['price'] = product_doc.get("price")
    results['amount'] = float(results['price'])*float(results['quantity'])
    results['amount'] = str(results['amount'])
    return results

if __name__ == "__main__":
    print(predict_class("una caja de pilsen chica"))