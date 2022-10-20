from operator import getitem
import pandas as pd
import numpy as np
from algorithm import Naivebayes
import re
import pyttsx3
from os import listdir

#-------------------------------------------
#--------------- Modelling ----------------
#-------------------------------------------


path_data = "./data"
file_names = listdir(path_data)

# 1. Get raw `data`

def get_data(name:str)->list:
    """
    name:str is the name files json in dir `data`

    e.g. `data_product.json`
    """
    assert isinstance(name, str), "name must a str"
    assert name in file_names, "the name of file must be contained in the dir data"
    with open(f'data/{name}', 'r', encoding='utf-8') as data:
        data_list = eval(data.read())
        item = getitem(data_list,0)
        assert item.get('features') and item.get('responses'), "`responses`  and `features` must be keys of the dict"
        assert isinstance(item.get('features'), list), "the value of `features` must be a list"
        # isinstance(item.get('responses'), int)
        assert isinstance(item.get('responses'), (str, int)), "the value of `responses` must be a string"
        return data_list

# 2. Convert data to `dataframe`

def get_frame(name:str):
    """
    name:str is the name files json in dir `data`

    e.g. `data_product.json`
    """
    data_list = get_data(name = name)
    if data_list:
        frame = pd.json_normalize(data_list, record_path='features', meta=["responses"])
        frame.columns = ['features', 'responses']
        resp_categorical = pd.Categorical(frame.responses)

        frame.responses = resp_categorical.codes
        return frame, resp_categorical
    
    else:
        return None

# 3. Training model

def fit_model(data:pd.DataFrame):
    """
    Training Naive Bayes Model 
    ---
    data:pd.DataFrame data must contain the `features` and `responses`
    """
    assert isinstance(data, pd.DataFrame), "the `data` mumst be a `pd.Dataframe`"
    
    X = np.array(data[['features']])
    y = np.array(data['responses'])
    nb = Naivebayes(model='n_gram', n = 2)
    nb.fit(X, y)
            
    return nb

# 4. Speech words

def talk(text:str)->None:
    """
    text:str speech the input text
    """
    speaker = pyttsx3.init()
    speaker.setProperty('rate', 150)
    speaker.say(text)
    speaker.runAndWait()

# 5. Predictions
 
def predict_naive_bayes(text:str, model:Naivebayes,regex:re.Pattern|None=None):

    """
    Prediction using Naive Bayes
    ---
    text: str 
      It is the sentence that we want to predict. e.g. `10 cajas de inca kola mediana`
    model: Naivebayes 
      It is the model already trained
    regex: re.Pattern|None=None 
      It is the pattern. e.g. re.compile(r"(caj\w*|pa[qk]\w*)(?=\sde)")
    """
    
    if regex:
        search = re.search(regex, text)
        
        assert search, "no group matched in %regex"%regex
        text_input = search.group(1)
        
        if text_input.isdigit():
            # return a value tyep string
            return {"value":text_input}
    else :
        text_input = text 
    
    input_array = np.array([[text_input]])
    output_array = model.predict(input_array)
    index = output_array[0]
    # return an index of some class in type `np.int8`
    return {"index":index}

if __name__ == "__main__":
    df, cat = get_frame('data_container.json')
    nb = fit_model(df)
    predict = predict_naive_bayes("2 cajas de pilsen chicas",
    nb,
    re.compile(r"(caj\w*|pa[qk]\w*|bidone.*)(?=\sde)")
    )

    if isinstance(predict.get('index'), np.int8):
        index = predict.get('index')
        # print(cat.categories)
        print(cat.categories[index], index)
    else:
        pass
        # print(predict.get('value'))