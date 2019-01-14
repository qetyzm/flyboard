import random

class DicePlugin:
    boards = ('b',)
    
    def process_message(self, message):
        if message.email != "#dice":
            return message
        
        message.email = ""

        if message.board in self.boards:
            text = message.processed_text
            output = '<span color="pink">Dice: <b>'
            output += str(random.randint(1, 6))
            output += '</b></span><br><br>'
            output += text
            message.processed_text = text

        return message
    
    def get_end_url(self):
        return None
    
    def get_name(self):
        return "dice"