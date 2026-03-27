# ykeyscore
A proof of concept showing how AI could be used to surveil social media.

## How this works
We use a reddit post archive API to retrieve all posts made by a user and then pass them through an LLM to make a summary.
The LLM will spit out information it could find about the user via. those posts once the process is finished.

## Dependencies
```
ollama
requests
```

Ollama can be downloaded at https://ollama.ai/ and the specific model you need to download for this is:
```
ollama pull qwen3:4b
```
