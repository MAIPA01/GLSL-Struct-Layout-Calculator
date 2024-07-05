BOOL = "bool"
INT = "int"
UINT = "uint"
FLOAT = "float"
DOUBLE = "double"

class StructValue:
    def __init__(self, name: str, size: int, typeName: str, baseAligement: int, aligementOffset: int, baseOffset: int, padding: int|None = None):
        self.__name = name
        self.__baseSize = size
        self.__typeName = typeName
        self.__baseAligement = baseAligement
        self.__aligementOffset = aligementOffset
        self.__baseOffset = baseOffset
        self.__padding = padding
        self.__subValues = []

    def append(self, value):
        self.__subValues.append(value)

    def setName(self, name: str):
        self.__name = name

    def setTypeName(self, typeName: str):
        self.__typeName = typeName

    def setBaseOffset(self, baseOffset: int):
        diff = baseOffset - self.__baseOffset
        self.__baseOffset += diff
        self.__aligementOffset += diff
        for value in self.__subValues:
            value.setBaseOffset(value.getBaseOffset() + diff)

    def setAligementOffset(self, aligementOffset: int):
        diff = aligementOffset - self.__aligementOffset
        self.__baseOffset += diff
        self.__aligementOffset += diff
        for value in self.__subValues:
            value.setAligementOffset(value.getAligementOffset() + diff)

    def setPadding(self, padding: int|None):
        self.__padding = padding

    def getName(self):
        return self.__name

    def getBaseOffset(self):
        return self.__baseOffset

    def getBaseAligement(self):
        return self.__baseAligement
    
    def getTypeName(self):
        return self.__typeName
    
    def getAligementOffset(self):
        return self.__aligementOffset

    def getSize(self):
        return self.__baseSize

    def getPadding(self):
        return self.__padding
    
    def getSubValuesCount(self):
        return len(self.__subValues)

    def getSubValue(self, name: str):
        value = None

        names = name.split('.')
        fullName = names[0]

        if self.__name == fullName:
            if len(names) > 1:
                for subValue in self.__subValues:
                    value = subValue.getSubValue('.'.join(names[1:]))
                    if value is not None:
                        return value
            else:
                return self

        # SEARCH ARRAY
        arrays = fullName.split('[')
        valueName = arrays[0]

        arrayName = None
        if self.__name == valueName:
            arrayName = valueName + '[' + arrays[1]
        else:
            for subValue in self.__subValues:
                if subValue.__name == valueName:
                    return subValue.getSubValue(name)

            for i in range(len(arrays) - 2):
                valueName += '[' + arrays[i + 1]
                if self.__name == valueName:
                    arrayName = valueName + '[' + arrays[i + 2]
                    break
            if arrayName is None:
                return None
        
        for subValue in self.__subValues:
            if subValue.__name == arrayName:
                value = subValue.getSubValue(fullName)
                break
        if value is None:
            return None
        
        # GET SUB VALUES
        if len(names) > 1:
            value = value.getSubValue('.'.join(names[1:]))

        return value

    def copy(self):
        c = StructValue(self.__name, 
                        self.__baseSize,
                        self.__typeName,
                        self.__baseAligement,
                        self.__aligementOffset,
                        self.__baseOffset,
                        self.__padding)
        for value in self.__subValues:
            c.append(value.copy())
        return c

    def print(self, indent: str = "") -> str:
        text = f"{indent}{self}"
        for subValue in self.__subValues:
            text += subValue.print(indent + "  ")
        if self.__padding is not None:
            GREEN = "\033[92m"
            YELLOW = "\033[93m"
            RESET = "\033[0m"
            text += f"{indent + '  '}- End padding of {GREEN}{self.__name}{RESET}: base size {YELLOW}{self.__padding}{RESET}, base off. {YELLOW}{self.__aligementOffset + self.__baseSize}{RESET}, align off. {YELLOW}{self.__aligementOffset + self.__baseSize + self.__padding}{RESET}\n"
        return text

    def __str__(self) -> str:
        BLUE = "\033[94m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        RESET = "\033[0m"
        return f"- {BLUE}{self.__typeName} {GREEN}{self.__name}{RESET}: base size {YELLOW}{self.__baseSize}{RESET}, base align {YELLOW}{self.__baseAligement}{RESET}, base off. {YELLOW}{self.__baseOffset}{RESET}, align off. {YELLOW}{self.__aligementOffset}{RESET}\n"

    def __repr__(self) -> str:
        return self.print()

class STD140Struct:
    def __init__(self):
        self.__baseOffset : int = 0
        self.__values : list[StructValue] = []
        self.__maxAligement : int = 0
        self.__typeSizes : dict[str, int] = { "bool" : 4, "int" : 4, "uint" : 4, "float" : 4, "double" : 8 }
        self.__vecTypes : dict[str, str] = { "bool" : "bvec", "int" : "ivec", "uint" : "uvec", "float" : "vec", "double" : "dvec" }
        self.__matTypes : dict[str, str] = { "bool" : "bmat", "int" : "imat", "uint" : "umat", "float" : "mat", "double" : "dmat" }

    def __add(self, typeName: str, valueName: str, baseAligement: int, baseOffset: int) -> int:
        aligementOffset = self.__baseOffset
        if self.__baseOffset % baseAligement != 0:
            aligementOffset += baseAligement - (self.__baseOffset % baseAligement)
        
        self.__values.append(StructValue(valueName, baseOffset, typeName, baseAligement, aligementOffset, self.__baseOffset))

        self.__baseOffset = aligementOffset + baseOffset
        if baseAligement > self.__maxAligement:
            self.__maxAligement = baseAligement
        return aligementOffset

    def __addArray(self, typeName: str, valueName: str, baseAligement: int, baseOffset: int, num: int) -> list[int]:
        if baseAligement % 16 != 0:
            baseAligement += 16 - (baseAligement % 16)

        aligementOffsets = []
        for i in range(num):
            aligementOffsets.append(self.__add(typeName, f"{valueName}[{i}]", baseAligement, baseOffset))

        firstValue = self.__values[-len(aligementOffsets)]
        lastValue = self.__values[-1]
        lastValuePadding = 0 if lastValue.getPadding() is None else lastValue.getPadding()

        self.__values.append(StructValue(valueName,
                                        (lastValue.getAligementOffset() + lastValue.getSize() + lastValuePadding) - firstValue.getAligementOffset(),
                                        f"{typeName}[{num}]",
                                        baseAligement,
                                        firstValue.getAligementOffset(),
                                        firstValue.getBaseOffset(),
                                        0))
        
        for i in range(num):
            self.__values[-1].append(self.__values[-(num - i) - 1])
            self.__values.pop(-(num - i) - 1)
        
        if self.__baseOffset % 16 != 0:
            self.__values[-1].setPadding(16 - (self.__baseOffset % 16))
            self.__baseOffset += 16 - (self.__baseOffset % 16)
        
        return aligementOffsets

    def addScalar(self, name: str, typeName: str) -> int:
        return self.__add(typeName, name, self.__typeSizes[typeName], self.__typeSizes[typeName])

    def addScalarArray(self, name: str, typeName: str, num: int) -> list[int]:
        return self.__addArray(typeName, name, self.__typeSizes[typeName], self.__typeSizes[typeName], num)

    def addVec(self, name: str, typeName: str, vecSize: int) -> int:
        baseAligement = self.__typeSizes[typeName] * vecSize if vecSize != 3 else self.__typeSizes[typeName] * (vecSize + 1)
        baseOffset = self.__typeSizes[typeName] * vecSize
        return self.__add(f"{self.__vecTypes[typeName]}{vecSize}", name, baseAligement, baseOffset)

    def addVecArray(self, name: str, typeName: str, vecSize: int, num: int) -> list[int]:
        baseAligement = self.__typeSizes[typeName] * vecSize if vecSize != 3 else self.__typeSizes[typeName] * (vecSize + 1)
        baseOffset = self.__typeSizes[typeName] * vecSize
        return self.__addArray(f"{self.__vecTypes[typeName]}{vecSize}", name, baseAligement, baseOffset, num)

    def addMat(self, name: str, typeName: str, cols: int, rows: int) -> int:
        rowsOffsets = []
        if rows in [1, 2, 3, 4]:
            if rows == 1:
                rowsOffsets = self.addScalarArray(name, typeName, cols)
            else:
                rowsOffsets = self.addVecArray(name, typeName, rows, cols)

            matValue = self.__values[-1]
            matValue.setName(name)
            matValue.setTypeName(f"{self.__matTypes[typeName]}{ f'{cols}x{rows}' if cols != rows else f'{cols}' }")

        else:
            print("Podano złą liczbę wierszy")
        return rowsOffsets[0] if len(rowsOffsets) != 0 else rowsOffsets

    def addMatArray(self, name: str, typeName: str, cols: int, rows: int, num: int) -> list[int]:
        matOffsets = []
        for i in range(num):
            matOffsets.append(self.addMat(f"{name}[{i}]", typeName, cols, rows))
        
        firstValue = self.__values[-len(matOffsets)]
        lastValue = self.__values[-1]
        lastValuePadding = 0 if lastValue.getPadding() is None else lastValue.getPadding()

        self.__values.append(StructValue(name,
                                         (lastValue.getAligementOffset() + lastValue.getSize() + lastValuePadding) - firstValue.getAligementOffset(),
                                         f"{self.__matTypes[typeName]}{ f'{cols}x{rows}' if cols != rows else f'{cols}'}[{num}]",
                                         firstValue.getBaseAligement(),
                                         firstValue.getAligementOffset(),
                                         firstValue.getBaseOffset(),
                                         0
                                         ))
        
        for i in range(num):
            self.__values[-1].append(self.__values[-(num - i) - 1])
            self.__values.pop(-(num - i) - 1)

        if self.__baseOffset % 16 != 0:
            self.__values[-1].setPadding(16 - (self.__baseOffset % 16))
            self.__baseOffset += 16 - (self.__baseOffset % 16)
        
        return matOffsets

    def addSqrMat(self, name: str, typeName: str, size: int) -> int:
        return self.addMat(name, typeName, size, size)

    def addSqrMatArray(self, name: str, typeName: str, size: int, num: int) -> list[int]:
        return self.addMatArray(name, typeName, size, size, num)

    def addStruct(self, name: str, struct) -> int:
        offset = self.__add("struct", name, struct.getBaseAligement(), struct.__baseOffset)
        for value in struct.__values:
            c : StructValue = value.copy()
            c.setBaseOffset(c.getBaseOffset() + offset)
            self.__values[-1].append(c)
        
        self.__values[-1].setPadding(0)
        if self.__baseOffset % 16 != 0:
            self.__values[-1].setPadding(16 - (self.__baseOffset % 16))
            self.__baseOffset += 16 - (self.__baseOffset % 16)

        return offset

    def addStructArray(self, name: str, struct, num: int) -> list[int]:
        offsets = []
        for i in range(num):
            offsets.append(self.addStruct(f"{name}[{i}]", struct))

        firstValue = self.__values[-len(offsets)]
        lastValue = self.__values[-1]
        lastValuePadding = 0 if lastValue.getPadding() is None else lastValue.getPadding()

        self.__values.append(StructValue(name,
                                         (lastValue.getAligementOffset() + lastValue.getSize() + lastValuePadding) - firstValue.getAligementOffset(),
                                        f"struct[{num}]",
                                        firstValue.getBaseAligement(),
                                        firstValue.getAligementOffset(),
                                        firstValue.getBaseOffset(),
                                        0))
        
        for i in range(num):
            self.__values[-1].append(self.__values[-(num - i) - 1])
            self.__values.pop(-(num - i) - 1)
        
        if self.__baseOffset % 16 != 0:
            self.__values[-1].setPadding(16 - (self.__baseOffset % 16))
            self.__baseOffset += 16 - (self.__baseOffset % 16)

        return offsets

    def getValue(self, name: str) -> StructValue:
        names = name.split('.')
        arrayName = names[0] if names[0].find('[') != -1 else None
        valueName = names[0] if arrayName is None else names[0].split('[')[0]
        subValueName = '.'.join([names[i] for i in range(len(names)) if i != 0]) if len(names) > 1 else None
        if arrayName is not None:
            if subValueName is None:
                subValueName = arrayName
            else:
                subValueName = arrayName + '.' + subValueName
        for value in self.__values:
            if value.getName() == valueName:
                if subValueName is None:
                    return value
                else:
                    return value.getSubValue(subValueName)
        return None

    def getBaseAligement(self) -> int:
        baseAligement = self.__maxAligement
        if (baseAligement % 16 != 0):
            baseAligement += 16 - (baseAligement % 16)
        return baseAligement

    def getStructSize(self) -> int:
        size = self.__baseOffset
        if size % 16 != 0:
            size += 16 - (size % 16)
        return size
    
    def __str__(self) -> str:
        text = "Struct layout STD140 (ALL VALUES IN BYTES):\n"        
        for value in self.__values:
            text += value.print("  ")
        return text