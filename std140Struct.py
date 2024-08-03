from structValue import *

class STD140Struct:
    __typeSizes : dict[str, int] = { StructValue.BOOL : 4, StructValue.INT : 4, StructValue.UINT : 4, StructValue.FLOAT : 4, StructValue.DOUBLE : 8 }
    __vecTypes : dict[str, str] = { StructValue.BOOL : "bvec", StructValue.INT : "ivec", StructValue.UINT : "uvec", StructValue.FLOAT : "vec", StructValue.DOUBLE : "dvec" }
    __matTypes : dict[str, str] = { StructValue.BOOL : "bmat", StructValue.INT : "imat", StructValue.UINT : "umat", StructValue.FLOAT : "mat", StructValue.DOUBLE : "dmat" }

    def __init__(self):
        self.reset()

# PRIVATE ADD FUNCTIONS

    def __addValue(self, name: str, typeName: str, size: int, baseAligement: int, baseOffset: int, aligementOffset: int, padding: int | None = None) -> None:
        self.__values.append(StructValue(name, typeName, size, baseAligement, baseOffset, aligementOffset, padding))

    def __add(self, name: str, typeName: str, baseAligement: int, baseOffset: int) -> int:
        aligementOffset = self.__baseOffset
        if self.__baseOffset % baseAligement != 0:
            aligementOffset += baseAligement - (self.__baseOffset % baseAligement)
        
        self.__addValue(name, typeName, baseOffset, baseAligement, aligementOffset, self.__baseOffset)

        self.__baseOffset = aligementOffset + baseOffset
        if baseAligement > self.__maxAligement:
            self.__maxAligement = baseAligement
        return aligementOffset

    def __addArray(self, name: str, typeName: str, baseAligement: int, baseOffset: int, num: int) -> list[int]:
        if baseAligement % 16 != 0:
            baseAligement += 16 - (baseAligement % 16)

        aligementOffsets = []
        for i in range(num):
            aligementOffsets.append(self.__add(f"{name}[{i}]", typeName, baseAligement, baseOffset))

        firstValue = self.__values[-len(aligementOffsets)]
        lastValue = self.__values[-1]
        lastValuePadding = 0 if lastValue.getPadding() is None else lastValue.getPadding()

        self.__addValue(name,
                        f"{typeName}[{num}]",
                        (lastValue.getAligementOffset() + lastValue.getSize() + lastValuePadding) - firstValue.getAligementOffset(),
                        baseAligement,
                        firstValue.getAligementOffset(),
                        firstValue.getBaseOffset(),
                        0)
        
        for i in range(num):
            self.__values[-1].append(self.__values[-(num - i) - 1])
            self.__values.pop(-(num - i) - 1)
        
        if self.__baseOffset % 16 != 0:
            self.__values[-1].setPadding(16 - (self.__baseOffset % 16))
            self.__baseOffset += 16 - (self.__baseOffset % 16)

        return aligementOffsets

# GENERAL ADD FUNCTIONS

    def addScalar(self, name: str, typeName: str) -> int:
        return self.__add(name, typeName, self.__typeSizes[typeName], self.__typeSizes[typeName])

    def addScalarArray(self, name: str, typeName: str, num: int) -> list[int]:
        return self.__addArray(name, typeName, self.__typeSizes[typeName], self.__typeSizes[typeName], num)

    def addVector(self, name: str, typeName: str, length: int) -> int | None:
        if length < 1 or length > 4:
            return None

        baseAligement = self.__typeSizes[typeName] * length if length != 3 else self.__typeSizes[typeName] * (length + 1)
        baseOffset = self.__typeSizes[typeName] * length
        return self.__add(name, f"{self.__vecTypes[typeName]}{length}", baseAligement, baseOffset)

    def addVectorArray(self, name: str, typeName: str, length: int, num: int) -> list[int] | None:
        if length < 1 or length > 4:
            return None
        
        baseAligement = self.__typeSizes[typeName] * length if length != 3 else self.__typeSizes[typeName] * (length + 1)
        baseOffset = self.__typeSizes[typeName] * length
        return self.__addArray(name, f"{self.__vecTypes[typeName]}{length}", baseAligement, baseOffset, num)

    def addMatrix(self, name: str, typeName: str, cols: int, rows: int) -> int | None:
        if rows < 1 or rows > 4 or cols < 1 or cols > 4:
            return None

        rowsOffsets = []
        if rows in [1, 2, 3, 4]:
            if rows == 1:
                rowsOffsets = self.addScalarArray(name, typeName, cols)
            else:
                rowsOffsets = self.addVectorArray(name, typeName, rows, cols)

            matValue = self.__values[-1]
            matValue.setName(name)
            matValue.setTypeName(f"{self.__matTypes[typeName]}{ f'{cols}x{rows}' if cols != rows else f'{cols}' }")

        else:
            print("Podano złą liczbę wierszy")
        return rowsOffsets[0] if len(rowsOffsets) != 0 else rowsOffsets

    def addMatrixArray(self, name: str, typeName: str, cols: int, rows: int, num: int) -> list[int] | None:
        if rows < 1 or rows > 4 or cols < 1 or cols > 4:
            return None
        
        matOffsets = []
        for i in range(num):
            matOffsets.append(self.addMatrix(f"{name}[{i}]", typeName, cols, rows))
        
        firstValue = self.__values[-len(matOffsets)]
        lastValue = self.__values[-1]
        lastValuePadding = 0 if lastValue.getPadding() is None else lastValue.getPadding()

        self.__addValue(name,
                        f"{self.__matTypes[typeName]}{ f'{cols}x{rows}' if cols != rows else f'{cols}'}[{num}]",
                        (lastValue.getAligementOffset() + lastValue.getSize() + lastValuePadding) - firstValue.getAligementOffset(),
                        firstValue.getBaseAligement(),
                        firstValue.getAligementOffset(),
                        firstValue.getBaseOffset(),
                        0)
        
        for i in range(num):
            self.__values[-1].append(self.__values[-(num - i) - 1])
            self.__values.pop(-(num - i) - 1)

        if self.__baseOffset % 16 != 0:
            self.__values[-1].setPadding(16 - (self.__baseOffset % 16))
            self.__baseOffset += 16 - (self.__baseOffset % 16)
        
        return matOffsets

    def addSquareMatrix(self, name: str, typeName: str, size: int) -> int | None:
        return self.addMatrix(name, typeName, size, size)

    def addSquareMatrixArray(self, name: str, typeName: str, size: int, num: int) -> list[int] | None:
        return self.addMatrixArray(name, typeName, size, size, num)

# SPECIFIED ADD FUNCTIONS

    def addBool(self, name: str) -> int:
        return self.addScalar(name, StructValue.BOOL)

    def addBoolArray(self, name: str, num: int) -> list[int]:
        return self.addScalarArray(name, StructValue.BOOL, num)

    def addInt(self, name: str) -> int:
        return self.addScalar(name, StructValue.INT)

    def addIntArray(self, name: str, num: int) -> list[int]:
        return self.addScalarArray(name, StructValue.INT, num)

    def addUint(self, name: str) -> int:
        return self.addScalar(name, StructValue.UINT)

    def addUintArray(self, name: str, num: int) -> list[int]:
        return self.addScalarArray(name, StructValue.UINT, num)

    def addFloat(self, name: str) -> int:
        return self.addScalar(name, StructValue.FLOAT)

    def addFloatArray(self, name: str, num: int) -> list[int]:
        return self.addScalarArray(name, StructValue.FLOAT, num)

    def addDouble(self, name: str) -> int:
        return self.addScalar(name, StructValue.DOUBLE)

    def addDoubleArray(self, name: str, num: int) -> list[int]:
        return self.addScalarArray(name, StructValue.DOUBLE, num)

##########################################

    def addBVec(self, name: str, length: int) -> int | None:
        return self.addVector(name, StructValue.BOOL, length)

    def addBVecArray(self, name: str, length: int, num: int) -> list[int] | None:
        return self.addVectorArray(name, StructValue.BOOL, length, num)

    def addIVec(self, name: str, length: int) -> int | None:
        return self.addVector(name, StructValue.INT, length)

    def addIVecArray(self, name: str, length: int, num: int) -> list[int] | None:
        return self.addVectorArray(name, StructValue.INT, length, num)

    def addUVec(self, name: str, length: int) -> int | None:
        return self.addVector(name, StructValue.UINT, length)

    def addUVecArray(self, name: str, length: int, num: int) -> list[int] | None:
        return self.addVectorArray(name, StructValue.UINT, length, num)

    def addVec(self, name: str, length: int) -> int | None:
        return self.addVector(name, StructValue.FLOAT, length)

    def addVecArray(self, name: str, length: int, num: int) -> list[int] | None:
        return self.addVectorArray(name, StructValue.FLOAT, length, num)

    def addDVec(self, name: str, length: int) -> int | None:
        return self.addVector(name, StructValue.DOUBLE, length)

    def addDVecArray(self, name: str, length: int, num: int) -> list[int] | None:
        return self.addVectorArray(name, StructValue.DOUBLE, length, num)

###################################

    def addBMat(self, name: str, cols: int, rows: int) -> int | None:
        return self.addMatrix(name, StructValue.BOOL, cols, rows)

    def addBMatArray(self, name: str, cols: int, rows: int, num: int) -> list[int] | None:
        return self.addMatrixArray(name, StructValue.BOOL, cols, rows, num)

    def addIMat(self, name: str, cols: int, rows: int) -> int | None:
        return self.addMatrix(name, StructValue.INT, cols, rows)

    def addIMatArray(self, name: str, cols: int, rows: int, num: int) -> list[int] | None:
        return self.addMatrixArray(name, StructValue.INT, cols, rows, num)

    def addUMat(self, name: str, cols: int, rows: int) -> int | None:
        return self.addMatrix(name, StructValue.UINT, cols, rows)

    def addUMatArray(self, name: str, cols: int, rows: int, num: int) -> list[int] | None:
        return self.addMatrixArray(name, StructValue.UINT, cols, rows, num)

    def addMat(self, name: str, cols: int, rows: int) -> int | None:
        return self.addMatrix(name, StructValue.FLOAT, cols, rows)

    def addMatArray(self, name: str, cols: int, rows: int, num: int) -> list[int] | None:
        return self.addMatrixArray(name, StructValue.FLOAT, cols, rows, num)

    def addDMat(self, name: str, cols: int, rows: int) -> int | None:
        return self.addMatrix(name, StructValue.DOUBLE, cols, rows)

    def addDMatArray(self, name: str, cols: int, rows: int, num: int) -> list[int] | None:
        return self.addMatrixArray(name, StructValue.DOUBLE, cols, rows, num)

###################################

    def addSqrBMat(self, name: str, size: int) -> int | None:
        return self.addSquareMatrix(name, StructValue.BOOL, size)

    def addSqrBMatArray(self, name: str, size: int, num: int) -> list[int] | None:
        return self.addSquareMatrixArray(name, StructValue.BOOL, size, num)

    def addSqrIMat(self, name: str, size: int) -> int | None:
        return self.addSquareMatrix(name, StructValue.INT, size)

    def addSqrIMatArray(self, name: str, size: int, num: int) -> list[int] | None:
        return self.addSquareMatrixArray(name, StructValue.INT, size, num)

    def addSqrUMat(self, name: str, size: int) -> int | None:
        return self.addSquareMatrix(name, StructValue.UINT, size)

    def addSqrUMatArray(self, name: str, size: int, num: int) -> list[int] | None:
        return self.addSquareMatrixArray(name, StructValue.UINT, size, num)

    def addSqrMat(self, name: str, size: int) -> int | None:
        return self.addSquareMatrix(name, StructValue.FLOAT, size)

    def addSqrMatArray(self, name: str, size: int, num: int) -> list[int] | None:
        return self.addSquareMatrixArray(name, StructValue.FLOAT, size, num)

    def addSqrDMat(self, name: str, size: int) -> int | None:
        return self.addSquareMatrix(name, StructValue.DOUBLE, size)

    def addSqrDMatArray(self, name: str, size: int, num: int) -> list[int] | None:
        return self.addSquareMatrixArray(name, StructValue.DOUBLE, size, num)

#####################################

    def addStruct(self, name: str, struct: Self) -> int:
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

    def addStructArray(self, name: str, struct: Self, num: int) -> list[int]:
        offsets = []
        for i in range(num):
            offsets.append(self.addStruct(f"{name}[{i}]", struct))

        firstValue = self.__values[-len(offsets)]
        lastValue = self.__values[-1]
        lastValuePadding = 0 if lastValue.getPadding() is None else lastValue.getPadding()

        self.__addValue(name,
                        f"struct[{num}]",
                        (lastValue.getAligementOffset() + lastValue.getSize() + lastValuePadding) - firstValue.getAligementOffset(),
                        firstValue.getBaseAligement(),
                        firstValue.getAligementOffset(),
                        firstValue.getBaseOffset(),
                        0)
        
        for i in range(num):
            self.__values[-1].append(self.__values[-(num - i) - 1])
            self.__values.pop(-(num - i) - 1)
        
        if self.__baseOffset % 16 != 0:
            self.__values[-1].setPadding(16 - (self.__baseOffset % 16))
            self.__baseOffset += 16 - (self.__baseOffset % 16)

        return offsets

# OPTIMALIZER

    def getLostBytes(self) -> int:
        lostBytes = self.getStructSize() - self.__baseOffset
        for value in self.__values:
            lostBytes += value.getLostBytes()
        return lostBytes

    def optimalize(self) -> None:
        sortedValues : list[StructValue] = self.__values.copy()
        sortedValues.sort()
        
        tempValues = []
        baseOffset = 0
        while len(tempValues) != len(self.__values):
            choosedValue = None
            for value in sortedValues:
                if baseOffset % value.getBaseAligement() == 0:
                    choosedValue = value
                    break
            
            if choosedValue is None:
                best = baseOffset % sortedValues[0].getBaseAligement()
                choosedValue = sortedValues[0]
                for value in sortedValues[1:]:
                    if baseOffset % value.getBaseAligement() < best:
                        choosedValue = value
                        
            choosedValue.setBaseOffset(baseOffset)
            choosedValue.setAligementOffset(baseOffset)
            if choosedValue.getAligementOffset() % choosedValue.getBaseAligement() != 0:
                choosedValue.setAligementOffset(choosedValue.getAligementOffset() + choosedValue.getBaseAligement() - (baseOffset % choosedValue.getBaseAligement()))
            tempValues.append(choosedValue)
            
            baseOffset = choosedValue.getAligementOffset() + choosedValue.getSize()
            if choosedValue.getPadding() is not None:
                baseOffset += choosedValue.getPadding()
            
            sortedValues.remove(choosedValue)
        
        self.__values = tempValues
        self.__baseOffset = baseOffset

# CLEANER

    def reset(self) -> None:
        self.__baseOffset : int = 0
        self.__values : list[StructValue] = []
        self.__maxAligement : int = 0

# GETTERS

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

    def getBaseOffset(self) -> int:
        return self.__baseOffset

    def getSize(self) -> int:
        size = self.__baseOffset
        if size % 16 != 0:
            size += 16 - (size % 16)
        return size
    
    def getInfo(self, short: bool = True, extended: bool = True) -> str:
        text = "Struct layout STD140 (ALL VALUES IN BYTES):\n"
        for value in self.__values:
            text += f'{value.getInfo(short, extended, "  ")}\n'
        return text

    def __str__(self) -> str:
        return self.getInfo()

    def __repr__(self) -> str:
        return self.getInfo(False)