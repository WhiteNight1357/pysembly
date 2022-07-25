class PyAsmScript:

    def __init__(self):
        self.script = []
        self.scriptpointer = 0
        self.memory = []
        self.register = 0
        self.stack = []
        self.labels = []
        self.labeldata = []
        self.debugging = False

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

    def label_line(self, label):     # label_line() labels NEXT line, not previous
        try:
            self.labels.index(label)
            raise Exception("this label is already in label list")
        except ValueError:
            if not isinstance(label, str):
                raise Exception("'label' should be string")
            self.labels.append(label)
            self.labeldata.append(len(self.script))

    def label_location(self, location, label):   # label_location() does not count as script
        try:
            self.labels.index(label)
            raise Exception("this label is already in label list")
        except ValueError:
            if not isinstance(label, str):
                raise Exception("'label' should be string")
            self.labels.append(label)
            self.labeldata.append(location)

    def null(self):
        self.script.append([None, None, None])

    def run(self):

        self.scriptpointer = 0

        while True:
            if self.scriptpointer == len(self.script):
                break

            code = self.script[self.scriptpointer][0]
            location = self.script[self.scriptpointer][1]
            mode = self.script[self.scriptpointer][2]

            if isinstance(location, str):
                location = self.labeldata[self.labels.index(location)]

            if mode == "Instant" or mode == "instant" or mode == "ins":
                mode = None
            elif mode == "Direct" or mode == "direct" or mode == "dir":
                mode = True
            elif mode == "Indirect" or mode == "indirect" or mode == "ind":
                mode = False

            if not (mode is None or mode is True or mode is False) and isinstance(mode, str):
                raise Exception("'mode' using string should be\n"
                                "'Instant', 'Direct', 'Indirect',\n"
                                "'instant', 'direct','indirect',\n"
                                "'ins',     'dir',     or 'ind'")

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
                self.scriptpointer -= 1

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

            if self.debugging:
                self.debug()

            self.scriptpointer += 1

    def clear_script(self):
        self.script = []

    def clear_memory(self):
        self.memory = []

    def clear_stack(self):
        self.stack = []

    def debug(self):
        print(self.memory)
        print(self.register)
        print(self.scriptpointer)
        print("---------------------------")


if __name__ == "__main__":
    asm = PyAsmScript()                # Sample Code: Calculates first fibonacci number higher than 200
    asm.debugging = True               # Enables debugging

    asm.label_location(0, "first")     # label: location 0 as label "first"
    asm.label_location(1, "second")    # label: location 1 as label "second"
    asm.label_location(2, "next")      # label: location 2 as label "next"

    asm.load(0, "ins")                 # 0:
    asm.store("first", "ins")          # 1: set first as int 0
    asm.load(1, "ins")                 # 2:
    asm.store("second", "ins")         # 3: set second as int 1
    asm.load(0, "ins")                 # 4:
    asm.store("next", "ins")           # 5: set next as int 0

    asm.label_line("a")                # label: line 6 as label "a"

    asm.load("first", "dir")           # 6: add first and second to
    asm.add("second", "dir")           # 7: calculate next
    asm.store("next", "ins")           # 8:

    asm.load("second", "dir")          # 9: move second to first
    asm.store("first", "ins")          # 10:
    asm.load("next", "dir")            # 11: move next to second
    asm.store("second", "ins")         # 12:

    asm.compare_less(200, "ins")       # 13: if second is less than int 200
    asm.goto("a", "ins")               # 14: goto "a" and repeat

    asm.run()

    print(asm.memory[1])               # print(second)