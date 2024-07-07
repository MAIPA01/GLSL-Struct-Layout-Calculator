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