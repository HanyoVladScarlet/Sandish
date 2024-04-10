from src.bpy_scripts.message_manager import *


if __name__ == '__main__':
    data = {
        'message': 'I\'m a message.',
        'type': 'test'
    }

    mm = MessageManager(port=11133)
    res = mm.push_message(data=data)