class Animal(object):
    makes_noise: bool = False

    def make_noise(self: "Animal") -> object:
        if self.makes_noise:
            print(self.sound())

    def sound(self: "Animal") -> str:
        return "???"
