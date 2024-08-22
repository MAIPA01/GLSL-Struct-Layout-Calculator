# BASE ALIGENMENT AND STRIDE OF ARRAYS OF SCALARS AND VECTORS IN RULE 4 
# AND STRUCTURES IN RULE 9 ARE NOT ROUNDED UP A MULTIPLE OF THE BASE ALIGNEMNT OF VEC4

from std140Struct import *
from structValue import *

class STD430Struct(STD140Struct):

# PRIVATE ADD FUNCTIONS

    def _addArray(self, name: str, typeName: str, baseAligement: int, baseOffset: int, num: int) -> list[int]:
        aligementOffsets = []
        for i in range(num):
            aligementOffsets.append(self._add(f"{name}[{i}]", typeName, baseAligement, baseOffset))

        firstValue = self._values[-len(aligementOffsets)]
        lastValue = self._values[-1]
        lastValuePadding = 0 if lastValue.getPadding() is None else lastValue.getPadding()

        self._addValue(name,
                        f"{typeName}[{num}]",
                        (lastValue.getAligementOffset() + lastValue.getSize() + lastValuePadding) - firstValue.getAligementOffset(),
                        baseAligement,
                        firstValue.getAligementOffset(),
                        firstValue.getBaseOffset(),
                        0)
        
        for i in range(num):
            self._values[-1].append(self._values[-(num - i) - 1])
            self._values.pop(-(num - i) - 1)
        
        if self._baseOffset % 16 != 0:
            self._values[-1].setPadding(16 - (self._baseOffset % 16))
            self._baseOffset += 16 - (self._baseOffset % 16)

        return aligementOffsets

#####################################

    def addStruct(self, name: str, struct: Self) -> int:
        offset = self._add("struct", name, struct.getBaseAligement(), struct._baseOffset)
        for value in struct._values:
            c : StructValue = value.copy()
            c.setBaseOffset(c.getBaseOffset() + offset)
            self._values[-1].append(c)
        
        self._values[-1].setPadding(0)
        if self._baseOffset % 16 != 0:
            self._values[-1].setPadding(16 - (self._baseOffset % 16))
            self._baseOffset += 16 - (self._baseOffset % 16)

        return offset

    def addStructArray(self, name: str, struct: Self, num: int) -> list[int]:
        offsets = []
        for i in range(num):
            offsets.append(self.addStruct(f"{name}[{i}]", struct))

        firstValue = self._values[-len(offsets)]
        lastValue = self._values[-1]
        lastValuePadding = 0 if lastValue.getPadding() is None else lastValue.getPadding()

        self._values.append(StructValue(name,
                                        f"struct[{num}]",
                                        (lastValue.getAligementOffset() + lastValue.getSize() + lastValuePadding) - firstValue.getAligementOffset(),
                                        firstValue.getBaseAligement(),
                                        firstValue.getAligementOffset(),
                                        firstValue.getBaseOffset(),
                                        0))
        
        for i in range(num):
            self._values[-1].append(self._values[-(num - i) - 1])
            self._values.pop(-(num - i) - 1)
        
        if self._baseOffset % 16 != 0:
            self._values[-1].setPadding(16 - (self._baseOffset % 16))
            self._baseOffset += 16 - (self._baseOffset % 16)

        return offsets

# GETTERS

    def getBaseAligement(self) -> int:
        return self._maxAligement
    
    def getInfo(self, short: bool = True, extended: bool = True) -> str:
        text = "Struct layout STD430 (ALL VALUES IN BYTES):\n"
        for value in self._values:
            text += f'{value.getInfo(short, extended, "  ")}\n'
        return text