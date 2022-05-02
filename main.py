class PyAsmScript:

    def __init__(self):
        self.script = []
        self.scriptpointer = 0
        self.memory = []
        self.accumulator = 0
        self.stack = []

    def load(self, location):
        self.script.append(["load", location])

    def store(self, location):
        self.script.append(["store", location])

    def goto(self, location):
        self.script.append(["goto", location])

    def add(self, location):
        self.script.append(["add", location])

    def sub(self, location):
        self.script.append(["sub", location])

    def compare_more(self, location):
        self.script.append(["cmp_more", location])

    def compare_less(self, location):
        self.script.append(("cmp_less", location))

    def compare_equal(self, location):
        self.script.append(["cmp_equal", location])

    def push(self, location):
        self.script.append(["push", location])

    def pop(self):
        self.script.append(["pop", None])

    def run(self):

        self.scriptpointer = 0

        while True:
            if self.scriptpointer == len(self.script):
                break

            code = self.script[self.scriptpointer][0]
            location = self.script[self.scriptpointer][1]

            if code == "load":
                try:
                    self.accumulator = self.memory[location]
                except TypeError:
                    self.accumulator = int(location)

            if code == "store":
                while len(self.memory) < location + 1:
                    self.memory.append(None)
                self.memory.pop(location)
                self.memory.insert(location, self.accumulator)

            if code == "goto":
                self.scriptpointer = location

            if code == "add":
                try:
                    self.accumulator += self.memory[location]
                except TypeError:
                    self.accumulator += int(location)

            if code == "sub":
                try:
                    self.accumulator -= self.memory[location]
                except TypeError:
                    self.accumulator -= int(location)

            if code == "cmp_more":
                try:
                    if not self.accumulator > self.memory[location]:
                        self.scriptpointer += 1
                except TypeError:
                    if not self.accumulator > int(location):
                        self.scriptpointer += 1

            if code == "cmp_less":
                try:
                    if not self.accumulator < self.memory[location]:
                        self.scriptpointer += 1
                except TypeError:
                    if not self.accumulator < int(location):
                        self.scriptpointer += 1

            if code == "cmp_equal":
                try:
                    if not self.accumulator == self.memory[location]:
                        self.scriptpointer += 1
                except TypeError:
                    if not self.accumulator == int(location):
                        self.scriptpointer += 1

            if code == "push":
                try:
                    self.stack.append(self.memory[location])
                except TypeError:
                    self.stack.append(int(location))

            if code == "pop":
                self.accumulator = self.stack.pop()

            self.scriptpointer += 1


if __name__ == "__main__":
    asm = PyAsmScript()

    asm.load("0")               # 0:
    asm.store(0)                # 1: set location 0 as int 0 (location 0 is var 'first' from now on)
    asm.load("1")               # 2:
    asm.store(1)                # 3: set location 1 as int 1 (location 1 is var 'second' from now on)
    asm.load("0")               # 4:
    asm.store(2)                # 5: set location 2 as int 0 (location 2 is var 'next' from now on)

    asm.load(0)                 # 6: add first and second to
    asm.add(1)                  # 7: calculate next
    asm.store(2)                # 8:

    asm.load(1)                 # 9: move second to first
    asm.store(0)                # 10:
    asm.load(2)                 # 11: move next to second
    asm.store(1)                # 12:

    asm.compare_less("200")     # 13: if second is less than int 200
    asm.goto(6)                 # 14: goto 6 and repeat

    asm.run()

    print(asm.memory[1])        # print(second)