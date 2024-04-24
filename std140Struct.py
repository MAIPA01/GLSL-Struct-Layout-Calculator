class STD140Struct:
    def __init__(self):
        self.baseOffset = 0
        self.offsets = {}
        self.maxAligement = 0

    def add(self, typeName: str, valueName: str, baseAligement: int, baseOffset: int):
        aligementOffset = self.baseOffset
        if self.baseOffset % baseAligement != 0:
            aligementOffset += baseAligement - (self.baseOffset % baseAligement)
        print(f"{typeName} {valueName}, baseAligement: {baseAligement}, baseOffset: {self.baseOffset}, aligementOffset: {aligementOffset}")
        self.offsets[valueName] = aligementOffset
        self.baseOffset = aligementOffset + baseOffset
        if baseAligement > self.maxAligement:
            self.maxAligement = baseAligement
        return aligementOffset

    def addArray(self, typeName: str, valueName: str, baseAligement: int, baseOffset: int, num: int):
        if baseAligement % 16 != 0:
            baseAligement += 16 - (baseAligement % 16)
        for i in range(num):
            self.add(typeName, f"{valueName}[{i}]", baseAligement, baseOffset)
        if self.baseOffset % 16 != 0:
            self.baseOffset += 16 - (self.baseOffset % 16)

    def addBool(self, name: str):
        self.add("bool", name, 4, 4)

    def addBoolArray(self, name: str, num: int):
        self.addArray("bool", name, 4, 4, num)

    def addInt(self, name: str):
        self.add("int", name, 4, 4)

    def addIntArray(self, name: str, num: int):
        self.addArray("int", name, 4, 4, num)

    def addUint(self, name: str):
        self.add("uint", name, 4, 4)

    def addUintArray(self, name: str, num: int):
        self.addArray("int", name, 4, 4, num)

    def addFloat(self, name: str):
        self.add("float", name, 4, 4)

    def addFloatArray(self, name: str, num: int):
        self.addArray("float", name, 4, 4, num)

    def addDouble(self, name: str):
        self.add("double", name, 4, 4)

    def addDoubleArray(self, name: str, num: int):
        self.addArray("double", name, 4, 4, num)

    def addVec2(self, name: str):
        self.add("vec2", name, 8, 8)

    def addVec2Array(self, name: str, num: int):
        self.addArray("vec2", name, 8, 8, num)

    def addBVec2(self, name: str):
        self.add("bvec2", name, 8, 8)

    def addBVec2Array(self, name: str, num: int):
        self.addArray("bvec2", name, 8, 8, num)

    def addVec3(self, name: str):
        self.add("vec3", name, 16, 12)

    def addVec3Array(self, name: str, num: int):
        self.addArray("vec3", name, 16, 12, num)

    def addUVec3(self, name: str):
        self.add("uvec3", name, 16, 12)

    def addUVec3Array(self, name: str, num: int):
        self.addArray("uvec3", name, 16, 12, num)

    def addVec4(self, name: str):
        self.add("vec4", name, 16, 16)

    def addVec4Array(self, name: str, num: int):
        self.addArray("vec4", name, 16, 16, num)

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
        aligementOffset = self.add("struct", name, baseAligement, struct.baseOffset)
        for key in struct.offsets:
            print(f"{name}.{key}, aligementOffset: {aligementOffset + struct.offsets[key]}")
        if self.baseOffset % 16 != 0:
            self.baseOffset += 16 - (self.baseOffset % 16)

    def addStructArray(self, name: str, struct, num: int):
        for i in range(num):
            self.addStruct(f"{name}[{i}]", struct)