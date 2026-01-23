

class Inference():
    
    def __init__(self, args):
        self.args = args
        self.device = args.device
        self.model_name = args.model_name
        
        self.create_model()
    
    def create_model(self):
        if "llama" in self.model_name:
            from transformers import LlamaForCausalLM, LlamaTokenizer
            self.tokenizer = LlamaTokenizer.from_pretrained(self.model_name)
            self.model = LlamaForCausalLM.from_pretrained(self.model_name).to(self.device)
        