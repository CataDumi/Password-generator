

ALPHABET = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','.','0','1','2','3','4','5','6','7','8','9',
    '!','@','#','$','%','^','&','*','(',')'
]

class Encode:
    def __init__(self,start_text,shift):
        self.end_text = ""
        for char in start_text:
            if char in ALPHABET:
                try:
                    self.position = ALPHABET.index(char)
                    self.new_position = self.position + shift
                    self.end_text += ALPHABET[self.new_position]
                except IndexError:
                    self.new_position = ALPHABET.index(char) % len(ALPHABET)
            else:
                self.end_text += char
        self.end_text = self.end_text
        print(f"Here's the result: {self.end_text}")