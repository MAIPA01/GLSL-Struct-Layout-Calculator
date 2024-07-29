from std140Struct import *
from std430Struct import *
import sys
import unittest

if __name__ == "__main__":
    def print(value: str = "", separator: str = '\n') -> None:
        out = sys.stdout
        for chunk in str(value):
            out.write(chunk)
        out.write(separator)

    def std140Test1():
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

    def std140Test2():
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

    def std140Test3():
        uniformBuffer = STD140Struct()

        uniformBuffer.addVec("windowSize", 2)
        uniformBuffer.addFloat("nearPlane")
        uniformBuffer.addFloat("farPlane")
        uniformBuffer.addFloat("gamma")

        print(uniformBuffer)
        print(f"size: {uniformBuffer.getStructSize()}")

    def std140Tests():
        print("----------START OF TEST1-----------")
        std140Test1()
        print("----------END OF TEST1-------------")
        print()
        print("----------START OF TEST2-----------")
        std140Test2()
        print("----------END OF TEST2-------------")
        print()
        print("----------START OF TEST3-----------")
        std140Test3()
        print("----------END OF TEST3-------------")

    def std430Test1():
        rect = STD430Struct()
        rect.addSqrMat("transform", 4)
        rect.addVec("size", 2)

        sprite = STD430Struct()
        sprite.addUVec("offset", 2)
        sprite.addUVec("size", 2)
        sprite.addBool("isActive")

        fill = STD430Struct()
        fill.addUint("type")
        fill.addUint("subType")
        fill.addFloat("offset")
        fill.addFloat("progress")
        fill.addFloat("rotation")
        fill.addBool("isActive")

        uiElement = STD430Struct()
        uiElement.addStruct("rect", rect)
        uiElement.addStruct("sprite", sprite)
        uiElement.addStruct("fill", fill)
        uiElement.addVec("color", 4)
        uiElement.addBool("isText")

        texture = STD430Struct()
        texture.addUVec("size", 2)
        texture.addBool("isActive")

        ssbo = STD430Struct()
        ssbo.addStructArray("uiElements", uiElement, 8)
        ssbo.addStruct("elementTexture", texture)
        ssbo.addInt("elementLayer")

        print(ssbo)
        print(f"baseOffset: {ssbo.getBaseOffset()}")
        print(f"size: {ssbo.getStructSize()}")

    def std430Test2():
        pointLight = STD430Struct()
        pointLight.addVec("position", 3)
        pointLight.addVec("color", 3)
        pointLight.addFloat("power")
        pointLight.addFloat("constant")
        pointLight.addFloat("linear")
        pointLight.addFloat("quadratic")

        spotLight = STD430Struct()
        spotLight.addVec("position", 3)
        spotLight.addVec("direction", 3)
        spotLight.addFloat("power")
        spotLight.addVec("color", 3)
        spotLight.addFloat("cutOff")
        spotLight.addFloat("outerCutOff")
        spotLight.addFloat("constant")
        spotLight.addFloat("linear")
        spotLight.addFloat("quadratic")

        dirLight = STD430Struct()
        dirLight.addVec("direction", 3)
        dirLight.addVec("color", 3)
        dirLight.addSqrMat("lightSpaceMatrix", 4)
        dirLight.addFloat("power")
        dirLight.addInt("padding1")
        dirLight.addInt("padding2")
        dirLight.addInt("padding3")

        ssbo = STD430Struct()
        ssbo.addUint("numberOfPointLights")
        ssbo.addUint("numberOfSpotLights")
        ssbo.addUint("numberOfDirLights")
        ssbo.addStructArray("pointLights", pointLight, 8)
        ssbo.addStructArray("spotLights", spotLight, 8)
        ssbo.addStructArray("directionalLights", dirLight, 4)

        print(ssbo)
        print(f"baseOffset: {ssbo.getBaseOffset()}")
        print(f"size: {ssbo.getStructSize()}")

    def std430Tests():
        print("----------START OF TEST1-----------")
        std430Test1()
        print("----------END OF TEST1-------------")
        print()
        print("----------START OF TEST1-----------")
        std430Test2()
        print("----------END OF TEST1-------------")

    def tests():
        print("-----------------START OF STD140 Tests------------------")
        std140Tests()
        print("-----------------END OF STD140 Tests------------------")
        print()
        print("-----------------START OF STD430 Tests------------------")
        std430Tests()
        print("-----------------END OF STD430 Tests------------------")

    # tests()

    class Std140Tests(unittest.TestCase):

        def test1(self):
            uniformBuffer = STD140Struct()
            self.assertEqual(uniformBuffer.addFloat("a"), 0)
            self.assertEqual(uniformBuffer.addVec("b", 2), 8)
            self.assertEqual(uniformBuffer.addVec("c", 3), 16)

            subStruct = STD140Struct()
            self.assertEqual(subStruct.addInt("d"), 0)
            self.assertEqual(subStruct.addBVec("e", 2), 8)

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

            self.assertEqual(uniformBuffer.addStructArray("o", subStruct, 2), [128, 304])

            self.assertEqual(uniformBuffer.getStructSize(), 480)

    unittest.main()