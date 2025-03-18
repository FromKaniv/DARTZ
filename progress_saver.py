import os
import pickle

def save_progress(name, engine):
    try:
        os.remove('saves//'+name)
    except FileNotFoundError:
        pass
    
    file = open('saves//'+name, 'ab')
    pickle.dump(engine, file)
    file.close()

def load_progress(name):
    with open('saves//'+name, 'rb') as file:
        return pickle.load(file)
