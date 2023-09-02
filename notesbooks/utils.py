import json
import os
# os.environ["LLAMA_CPP_LIB"] = "/home/brian/github/llama.cpp/libllama.so"
from llama_cpp import Llama, Completion, LlamaTokenizer


def translate_paragraph(text, llm, use_example=None, method=None, translate_to=None):
    """
    Translation function that supports Completion and ChatCompletion for Chinese-LLaMA-2
    """
    model_path = "/home/brian/github/llama.cpp/models/7B/Chinese-Alpaca-2/ggml-model-q4_0.bin"

    # ChatCompletion
    system_prompt="Translate from Chinese to English, only reply in English 把中文翻译成英文，只用英文回答问题"
    n_ctx = 4096

    if translate_to == "EN":
        completion_prompt = f"### Chinese:\n你好\n\n### English:\nHello\n\n### Chinese:\n${text}\n\n### English:\n"
    elif translate_to == "CN":
        completion_prompt = f"n### English:\nHello\n\n### Chinese:\n你好\n\### English:\n${text}\n\n### Chinese:\n"
    else:
        raise Exception("Must include a target_to langauge: EN or CN")
    stop = ["\n","###"]
    response = llm.create_completion(max_tokens=5000,model=model_path, prompt=completion_prompt, stop=stop)
    print(text)
    print(response["choices"][0]["text"])
    return response