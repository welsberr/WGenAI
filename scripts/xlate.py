#!/home/netuser/bin/mambaforge/bin/python

import sys
import os
import traceback
import glob
import time
import random
import tempfile

import llmcall
from llmcall import llm_info, llms, make_llm_cmd, call_llm_process, read_file

from multiglob import find_files


langinfo = {
    "Python 2": {
        "srcpat": "*.py",
        "destext": ".py",
        "srctag": "PYTHON2",
        "sysprompt_extra_dest": """You use the Click package for commond-line parameters, type hinting in function and method declarations, docstrings, and extensive comments.""",
        },
    "Python 3": {
        "srcpat": "*.py",
        "destext": ".py",
        "srctag": "PYTHON3",
        "sysprompt_extra_dest": """You use the Click package for commond-line parameters, the pysimplegui package for user interfaces, type hinting in function and method declarations, docstrings, and extensive comments. You use PySimpleGUI for GUI interfaces by preference. Enclose calls to external sources in try .. except blocks.""",
        },
    "MATLAB": {
        "srcpat": "*.m",
        "destext": ".m",
        "srctag": "MATLAB",
        },
    "Javascript": {
        "srcpat": "*.js",
        "destext": ".js",
        "srctag": "JAVASCRIPT",
        },
    "Perl": {
        "srcpat": "*.pl",
        "destext": ".pl",
        "srctag": "PERL",
        },
    "C": {
        "srcpat": "*.c",
        "destext": ".c",
        "srctag": "C",
        },
    "C headers": {
        "srcpat": "*.h",
        "destext": ".h",
        "srctag": "C",
        },
    "C++": {
        "srcpat": "*.cpp",
        "destext": ".cpp",
        "srctag": "C++",
        },
    "C++ headers": {
        "srcpat": "*.hpp",
        "destext": ".hpp",
        "srctag": "C++",
        },
    "C#": {
        "srcpat": "*.cs",
        "destext": ".cs",
        "srctag": "C#",
        },
    "Visual BASIC": {
        "srcpat": "*.vb",
        "destext": ".vb",
        "srctag": "VISUAL BASIC",
        },
    "BASIC": {
        "srcpat": "*.bas",
        "destext": ".bas",
        "srctag": "BASIC",
        },
    "Java": {
        "srcpat": "*.java",
        "destext": ".java",
        "srctag": "JAVA",
        },
    "DaDISP": {
        "srcpat": "*.dd",
        "destext": ".dd",
        "srctag": "DADISP",
        },
    "Pascal": {
        "srcpat": "*.pas",
        "destext": ".pas",
        "srctag": "PASCAL",
        },
    "JOVIAL": {
        "srcpat": "*.jvl",
        "destext": ".jvl",
        "srctag": "JOVIAL",
        },
    "R": {
        "srcpat": "*.r",
        "destext": ".r",
        "srctag": "R",
        },
    "Julia": {
        "srcpat": "*.jl",
        "destext": ".jl",
        "srctag": "JULIA",
        },
    "XLISP": {
        "srcpat": "*.lsp",
        "destext": ".lsp",
        "srctag": "XLISP",
        },
    "LISP": {
        "srcpat": "*.lsp",
        "destext": ".lsp",
        "srctag": "LISP",
        },
    "FORTRAN": {
        "srcpat": "*.f",
        "destext": ".f",
        "srctag": "FORTRAN",
        },
    "Scheme": {
        "srcpat": "*.s",
        "destext": ".s",
        "srctag": "SCHEME",
        },
    "Rust": {
        "srcpat": "*.rs",
        "destext": ".rs",
        "srctag": "RUST",
        },
    }


def get_perl_files():
    files = glob.glob("*.pl")
    return files

def process_perl():
    sysprompt = """You are an expert software engineer using best practices.
You are adept in translating Perl programs into functional and well-documented Python 3 programs, taking care to handle modularization of spaghetti code in the process. You use the Click package for commond-line parameters, type hinting in function and method declarations, docstrings, and extensive comments. You refrain from non-code text, including preambles and post-code commentary, preferring to put all explanations in the form of program comments and docstrings."""
    prompt = "Translate the following Perl source code to Python 3 code. PERL: {SOURCE}"
    pfiles = sorted(get_perl_files())
    for pfilei in pfiles:
        llm = "codebooga"
        basename, baseext = os.path.splitext(pfilei)

        pyname = basename +  f"_{llm}.py"
        redirectfn = pyname

        pcontent = read_file(pfilei)
        myprompt = prompt.format(**{"SOURCE": pcontent})
        call_llm_process(llm=llm, sysprompt=sysprompt, prompt=myprompt, redirectfn=redirectfn)
        time.sleep(3)
        # break

def process_translate(srclang='MATLAB', destlang='Python 3', srctag='MATLAB', destext=".py", srcpat="*.m", overwrite=True, recurse=False, ptest=False):
    """
    Function to translate code to a different langauge.
    """
    sysprompt = """You are an expert software engineer using best practices.
You are adept in translating {SRCLANG} programs into functional and well-documented {DESTLANG} programs, taking care to handle modularization of spaghetti code in the process. You refrain from non-code text, including preambles and post-code commentary, preferring to put all explanations in the form of program comments and docstrings. {DEST_LANG_SYSPROMPT}"""

    # Conditional prompting for various languages. Pull from langinfo.
    # Source
    spes =  langinfo.get(srclang, {}).get('sysprompt_extra_src', False)
    if spes:
        sysprompt += f"\n{spes}\n"
    # Destination
    if ptest:
        print(f"destlang {langinfo.get(destlang, {}).get('sysprompt_extra_dest', False)}")
    sped =  langinfo.get(destlang, {}).get('sysprompt_extra_dest', False)
    if sped:
        sysprompt += f"\n{sped}\n"
        
    prompt = "Translate the following {SRCLANG} source code to {DESTLANG} code. {SRCTAG}: {SOURCE}"

    params = {"SRCLANG": srclang, "DESTLANG": destlang, "SRCTAG": srctag, "SOURCE": "", "DEST_LANG_SYSPROMPT": ""}
    params["DEST_LANG_SYSPROMPT"] = langinfo.get(srclang, {}).get('sysprompt_extra_dest', "")
    sysprompt = sysprompt.format(**params)
    # pfiles = sorted(glob.glob(srcpat))
    pfiles = sorted(find_files('.', [srcpat[1:]], recurse=recurse))
    for pfilei in pfiles:
        # The source language is what I would expect to matter more for picking an LLM.
        # Default to Codebooga 34b.
        llm = langinfo.get(srclang, {}).get("llm", "codebooga")
        print(f"LLM: {llm}")
        print(os.path.abspath(pfilei)) # Breadcrumb in output
        basename, baseext = os.path.splitext(pfilei)

        print(f"{basename=} {llm=} {basename.find(llm)}")
        if -1 >= basename.find(llm):
            outname = basename +  f"_xlate_{llm}" + destext
            redirectfn = outname
            
            if overwrite or not os.path.exists(redirectfn):
                print(f"Translating {pfilei} {srclang} to {redirectfn} {destlang}.")
                
                pcontent = read_file(pfilei)
                params["SOURCE"] = pcontent
                myprompt = prompt.format(**params)
                if not ptest:
                    call_llm_process(llm=llm, sysprompt=sysprompt, prompt=myprompt, redirectfn=redirectfn)
                else:
                    print(f"ptest: {sysprompt=} {myprompt=}")
                time.sleep(3) # Possible to keyboard interrupt this if needed
            else:
                print(f"Destination file {redirectfn} exists, skpping")
        else:
            print(f"Source file includes LLM name, skipping.")

        # break  # Debugging break


def process_files(srclang='MATLAB', destlang='Python 3', srctag='MATLAB', destext=".py", srcpat="*.m", overwrite=True, recurse=False, ptest=False, sysprompt=None):
    """
    Function to translate code to a different langauge.
    """
    if sysprompt in [None, ""]:
        sysprompt = """You are an expert software engineer using best practices.
You are adept in translating {SRCLANG} programs into functional and well-documented {DESTLANG} programs, taking care to handle modularization of spaghetti code in the process. You refrain from non-code text, including preambles and post-code commentary, preferring to put all explanations in the form of program comments and docstrings. {DEST_LANG_SYSPROMPT}"""

    # Conditional prompting for various languages. Pull from langinfo.
    # Source
    spes =  langinfo.get(srclang, {}).get('sysprompt_extra_src', False)
    if spes:
        sysprompt += f"\n{spes}\n"
    # Destination
    if ptest:
        print(f"destlang {langinfo.get(destlang, {}).get('sysprompt_extra_dest', False)}")
    sped =  langinfo.get(destlang, {}).get('sysprompt_extra_dest', False)
    if sped:
        sysprompt += f"\n{sped}\n"
        
    prompt = "Translate the following {SRCLANG} source code to {DESTLANG} code. {SRCTAG}: {SOURCE}"

    params = {"SRCLANG": srclang, "DESTLANG": destlang, "SRCTAG": srctag, "SOURCE": "", "DEST_LANG_SYSPROMPT": ""}
    params["DEST_LANG_SYSPROMPT"] = langinfo.get(srclang, {}).get('sysprompt_extra_dest', "")
    sysprompt = sysprompt.format(**params)
    # pfiles = sorted(glob.glob(srcpat))
    pfiles = sorted(find_files('.', [srcpat[1:]], recurse=recurse))
    for pfilei in pfiles:
        # The source language is what I would expect to matter more for picking an LLM.
        # Default to Codebooga 34b.
        llm = langinfo.get(srclang, {}).get("llm", "codebooga")
        print(f"LLM: {llm}")
        print(os.path.abspath(pfilei)) # Breadcrumb in output
        basename, baseext = os.path.splitext(pfilei)

        print(f"{basename=} {llm=} {basename.find(llm)}")
        if -1 >= basename.find(llm):
            outname = basename +  f"_xlate_{llm}" + destext
            redirectfn = outname
            
            if overwrite or not os.path.exists(redirectfn):
                print(f"Translating {pfilei} {srclang} to {redirectfn} {destlang}.")
                
                pcontent = read_file(pfilei)
                params["SOURCE"] = pcontent
                myprompt = prompt.format(**params)
                if not ptest:
                    call_llm_process(llm=llm, sysprompt=sysprompt, prompt=myprompt, redirectfn=redirectfn)
                else:
                    print(f"ptest: {sysprompt=} {myprompt=}")
                time.sleep(3) # Possible to keyboard interrupt this if needed
            else:
                print(f"Destination file {redirectfn} exists, skpping")
        else:
            print(f"Source file includes LLM name, skipping.")

        # break  # Debugging break


        
def process_lang1_2_lang2(srclang, destlang, recurse=False):
    """
    """
    process_translate(srclang=srclang, destlang=destlang, srctag=langinfo[srclang]["srctag"],
                      destext=langinfo[destlang]["destext"],
                      srcpat=langinfo[srclang]["srcpat"],
                      recurse=recurse)

    
if __name__ == "__main__":

    # process_perl()

    srclang = "MATLAB"
    destlang = "Python 3"
    if 3 == len(sys.argv):
    
        srclang = sys.argv[1]
        destlang = sys.argv[2]
        print(f"set {srclang=} {destlang=}")
        
    process_lang1_2_lang2(srclang, destlang, recurse=True)


