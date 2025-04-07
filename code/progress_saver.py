import os
import pickle

def save_progress(name, engine):
    try:
        saves_dir = os.path.join(os.path.dirname(os.getcwd()), 'saves')
        
        file_path = os.path.join(saves_dir, name)
        os.remove(file_path)
    except FileNotFoundError:
        pass

    os.makedirs(saves_dir, exist_ok=True)

    with open(file_path, 'ab') as file:
        pickle.dump(engine, file)

def load_progress(name):
    with open('.saves//'+name, 'rb') as file:
        return pickle.load(file)
