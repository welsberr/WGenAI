# Resources for AI

I've mostly been interested in what AI projects and tooling can be
used with local execution. There are plenty of projects and tools
that assume use of third-party subscription services; these are of
less interest to me currently because of a variety of concerms,
the first being cost containment, the second being data security,
and the third being restrictive rate limits. These may be addressed
in some ways in the future that would change my mind, but right now
I'm concentrating on making progress in applying AI using just the
computational power I can apply locally.

## Local Processing for Generative AI

At the current time, the easiest way to get the most generative AI
software and tools running locally is via use of Nvidia GPUs. Nvidia's
hegemony may not be as complete as it was even a year ago, but it
still is easier and faster to simply have a compatible Nvidia GPU
(or several) at your disposal.

Apple's 'Silicon' processors have shown good performance in running
local LLMs. AMD GPUs are supported for certain tools via ROC-m.
Intel's GPUs have been applied to certain generative AI projects.
And 'llama.cpp' has allowed inference on LLMs entirely via CPU and
system RAM, where performance comes down to the number of threads
the CPU can support and the memory bandwidth of the system RAM.

This is not yet organized in a systematic fashion, but I want to
list certain things I've found useful, relevant, or in some cases
worthy of watching for future development.

### Llamafile

Llamafile is a project out of Mozilla/Ocho headed by Justine Tunney
that is all about making it as simple as possible to run a
large language model (LLM) for inference locally. Justine Tunney
developed a project called 'Cosmopolitan' that sets up a cross-platform
libc implementation, a technology that allowed her to create what she
termed "Actually Portable Executable" format. These are single-file
executables that can be executed under multiple different operating
systems and even directly from BIOS, and even multiple different
architectures (amd64 vs. arm64). Mozilla asked Justine to apply her
Cosmopolitan libc to making a 'llama.cpp' implementation that could be
run as a portable executable. Tunney delivered with 'llamafile'. The
original release in November 2023 packaged 'llama.cpp' with the Llava
1.5 multi-model LLM in a single (large) executable file named
'llamafile'. Because 'llama.cpp' can run an LLM for inference on
CPU alone, llamafile allows running an LLM anywhere one has enough
memory to handle the job. If it is running on CPU alone, it will run
more slowly, but it will run. On systems with Nvidia or AMD GPUs, or
Apple Silicon, it can be set up to be able to use those for faster
inference.

https://github.com/Mozilla-Ocho/llamafile

### Whisperfile

A related project is 'whisperfile', a single-file executable based
on Cosmopolitan that packages the 'whisper.cpp' tool with the
Whisper 'base.en' model for generic English speech-to-text tasks.
So far, this only seems to exist as a demonstration project that
Justine Tunney wrote in response to a 'llamafile' issue where
someone asked if 'whisper.cpp' could be incorporated into a
llamafile. Justine said it required some changes in Cosmopolitan,
so this probably isn't generically feasible unitl she releases
those changs. Look for the 'whisperfile.gz' download link.

https://github.com/Mozilla-Ocho/llamafile/issues/17#issuecomment-1953139295



