from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
import exifread
import os


minBoarderWidth = 0.1
minBoarderHeight = 0.2


def AddedSquareBoarder(sourceLocation, backgroundColor, textColor, textSize, fontPath ,finalImageRatio, minBoarderWidth, minBoarderHeight, displayTopLeft, displayTopRight, displayBottomLeft, displayBottomRight):
    sourceImage = Image.open(sourceLocation)
    sourceWidth = sourceImage.size[0]
    sourceHeight = sourceImage.size[1]
    if (sourceWidth/finalImageRatio)>sourceHeight:
        resultWidth = int(sourceWidth*(1+minBoarderWidth))
        resultHeight = int(resultWidth/finalImageRatio)
        textHeight = int(resultWidth-sourceWidth)*(minBoarderHeight/minBoarderWidth)/2*textSize
    else:
        resultHeight = int(sourceHeight*(1+minBoarderHeight))
        resultWidth = int(resultHeight*finalImageRatio)
        textHeight =  int(resultHeight-sourceHeight)/2*textSize
    resultImage = Image.new("RGB", (resultWidth, resultHeight), backgroundColor)
    resultImage.paste(sourceImage, (int((resultWidth-sourceWidth)/2),int((resultHeight-sourceHeight)/2)))



    draw = ImageDraw.Draw(resultImage)

    f = open(sourceLocation, "rb")

    tags = exifread.process_file(f)

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





    paddingHeight = int(resultHeight-sourceHeight)/2
    paddingWidth = int(resultWidth-sourceWidth)/2



    cameraSettingFont = ImageFont.truetype(fontPath, int(textHeight))
    cameraInfoFont = ImageFont.truetype(fontPath, int(textHeight))



    topLeftTextOffset = (paddingWidth,paddingHeight/2)
    topRightTextOffset = (resultWidth-paddingWidth,paddingHeight/2)
    bottomLeftTextOffset = (paddingWidth,resultHeight-paddingHeight/2)
    bottomRightTextOffset = (resultWidth-paddingWidth,resultHeight-paddingHeight/2)
    if displayTopLeft: draw.text(topLeftTextOffset, cameraSettingString, font=cameraSettingFont, fill=textColor, anchor="lm")
    if displayTopRight: draw.text(topRightTextOffset, exposureProgramString, font=cameraSettingFont, fill=textColor, anchor="rm")
    if displayBottomLeft: draw.text(bottomLeftTextOffset, focalLengthString, font=cameraSettingFont, fill=textColor, anchor="lm")
    if displayBottomRight: draw.multiline_text(bottomRightTextOffset, cameraNameString+"\n"+lensNameString, font=cameraInfoFont, fill=textColor,align="right", anchor="rm",spacing=int(textHeight*0.1))
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

        self.textColorRValue = 0
        self.textColorGValue = 0
        self.textColorBValue = 0

        self.textSize = 0.2

        self.imageWidthRatioValue = 1
        self.imageHeightRatioValue = 1

        self.displayTopLeft = False
        self.displayTopRight = False
        self.displayBottomLeft = False
        self.displayBottomRight = False

        self.fontFileDirectory = "calibri-italic.ttf"

        self.minBoarderWidth = 0.1
        self.minBoarderHeight = 0.2

#Browse button for directory input
        inputLayout = QVBoxLayout()
#============================================================================Directory Input
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
#===============================================================================Preview & Start Buttons
        previewButton = QPushButton("Preview")
        previewButton.clicked.connect(self.Preview)
        startButton = QPushButton("Convert")
        startButton.released.connect(self.Start)


#=================================================== Toggle Display Elements
        toggleLayout = QGridLayout()

        toggleSettingsCheckBox = QCheckBox()
        toggleSettingsCheckBox.setCheckable(True)
        toggleSettingsCheckBox.setText("Show Camera Settings")
        toggleSettingsCheckBox.stateChanged.connect(self.SetDisplayTopLeft)
        #remember to connect the checkboxes

        toggleProgramCheckBox = QCheckBox()
        toggleProgramCheckBox.setCheckable(True)
        toggleProgramCheckBox.setText("Show Exposure Program")
        toggleProgramCheckBox.stateChanged.connect(self.SetDisplayTopRight)

        toggleFocalLengthCheckBox = QCheckBox()
        toggleFocalLengthCheckBox.setCheckable(True)
        toggleFocalLengthCheckBox.setText("Show Focal Length")
        toggleFocalLengthCheckBox.stateChanged.connect(self.SetDisplayBottomLeft)


        toggleCameraInfoCheckBox = QCheckBox()
        toggleCameraInfoCheckBox.setCheckable(True)
        toggleCameraInfoCheckBox.setText("Show Camera Info")
        toggleCameraInfoCheckBox.stateChanged.connect(self.SetDisplayBottomRight)


        toggleLayout.addWidget(toggleSettingsCheckBox,0,0)
        toggleLayout.addWidget(toggleProgramCheckBox,0,1)
        toggleLayout.addWidget(toggleFocalLengthCheckBox,1,0)
        toggleLayout.addWidget(toggleCameraInfoCheckBox,1,1)
#==================================================================Set Background Color

        backgroundColorInputLayout = QHBoxLayout()
        backgroundColorInputLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        backgroundColorRInput = QDoubleSpinBox()
        backgroundColorRInput.setMaximum(255)
        backgroundColorRInput.setMinimum(0)
        backgroundColorRInput.setDecimals(0)
        backgroundColorRInput.setValue(self.backgroundColorRValue)
        backgroundColorRInput.valueChanged.connect(self.SetBackgroundColorRValue)

        backgroundColorGInput = QDoubleSpinBox()
        backgroundColorGInput.setMaximum(255)
        backgroundColorGInput.setMinimum(0)
        backgroundColorGInput.setDecimals(0)
        backgroundColorGInput.setValue(self.backgroundColorGValue)
        backgroundColorGInput.valueChanged.connect(self.SetBackgroundColorGValue)

        backgroundColorBInput = QDoubleSpinBox()
        backgroundColorBInput.setMaximum(255)
        backgroundColorBInput.setMinimum(0)
        backgroundColorBInput.setDecimals(0)
        backgroundColorBInput.setValue(self.backgroundColorBValue)
        backgroundColorBInput.valueChanged.connect(self.SetBackgroundColorBValue)

        backgroundColorInputLayout.addWidget(QLabel("Background Color: "))
        backgroundColorInputLayout.addWidget(QLabel("R:"))
        backgroundColorInputLayout.addWidget(backgroundColorRInput)
        backgroundColorInputLayout.addWidget(QLabel("G:"))
        backgroundColorInputLayout.addWidget(backgroundColorGInput)
        backgroundColorInputLayout.addWidget(QLabel("B:"))
        backgroundColorInputLayout.addWidget(backgroundColorBInput)
#=================================================================
        textColorInputLayout = QHBoxLayout()
        textColorInputLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        textColorRInput = QDoubleSpinBox()
        textColorRInput.setMaximum(255)
        textColorRInput.setMinimum(0)
        textColorRInput.setDecimals(0)
        textColorRInput.setValue(self.textColorRValue)
        textColorRInput.valueChanged.connect(self.SetTextColorRValue)

        textColorGInput = QDoubleSpinBox()
        textColorGInput.setMaximum(255)
        textColorGInput.setMinimum(0)
        textColorGInput.setDecimals(0)
        textColorGInput.setValue(self.textColorGValue)
        textColorGInput.valueChanged.connect(self.SetTextColorGValue)

        textColorBInput = QDoubleSpinBox()
        textColorBInput.setMaximum(255)
        textColorBInput.setMinimum(0)
        textColorBInput.setDecimals(0)
        textColorBInput.setValue(self.textColorBValue)
        textColorBInput.valueChanged.connect(self.SetTextColorBValue)

        textColorInputLayout.addWidget(QLabel("Text Color: "))
        textColorInputLayout.addWidget(QLabel("R:"))
        textColorInputLayout.addWidget(textColorRInput)
        textColorInputLayout.addWidget(QLabel("G:"))
        textColorInputLayout.addWidget(textColorGInput)
        textColorInputLayout.addWidget(QLabel("B:"))
        textColorInputLayout.addWidget(textColorBInput)

#==================================================================================Set Image Ratio

        ratioInputLayout = QHBoxLayout()
        ratioInputLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        widthRatioInput = QDoubleSpinBox()
        widthRatioInput.setDecimals(0)
        widthRatioInput.setMinimum(0)
        widthRatioInput.setValue(self.imageWidthRatioValue)
        widthRatioInput.valueChanged.connect(self.SetImageWidthRatioValue)

        heightRatioInput = QDoubleSpinBox()
        heightRatioInput.setDecimals(0)
        heightRatioInput.setMinimum(0)
        heightRatioInput.setValue(self.imageHeightRatioValue)
        heightRatioInput.valueChanged.connect(self.SetImageHeightRatioValue)


        ratioInputLayout.addWidget(QLabel("Set Final Image Ratio (Width:Height)"))
        ratioInputLayout.addWidget(widthRatioInput)
        ratioInputLayout.addWidget(QLabel(":"))
        ratioInputLayout.addWidget(heightRatioInput)
#==========================================================================Text Size Input

        textSizeInputLayout = QHBoxLayout()
        textSizeInputLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        textSizeInput = QDoubleSpinBox()
        textSizeInput.setDecimals(2)
        textSizeInput.setMaximum(1)
        textSizeInput.setMinimum(0)
        textSizeInput.setSingleStep(0.01)
        textSizeInput.setValue(self.textSize)
        textSizeInput.valueChanged.connect(self.SetTextSize)

        textSizeInputLayout.addWidget(QLabel("Text Height (Relative):"))
        textSizeInputLayout.addWidget(textSizeInput)

#=======================================================================font file browse

        fontDirectoryInputLayout = QHBoxLayout()

        fontDirectoryBrowseButton = QPushButton("Browse")
        fontDirectoryBrowseButton.clicked.connect(self.GetFontDirectory)
        self.fontDirectoryLabel = QLabel()

        fontDirectoryInputLayout.addWidget(QLabel("Font File:"))
        fontDirectoryInputLayout.addWidget(self.fontDirectoryLabel)
        fontDirectoryInputLayout.addWidget(fontDirectoryBrowseButton)


#=======================================================================Image Boarder control

        imageBoarderInputLayout = QHBoxLayout()

        imageBoarderHeightInput = QDoubleSpinBox()
        imageBoarderHeightInput.setMinimum(0)
        imageBoarderHeightInput.setMaximum(1)
        imageBoarderHeightInput.setSingleStep(0.01)
        imageBoarderHeightInput.setValue(self.minBoarderHeight)
        imageBoarderHeightInput.valueChanged.connect(self.SetMinBoarderHeight)

        imageBoarderWidthInput = QDoubleSpinBox()
        imageBoarderWidthInput.setMinimum(0)
        imageBoarderWidthInput.setMaximum(1)
        imageBoarderWidthInput.setSingleStep(0.01)
        imageBoarderWidthInput.setValue(self.minBoarderWidth)
        imageBoarderWidthInput.valueChanged.connect(self.SetMinBoarderWidth)

        imageBoarderInputLayout.addWidget(QLabel("Minimum Frame Width (Relative to Source):"))
        imageBoarderInputLayout.addWidget(imageBoarderWidthInput)
        imageBoarderInputLayout.addWidget(QLabel("Minimum Frame Height (Relative to Source):"))
        imageBoarderInputLayout.addWidget(imageBoarderHeightInput)
#===============
        previewLayout = QHBoxLayout()
        previewLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.previewImageLabel1 = QLabel()
        self.previewImageLabel2 = QLabel()
        self.previewImageLabel1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        previewLayout.addWidget(self.previewImageLabel1)
        previewLayout.addWidget(self.previewImageLabel2)


#=======================================================================
        inputLayout.addLayout(directoryInputLayout)
        inputLayout.addLayout(ratioInputLayout)
        inputLayout.addLayout(imageBoarderInputLayout)
        inputLayout.addWidget(QLabel("Display Elements:"))
        inputLayout.addLayout(toggleLayout)
        inputLayout.addLayout(backgroundColorInputLayout)
        inputLayout.addLayout(textSizeInputLayout)
        inputLayout.addLayout(textColorInputLayout)
        inputLayout.addLayout(fontDirectoryInputLayout)
        inputLayout.addWidget(previewButton)
        inputLayout.addWidget(startButton)
        inputLayout.addLayout(previewLayout)

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

    def GetFontDirectory(self):
        fontFileDialog = QFileDialog()
        fontFileDialog.setDefaultSuffix("ttf")
        fontFileDialog.setNameFilter("*.ttf")
        dir = fontFileDialog.getOpenFileName(self, "Select Custom Font File (ttf)")[0]
        try:
            if dir.split(".")[1]=="ttf":
                self.fontFileDirectory = str(Path(dir))
                self.fontDirectoryLabel.setText(self.fontFileDirectory)
        except:
            self.fontFileDirectory = "calibri-italic.ttf"

    def Preview(self):
        AddedSquareBoarder(str(Path(os.getcwd())/Path("DSC_0647.jpg")),(self.backgroundColorRValue, self.backgroundColorGValue, self.backgroundColorBValue), (self.textColorRValue, self.textColorGValue,self.textColorBValue), self.textSize, self.fontFileDirectory, (self.imageWidthRatioValue/self.imageHeightRatioValue), self.minBoarderWidth,self.minBoarderHeight, self.displayTopLeft,self.displayTopRight,self.displayBottomLeft,self.displayBottomRight).resize((int(350),int(350*self.imageHeightRatioValue/self.imageWidthRatioValue))).save("temp1.jpg")
        AddedSquareBoarder(str(Path(os.getcwd())/Path("DSC_9871.jpg")),(self.backgroundColorRValue, self.backgroundColorGValue, self.backgroundColorBValue), (self.textColorRValue, self.textColorGValue,self.textColorBValue), self.textSize, self.fontFileDirectory, (self.imageWidthRatioValue/self.imageHeightRatioValue), self.minBoarderWidth,self.minBoarderHeight, self.displayTopLeft,self.displayTopRight,self.displayBottomLeft,self.displayBottomRight).resize((int(350),int(350*self.imageHeightRatioValue/self.imageWidthRatioValue))).save("temp2.jpg")
        self.previewImageLabel1.setPixmap(QPixmap(str(Path(os.getcwd())/Path("temp1.jpg"))))
        self.previewImageLabel2.setPixmap(QPixmap(str(Path(os.getcwd())/Path("temp2.jpg"))))
    def Start(self):
        for image in os.listdir(self.sourceDirectory):
            AddedSquareBoarder(str(Path(self.sourceDirectory)/Path(image)),(self.backgroundColorRValue, self.backgroundColorGValue, self.backgroundColorBValue), (self.textColorRValue, self.textColorGValue,self.textColorBValue),self.textSize, self.fontFileDirectory, (self.imageWidthRatioValue/self.imageHeightRatioValue), self.minBoarderWidth,self.minBoarderHeight, self.displayTopLeft,self.displayTopRight,self.displayBottomLeft,self.displayBottomRight).save(str(Path(self.targetDirectory)/Path("framed"+image)))

    def SetDisplayTopLeft(self, checked):
        self.displayTopLeft = checked
    def SetDisplayTopRight(self, checked):
        self.displayTopRight = checked
    def SetDisplayBottomLeft(self, checked):
        self.displayBottomLeft = checked
    def SetDisplayBottomRight(self, checked):
        self.displayBottomRight = checked
    def SetBackgroundColorRValue(self, value):
        self.backgroundColorRValue = int(value)
    def SetBackgroundColorGValue(self, value):
        self.backgroundColorGValue = int(value)
    def SetBackgroundColorBValue(self, value):
        self.backgroundColorBValue = int(value)
    def SetTextColorRValue(self, value):
        self.textColorRValue = int(value)
    def SetTextColorGValue(self, value):
        self.textColorGValue = int(value)
    def SetTextColorBValue(self, value):
        self.textColorBValue = int(value)
    def SetImageWidthRatioValue(self, value):
        self.imageWidthRatioValue = value
    def SetImageHeightRatioValue(self, value):
        self.imageHeightRatioValue = value
    def SetTextSize(self, value):
        self.textSize = value
    def SetMinBoarderHeight(self, value):
        self.minBoarderHeight = value
    def SetMinBoarderWidth(self, value):
        self.minBoarderWidth = value



app = QApplication([])

# Create a Qt widget, which will be our window.
window = MainWindow()
window.setWindowTitle("Image Frame Generator")
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()




"""for image in os.listdir(sourceDirectory):
    AddedSquareBoarder(str(sourceDirectory)+"+str(image),(255,255,255)).save(str(targetDirectory)+"\\"+str(image)+"-framed.jpg","JPEG")"""