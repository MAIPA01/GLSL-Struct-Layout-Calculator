from typing import Self

class StructValue:
    BOOL = "bool"
    INT = "int"
    UINT = "uint"
    FLOAT = "float"
    DOUBLE = "double"

    __BLUE = "\033[94m"
    __GREEN = "\033[92m"
    __YELLOW = "\033[93m"
    __RESET = "\033[0m"

    def __init__(self, name: str, typeName: str, size: int, baseAligement: int, aligementOffset: int, baseOffset: int, padding: int | None = None):
        self.__name: str = name
        self.__typeName: str = typeName
        self.__size: int = size
        self.__baseAligement: int = baseAligement
        self.__aligementOffset: int = aligementOffset
        self.__baseOffset: int = baseOffset
        self.__padding: int | None = padding
        self.__subValues: list[Self] = []

    def append(self, value: Self) -> None:
        self.__subValues.append(value)

    def setName(self, name: str) -> None:
        self.__name = name

    def setTypeName(self, typeName: str) -> None:
        self.__typeName = typeName

    def setBaseOffset(self, baseOffset: int) -> None:
        diff = baseOffset - self.__baseOffset
        self.__baseOffset += diff
        self.__aligementOffset += diff
        if self.__aligementOffset < 0:
            self.__aligementOffset = 0
        for value in self.__subValues:
            value.setBaseOffset(value.getBaseOffset() + diff)
        if self.__padding is not None:
            baseOffset = self.__aligementOffset + self.__size
            if baseOffset % 16 != 0:
                self.__padding = 16 - (baseOffset % 16)
            else:
                self.__padding = 0

    def setAligementOffset(self, aligementOffset: int) -> None:
        diff = aligementOffset - self.__aligementOffset
        self.__baseOffset += diff
        if self.__baseOffset < 0:
            self.__baseOffset = 0
        self.__aligementOffset += diff
        for value in self.__subValues:
            value.setAligementOffset(value.getAligementOffset() + diff)
        if self.__padding is not None:
            baseOffset = self.__aligementOffset + self.__size
            if baseOffset % 16 != 0:
                self.__padding = 16 - (baseOffset % 16)
            else:
                self.__padding = 0

    def setPadding(self, padding: int|None) -> None:
        self.__padding = padding

    def getName(self) -> str:
        return self.__name

    def getBaseOffset(self) -> int:
        return self.__baseOffset

    def getBaseAligement(self) -> int:
        return self.__baseAligement
    
    def getTypeName(self) -> str:
        return self.__typeName
    
    def getAligementOffset(self) -> int:
        return self.__aligementOffset

    def getSize(self) -> int:
        return self.__size

    def getPadding(self) -> int | None:
        return self.__padding
    
    def getLostBytes(self) -> int:
        lostBytes = self.__aligementOffset - self.__baseOffset

        for subValue in self.__subValues:
            lostBytes += subValue.getLostBytes()

        if self.__padding is not None:
            lostBytes += self.__padding
        return lostBytes

    def getSubValuesCount(self) -> int:
        return len(self.__subValues)

    def getSubValue(self, name: str) -> Self:
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

    def getInfo(self, short: bool = False, extended: bool = False, indent: str = "") -> str:
        info = f"{indent}- {self.__BLUE}{self.__typeName} {self.__GREEN}{self.__name}{self.__RESET}"
        if not short:
            info += f": base size {self.__YELLOW}{self.__size}{self.__RESET}, base align {self.__YELLOW}{self.__baseAligement}{self.__RESET}, base off. {self.__YELLOW}{self.__baseOffset}{self.__RESET}, align off. {self.__YELLOW}{self.__aligementOffset}{self.__RESET}"
        
        if extended:
            if len(self.__subValues) > 0:
                info += "\n"
                if len(self.__subValues) > 1:
                    for subValue in self.__subValues[:-1]:
                        info += f'{subValue.getInfo(short, extended, indent + "  ")}\n'
                info += self.__subValues[-1].getInfo(short, extended, indent + "  ")
            if self.__padding is not None and not short:
                info += f"\n{indent + '  '}- End padding of {self.__GREEN}{self.__name}{self.__RESET}: base size {self.__YELLOW}{self.__padding}{self.__RESET}, base off. {self.__YELLOW}{self.__aligementOffset + self.__size}{self.__RESET}, align off. {self.__YELLOW}{self.__aligementOffset + self.__size + self.__padding}{self.__RESET}"
        return info

    def copy(self) -> Self:
        c = StructValue(self.__name, 
                        self.__typeName,
                        self.__size,
                        self.__baseAligement,
                        self.__aligementOffset,
                        self.__baseOffset,
                        self.__padding)
        for value in self.__subValues:
            c.append(value.copy())
        return c

    def __lt__(self, other) -> bool:
        if isinstance(other, StructValue):
            return not (other.__baseAligement > self.__baseAligement or (other.__baseAligement == self.__baseAligement and other.__size > self.__size))
        else:
            return False

    def __str__(self) -> str:
        return self.getInfo()

    def __repr__(self) -> str:
        return self.getInfo(extended=True)