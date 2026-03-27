# ykeyscore
A proof of concept showing how AI could be used to surveil social media.

## How this works
We use a reddit post archive API to retrieve all posts made by a user and then pass them through an LLM to make a summary.
The LLM will spit out information it could find about the user via. those posts once the process is finished.

## Dependencies
```
ollama w/ qwen3:4b downloaded on your device
requests
```
