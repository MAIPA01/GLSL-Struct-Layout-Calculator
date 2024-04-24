class STD140Struct:
    def __init__(self):
        self.baseOffset = 0
        self.offsets = {}
        self.maxAligement = 0

    def add(self, typeName: str, valueName: str, baseAligement: int):
        aligementOffset = self.baseOffset
        if self.baseOffset % baseAligement != 0:
            aligementOffset += baseAligement - (self.baseOffset % baseAligement)
        print(f"{typeName} {valueName}, baseAligement: {baseAligement}, baseOffset: {self.baseOffset}, aligementOffset: {aligementOffset}")
        self.offsets[valueName] = aligementOffset
        self.baseOffset = aligementOffset + baseAligement
        if baseAligement > self.maxAligement:
            self.maxAligement = baseAligement

    def addArray(self, typeName: str, valueName: str, baseAligement: int, num: int):
        if baseAligement % 16 != 0:
            baseAligement += 16 - (baseAligement % 16)
        for i in range(num):
            self.add(typeName, f"{valueName}[{i}]", baseAligement)

    def addInt(self, name: str):
        self.add("int", name, 4)

    def addFloat(self, name: str):
        self.add("float", name, 4)

    def addFloatArray(self, name: str, num: int):
        self.addArray("float", name, 4, num)

    def addVec2(self, name: str):
        self.add("vec2", name, 8)

    def addVec2Array(self, name: str, num: int):
        self.addArray("vec2", name, 8, num)

    def addBVec2(self, name: str):
        self.add("bvec2", name, 8)

    def addVec3(self, name: str):
        self.add("vec3", name, 16)

    def addVec3Array(self, name: str, num: int):
        self.addArray("vec3", name, 16, num)

    def addUVec3(self, name: str):
        self.add("uvec3", name, 16)

    def addVec4(self, name: str):
        self.add("vec4", name, 16)

    def addVec4Array(self, name: str, num: int):
        self.addArray("vec4", name, 16, num)

    def addMat(self, name: str, cols: int, rows: int):
        if rows == 1:
            self.addFloatArray(name, cols)
        elif rows == 2:
            self.addVec2Array(name, cols)
        elif rows == 3:
            self.addVec3Array(name, cols)
        elif rows == 4:
            self.addVec4Array(name, cols)
        else:
            print("Podano złą liczbę wierszy")

    def addMatArray(self, name: str, cols: int, rows: int, num: int):
        for i in range(num):
            self.addMat(f"{name}[{i}]", cols, rows)

    def addSqrMat(self, name: str, size: int):
        self.addMat(name, size, size)

    def addSqrMatArray(self, name: str, size: int, num: int):
        self.addMatArray(name, size, size, num)

    def addStruct(self, name: str, struct):
        baseAligement = struct.maxAligement
        if (baseAligement % 16 != 0):
            baseAligement += 16 - (baseAligement % 16)
        for key in struct.offsets:
            print(f"{name}.{key}, aligementOffset: {struct.offsets[key] + self.baseOffset}")
        self.add("struct", name, baseAligement)
        self.baseOffset += struct.baseOffset - baseAligement

    def addStructArray(self, name: str, struct, num: int):
        for i in range(num):
            self.addStruct(f"{name}[{i}]", struct)

uniformBuffer = STD140Struct()
# uniformBuffer.addFloat("a")
# uniformBuffer.addVec2("b")
# uniformBuffer.addVec3("c")

# print("SUB STRUCT START")
# subStruct = STD140Struct()
# subStruct.addInt("d")
# subStruct.addBVec2("e")
# print("SUB STRUCT END")

# uniformBuffer.addStruct("f", subStruct)
# uniformBuffer.addFloat("g")
# uniformBuffer.addFloatArray("h", 2)
# uniformBuffer.addMat("i", 2, 3)

# print("SUB STRUCT START")
# subStruct = STD140Struct()
# subStruct.addUVec3("j")
# subStruct.addVec2("k")
# subStruct.addFloatArray("l", 2)
# subStruct.addVec2("m")
# subStruct.addSqrMatArray("n", 3, 2)
# print("SUB STRUCT END")

# uniformBuffer.addStructArray("o", subStruct, 2)

print(f"last offset: {uniformBuffer.baseOffset}")