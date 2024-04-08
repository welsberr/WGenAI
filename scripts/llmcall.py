"""
llmcall.py

Wesley R. Elsberry

Package to assist in making command lines to call an LLM to do a task.

Initial work done to manage calls to Llamafile or GGUF LLM weghts
using Llamafile. Aiming to make this more generic over time.

Usage in programs:

import llmcall
from llmcall import llm_info, llms, make_llm_cmd, call_llm_process, read_file

"""

import sys
import os
import traceback
import glob
import time
import random
import tempfile
import chardet

import unicodedata


"""


# Create a temporary file
with tempfile.TemporaryFile() as tmp_file:
    # Write a string to the file
    tmp_file.write(b"This is a test string.")
    
    # Get the name of the file
    file_name = tmp_file.name
    
# Print the name of the file
print("File Name:", file_name)


# codellama
LLM_CODELLAMA_GGUF=codellama-7b-instruct.Q6_K.gguf
# deepseek
LLM_DEEPSEEK_GGUF=deepseek-coder-6.7b-instruct.Q5_K_M.gguf
# yarnmistral
LLM_YARNMISTRAL_GGUF=flexingd-yarn-mistral-7b-65k-instruct-ggml-model-q5_k.gguf
# mixtralinstruct
LLM_MIXTRALINSTRUCT_GGUF=mixtral-8x7b-instruct-v0.1.Q5_K_M.gguf
# mixtral
LLM_MIXTRAL_GGUF=mixtral-8x7b-v0.1.Q5_K_M.gguf
# phindcodellama
LLM_PHINDCODELLAMA_GGUF=phind-codellama-34b-python-v1.Q5_K_M.gguf
# starcoder
LLM_STARCODER_GGUF=starcoder-ggml-model-q4_0.gguf
# yarnmistral
LLM_YARNMISTRAL_GGUF=yarn-mistral-7b-128k.Q6_K.gguf

# llava
LLM_LLAVA_LF=llava-v1.5-7b-q4-main.llamafile
# llavas 
LLM_LLAVA_LFS=llava-v1.5-7b-q4-server.llamafile
# mistrallf
LLM_MISTRAL_LF=mistral-7b-instruct-v0.2.Q5_K_M.llamafile
# ohi2
LLM_PHI2_LF=phi-2.Q5_K_M.llamafile
# rocket
LLM_ROCKET_LF=rocket-3b.Q5_K_M.llamafile
# wizardcoder
LLM_WIZARDCODER_LF=wizardcoder-python-13b.llamafile


codebooga-34b-v0.1.Q5_K_M.gguf
codellama-13b-instruct.Q5_K_M.gguf
codellama-7b-instruct.Q6_K.gguf
deepseek-coder-6.7b-instruct.Q5_K_M.gguf
dolphin-2.7-mixtral-8x7b.Q5_K_M.gguf
flexingd-yarn-mistral-7b-65k-instruct-ggml-model-q5_k.gguf
mixtral-8x7b-instruct-v0.1.Q5_K_M.gguf
mixtral-8x7b-v0.1.Q5_K_M.gguf
phind-codellama-34b-python-v1.Q5_K_M.gguf
starcoder-ggml-model-q4_0.gguf
yarn-mistral-7b-128k.Q6_K.gguf



"""

"""
llm_info is a dict structure to hold needed information
on LLMs known to this package. So far, this is my ad hoc
collection based on what I have downloaded as model
weights.
"""
llm_info = {
    # codebooga-34b-v0.1.Q5_K_M.gguf
    "codebooga": {
        "modelprops": {
            "type": "",
            "format": "GGUF",
            "file": "codebooga-34b-v0.1.Q5_K_M.gguf",
            "maxcontext": 32768, 
            "context": 32768,
        },
        "prompting": {
            "inference_template": """### Instruction:
{SYSTEMPROMPT}

{PROMPT}

### Response:
 """,
            "chat_completion_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "inference_ref": "",
            "chat_completion_ref": "",
        }
    },
    
    "codellama": {
        "modelprops": {
            "type": "",
            "format": "GGUF",
            "file": "codellama-7b-instruct.Q6_K.gguf",
            "maxcontext": 2048,
            "context": 2048,
        },
        "prompting": {
            "inference_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "chat_completion_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "inference_ref": "",
            "chat_completion_ref": "",
        }
    },
    
    "codellama13b": {
        "modelprops": {
            "type": "",
            "format": "GGUF",
            "file": "codellama-13b-instruct.Q6_K_M.gguf",
            "maxcontext": 2048,
            "context": 2048,
        },
        "prompting": {
            "inference_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "chat_completion_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "inference_ref": "",
            "chat_completion_ref": "",
        }
    },

    "deepseek": {
        "modelprops": {
            "type": "",
            "format": "GGUF",
            "file": "deepseek-coder-6.7b-instruct.Q5_K_M.gguf",
            "maxcontext": 2048,
            "context": 2048,
        },
        "prompting": {
            "inference_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "chat_completion_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "inference_ref": "",
            "chat_completion_ref": "",
        }
    },
    "flexingdyarnmistral": {
        "modelprops": {
            "type": "instruct",
            "format": "GGUF",
            "file": "flexingd-yarn-mistral-7b-65k-instruct-ggml-model-q5_k.gguf",
            "maxcontext": 2048,
            "context": 2048,
        },
        "prompting": {
            "inference_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "chat_completion_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "inference_ref": "",
            "chat_completion_ref": "",
        }
    },
    "mixtralinstruct": {
        "modelprops": {
            "type": "instruct",
            "format": "GGUF",
            "file": "mixtral-8x7b-instruct-v0.1.Q5_K_M.gguf",
            "maxcontext": 32768,
            "context": 32768,
        },
        "prompting": {
            "inference_template": """[INST] {SYSTEMPROMPT}\n{PROMPT} [/INST]""",
            "chat_completion_template": """
            [
            {"role": "system", "content": "{SYSTEMPROMPT}"},
            {
            "role": "user",
            "content": "{PROMPT}"
            }
            ]""",
            "inference_ref": """
# Simple inference example
output = llm(
  "[INST] {prompt} [/INST]", # Prompt
  max_tokens=512,  # Generate up to 512 tokens
  stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
  echo=True        # Whether to echo the prompt
)

            )""",
            "chat_completion_ref": """
# Chat Completion API

llm = Llama(model_path="./mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf", chat_format="llama-2")  # Set chat_format according to the model you are using
llm.create_chat_completion(
    messages = [
        {"role": "system", "content": "You are a story writing assistant."},
        {
            "role": "user",
            "content": "Write a story about llamas."
        }
    ]

            """,
        }
    },
    "mixtral": {
        "modelprops": {
            "type": "chat",
            "format": "GGUF",
            "file": "mixtral-8x7b-v0.1.Q5_K_M.gguf",
            "maxcontext": 32768,
            "context": 32768,
        },
        "prompting": {
            "inference_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "chat_completion_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "inference_ref": "",
            "chat_completion_ref": "",
        }
    },
    "phindcodellama": {
        "modelprops": {
            "type": "",
            "format": "GGUF",
            "file": "phind-codellama-34b-python-v1.Q5_K_M.gguf",
            "maxcontext": 2048,
            "context": 2048,
        },
        "prompting": {
            "inference_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "chat_completion_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "inference_ref": "",
            "chat_completion_ref": "",
        }
    },
    "starcoder": {
        "modelprops": {
            "type": "",
            "format": "GGUF",
            "file": "starcoder-ggml-model-q4_0.gguf",
            "maxcontext": 2048,
            "context": 2048,
        },
        "prompting": {
            "inference_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "chat_completion_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "inference_ref": "",
            "chat_completion_ref": "",
        }
    },
    "yarnmistral": {
        "modelprops": {
            "type": "",
            "format": "GGUF",
            "file": "yarn-mistral-7b-128k.Q6_K.gguf",
            "maxcontext": 2048,
            "context": 2048,
        },
        "prompting": {
            "inference_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "chat_completion_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "inference_ref": "",
            "chat_completion_ref": "",
        }
    },
    "llava": {
        "modelprops": {
            "type": "",
            "format": "llamafile",
            "file": "llava-v1.5-7b-q4-main.llamafile",
            "maxcontext": 2048,
            "context": 2048,
        },
        "prompting": {
            "inference_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "chat_completion_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "inference_ref": "",
            "chat_completion_ref": "",
        }
    },
    "llavas": {
        "modelprops": {
            "type": "",
            "format": "llamafile",
            "file": "llava-v1.5-7b-q4-server.llamafile",
            "maxcontext": 2048,
            "context": 2048,
        },
        "prompting": {
            "inference_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "chat_completion_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "inference_ref": "",
            "chat_completion_ref": "",
        }
    },
    "mistrallf": {
        "modelprops": {
            "type": "instruct",
            "format": "llamafile",
            "file": "mistral-7b-instruct-v0.2.Q5_K_M.llamafile",
            "maxcontext": 2048,
            "context": 2048,
        },
        "prompting": {
            "inference_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "chat_completion_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "inference_ref": "",
            "chat_completion_ref": "",
        }
    },
    "phi2": {
        "modelprops": {
            "type": "",
            "format": "llamafile",
            "file": "phi-2.Q5_K_M.llamafile",
            "maxcontext": 2048,
            "context": 2048,
        },
        "prompting": {
            "inference_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "chat_completion_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "inference_ref": "",
            "chat_completion_ref": "",
        }
    },
    "rocket": {
        "modelprops": {
            "type": "",
            "format": "llamafile",
            "file": "rocket-3b.Q5_K_M.llamafile",
            "maxcontext": 2048,
            "context": 2048,
        },
        "prompting": {
            "inference_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "chat_completion_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "inference_ref": "",
            "chat_completion_ref": "",
        }
    },
    "wizardcoder": {
        "modelprops": {
            "type": "",
            "format": "llamafile",
            "file": "wizardcoder-python-13b.llamafile",
            "maxcontext": 2048,
            "context": 2048,
        },
        "prompting": {
            "inference_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "chat_completion_template": """System: {SYSTEMPROMPT} User: {PROMPT} """,
            "inference_ref": "",
            "chat_completion_ref": "",
        }
    },

    
    "dolphinmixtral": {
        "modelprops": {
            "type": "instruct",
            "format": "GGUF",
            "file": "",
            "maxcontext": 32768,
            "context": 32768,
            },
        "prompting": {
            "inference_ref": """
# Simple inference example
output = llm(
  "<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant", # Prompt
  max_tokens=512,  # Generate up to 512 tokens
  stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
  echo=True        # Whether to echo the prompt
)
            """,
            "inference_template": """<|im_start|>system\n{{SYSTEMPROMPT}}<|im_end|>\n<|im_start|>user\n{{PROMPT}}<|im_end|>\n<|im_start|>assistant""",
            "chatcompletion_ref": """
# Chat Completion API

llm = Llama(model_path="./dolphin-2.7-mixtral-8x7b.Q4_K_M.gguf", chat_format="llama-2")  # Set chat_format according to the model you are using
llm.create_chat_completion(
    messages = [
        {"role": "system", "content": "You are a story writing assistant."},
        {
            "role": "user",
            "content": "Write a story about llamas."
        }
    ]
)
            """,
            "chatcompletion_template": """[
            {"role": "system", "content": "{SYSTEMPROMPT"},
            {
            "role": "user",
            "content": "{PROMPT}"
            }
            ]""",
        }
    },
}



llms = sorted(list(llm_info.keys()))


def make_llm_cmd(calltype="llamafile-cli", llmalias=None, llminfo=None, sysprompt="", prompt="", temp="0", gpulayers="35", gpusplit="4,8"):

    modeldir = "/home/netuser/bin"
    llamafilefn = "llamafile"
    
    if calltype in ["llamafile-cli"]: # --------------------------

        params = {
            "LLAMAFILE": llamafilefn,
            "LLM": str(llminfo['modelprops']['file']),
            "GGUFDIR": modeldir,
            "C_SIZE": str(llminfo['modelprops']['context']),
            "TMPFILE": "",
            "SYSTEMPROMPT": sysprompt,
            "PROMPT": prompt,
            "TEMP": str(temp),
            # "VERBOSE": "--verbose",
            "VERBOSE": "",
        }
        if 0 < int(gpulayers):
            params['NGL'] = f"-ngl {str(gpulayers)}"
            params['TS'] = f"-ts {str(gpusplit)}"
        else:
            params['NGL'] = "" # No GPU offloading
            params['TS'] = ""  # No tensor split

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            # Get the name of the file
            tmpfile_name = tmp_file.name
            print('tmpfile', tmpfile_name)
            print(tmp_file)
            params['TMPFILE'] = tmpfile_name
            pstr = llminfo['prompting']['inference_template'].format(**params)
            # Write a string to the file
            tmp_file.write(bytes(pstr, "utf-8"))
        
        
        call_template = """{LLAMAFILE} --cli -m {GGUFDIR}/{LLM} --silent-prompt 2>/dev/null --temp {TEMP} {NGL} -c {C_SIZE} {TS} -f {TMPFILE} {VERBOSE}"""
        llmcmd = call_template.format(**params)
        pass
    elif calltype in ["llamafile-server"]: # -------------------------
        call_template = """{LLAMAFILE} --server -m ${GGUFDIR}/${LLM} --silent-prompt 2>/dev/null --temp 0 -ngl 33 -c {C_SIZE} -ts 4,7 -f $TMPFILE {VERBOSE} """
        pass
    else:
        print(f"Unrecognized calltype {calltype}")

    return llmcmd

def call_llm_process(llm=None, sysprompt=None, prompt=None, redirectfn=None,
                     redirectoverride=False, fn=None):
    if llm in [None, '']:
        llm = random.choice(list(llm_info.keys()))

    llminfo = llm_info.get(llm,"flexingdyarnmistral") # default to FLexingd Yarn Mistral

    redirectname = ""
    redirect = ""
    if redirectfn in [None, "", '']:
        print("No redirectfn")
        pass
    elif not os.path.exists(redirectfn) or redirectoverride:
        redirect = f" > '{redirectfn}'"
    
    llmcmd = make_llm_cmd(llmalias=llm, llminfo=llminfo,
                          sysprompt=sysprompt,
                          prompt=prompt)

    if not os.path.exists(redirectfn) or redirectoverride:
        # No redirectfn, so do the translate
        cmd = llmcmd + f" {redirect}"
        print(cmd)
        os.system(cmd)
        print(f"{redirectfn}: -> {redirectfn} done with {llm}.")
    else:
        print(f"{redirectfn}: File {redirectfn} already exists, skipping.")

"""
If the source code has ^Z in it, the program terminates 
without producing anything. So the following routine from
StackOverflow is supposed to filter out control characters.

https://stackoverflow.com/a/19016117
"""
def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def find_encoding(fn, sample_size=32768):
    # First, read the file in binary mode to detect its encoding
    with open(fn, 'rb') as file:
        raw_data = file.read(sample_size)
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        

    # Now, read the file with the detected encoding
    # with open('yourfile', 'r', encoding=encoding) as file:
    #     file_contents = file.read()
    print(f"{encoding=}")
    return encoding

def read_file(file):
    """Reads in contents of given file to a single string"""
    with open(file, mode='r', encoding=find_encoding(file)) as f:
        contents = remove_control_characters(f.read())
    return contents

if __name__ == "__main__":

    pass
