import datasets

def load_attack_dataset(dataset_name: str):
    if dataset_name == 'sst2':
        dataset = datasets.load_dataset("glue", "sst2")
        attack_set = dataset['validation']
    return attack_set

def get_class_num(dataset_name):
    if dataset_name == 'sst2':
        return 2