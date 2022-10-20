from utils import *
from data import data

prices = {'Pilsen Lt. x12 vidrio': "78.5", 'Pilsen 630ml. x12 vidrio': "59.0", 'Inca Kola 296ml. x24 vidrio':"27.0"}

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
    results['price'] = prices[results['name_product']]
    results['amount'] = float(results['price'])*float(results['quantity'])
    results['amount'] = str(results['amount'])
    return results

if __name__ == "__main__":
    print(predict_class("10 caja de pilsen chica"))