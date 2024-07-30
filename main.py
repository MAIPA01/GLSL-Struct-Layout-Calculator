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
            self.assertEqual(subStruct.getStructSize(), 16)

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
            self.assertEqual(subStruct.getStructSize(), 176)

            self.assertEqual(uniformBuffer.addStructArray("o", subStruct, 2), [128, 304])

            self.assertEqual(uniformBuffer.getStructSize(), 480)

        def test2(self):
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
            self.assertEqual(subStruct.getStructSize(), 80)

            self.assertEqual(uniformBuffer.addStructArray("materialInputs", subStruct, 8), [0, 80, 160, 240, 320, 400, 480, 560])
            self.assertEqual(uniformBuffer.getStructSize(), 640)

        def test3(self):
            uniformBuffer = STD140Struct()

            self.assertEqual(uniformBuffer.addVec("windowSize", 2), 0)
            self.assertEqual(uniformBuffer.addFloat("nearPlane"), 8)
            self.assertEqual(uniformBuffer.addFloat("farPlane"), 12)
            self.assertEqual(uniformBuffer.addFloat("gamma"), 16)

            self.assertEqual(uniformBuffer.getStructSize(), 32)

    class Std430Tests(unittest.TestCase):

        def test1(self):
            rect = STD430Struct()
            self.assertEqual(rect.addSqrMat("transform", 4), 0)
            self.assertEqual(rect.addVec("size", 2), 64)
            self.assertEqual(rect.getStructSize(), 80)

            sprite = STD430Struct()
            self.assertEqual(sprite.addUVec("offset", 2), 0)
            self.assertEqual(sprite.addUVec("size", 2), 8)
            self.assertEqual(sprite.addBool("isActive"), 16)
            self.assertEqual(sprite.getStructSize(), 32)

            fill = STD430Struct()
            self.assertEqual(fill.addUint("type"), 0)
            self.assertEqual(fill.addUint("subType"), 4)
            self.assertEqual(fill.addFloat("offset"), 8)
            self.assertEqual(fill.addFloat("progress"), 12)
            self.assertEqual(fill.addFloat("rotation"), 16)
            self.assertEqual(fill.addBool("isActive"), 20)
            self.assertEqual(fill.getStructSize(), 32)

            uiElement = STD430Struct()
            self.assertEqual(uiElement.addStruct("rect", rect), 0)
            self.assertEqual(uiElement.addStruct("sprite", sprite), 80)
            self.assertEqual(uiElement.addStruct("fill", fill), 112)
            self.assertEqual(uiElement.addVec("color", 4), 144)
            self.assertEqual(uiElement.addBool("isText"), 160)
            self.assertEqual(uiElement.getStructSize(), 176)

            texture = STD430Struct()
            self.assertEqual(texture.addUVec("size", 2), 0)
            self.assertEqual(texture.addBool("isActive"), 8)
            self.assertEqual(texture.getStructSize(), 16)

            ssbo = STD430Struct()
            self.assertEqual(ssbo.addStructArray("uiElements", uiElement, 8), [0, 176, 352, 528, 704, 880, 1056, 1232])
            self.assertEqual(ssbo.addStruct("elementTexture", texture), 1408)
            self.assertEqual(ssbo.addInt("elementLayer"), 1424)
            self.assertEqual(ssbo.getStructSize(), 1440)

        def test2(self):
            pointLight = STD430Struct()
            self.assertEqual(pointLight.addVec("position", 3), 0)
            self.assertEqual(pointLight.addVec("color", 3), 16)
            self.assertEqual(pointLight.addFloat("power"), 28)
            self.assertEqual(pointLight.addFloat("constant"), 32)
            self.assertEqual(pointLight.addFloat("linear"), 36)
            self.assertEqual(pointLight.addFloat("quadratic"), 40)
            self.assertEqual(pointLight.getStructSize(), 48)

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
            self.assertEqual(spotLight.getStructSize(), 64)

            dirLight = STD430Struct()
            self.assertEqual(dirLight.addVec("direction", 3), 0)
            self.assertEqual(dirLight.addVec("color", 3), 16)
            self.assertEqual(dirLight.addSqrMat("lightSpaceMatrix", 4), 32)
            self.assertEqual(dirLight.addFloat("power"), 96)
            self.assertEqual(dirLight.addInt("padding1"), 100)
            self.assertEqual(dirLight.addInt("padding2"), 104)
            self.assertEqual(dirLight.addInt("padding3"), 108)
            self.assertEqual(dirLight.getStructSize(), 112)

            ssbo = STD430Struct()
            self.assertEqual(ssbo.addUint("numberOfPointLights"), 0)
            self.assertEqual(ssbo.addUint("numberOfSpotLights"), 4)
            self.assertEqual(ssbo.addUint("numberOfDirLights"), 8)
            self.assertEqual(ssbo.addStructArray("pointLights", pointLight, 8), [16, 64, 112, 160, 208, 256, 304, 352])
            self.assertEqual(ssbo.addStructArray("spotLights", spotLight, 8), [400, 464, 528, 592, 656, 720, 784, 848])
            self.assertEqual(ssbo.addStructArray("directionalLights", dirLight, 4), [912, 1024, 1136, 1248])
            self.assertEqual(ssbo.getStructSize(), 1360)

    unittest.main()