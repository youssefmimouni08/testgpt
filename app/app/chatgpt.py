from openai import OpenAI
import openai
import os

# define the OpenAI class with the API key
client = OpenAI(
        api_key = os.environ["API_KEY"],
        timeout = 30,
        max_retries = 3
    )

# The following function is used to chat with ChatGPT
def chat_with_gpt(model,purpose,chat_history):
    if purpose == "summarization":
        system = "Please summarize the following conversation log for a meeting. Please summarize i bullet points. If any action is needed, please define who handle it. Please cover all topics in the conversation."
    else:
        system = ""
    messages = [{"role": "system", "content": system}]
    # add the chat history to the messages
    for chat in chat_history:
        messages.append(chat)
    try:
        response = client.with_options(timeout=5 * 60).chat.completions.create(
                        model = model,
                        messages = messages,
                    )
        reply = response.choices[0].message.content
    except openai.APIConnectionError as e:
        return "The server could not be reached", False
    except openai.RateLimitError as e:
        return "A 429 status code was received; we should back off a bit.", False
    except openai.APIStatusError as e:
        return "Another non-200-range status code was received", False
    chat_history.append({"role":"assistant","content":reply})
    return reply,chat_history
