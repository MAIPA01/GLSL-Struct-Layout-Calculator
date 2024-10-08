from std140Struct import *
from std430Struct import *
import unittest

class Std140Tests(unittest.TestCase):

    struct = STD140Struct()

    def updateBaseOffset(self, bo: int, ba: int, size: int) -> int:
        if bo % ba != 0:
            bo += ba - (bo % ba)
        bo += size
        return bo

    def updateAligement(self, bo: int, ba: int) -> int:
        if bo % ba != 0:
            bo += ba - (bo % ba)
        return bo

    def updateBaseOffsetArray(self, bo: int, size: int, ba: int, num: int) -> int:
        for _ in range(num):
            if bo % ba != 0:
                bo += ba - (bo % ba)
            bo += size
        if num > 0:
            if bo % ba != 0:
                bo += ba - (bo % ba)
        return bo

    def test_AddScalars(self):
        # Add Scalar Func
        self.struct.reset()

        # Bool
        self.assertEqual(self.struct.addScalar("Bool1", StructValue.BOOL), 0)
        self.assertEqual(self.struct.addBool("Bool2"), 4)

        # Int
        self.assertEqual(self.struct.addScalar("Int1", StructValue.INT), 8)
        self.assertEqual(self.struct.addInt("Int2"), 12)

        # Uint
        self.assertEqual(self.struct.addScalar("Uint1", StructValue.UINT), 16)
        self.assertEqual(self.struct.addUint("Uint2"), 20)

        # Float
        self.assertEqual(self.struct.addScalar("Float1", StructValue.FLOAT), 24)
        self.assertEqual(self.struct.addFloat("Float2"), 28)

        # Double
        self.assertEqual(self.struct.addScalar("Double1", StructValue.DOUBLE), 32)
        self.assertEqual(self.struct.addDouble("Double2"), 40)

    def test_AddScalarsArray(self):
        # Add Scalar Array Func
        self.struct.reset()

        # Bool
        self.assertEqual(self.struct.addScalarArray("Bool1", StructValue.BOOL, 2), [0, 16])
        self.assertEqual(self.struct.addBoolArray("Bool2", 2), [32, 48])

        # Int
        self.assertEqual(self.struct.addScalarArray("Int1", StructValue.INT, 2), [64, 80])
        self.assertEqual(self.struct.addIntArray("Int2", 2), [96, 112])

        # Uint
        self.assertEqual(self.struct.addScalarArray("Uint1", StructValue.UINT, 2), [128, 144])
        self.assertEqual(self.struct.addUintArray("Uint2", 2), [160, 176])

        # Float
        self.assertEqual(self.struct.addScalarArray("Float1", StructValue.FLOAT, 2), [192, 208])
        self.assertEqual(self.struct.addFloatArray("Float2", 2), [224, 240])

        # Double
        self.assertEqual(self.struct.addScalarArray("Double1", StructValue.DOUBLE, 2), [256, 272])
        self.assertEqual(self.struct.addDoubleArray("Double2", 2), [288, 304])

    def test_AddVectors(self):
        # Add Vector Func

        # length 1 - 5
        for length in range(1, 6):
            self.struct.reset()

            if length == 1 or length == 5:
                # Bool
                self.assertEqual(self.struct.addVector("Bool1", StructValue.BOOL, length), None)
                self.assertEqual(self.struct.addBVec("Bool2", length), None)

                # Int
                self.assertEqual(self.struct.addVector("Int1", StructValue.INT, length), None)
                self.assertEqual(self.struct.addIVec("Int2", length), None)

                # Uint
                self.assertEqual(self.struct.addVector("Uint1", StructValue.UINT, length), None)
                self.assertEqual(self.struct.addUVec("Uint2", length), None)

                # Float
                self.assertEqual(self.struct.addVector("Float1", StructValue.FLOAT, length), None)
                self.assertEqual(self.struct.addVec("Float2", length), None)

                # Double
                self.assertEqual(self.struct.addVector("Double1", StructValue.DOUBLE, length), None)
                self.assertEqual(self.struct.addDVec("Double2", length), None)
            else:
                baseOffset = 0
                baseAligement = length if length != 3 else 4

                # Bool
                baseOffset = self.updateAligement(baseOffset, baseAligement * 4)
                self.assertEqual(self.struct.addVector("Bool1", StructValue.BOOL, length), baseOffset)
                baseOffset = self.updateBaseOffset(baseOffset, baseAligement * 4, length * 4)
                
                baseOffset = self.updateAligement(baseOffset, baseAligement * 4)
                self.assertEqual(self.struct.addBVec("Bool2", length), baseOffset)
                baseOffset = self.updateBaseOffset(baseOffset, baseAligement * 4, length * 4)

                # Int
                baseOffset = self.updateAligement(baseOffset, baseAligement * 4)
                self.assertEqual(self.struct.addVector("Int1", StructValue.INT, length), baseOffset)
                baseOffset = self.updateBaseOffset(baseOffset, baseAligement * 4, length * 4)
                
                baseOffset = self.updateAligement(baseOffset, baseAligement * 4)
                self.assertEqual(self.struct.addIVec("Int2", length), baseOffset)
                baseOffset = self.updateBaseOffset(baseOffset, baseAligement * 4, length * 4)

                # Uint
                baseOffset = self.updateAligement(baseOffset, baseAligement * 4)
                self.assertEqual(self.struct.addVector("Uint1", StructValue.UINT, length), baseOffset)
                baseOffset = self.updateBaseOffset(baseOffset, baseAligement * 4, length * 4)
                
                baseOffset = self.updateAligement(baseOffset, baseAligement * 4)
                self.assertEqual(self.struct.addUVec("Uint2", length), baseOffset)
                baseOffset = self.updateBaseOffset(baseOffset, baseAligement * 4, length * 4)

                # Float
                baseOffset = self.updateAligement(baseOffset, baseAligement * 4)
                self.assertEqual(self.struct.addVector("Float1", StructValue.FLOAT, length), baseOffset)
                baseOffset = self.updateBaseOffset(baseOffset, baseAligement * 4, length * 4)
                
                baseOffset = self.updateAligement(baseOffset, baseAligement * 4)
                self.assertEqual(self.struct.addVec("Float2", length), baseOffset)
                baseOffset = self.updateBaseOffset(baseOffset, baseAligement * 4, length * 4)

                # Double
                baseOffset = self.updateAligement(baseOffset, baseAligement * 8)
                self.assertEqual(self.struct.addVector("Double1", StructValue.DOUBLE, length), baseOffset)
                baseOffset = self.updateBaseOffset(baseOffset, baseAligement * 8, length * 8)
                
                baseOffset = self.updateAligement(baseOffset, baseAligement * 8)
                self.assertEqual(self.struct.addDVec("Double2", length), baseOffset)
                baseOffset = self.updateBaseOffset(baseOffset, baseAligement * 8, length * 8)

    def test_AddVectorsArray(self):
        # Add Vector Array Func

        # length 1 - 5
        for length in range(1, 6):
            self.struct.reset()

            if length == 1 or length == 5:
                # Bool
                self.assertEqual(self.struct.addVectorArray("Bool1", StructValue.BOOL, length, 2), None)
                self.assertEqual(self.struct.addBVecArray("Bool2", length, 2), None)

                # Int
                self.assertEqual(self.struct.addVectorArray("Int1", StructValue.INT, length, 2), None)
                self.assertEqual(self.struct.addIVecArray("Int2", length, 2), None)

                # Uint
                self.assertEqual(self.struct.addVectorArray("Uint1", StructValue.UINT, length, 2), None)
                self.assertEqual(self.struct.addUVecArray("Uint2", length, 2), None)

                # Float
                self.assertEqual(self.struct.addVectorArray("Float1", StructValue.FLOAT, length, 2), None)
                self.assertEqual(self.struct.addVecArray("Float2", length, 2), None)

                # Double
                self.assertEqual(self.struct.addVectorArray("Double1", StructValue.DOUBLE, length, 2), None)
                self.assertEqual(self.struct.addDVecArray("Double2", length, 2), None)
            else:
                num = 2
                baseOffset = 0
                baseOffsets = []
                for i in range(num):
                    baseOffsets.append(0)
                    for _ in range(i):
                        baseOffsets[i] = self.updateAligement(baseOffsets[i], 16)
                        baseOffsets[i] = self.updateBaseOffset(baseOffsets[i], 16, 4 * length)
                    baseOffsets[i] = self.updateAligement(baseOffsets[i], 16)

                # Bool
                self.assertEqual(self.struct.addVectorArray("Bool1", StructValue.BOOL, length, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffset(baseOffset, 16, 4 * length)
                baseOffset = self.updateAligement(baseOffset, 16)
                self.assertEqual(self.struct.addBVecArray("Bool2", length, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffset(baseOffset, 16, 4 * length)
                baseOffset = self.updateAligement(baseOffset, 16)

                # Int
                self.assertEqual(self.struct.addVectorArray("Int1", StructValue.INT, length, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffset(baseOffset, 16, 4 * length)
                baseOffset = self.updateAligement(baseOffset, 16)
                self.assertEqual(self.struct.addIVecArray("Int2", length, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffset(baseOffset, 16, 4 * length)
                baseOffset = self.updateAligement(baseOffset, 16)

                # Uint
                self.assertEqual(self.struct.addVectorArray("Uint1", StructValue.UINT, length, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffset(baseOffset, 16, 4 * length)
                baseOffset = self.updateAligement(baseOffset, 16)
                self.assertEqual(self.struct.addUVecArray("Uint2", length, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffset(baseOffset, 16, 4 * length)
                baseOffset = self.updateAligement(baseOffset, 16)

                # Float
                self.assertEqual(self.struct.addVectorArray("Float1", StructValue.FLOAT, length, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffset(baseOffset, 16, 4 * length)
                baseOffset = self.updateAligement(baseOffset, 16)
                self.assertEqual(self.struct.addVecArray("Float2", length, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffset(baseOffset, 16, 4 * length)
                baseOffset = self.updateAligement(baseOffset, 16)

                # Double
                baseAligementSize = 8 * (length if length != 3 else length + 1)
                if baseAligementSize % 16 != 0:
                    baseAligementSize += (16 - (baseAligementSize % 16))

                for i in range(num):
                    baseOffsets[i] = 0
                    for _ in range(i):
                        baseOffsets[i] = self.updateAligement(baseOffsets[i], baseAligementSize)
                        baseOffsets[i] = self.updateBaseOffset(baseOffsets[i], baseAligementSize, 8 * length)
                    baseOffsets[i] = self.updateAligement(baseOffsets[i], baseAligementSize)

                self.assertEqual(self.struct.addVectorArray("Double1", StructValue.DOUBLE, length, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffset(baseOffset, baseAligementSize, 8 * length)
                baseOffset = self.updateAligement(baseOffset, baseAligementSize)
                self.assertEqual(self.struct.addDVecArray("Double2", length, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffset(baseOffset, baseAligementSize, 8 * length)
                baseOffset = self.updateAligement(baseOffset, baseAligementSize)

    def test_AddMatrixes(self):
        # Add Matrix Func

        # 1 - 5 Rows
        for r in range(1, 6):
            # 1 - 5 Columns
            for c in range (1, 6):
                self.struct.reset()

                if r == 1 or r == 5 or c == 1 or c == 5:
                    # Bool
                    self.assertEqual(self.struct.addMatrix("Bool1", StructValue.BOOL, c, r), None)
                    self.assertEqual(self.struct.addBMat("Bool2", c, r), None)

                    # Int
                    self.assertEqual(self.struct.addMatrix("Int1", StructValue.INT, c, r), None)
                    self.assertEqual(self.struct.addIMat("Int2", c, r), None)

                    # Uint
                    self.assertEqual(self.struct.addMatrix("Uint1", StructValue.UINT, c, r), None)
                    self.assertEqual(self.struct.addUMat("Uint2", c, r), None)

                    # Float
                    self.assertEqual(self.struct.addMatrix("Float1", StructValue.FLOAT, c, r), None)
                    self.assertEqual(self.struct.addMat("Float2", c, r), None)

                    # Double
                    self.assertEqual(self.struct.addMatrix("Double1", StructValue.DOUBLE, c, r), None)
                    self.assertEqual(self.struct.addDMat("Double2", c, r), None)
                else:
                    baseOffset = 0

                    # Bool
                    self.assertEqual(self.struct.addMatrix("Bool1", StructValue.BOOL, c, r), baseOffset)
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * r, 16, c)
                    self.assertEqual(self.struct.addBMat("Bool2", c, r), baseOffset)
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * r, 16, c)

                    # Int
                    self.assertEqual(self.struct.addMatrix("Int1", StructValue.INT, c, r), baseOffset)
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * r, 16, c)
                    self.assertEqual(self.struct.addIMat("Int2", c, r), baseOffset)
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * r, 16, c)

                    # Uint
                    self.assertEqual(self.struct.addMatrix("Uint1", StructValue.UINT, c, r), baseOffset)
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * r, 16, c)
                    self.assertEqual(self.struct.addUMat("Uint2", c, r), baseOffset)
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * r, 16, c)

                    # Float
                    self.assertEqual(self.struct.addMatrix("Float1", StructValue.FLOAT, c, r), baseOffset)
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * r, 16, c)
                    self.assertEqual(self.struct.addMat("Float2", c, r), baseOffset)
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * r, 16, c)

                    # Double
                    self.assertEqual(self.struct.addMatrix("Double1", StructValue.DOUBLE, c, r), baseOffset)
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 8 * r, 16, c)
                    self.assertEqual(self.struct.addDMat("Double2", c, r), baseOffset)
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 8 * r, 16, c)


        # 1 - 5 Square
        for s in range (1, 6):
            self.struct.reset()

            if s == 1 or s == 5:
                # Bool
                self.assertEqual(self.struct.addSquareMatrix("Bool1", StructValue.BOOL, s), None)
                self.assertEqual(self.struct.addSqrBMat("Bool2", s), None)

                # Int
                self.assertEqual(self.struct.addSquareMatrix("Int1", StructValue.INT, s), None)
                self.assertEqual(self.struct.addSqrIMat("Int2", s), None)

                # Uint
                self.assertEqual(self.struct.addSquareMatrix("Uint1", StructValue.UINT, s), None)
                self.assertEqual(self.struct.addSqrUMat("Uint2", s), None)

                # Float
                self.assertEqual(self.struct.addSquareMatrix("Float1", StructValue.FLOAT, s), None)
                self.assertEqual(self.struct.addSqrMat("Float2", s), None)

                # Double
                self.assertEqual(self.struct.addSquareMatrix("Double1", StructValue.DOUBLE, s), None)
                self.assertEqual(self.struct.addSqrDMat("Double2", s), None)
            else:
                baseOffset = 0

                # Bool
                self.assertEqual(self.struct.addSquareMatrix("Bool1", StructValue.BOOL, s), baseOffset)
                baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * s, 16, s)
                self.assertEqual(self.struct.addSqrBMat("Bool2", s), baseOffset)
                baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * s, 16, s)

                # Int
                self.assertEqual(self.struct.addSquareMatrix("Int1", StructValue.INT, s), baseOffset)
                baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * s, 16, s)
                self.assertEqual(self.struct.addSqrIMat("Int2", s), baseOffset)
                baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * s, 16, s)

                # Uint
                self.assertEqual(self.struct.addSquareMatrix("Uint1", StructValue.UINT, s), baseOffset)
                baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * s, 16, s)
                self.assertEqual(self.struct.addSqrUMat("Uint2", s), baseOffset)
                baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * s, 16, s)

                # Float
                self.assertEqual(self.struct.addSquareMatrix("Float1", StructValue.FLOAT, s), baseOffset)
                baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * s, 16, s)
                self.assertEqual(self.struct.addSqrMat("Float2", s), baseOffset)
                baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * s, 16, s)

                # Double
                self.assertEqual(self.struct.addSquareMatrix("Double1", StructValue.DOUBLE, s), baseOffset)
                baseOffset = self.updateBaseOffsetArray(baseOffset, 8 * s, 16, s)
                self.assertEqual(self.struct.addSqrDMat("Double2", s), baseOffset)
                baseOffset = self.updateBaseOffsetArray(baseOffset, 8 * s, 16, s)

    def test_AddMatrixesArray(self):
        # Add Matrix Array Func
        
        # 1 - 5 Rows
        for r in range(1, 6):
            # 1 - 5 Columns
            for c in range(1, 6):
                self.struct.reset()

                if r == 1 or r == 5 or c == 1 or c == 5:
                    # Bool
                    self.assertEqual(self.struct.addMatrixArray("Bool1", StructValue.BOOL, c, r, 2), None)
                    self.assertEqual(self.struct.addBMatArray("Bool2", c, r, 2), None)

                    # Int
                    self.assertEqual(self.struct.addMatrixArray("Int1", StructValue.INT, c, r, 2), None)
                    self.assertEqual(self.struct.addIMatArray("Int2", c, r, 2), None)

                    # Uint
                    self.assertEqual(self.struct.addMatrixArray("Uint1", StructValue.UINT, c, r, 2), None)
                    self.assertEqual(self.struct.addUMatArray("Uint2", c, r, 2), None)

                    # Float
                    self.assertEqual(self.struct.addMatrixArray("Float1", StructValue.FLOAT, c, r, 2), None)
                    self.assertEqual(self.struct.addMatArray("Float2", c, r, 2), None)

                    # Double
                    self.assertEqual(self.struct.addMatrixArray("Double1", StructValue.DOUBLE, c, r, 2), None)
                    self.assertEqual(self.struct.addDMatArray("Double2", c, r, 2), None)
                else:
                    num = 2
                    baseOffset = 0
                    baseOffsets = []
                    for i in range(num):
                        baseOffsets.append(0)
                        for _ in range(i):
                            baseOffsets[i] = self.updateBaseOffsetArray(baseOffsets[i], 4 * r, 16, c)

                    # Bool
                    self.assertEqual(self.struct.addMatrixArray("Bool1", StructValue.BOOL, c, r, num), [bo + baseOffset for bo in baseOffsets])
                    baseOffset += baseOffsets[-1]
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * r, 16, c)
                    self.assertEqual(self.struct.addBMatArray("Bool2", c, r, num), [bo + baseOffset for bo in baseOffsets])
                    baseOffset += baseOffsets[-1]
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * r, 16, c)

                    # Int
                    self.assertEqual(self.struct.addMatrixArray("Int1", StructValue.INT, c, r, num), [bo + baseOffset for bo in baseOffsets])
                    baseOffset += baseOffsets[-1]
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * r, 16, c)
                    self.assertEqual(self.struct.addIMatArray("Int2", c, r, num), [bo + baseOffset for bo in baseOffsets])
                    baseOffset += baseOffsets[-1]
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * r, 16, c)

                    # Uint
                    self.assertEqual(self.struct.addMatrixArray("Uint1", StructValue.UINT, c, r, num), [bo + baseOffset for bo in baseOffsets])
                    baseOffset += baseOffsets[-1]
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * r, 16, c)
                    self.assertEqual(self.struct.addUMatArray("Uint2", c, r, num), [bo + baseOffset for bo in baseOffsets])
                    baseOffset += baseOffsets[-1]
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * r, 16, c)

                    # Float
                    self.assertEqual(self.struct.addMatrixArray("Float1", StructValue.FLOAT, c, r, num), [bo + baseOffset for bo in baseOffsets])
                    baseOffset += baseOffsets[-1]
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * r, 16, c)
                    self.assertEqual(self.struct.addMatArray("Float2", c, r, num), [bo + baseOffset for bo in baseOffsets])
                    baseOffset += baseOffsets[-1]
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * r, 16, c)

                    # Double
                    baseAligementSize = 8 * r
                    if baseAligementSize % 16 != 0:
                        baseAligementSize += (16 - baseAligementSize % 16)
                    for i in range(num):
                        baseOffsets[i] = 0
                        for _ in range(i):
                            baseOffsets[i] = self.updateBaseOffsetArray(baseOffsets[i], 4 * r, baseAligementSize, c)
                    self.assertEqual(self.struct.addMatrixArray("Double1", StructValue.DOUBLE, c, r, num), [bo + baseOffset for bo in baseOffsets])
                    baseOffset += baseOffsets[-1]
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * r, baseAligementSize, c)
                    self.assertEqual(self.struct.addDMatArray("Double2", c, r, num), [bo + baseOffset for bo in baseOffsets])
                    baseOffset += baseOffsets[-1]
                    baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * r, baseAligementSize, c)

        # 1 - 5 Square
        for s in range(1, 6):
            self.struct.reset()

            if s == 1 or s == 5:
                # Bool
                self.assertEqual(self.struct.addSquareMatrixArray("Bool1", StructValue.BOOL, s, 2), None)
                self.assertEqual(self.struct.addSqrBMatArray("Bool2", s, 2), None)

                # Int
                self.assertEqual(self.struct.addSquareMatrixArray("Int1", StructValue.INT, s, 2), None)
                self.assertEqual(self.struct.addSqrIMatArray("Int2", s, 2), None)

                # Uint
                self.assertEqual(self.struct.addSquareMatrixArray("Uint1", StructValue.UINT, s, 2), None)
                self.assertEqual(self.struct.addSqrUMatArray("Uint2", s, 2), None)

                # Float
                self.assertEqual(self.struct.addSquareMatrixArray("Float1", StructValue.FLOAT, s, 2), None)
                self.assertEqual(self.struct.addSqrMatArray("Float2", s, 2), None)

                # Double
                self.assertEqual(self.struct.addSquareMatrixArray("Double1", StructValue.DOUBLE, s, 2), None)
                self.assertEqual(self.struct.addSqrDMatArray("Double2", s, 2), None)
            else:
                num = 2
                baseOffset = 0
                baseOffsets = []
                for i in range(num):
                    baseOffsets.append(0)
                    for _ in range(i):
                        baseOffsets[i] = self.updateBaseOffsetArray(baseOffsets[i], 4 * s, 16, s)

                # Bool
                self.assertEqual(self.struct.addSquareMatrixArray("Bool1", StructValue.BOOL, s, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * s, 16, s)
                self.assertEqual(self.struct.addSqrBMatArray("Bool2", s, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * s, 16, s)

                # Int
                self.assertEqual(self.struct.addSquareMatrixArray("Int1", StructValue.INT, s, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * s, 16, s)
                self.assertEqual(self.struct.addSqrIMatArray("Int2", s, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * s, 16, s)

                # Uint
                self.assertEqual(self.struct.addSquareMatrixArray("Uint1", StructValue.UINT, s, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * s, 16, s)
                self.assertEqual(self.struct.addSqrUMatArray("Uint2", s, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * s, 16, s)

                # Float
                self.assertEqual(self.struct.addSquareMatrixArray("Float1", StructValue.FLOAT, s, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * s, 16, s)
                self.assertEqual(self.struct.addSqrMatArray("Float2", s, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * s, 16, s)

                # Double
                baseAligementSize = 8 * s
                if baseAligementSize % 16 != 0:
                    baseAligementSize += (16 - baseAligementSize % 16)
                for i in range(num):
                    baseOffsets[i] = 0
                    for _ in range(i):
                        baseOffsets[i] = self.updateBaseOffsetArray(baseOffsets[i], 4 * s, baseAligementSize, s)
                self.assertEqual(self.struct.addSquareMatrixArray("Double1", StructValue.DOUBLE, s, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * s, baseAligementSize, s)
                self.assertEqual(self.struct.addSqrDMatArray("Double2", s, num), [bo + baseOffset for bo in baseOffsets])
                baseOffset += baseOffsets[-1]
                baseOffset = self.updateBaseOffsetArray(baseOffset, 4 * s, baseAligementSize, s)

    def test_AddStruct(self):
        # Add Struct Test
        pass

    def test_AddStructArray(self):
        # Add Struct Test
        pass

    def test_OffsetCalculation1(self):
        uniformBuffer = STD140Struct()
        self.assertEqual(uniformBuffer.addFloat("a"), 0)
        self.assertEqual(uniformBuffer.addVec("b", 2), 8)
        self.assertEqual(uniformBuffer.addVec("c", 3), 16)

        subStruct = STD140Struct()
        self.assertEqual(subStruct.addInt("d"), 0)
        self.assertEqual(subStruct.addBVec("e", 2), 8)
        self.assertEqual(subStruct.getSize(), 16)

        self.assertEqual(uniformBuffer.addStruct("f", subStruct), 32)
        self.assertEqual(uniformBuffer.addFloat("g"), 48)
        self.assertEqual(uniformBuffer.addFloatArray("h", 2), [64, 80])
        self.assertEqual(uniformBuffer.addMat("i", 2, 3), 96)

        subStruct = STD140Struct()
        self.assertEqual(subStruct.addUVec("j", 3), 0)
        self.assertEqual(subStruct.addVec("k", 2), 16)
        self.assertEqual(subStruct.addFloatArray("l", 2), [32, 48])
        self.assertEqual(subStruct.addVec("m", 2), 64)
        self.assertEqual(subStruct.addSqrMatArray("n", 3, 2), [80, 128])
        self.assertEqual(subStruct.getSize(), 176)

        self.assertEqual(uniformBuffer.addStructArray("o", subStruct, 2), [128, 304])

        self.assertEqual(uniformBuffer.getSize(), 480)

    def test_OffsetCalculation2(self):
        uniformBuffer = STD140Struct()

        subStruct = STD140Struct()
        self.assertEqual(subStruct.addBool("has_diffuse_texture"), 0)
        self.assertEqual(subStruct.addBool("has_specular_texture"), 4)
        self.assertEqual(subStruct.addVec("color", 3), 16)
        self.assertEqual(subStruct.addFloat("shininess"), 28)
        self.assertEqual(subStruct.addUint("diffuse_toon_borders"), 32)
        self.assertEqual(subStruct.addUint("specular_toon_borders"), 36)
        self.assertEqual(subStruct.addVec("highlight_translate", 2), 40)
        self.assertEqual(subStruct.addVec("highlight_rotation", 2), 48)
        self.assertEqual(subStruct.addVec("highlight_scale", 2), 56)
        self.assertEqual(subStruct.addVec("highlight_split", 2), 64)
        self.assertEqual(subStruct.addInt("highlight_square_n"), 72)
        self.assertEqual(subStruct.addFloat("highlight_square_x"), 76)
        self.assertEqual(subStruct.getSize(), 80)

        self.assertEqual(uniformBuffer.addStructArray("materialInputs", subStruct, 8), [0, 80, 160, 240, 320, 400, 480, 560])
        self.assertEqual(uniformBuffer.getSize(), 640)

    def test_OffsetCalculation3(self):
        uniformBuffer = STD140Struct()

        self.assertEqual(uniformBuffer.addVec("windowSize", 2), 0)
        self.assertEqual(uniformBuffer.addFloat("nearPlane"), 8)
        self.assertEqual(uniformBuffer.addFloat("farPlane"), 12)
        self.assertEqual(uniformBuffer.addFloat("gamma"), 16)

        self.assertEqual(uniformBuffer.getSize(), 32)

class Std430Tests(unittest.TestCase):

    def test_OffsetCalculation1(self):
        rect = STD430Struct()
        self.assertEqual(rect.addSqrMat("transform", 4), 0)
        self.assertEqual(rect.addVec("size", 2), 64)
        self.assertEqual(rect.getSize(), 80)

        sprite = STD430Struct()
        self.assertEqual(sprite.addUVec("offset", 2), 0)
        self.assertEqual(sprite.addUVec("size", 2), 8)
        self.assertEqual(sprite.addBool("isActive"), 16)
        self.assertEqual(sprite.getSize(), 32)

        fill = STD430Struct()
        self.assertEqual(fill.addUint("type"), 0)
        self.assertEqual(fill.addUint("subType"), 4)
        self.assertEqual(fill.addFloat("offset"), 8)
        self.assertEqual(fill.addFloat("progress"), 12)
        self.assertEqual(fill.addFloat("rotation"), 16)
        self.assertEqual(fill.addBool("isActive"), 20)
        self.assertEqual(fill.getSize(), 32)

        uiElement = STD430Struct()
        self.assertEqual(uiElement.addStruct("rect", rect), 0)
        self.assertEqual(uiElement.addStruct("sprite", sprite), 80)
        self.assertEqual(uiElement.addStruct("fill", fill), 112)
        self.assertEqual(uiElement.addVec("color", 4), 144)
        self.assertEqual(uiElement.addBool("isText"), 160)
        self.assertEqual(uiElement.getSize(), 176)

        texture = STD430Struct()
        self.assertEqual(texture.addUVec("size", 2), 0)
        self.assertEqual(texture.addBool("isActive"), 8)
        self.assertEqual(texture.getSize(), 16)

        ssbo = STD430Struct()
        self.assertEqual(ssbo.addStructArray("uiElements", uiElement, 8), [0, 176, 352, 528, 704, 880, 1056, 1232])
        self.assertEqual(ssbo.addStruct("elementTexture", texture), 1408)
        self.assertEqual(ssbo.addInt("elementLayer"), 1424)
        self.assertEqual(ssbo.getSize(), 1440)

    def test_OffsetCalculation2(self):
        pointLight = STD430Struct()
        self.assertEqual(pointLight.addVec("position", 3), 0)
        self.assertEqual(pointLight.addVec("color", 3), 16)
        self.assertEqual(pointLight.addFloat("power"), 28)
        self.assertEqual(pointLight.addFloat("constant"), 32)
        self.assertEqual(pointLight.addFloat("linear"), 36)
        self.assertEqual(pointLight.addFloat("quadratic"), 40)
        self.assertEqual(pointLight.getSize(), 48)

        spotLight = STD430Struct()
        self.assertEqual(spotLight.addVec("position", 3), 0)
        self.assertEqual(spotLight.addVec("direction", 3), 16)
        self.assertEqual(spotLight.addFloat("power"), 28)
        self.assertEqual(spotLight.addVec("color", 3), 32)
        self.assertEqual(spotLight.addFloat("cutOff"), 44)
        self.assertEqual(spotLight.addFloat("outerCutOff"), 48)
        self.assertEqual(spotLight.addFloat("constant"), 52)
        self.assertEqual(spotLight.addFloat("linear"), 56)
        self.assertEqual(spotLight.addFloat("quadratic"), 60)
        self.assertEqual(spotLight.getSize(), 64)

        dirLight = STD430Struct()
        self.assertEqual(dirLight.addVec("direction", 3), 0)
        self.assertEqual(dirLight.addVec("color", 3), 16)
        self.assertEqual(dirLight.addSqrMat("lightSpaceMatrix", 4), 32)
        self.assertEqual(dirLight.addFloat("power"), 96)
        self.assertEqual(dirLight.addInt("padding1"), 100)
        self.assertEqual(dirLight.addInt("padding2"), 104)
        self.assertEqual(dirLight.addInt("padding3"), 108)
        self.assertEqual(dirLight.getSize(), 112)

        ssbo = STD430Struct()
        self.assertEqual(ssbo.addUint("numberOfPointLights"), 0)
        self.assertEqual(ssbo.addUint("numberOfSpotLights"), 4)
        self.assertEqual(ssbo.addUint("numberOfDirLights"), 8)
        self.assertEqual(ssbo.addStructArray("pointLights", pointLight, 8), [16, 64, 112, 160, 208, 256, 304, 352])
        self.assertEqual(ssbo.addStructArray("spotLights", spotLight, 8), [400, 464, 528, 592, 656, 720, 784, 848])
        self.assertEqual(ssbo.addStructArray("directionalLights", dirLight, 4), [912, 1024, 1136, 1248])
        self.assertEqual(ssbo.getSize(), 1360)


if __name__ == "__main__":
    unittest.main(verbosity=2)