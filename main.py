from std140Struct import *

if __name__ == "__main__":
    def test1():
        uniformBuffer = STD140Struct()
        uniformBuffer.addScalar("a", FLOAT)
        uniformBuffer.addVec("b", FLOAT, 2)
        uniformBuffer.addVec("c", FLOAT, 3)

        subStruct = STD140Struct()
        subStruct.addScalar("d", INT)
        subStruct.addVec("e", BOOL, 2)

        uniformBuffer.addStruct("f", subStruct)
        uniformBuffer.addScalar("g", FLOAT)
        uniformBuffer.addScalarArray("h", FLOAT, 2)
        uniformBuffer.addMat("i", FLOAT, 2, 3)

        subStruct = STD140Struct()
        subStruct.addVec("j", UINT, 3)
        subStruct.addVec("k", FLOAT, 2)
        subStruct.addScalarArray("l", FLOAT, 2)
        subStruct.addVec("m", FLOAT, 2)
        subStruct.addSqrMatArray("n", FLOAT, 3, 2)

        uniformBuffer.addStructArray("o", subStruct, 2)
        print(uniformBuffer)
        print(f"size: {uniformBuffer.getStructSize()}")

    def test2():
        uniformBuffer = STD140Struct()

        subStruct = STD140Struct()
        subStruct.addScalar("has_diffuse_texture", BOOL)
        subStruct.addScalar("has_specular_texture", BOOL)
        subStruct.addVec("color", FLOAT, 3)
        subStruct.addScalar("shininess", FLOAT)
        subStruct.addScalar("diffuse_toon_borders", UINT)
        subStruct.addScalar("specular_toon_borders", UINT)
        subStruct.addVec("highlight_translate", FLOAT, 2)
        subStruct.addVec("highlight_rotation", FLOAT, 2)
        subStruct.addVec("highlight_scale", FLOAT, 2)
        subStruct.addVec("highlight_split", FLOAT, 2)
        subStruct.addScalar("highlight_square_n", INT)
        subStruct.addScalar("highlight_square_x", FLOAT)

        uniformBuffer.addStructArray("materialInputs", subStruct, 8)
        print(uniformBuffer)
        print(f"size: {uniformBuffer.getStructSize()}")

    def test3():
        uniformBuffer = STD140Struct()

        uniformBuffer.addVec("windowSize", FLOAT, 2)
        uniformBuffer.addScalar("nearPlane", FLOAT)
        uniformBuffer.addScalar("farPlane", FLOAT)
        uniformBuffer.addScalar("gamma", FLOAT)

        print(uniformBuffer)
        print(f"size: {uniformBuffer.getStructSize()}")

    # test1()
    # test2()
    # test3()