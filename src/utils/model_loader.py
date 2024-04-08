"""
model_loader.py

by Wesley R. Elsberry and ChatGPT (GPT-4)

This is a module to aid in handling model metadata for a variety of 
generative AI tasks.

"""

import json
import os
from glob import glob
from transformers import AutoModel, AutoTokenizer
from huggingface_hub import list_models
import simplejson as json

import pprint

def pretty_print_non_json_serializable(obj):
    """
    Attempts to pretty-print the string representation of an object
    that is not JSON serializable, leveraging the object's dictionary
    representation if available.

    Parameters:
    - obj: The object to pretty-print.
    """
    try:
        # Attempt to convert object to a dictionary or use __dict__ if available
        if hasattr(obj, '__dict__'):
            obj_dict = obj.__dict__
        else:
            obj_dict = dict(obj)
        # Pretty print the dictionary representation
        pprint.pprint(obj_dict)
    except (TypeError, ValueError):
        # If conversion fails or is not meaningful, fall back to simple pretty print
        pprint.pprint(obj)

'''
# Example usage
class CustomObject:
    def __init__(self, name, value):
        self.name = name
        self.value = value

# Creating an example custom object
example_obj = CustomObject("Example Name", 123)

# Pretty-printing the custom object
pretty_print_non_json_serializable(example_obj)
'''

def download_model(model_name, destination_dir):
    # Ensure the destination directory exists
    os.makedirs(destination_dir, exist_ok=True)

    # Download and save the model
    model = AutoModel.from_pretrained(model_name)
    model.save_pretrained(destination_dir)
    
    # Download and save the tokenizer associated with the model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.save_pretrained(destination_dir)

'''
# Example usage
model_name = "bert-base-uncased"
destination_dir = "src/models/bert-base-uncased"
download_model(model_name, destination_dir)
'''

class ModelLoader:
    def __init__(self, models_dir='src/models'):
        self.models_dir = models_dir
        self.models_info = self._load_model_metadata()

    def _load_model_metadata(self):
        models_info = {}
        # Existing metadata loading logic...
        return models_info

    def getModelByName(self, name):
        """Retrieve model metadata by name."""
        return self.models_info.get(name)

    def getModelsByTask(self, task):
        """Retrieve models by task, now supporting multiple tasks per model."""
        return {name: info for name, info in self.models_info.items() if task in info.get('tasks', [])}

    def searchModels(self, attributes):
        """Search models by matching attributes, now considering 'tasks' as a list."""
        matched_models = {}
        for name, info in self.models_info.items():
            match = True
            for attr, value in attributes.items():
                if attr == 'tasks':
                    # Special handling for 'tasks' to support list-based searching
                    if not any(task in info.get('tasks', []) for task in value):
                        match = False
                        break
                elif info.get(attr) != value:
                    match = False
                    break
            if match:
                matched_models[name] = info
        return matched_models

    def publish_models(self, destination_dir, task):
        """Publish models for a specific task to a destination directory using symlinks."""
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir, exist_ok=True)

        for model_name, model_info in self.models_info.items():
            if model_info.get('task') == task and model_info.get('publish', False):
                # Construct the path to the model's directory
                model_dir = os.path.join(self.models_dir, model_name)
                dest_model_dir = os.path.join(destination_dir, model_name)

                # Check and create destination model directory
                if not os.path.exists(dest_model_dir):
                    os.makedirs(dest_model_dir, exist_ok=True)

                # Create symlinks for the model files in the destination directory
                for item in os.listdir(model_dir):
                    source_item = os.path.join(model_dir, item)
                    dest_item = os.path.join(dest_model_dir, item)
                    if not os.path.exists(dest_item):  # Check to avoid overwriting existing links
                        os.symlink(source_item, dest_item)

                print(f"Published model '{model_name}' to '{dest_model_dir}' via symlinks.")



class HFHelper(object):
    def __init__(self):
        pass

    def search_models(self, searchterm, searchlimit=None, tags=None):
        if searchlimit in [None, 0]:
            models = [x for x in list_models(search=searchterm)]
        else:
            models = [x for x in list_models(search=searchterm, limit=searchlimit)]
        newmodels = []
        if tags in [None, []]:
            newmodels = models
        else:
            for mi in models:
                found = True
                for ti in tags:
                    if not ti in mi.tags:
                        found = False
                if found:
                    newmodels.append(mi)
        
        return newmodels

    
    
# Example usage
if __name__ == '__main__':
    loader = ModelLoader()

    # Example: Retrieve a model by name
    model_name = 'Example Model Name'
    print(f"Model by name '{model_name}':", loader.getModelByName(model_name))

    # Example: Retrieve models for a specific task
    task = 'text-to-image'
    print(f"Models for task '{task}':", loader.getModelsByTask(task))

    # Example: Search models with specific attributes
    attributes = {'task': 'text-to-image', 'requirements.framework': 'PyTorch'}
    print("Models matching attributes:", loader.searchModels(attributes))

    hfh = HFHelper()
    searchterm = "dolphin"
    tags = ['gguf']
    hfmodels = hfh.search_models(searchterm, tags=tags)
    for hfmi in hfmodels:
        print(pretty_print_non_json_serializable(hfmi))
    
