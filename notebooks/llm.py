import json

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig


class LlmHelper:
    def __init__(self, hf_model_name):
        self.hf_model_name = hf_model_name
        self.tokenizer = None
        self.model = None
        self.set_up_tokenizer()
        self.set_up_model()
        self.set_up_model_config()
        self.short_name = hf_model_name.split("/")[-1].replace("-", "_").lower()

    def set_up_tokenizer(self):
        print("set up tokenizer...", end=" ")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.hf_model_name,
            use_fast=False,
            trust_remote_code=True
        )
        print("✅")

    def set_up_model(self):
        print("set up AutoModelForCausalLM...", end=" ")
        self.model = AutoModelForCausalLM.from_pretrained(
            self.hf_model_name,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True
        )
        print("✅")

    def set_up_model_config(self):
        print("GenerationConfig...", end=" ")
        self.model.generation_config = GenerationConfig.from_pretrained(
            self.hf_model_name,
            max_new_tokens=4000,
            temperature=1
        )
        print("✅")

    def sample_task(self):
        messages = []
        user_prompt = "自我介绍"
        if self.hf_model_name == "baichuan-inc/Baichuan2-7B-Chat":
            messages.append({"role": "user", "content": user_prompt})
            response = self.model.chat(self.tokenizer, messages)
        if self.hf_model_name == "Qwen/Qwen-7B-Chat":
            response = self.model.chat(self.tokenizer, user_prompt, history=None)[0]
        print(response)
        return response

    def inference(self, system_prompt, user_prompt):
        messages = []
        messages.append({"role": "system", "content": system_prompt})
        if self.hf_model_name == "baichuan-inc/Baichuan2-7B-Chat":
            messages.append({"role": "user", "content": user_prompt})
            response = self.model.chat(self.tokenizer, messages)
        if self.hf_model_name == "Qwen/Qwen-7B-Chat":
            response = self.model.chat(self.tokenizer, user_prompt, history=messages)
        return response

    def inference(self, system_prompt=None, user_prompt=None):

        if self.hf_model_name == "Qwen/Qwen-7B-Chat":

            response, history = self.model.chat(self.tokenizer, system_prompt, history=None)

            response, history = self.model.chat(self.tokenizer, user_prompt, history=history)

            return response

        if self.hf_model_name == "baichuan-inc/Baichuan2-7B-Chat":
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            if user_prompt:
                messages.append({"role": "user", "content": user_prompt})
            response = self.model.chat(self.tokenizer, messages)

            return response