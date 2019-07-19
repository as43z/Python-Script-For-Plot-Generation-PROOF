import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# PART OF THE SCRIPT THAT READS THE FILES---------------------------
class observedobjects():
    #This class contains the properties of the objects
    #INIT function to get all the properties
    def __init__(self, ID, DIAM, MAG, SNR, RA, DEC):
        self.ID = ID
        self.DIAM = DIAM
        self.MAG = MAG
        self.SNR = SNR
        self.RA = RA
        self.DEC = DEC

def GetObjects(name_filedet):
    #This function gets all the crossing objects + detected objects    
    #List of Objects
    Objects = []

    print "-----------GETTING---OBJECTS-----------"
    Objects = ReadFile(name_filedet)
    
    return Objects


def ReadFile(file_to_read):
    #This function reads the file and returns a list
    Objects = []
    
    #File to read
    fileopt = open(file_to_read, "r")
    
    print file_to_read
    indicator = 1
    for line in fileopt:
        print "Reading Line..." + str(indicator)
        traspaser = line.split()
        if not traspaser[0].find("#")  == 0:
            ID = traspaser[0]
            DIAM = ExpresionConverter(traspaser[1])
            MAG = float(traspaser[20])
            SNR = ExpresionConverter(traspaser[22])
            RA = float(traspaser[23])
            DEC = float(traspaser[24])
            if MAG > 0:
                observed = observedobjects(ID, DIAM, MAG, SNR, RA, DEC)
                Objects.append(observed)
                print "Object " + ID + " Appended"

        print "Read Line " + str(indicator)
        indicator += 1

    fileopt.close()
    return Objects

def ExpresionConverter(Expresion):
    #This function changes the format .XXXXEXX to a Float number
    Numbers = Expresion.split("E")
    Num = float(Numbers[0])

    #Depending on the sign of the E we multiply or we divide
    if Numbers[1].find("+"):
        Total = Num * (10 ** int(Numbers[1]))
    elif Numbers[1].find("-"):
        Total = Num/(10**int(Numbers[1]))
    
    return Total

#-------------------------------------------------------------------
# SCRIPT THAT SEARCHES FOR THE FILES--------------------------------
def SearchForFiles(path):
    #Search For Files
    print "Gathering Files..."
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
            print os.path.join(r, file)

    print "Done."
    return files
#-------------------------------------------------------------------
# SCRIPT THAT SETS UP THE OBJECTS-----------------------------------
def SetUp(filea):
    #This function sets up the objects
    return ReadFile(filea)

#-------------------------------------------------------------------
# SCRIPT THAT PLOTS OBJECTS-----------------------------------------
def MakePLOTS(Objects, folder):
    #Do all the plots
    MakeHistogramRA(Objects, folder)
    MakeHistogramDEC(Objects, folder)

def MakeHistogramRA(Objects, folder):
    #This is a function to make a Histogram
    RAs30 = []
    RAs15 = []
    RAs0 = []
    RAs_15 = []
    RAs_30 = []
    DECs =[]

    for Object in Objects:
        DECs.append(Object.DEC)
        if Object.DEC == 30.0:
            RAs30.append(Object.RA)
        elif Object.DEC == 15.0:
            RAs15.append(Object.RA)
        elif Object.DEC == 0:
            RAs0.append(Object.RA)
        elif Object.DEC == -15.0:
            RAs_15.append(Object.RA)
        elif Object.DEC == -30.0:
            RAs_30.append(Object.RA)
    num_bins = 10
    n, bins, patches = plt.hist([RAs30, RAs15, RAs0, RAs_15, RAs_30], num_bins, color = ['blue', 'yellow', 'red', 'green', 'purple'])
    plt.title("Histogram\n N Detection[-] vs Right Ascension [deg]")
    plt.xlabel("Right Ascension[deg]")
    plt.ylabel("N Detected Objects[-]")
    plt.xlim(0,360)
    plt.ylim(0, max(max(RAs30), max(RAs15), max(RAs0), max(RAs_15), max(RAs_30)))

    D30 = mpatches.Patch(color ='blue', label = '30 degrees Declination')
    D15 = mpatches.Patch(color ='yellow', label = '15 degrees Declination')
    D0 = mpatches.Patch(color ='green', label = '0 degrees Declination')
    D_15 = mpatches.Patch(color ='red', label = '-15 degrees Declination')
    D_30 = mpatches.Patch(color ='purple', label = '-30 degrees Declination')

    plt.legend(handles=[D30, D15, D0, D_15, D_30])

    plt.savefig('/home/albert/Escritorio/' + folder  + '/Histog_RA.png')
    plt.clf()
    plt.cla()
    plt.close()

def MakeHistogramDEC(Objects, folder):
    #Function to make a plot for all the declination
    DECs = []
    DEC30 = []
    DEC15 = []
    DEC0 = []
    DEC_15 = []
    DEC_30 = []

    for Object in Objects:
        DECs.append(Object.DEC)
        if Object.DEC == 30:
            DEC30.append(Object.DEC)
        elif Object.DEC == 15:
            DEC15.append(Object.DEC)
        elif Object.DEC == 0:
            DEC0.append(Object.DEC)
        elif Object.DEC == -15:
            DEC_15.append(Object.DEC)
        elif Object.DEC == -30:
            DEC_30.append(Object.DEC)

    num_bins = 5
    n, bins, patches = plt.hist(DECs, num_bins, facecolor = 'Red', edgecolor = 'black',linewidth = 1.0)

    plt.title("Histogram\n N of Detection[-] vs Declination [deg]")
    plt.xlabel("Declination[deg]")
    plt.ylabel("N Detected Objects[-]")
    plt.xlim(-40, 40)
    plt.ylim(0, max(len(DEC30), len(DEC15), len(DEC0), len(DEC_15), len(DEC_30)) + 100)

    plt.savefig('/home/albert/Escritorio/' + folder + '/Histog_Dec.png')
    plt.clf()
    plt.cla()
    plt.close()

#-------------------------------------------------------------------
# ACTUAL PROGRAM----------------------------------------------------
ob = []
objects = []

#Need to enter the full path
pth = raw_input("Folder to search for: ")

#Need to enter only the name of the folder (A folder will be created automatically on the Desktop)
fld = raw_input("Create folder (Folder Name you want to create): ")

os.system("mkdir /home/albert/Escritorio/" + fld)

files = SearchForFiles(pth)
for fil in files:
    ob = SetUp(fil)
    for objekt in ob:
        objects.append(objekt)

for Object in objects:
    print Object.ID + " " + str(Object.RA)

MakePLOTS(objects, fld)
