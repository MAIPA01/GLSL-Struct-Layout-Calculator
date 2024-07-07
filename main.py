from std140Struct import *
from std430Struct import *

if __name__ == "__main__":
    def test1():
        uniformBuffer = STD140Struct()
        uniformBuffer.addFloat("a")
        uniformBuffer.addVec("b", 2)
        uniformBuffer.addVec("c", 3)

        subStruct = STD140Struct()
        subStruct.addInt("d")
        subStruct.addBVec("e", 2)

        uniformBuffer.addStruct("f", subStruct)
        uniformBuffer.addFloat("g")
        uniformBuffer.addFloatArray("h", 2)
        uniformBuffer.addMat("i", 2, 3)

        subStruct = STD140Struct()
        subStruct.addUVec("j", 3)
        subStruct.addVec("k", 2)
        subStruct.addFloatArray("l", 2)
        subStruct.addVec("m", 2)
        subStruct.addSqrMatArray("n", 3, 2)

        uniformBuffer.addStructArray("o", subStruct, 2)
        print(uniformBuffer)
        print(f"size: {uniformBuffer.getStructSize()}")

    def test2():
        uniformBuffer = STD140Struct()

        subStruct = STD140Struct()
        subStruct.addBool("has_diffuse_texture")
        subStruct.addBool("has_specular_texture")
        subStruct.addVec("color", 3)
        subStruct.addFloat("shininess")
        subStruct.addUint("diffuse_toon_borders")
        subStruct.addUint("specular_toon_borders")
        subStruct.addVec("highlight_translate", 2)
        subStruct.addVec("highlight_rotation", 2)
        subStruct.addVec("highlight_scale", 2)
        subStruct.addVec("highlight_split", 2)
        subStruct.addInt("highlight_square_n")
        subStruct.addFloat("highlight_square_x")

        uniformBuffer.addStructArray("materialInputs", subStruct, 8)
        print(uniformBuffer)
        print(f"size: {uniformBuffer.getStructSize()}")

    def test3():
        uniformBuffer = STD140Struct()

        uniformBuffer.addVec("windowSize", 2)
        uniformBuffer.addFloat("nearPlane")
        uniformBuffer.addFloat("farPlane")
        uniformBuffer.addFloat("gamma")

        print(uniformBuffer)
        print(f"size: {uniformBuffer.getStructSize()}")

    # test1()
    # test2()
    # test3()