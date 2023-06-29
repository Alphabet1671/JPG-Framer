from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
import exifread
import os


minBoarderWidth = 0.1
minBoarderHeight = 0.2


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


    cameraSettingFont = ImageFont.truetype("calibri-italic.ttf", int(textHeight))
    cameraInfoFont = ImageFont.truetype("calibri-italic.ttf", int(textHeight))


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


#GUI Shell here
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widgets App")
        self.sourceDirectory = ""
        self.targetDirectory = ""
        self.backgroundColorRValue = 255
        self.backgroundColorGValue = 255
        self.backgroundColorBValue = 255

#Browse button for directory input

        directoryInputLayout = QGridLayout()

        sourceDirectoryBrowseButton = QPushButton("Browse")
        sourceDirectoryBrowseButton.clicked.connect(self.GetSourceDirectory)
        targetDirectoryBrowseButton = QPushButton("Browse")
        targetDirectoryBrowseButton.clicked.connect(self.GetTargetDirectory)
        self.sourceDirectoryLabel = QLabel("From: "+self.sourceDirectory)
        self.targetDirectoryLabel = QLabel("To: "+self.targetDirectory)

        directoryInputLayout.addWidget(self.sourceDirectoryLabel,0,0)
        directoryInputLayout.addWidget(sourceDirectoryBrowseButton,0,1)
        directoryInputLayout.addWidget(self.targetDirectoryLabel,1,0)
        directoryInputLayout.addWidget(targetDirectoryBrowseButton,1,1)

        previewButton = QPushButton("Preview")
        previewButton.clicked.connect(self.Preview)
        startButton = QPushButton("Convert")
        startButton.released.connect(self.Start)
        inputLayout = QVBoxLayout()

        inputLayout.addLayout(directoryInputLayout)
        inputLayout.addWidget(previewButton)
        inputLayout.addWidget(startButton)


        widget = QWidget()
        widget.setLayout(inputLayout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

    def GetSourceDirectory(self):
        dir = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        if dir:
            self.sourceDirectory = str(Path(dir))
            self.sourceDirectoryLabel.setText(str(Path(dir)))

    def GetTargetDirectory(self):
        dir = QFileDialog.getExistingDirectory(self, "Select Target Directory")
        if dir:
            self.targetDirectory = str(Path(dir))
            self.targetDirectoryLabel.setText(str(Path(dir)))

    def Preview(self):
        AddedSquareBoarder("DSC_0647.jpg",(self.backgroundColorRValue,self.backgroundColorGValue,self.backgroundColorBValue)).show("Sample 1")
        AddedSquareBoarder("DSC_9871.jpg",(self.backgroundColorRValue, self.backgroundColorGValue, self.backgroundColorBValue)).show("Sample 2")
    def Start(self):
        for image in os.listdir(self.sourceDirectory):
            AddedSquareBoarder(str(Path(self.sourceDirectory)/Path(image)),(self.backgroundColorRValue, self.backgroundColorGValue, self.backgroundColorBValue)).save(str(Path(self.targetDirectory)/Path("framed"+image)))

app = QApplication([])

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()




"""for image in os.listdir(sourceDirectory):
    AddedSquareBoarder(str(sourceDirectory)+"+str(image),(255,255,255)).save(str(targetDirectory)+"\\"+str(image)+"-framed.jpg","JPEG")"""