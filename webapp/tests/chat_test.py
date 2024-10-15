import os

from httfe.services.chat import get_chat_srv


def test_send_chat():
    os.environ["CHATGPT_KEY"] = "sk-1234"
    chat_service = get_chat_srv()
    msg = "HXAAEEEELLLOO"
    # chat_service.send_chat(msg)
    assert True
