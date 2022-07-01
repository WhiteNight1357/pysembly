class PyAsmScript:

    def __init__(self):
        self.script = []
        self.scriptpointer = 0
        self.memory = []
        self.register = 0
        self.stack = []
        self.labels = []
        self.labeldata = []

    def load(self, location, mode):
        self.script.append(["load", location, mode])

    def store(self, location, mode):
        self.script.append(["store", location, mode])

    def goto(self, location, mode):
        self.script.append(["goto", location, mode])

    def add(self, location, mode):
        self.script.append(["add", location, mode])

    def sub(self, location, mode):
        self.script.append(["sub", location, mode])

    def compare_more(self, location, mode):
        self.script.append(["cmp_more", location, mode])

    def compare_less(self, location, mode):
        self.script.append(["cmp_less", location, mode])

    def compare_equal(self, location, mode):
        self.script.append(["cmp_equal", location, mode])

    def push(self, location, mode):
        self.script.append(["push", location, mode])

    def pop(self):
        self.script.append(["pop", None, None])

    def label(self, label):     # label() labels NEXT line, not previous
        try:
            self.labels.index(label)
            raise Exception("this label is already in label list")
        except ValueError:
            if not isinstance(label, str):
                raise Exception("'label' should be string")
            self.labels.append(label)
            self.labeldata.append(len(self.script))

    def run(self):

        self.scriptpointer = 0

        while True:
            if self.scriptpointer == len(self.script):
                break

            code = self.script[self.scriptpointer][0]
            location = self.script[self.scriptpointer][1]
            mode = self.script[self.scriptpointer][2]

            if mode is None:
                value = location
            elif mode is True:
                value = self.memory[location]
            elif mode is False:
                value = self.memory[self.memory[location]]
            else:
                raise Exception("'mode' should be None, True, or False")

            if code == "load":
                self.register = value

            if code == "store":
                while len(self.memory) < value + 1:
                    self.memory.append(None)
                self.memory.pop(value)
                self.memory.insert(value, self.register)

            if code == "goto":
                if value is None:
                    self.scriptpointer = self.register
                elif isinstance(value, str):
                    self.scriptpointer = self.labeldata[self.labels.index(value)]
                else:
                    self.scriptpointer = value

            if code == "add":
                self.register += value

            if code == "sub":
                self.register -= value

            if code == "cmp_more":
                if not self.register > value:
                    self.scriptpointer += 1

            if code == "cmp_less":
                if not self.register < value:
                    self.scriptpointer += 1

            if code == "cmp_equal":
                if not self.register == value:
                    self.scriptpointer += 1

            if code == "push":
                self.stack.append(value)

            if code == "pop":
                self.register = self.stack.pop()

            self.scriptpointer += 1

    def clear_script(self):
        self.script = []

    def clear_memory(self):
        self.memory = []

    def clear_stack(self):
        self.stack = []


if __name__ == "__main__":
    asm = PyAsmScript()

    asm.load(0, None)                  # 0:
    asm.store(0, None)                 # 1: set location 0 as int 0 (location 0 is var 'first' from now on)
    asm.load(1, None)                  # 2:
    asm.store(1, None)                 # 3: set location 1 as int 1 (location 1 is var 'second' from now on)
    asm.load(0, None)                  # 4:
    asm.store(2, None)                 # 5: set location 2 as int 0 (location 2 is var 'next' from now on)

    asm.label("a")                     # label: line 6 as label "a"

    asm.load(0, True)                  # 6: add first and second to
    asm.add(1, True)                   # 7: calculate next
    asm.store(2, None)                 # 8:

    asm.load(1, True)                  # 9: move second to first
    asm.store(0, None)                 # 10:
    asm.load(2, True)                  # 11: move next to second
    asm.store(1, None)                 # 12:

    asm.compare_less(200, None)        # 13: if second is less than int 200
    asm.goto("a", None)                # 14: goto "a" and repeat

    asm.run()

    print(asm.memory[1])               # print(second)