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

    def load(self, location, mode, *, indcount=1):
        self.script.append(indcountcheck(["load", location, mode, indcount]))

    def store(self, location, mode, *, indcount=1):
        self.script.append(indcountcheck(["store", location, mode, indcount]))

    def goto(self, location, mode, *, indcount=1):
        self.script.append(indcountcheck(["goto", location, mode, indcount]))

    def add(self, location, mode, *, indcount=1):
        self.script.append(indcountcheck(["add", location, mode, indcount]))

    def sub(self, location, mode, *, indcount=1):
        self.script.append(indcountcheck(["sub", location, mode, indcount]))

    def compare_more(self, location, mode, *, indcount=1):
        self.script.append(indcountcheck(["cmp_more", location, mode, indcount]))

    def compare_less(self, location, mode, *, indcount=1):
        self.script.append(indcountcheck(["cmp_less", location, mode, indcount]))

    def compare_equal(self, location, mode, *, indcount=1):
        self.script.append(indcountcheck(["cmp_equal", location, mode, indcount]))

    def push(self, location, mode, *, indcount=1):
        self.script.append(indcountcheck(["push", location, mode, indcount]))

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
            try:
                indcount = self.script[self.scriptpointer][3]
            except IndexError:
                indcount = None

            if isinstance(location, str):
                location = self.labeldata[self.labels.index(location)]

            if mode == "Instant" or mode == "instant" or mode == "ins":
                mode = None
            elif mode == "Direct" or mode == "direct" or mode == "dir":
                mode = True
            elif mode == "Indirect" or mode == "indirect" or mode == "ind":
                mode = False

            if not (mode is None or mode is True or mode is False) and isinstance(mode, str):
                raise Exception("'mode' using string should be:\n"
                                "'Instant', 'Direct', 'Indirect',\n"
                                "'instant', 'direct', 'indirect',\n"
                                "'ins',     'dir',     or 'ind'")

            if mode is None:
                value = location
            elif mode is True:
                value = self.memory[location]
            elif mode is False:
                a = self.memory[location]
                indcount -= 1
                while not indcount == 0:
                    a = self.memory[a]
                    indcount -= 1
                value = a
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


def indcountcheck(param):
    if param[2] == "Indirect" or param[2] == "indirect" or param[2] == "ind":
        if not isinstance(param[3], int):
            raise Exception("'indcount' should be int")
        return param
    else:
        del param[3]
        return param


if __name__ == "__main__":
    asm = PyAsmScript()                # Sample Code: Calculate fibonacci sequence until it gets higher than 200
    asm.debugging = True               # Enables debugging

    # TODO: Write Sample Code Comments

    asm.label_location(20, "first")    # label: location 20 as label "first"
    asm.label_location(21, "second")   # label: location 21 as label "second"
    asm.label_location(22, "next")     # label: location 22 as label "next"
    asm.label_location(23, "counter")  # label: location 23 as label "counter"

    asm.load(0, "ins")
    asm.store("first", "ins")
    asm.store(0, "ins")
    asm.load(1, "ins")
    asm.store("second", "ins")
    asm.store(1, "ins")
    asm.load(0, "ins")
    asm.store("next", "ins")
    asm.load(2, "ins")
    asm.store("counter", "ins")

    asm.label_line("a")

    asm.load("first", "dir")
    asm.add("second", "dir")
    asm.store("next", "ins")
    asm.store("counter", "dir")

    asm.load("counter", "dir")
    asm.add(1, "ins")
    asm.store("counter", "ins")

    asm.load("second", "dir")
    asm.store("first", "ins")
    asm.load("next", "dir")
    asm.store("second", "ins")

    asm.compare_less(200, "ins")
    asm.goto("a", "ins")



    asm.run()

    print(asm.memory[1:20])               # print(second)