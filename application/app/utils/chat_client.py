from g4f.client import Client


class ChatClient:
    history = []
    client = Client()

    @classmethod
    def send_message(cls, text):
        try:
            response = cls.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": text}],
            )
            assistant_response = response.choices[0].message.content
            cls.history.append(f"You: {text}")
            cls.history.append(f"Assistant: {assistant_response}")
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @classmethod
    def get_history(cls):
        return cls.history
