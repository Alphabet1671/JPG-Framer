import PySimpleGUI as gui
from PIL import Image, ImageFont, ImageDraw
import exifread
import os


minBoarderWidth = 0.1
minBoarderHeight = 0.2

maxTextHeight = 40

sourceDirectory = ""
targetDirectory = ""

def AddedSquareBoarder(sourceLocation, color):
    sourceImage = Image.open(sourceLocation)
    sourceWidth = sourceImage.size[0]
    sourceHeight = sourceImage.size[1]
    if sourceWidth>sourceHeight:
        resultWidth = int(sourceWidth*(1+minBoarderWidth))
        textHeight = (resultWidth-sourceWidth)*0.25
    else:
        resultWidth = int(sourceHeight*(1+minBoarderHeight))
        textHeight = int(int(resultWidth-sourceHeight)*0.1)
    resultImage = Image.new("RGB", (resultWidth, resultWidth), color)
    resultImage.paste(sourceImage, (int((resultWidth-sourceWidth)/2),int((resultWidth-sourceHeight)/2)))



    draw = ImageDraw.Draw(resultImage)

    f = open(sourceLocation, "rb")

    tags = exifread.process_file(f)
    print(str(tags))

    """
    shutterSpeedString = str(tags["EXIF ExposureTime"])
    apertureString = "f/"+str(tags["EXIF FNumber"])
    isoSpeedString = "ISO"+str(tags["EXIF ISOSpeedRatings"])
    exposureProgramString = str(tags["EXIF ExposureProgram"])
    focalLengthString = str(tags["EXIF FocalLength"])

    cameraNameString = str(tags["Image Model"])

    lensNameString = str(tags["EXIF LensModel"])
    """
    try:
        shutterSpeedString = str(tags["EXIF ExposureTime"])+" sec"
    except:
        shutterSpeedString = ""

    try:
        if "/" in str(tags["EXIF FNumber"]):
            tempList = str(tags["EXIF FNumber"]).split("/")
            apertureString = "f/"+str(round(float(tempList[0])/float(tempList[1]),1))
        else:
            apertureString = "f/" + str(tags["EXIF FNumber"])
    except:
        apertureString = ""

    try:
        isoSpeedString = "ISO" + str(tags["EXIF ISOSpeedRatings"])
    except:
        isoSpeedString = ""
    try:
        exposureProgramString = str(tags["EXIF ExposureProgram"])+" Exposure"
    except:
        exposureProgramString = ""
    try:
        focalLengthString = str(tags["EXIF FocalLength"])+"mm"
    except:
        focalLengthString = ""

    cameraNameString = str(tags["Image Model"])

    lensNameString = str(tags["EXIF LensModel"])

    cameraSettingString = shutterSpeedString+"   "+apertureString+"   "+isoSpeedString





    paddingHeight = int(resultWidth-sourceHeight)/2
    paddingWidth = int(resultWidth-sourceWidth)/2


    cameraSettingFont = ImageFont.truetype("Fonts/calibri-italic.ttf", int(textHeight))
    cameraInfoFont = ImageFont.truetype("Fonts/calibri-italic.ttf", int(textHeight))


    topLeftTextOffset = (paddingWidth,paddingHeight/2)
    topRightTextOffset = (resultWidth-paddingWidth,paddingHeight/2)
    bottomLeftTextOffset = (paddingWidth,resultWidth-paddingHeight/2)
    bottomRightTextOffset = (resultWidth-paddingWidth,resultWidth-paddingHeight/2)
    draw.text(topLeftTextOffset, cameraSettingString, font=cameraSettingFont, fill=(0,0,0,255), anchor="lm")
    draw.text(topRightTextOffset, exposureProgramString, font=cameraSettingFont, fill=(0,0,0,255), anchor="rm")
    draw.text(bottomLeftTextOffset, focalLengthString, font=cameraSettingFont, fill=(0,0,0,255), anchor="lm")
    draw.multiline_text(bottomRightTextOffset, cameraNameString+"\n"+lensNameString, font=cameraInfoFont, fill=(0,0,0,255),align="right", anchor="rm",spacing=int(textHeight*0.1))
    return resultImage


#AddedSquareBoarder("Test/DSC_0647.jpg",(255,255,255)).show()
#AddedSquareBoarder("Test/DSC_9871.jpg",(255,255,255)).show()
#test images

layout = [
    [gui.Text("Enter Source Directory:")],
    [gui.InputText(key="sourceDirectory")],
    [gui.Text("Enter Target Directory:")],
    [gui.InputText(key="targetDirectory")],
    [gui.Submit("Start")]
]


window = gui.Window("Square Image Generator", layout)
event, values = window.read()
window.close()
sourceDirectory = values["sourceDirectory"]
targetDirectory = values["targetDirectory"]


for image in os.listdir(sourceDirectory):
    AddedSquareBoarder(str(sourceDirectory)+"\\"+str(image),(255,255,255)).save(str(targetDirectory)+"\\"+str(image)+"-framed.jpg","JPEG")
gui.popup_ok("Finished!")