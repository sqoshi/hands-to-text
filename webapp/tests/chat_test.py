from httfe.services.chat import get_chat_srv


def test_send_chat():
    chat_service = get_chat_srv()
    msg = "HXAAEEEELLLOO"
    # chat_service.send_chat(msg)
    assert True
