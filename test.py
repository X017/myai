import ollama

messages = []  # store chat history

while True:
    user_input = input("prompt: ").strip()
    if not user_input:
        continue

    messages.append({"role": "user", "content": user_input})

    print("Calculating...")  # show before response

    response = ollama.chat(
        model="llama2",
        messages=messages
    )

    message = response.get("message", {}).get("content", "")
    print("LLM:", message if message else "[No response]")

    if message:
        messages.append({"role": "assistant", "content": message})



