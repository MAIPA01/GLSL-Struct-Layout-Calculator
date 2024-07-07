from structValue import *

class STD140Struct:
    def __init__(self):
        self.__baseOffset : int = 0
        self.__values : list[StructValue] = []
        self.__maxAligement : int = 0
        self.__typeSizes : dict[str, int] = { "bool" : 4, "int" : 4, "uint" : 4, "float" : 4, "double" : 8 }
        self.__vecTypes : dict[str, str] = { "bool" : "bvec", "int" : "ivec", "uint" : "uvec", "float" : "vec", "double" : "dvec" }
        self.__matTypes : dict[str, str] = { "bool" : "bmat", "int" : "imat", "uint" : "umat", "float" : "mat", "double" : "dmat" }

# PRIVATE ADD FUNCTIONS

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

# GENERAL ADD FUNCTIONS

    def addScalar(self, name: str, typeName: str) -> int:
        return self.__add(typeName, name, self.__typeSizes[typeName], self.__typeSizes[typeName])

    def addScalarArray(self, name: str, typeName: str, num: int) -> list[int]:
        return self.__addArray(typeName, name, self.__typeSizes[typeName], self.__typeSizes[typeName], num)

    def addVector(self, name: str, typeName: str, length: int) -> int:
        baseAligement = self.__typeSizes[typeName] * length if length != 3 else self.__typeSizes[typeName] * (length + 1)
        baseOffset = self.__typeSizes[typeName] * length
        return self.__add(f"{self.__vecTypes[typeName]}{length}", name, baseAligement, baseOffset)

    def addVectorArray(self, name: str, typeName: str, length: int, num: int) -> list[int]:
        baseAligement = self.__typeSizes[typeName] * length if length != 3 else self.__typeSizes[typeName] * (length + 1)
        baseOffset = self.__typeSizes[typeName] * length
        return self.__addArray(f"{self.__vecTypes[typeName]}{length}", name, baseAligement, baseOffset, num)

    def addMatrix(self, name: str, typeName: str, cols: int, rows: int) -> int:
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

    def addMatrixArray(self, name: str, typeName: str, cols: int, rows: int, num: int) -> list[int]:
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

    def addSquareMatrix(self, name: str, typeName: str, size: int) -> int:
        return self.addMat(name, typeName, size, size)

    def addSquareMatrixArray(self, name: str, typeName: str, size: int, num: int) -> list[int]:
        return self.addMatArray(name, typeName, size, size, num)

# SPECIFIED ADD FUNCTIONS

    def addBool(self, name: str) -> int:
        return self.addScalar(name, BOOL)

    def addBoolArray(self, name: str, num: int) -> list[int]:
        return self.addScalarArray(name, BOOL, num)

    def addInt(self, name: str) -> int:
        return self.addScalar(name, INT)

    def addIntArray(self, name: str, num: int) -> list[int]:
        return self.addScalarArray(name, INT, num)

    def addUint(self, name: str) -> int:
        return self.addScalar(name, UINT)

    def addUintArray(self, name: str, num: int) -> list[int]:
        return self.addScalarArray(name, UINT, num)

    def addFloat(self, name: str) -> int:
        return self.addScalar(name, FLOAT)

    def addFloatArray(self, name: str, num: int) -> list[int]:
        return self.addScalarArray(name, FLOAT, num)

    def addDouble(self, name: str) -> int:
        return self.addScalar(name, DOUBLE)

    def addDoubleArray(self, name: str, num: int) -> list[int]:
        return self.addScalarArray(name, DOUBLE, num)

##########################################

    def addBVec(self, name: str, length: int) -> int:
        return self.addVector(name, BOOL, length)

    def addBVecArray(self, name: str, length: int, num: int) -> list[int]:
        return self.addVectorArray(name, BOOL, length, num)

    def addIVec(self, name: str, length: int) -> int:
        return self.addVector(name, INT, length)

    def addIVecArray(self, name: str, length: int, num: int) -> list[int]:
        return self.addVectorArray(name, INT, length, num)

    def addUVec(self, name: str, length: int) -> int:
        return self.addVector(name, UINT, length)

    def addUVecArray(self, name: str, length: int, num: int) -> list[int]:
        return self.addVectorArray(name, UINT, length, num)

    def addVec(self, name: str, length: int) -> int:
        return self.addVector(name, FLOAT, length)

    def addVecArray(self, name: str, length: int, num: int) -> list[int]:
        return self.addVectorArray(name, FLOAT, length, num)

    def addDVec(self, name: str, length: int) -> int:
        return self.addVector(name, DOUBLE, length)

    def addDVecArray(self, name: str, length: int, num: int) -> list[int]:
        return self.addVectorArray(name, DOUBLE, length, num)

###################################

    def addBMat(self, name: str, cols: int, rows: int) -> int:
        return self.addMatrix(name, BOOL, cols, rows)

    def addBMatArray(self, name: str, cols: int, rows: int, num: int) -> list[int]:
        return self.addMatrixArray(name, BOOL, cols, rows, num)

    def addIMat(self, name: str, cols: int, rows: int) -> int:
        return self.addMatrix(name, INT, cols, rows)

    def addIMatArray(self, name: str, cols: int, rows: int, num: int) -> list[int]:
        return self.addMatrixArray(name, INT, cols, rows, num)

    def addUMat(self, name: str, cols: int, rows: int) -> int:
        return self.addMatrix(name, UINT, cols, rows)

    def addUMatArray(self, name: str, cols: int, rows: int, num: int) -> list[int]:
        return self.addMatrixArray(name, UINT, cols, rows, num)

    def addMat(self, name: str, cols: int, rows: int) -> int:
        return self.addMatrix(name, FLOAT, cols, rows)

    def addMatArray(self, name: str, cols: int, rows: int, num: int) -> list[int]:
        return self.addMatrixArray(name, FLOAT, cols, rows, num)

    def addDMat(self, name: str, cols: int, rows: int) -> int:
        return self.addMatrix(name, DOUBLE, cols, rows)

    def addDMatArray(self, name: str, cols: int, rows: int, num: int) -> list[int]:
        return self.addMatrixArray(name, DOUBLE, cols, rows, num)

###################################

    def addSqrBMat(self, name: str, size: int) -> int:
        return self.addSquareMatrix(name, BOOL, size)

    def addSqrBMatArray(self, name: str, size: int, num: int) -> list[int]:
        return self.addSquareMatrixArray(name, BOOL, size, num)

    def addSqrIMat(self, name: str, size: int) -> int:
        return self.addSquareMatrix(name, INT, size)

    def addSqrIMatArray(self, name: str, size: int, num: int) -> list[int]:
        return self.addSquareMatrixArray(name, INT, size, num)

    def addSqrUMat(self, name: str, size: int) -> int:
        return self.addSquareMatrix(name, UINT, size)

    def addSqrUMatArray(self, name: str, size: int, num: int) -> list[int]:
        return self.addSquareMatrixArray(name, UINT, size, num)

    def addSqrMat(self, name: str, size: int) -> int:
        return self.addSquareMatrix(name, FLOAT, size)

    def addSqrMatArray(self, name: str, size: int, num: int) -> list[int]:
        return self.addSquareMatrixArray(name, FLOAT, size, num)

    def addSqrDMat(self, name: str, size: int) -> int:
        return self.addSquareMatrix(name, DOUBLE, size)

    def addSqrDMatArray(self, name: str, size: int, num: int) -> list[int]:
        return self.addSquareMatrixArray(name, DOUBLE, size, num)

#####################################

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