npmai

npmai (by Sonu Kumar Ramashish) is a lightweight Python package that seamlessly connects LangChain with real-time web-based LLMs like Gemini, ChatGPT, Grok, and Perplexity via Selenium automation.

🚀 Features

Execute prompts on multiple LLMs simultaneously: Gemini, ChatGPT, Grok, Perplexity.

Fully LangChain-compatible interface.

Simple and intuitive invoke() API for instant responses.

Browser automation with headless Chrome via Selenium.

Supports continuous conversation mode for long-running interactions with ChatGPT or Gemini.

Encourages responsible usage—please respect AI companies like OpenAI, Google, X AI, Perplexity, and support them if used at scale.

⚙️ Installation
pip install npmai


Tip: For Python 3.13, make sure to use:

py -3.13 -m pip install npmai

💡 How to Use

Import the models you need—either one, two, or all:

from npmai import ChatGPT, Grok, Perplexity, Gemini, GeminiAIMode,Image


Initialize a model:

llm = ChatGPT()       # or Gemini(), Grok(), Perplexity(),Image()


Invoke a prompt and get the response:

response = llm.invoke("Your prompt here")
print(response) 

#Latest Update :
version 0.0.5 Here you will get models that can generate Images also.

⚠️ Important Notes

Designed for educational and small-scale experimentation.

If using at a larger scale, consider supporting the original AI platforms—they invest heavily in research and infrastructure.

Continuous mode allows extended conversations, but use responsibly to avoid overloading web-based LLM services.

✅ npmai makes it effortless to connect web-based AI models with Python, bringing automation, experimentation, and LangChain integration together in a single, easy-to-use package.
