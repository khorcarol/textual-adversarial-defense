import datasets

def load_attack_dataset(dataset_name: str):
    if dataset_name == 'sst2':
        dataset = datasets.load_dataset("glue", "sst2")
        attack_set = dataset['validation']
    elif dataset_name == 'mnli':
        dataset = datasets.load_dataset("glue", "mnli")
        attack_set = dataset['validation_matched']
        return attack_set
    elif dataset_name == 'qnli':
        dataset = datasets.load_dataset("glue", "qnli")
        attack_set = dataset['validation']
        attack_set = attack_set.rename_column("question", "premise")
        attack_set = attack_set.rename_column("sentence", "hypothesis")
        return attack_set
    elif dataset_name == 'rte':
        dataset = datasets.load_dataset("glue", "rte")
        attack_set = dataset['validation']
        attack_set = attack_set.rename_column("sentence1", "premise")
        attack_set = attack_set.rename_column("sentence2", "hypothesis")
        return attack_set
    elif dataset_name == 'agnews':
        dataset = datasets.load_dataset("ag_news")
        attack_set = dataset['test']
        attack_set = attack_set.rename_column("text", 'sentence')
        return dataset['test']
    return attack_set

def get_class_num(dataset_name):
    if dataset_name in ['sst2', 'rte', 'qnli']:
        return 2
    elif dataset_name in ['mnli']:
        return 3
    elif dataset_name in ['agnews']:
        return 4