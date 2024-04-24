from std140Struct import STD140Struct

if __name__ == "__main__":
    def test1():
        uniformBuffer = STD140Struct()
        uniformBuffer.addFloat("a")
        uniformBuffer.addVec2("b")
        uniformBuffer.addVec3("c")

        print("SUB STRUCT START")
        subStruct = STD140Struct()
        subStruct.addInt("d")
        subStruct.addBVec2("e")
        print("SUB STRUCT END")

        uniformBuffer.addStruct("f", subStruct)
        uniformBuffer.addFloat("g")
        uniformBuffer.addFloatArray("h", 2)
        uniformBuffer.addMat("i", 2, 3)

        print("SUB STRUCT START")
        subStruct = STD140Struct()
        subStruct.addUVec3("j")
        subStruct.addVec2("k")
        subStruct.addFloatArray("l", 2)
        subStruct.addVec2("m")
        subStruct.addSqrMatArray("n", 3, 2)
        print("SUB STRUCT END")

        uniformBuffer.addStructArray("o", subStruct, 2)
        print(f"last offset: {uniformBuffer.baseOffset}")

    def test2():
        uniformBuffer = STD140Struct()

        print("SUB STRUCT BEGIN")
        subStruct = STD140Struct()
        subStruct.addBool("has_diffuse_texture")
        subStruct.addBool("has_specular_texture")
        subStruct.addVec3("color")
        subStruct.addFloat("shininess")
        subStruct.addUint("diffuse_toon_borders")
        subStruct.addUint("specular_toon_borders")
        subStruct.addVec2("highlight_translate")
        subStruct.addVec2("highlight_rotation")
        subStruct.addVec2("highlight_scale")
        subStruct.addVec2("highlight_split")
        subStruct.addInt("highlight_square_n")
        subStruct.addFloat("highlight_square_x")
        print("SUB STRUCT END")

        uniformBuffer.addStructArray("materialInputs", subStruct, 8)
        print(f"last offset: {uniformBuffer.baseOffset}")

    # test1()
    # test2()