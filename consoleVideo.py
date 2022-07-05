import cv2
import PIL.Image
import os
import sys
import time

framesAscii = []

def convertVideo(vPath):
    framesFolderPath = "./frames/"
    vidcap = cv2.VideoCapture(vPath)
    success,image = vidcap.read()
    count = 0

    if(not os.path.exists("frames")):
        os.makedirs("frames")
    if(not os.path.exists("ascii")):
        os.makedirs("ascii")

    while success:
        cv2.imwrite("frames/%d.jpg" % count, image)  
        success,image = vidcap.read()
        print('Frame: ' + str(count) + " finalizado")
        count += 1

    count = 0
    for file in sorted(os.listdir(framesFolderPath)):
        f = os.path.join(framesFolderPath, str(count)+".jpg")
        print(f)
        if os.path.isfile(f):
            img_flag = True
            try:
                img = PIL.Image.open(f)
                img_flag = True
            except:
                print(f, "Unable to find image ")
            
            #Redimensionamiento
            width, height = img.size
            aspect_ratio = height/width
            new_width = 120
            new_height = aspect_ratio * new_width * 0.55
            img = img.resize((new_width, int(new_height)))
            
            img = img.convert('L')
            
            chars = [" ", "J", "D", "%", "*", "P", "+", "Y", "$", ",", "@"]
            
            #Reemplazo de pixeles
            pixels = img.getdata()
            new_pixels = [chars[pixel//25] for pixel in pixels]
            new_pixels = ''.join(new_pixels)
            new_pixels_count = len(new_pixels)
            ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
            ascii_image = "\n".join(ascii_image)
            
            #Guardar frame en carpeta ascii
            with open("ascii/%d.txt" % count, "w") as f:
                f.write(ascii_image)
            print(f)
            count += 1

def loadFrames():
    count = 0
    if(os.path.exists("ascii")):
        for file in sorted(os.listdir("./ascii/")):
            f = open("./ascii/" + str(count)+".txt", 'r')
            contents = f.read()
            framesAscii.append(contents)
            count += 1
        print("%d frames cargados" % len(framesAscii))
        input("Presione una tecla para continuar.")
    else:
        print("No se encontró la carpeta ascii.")
        input("Presione una tecla para continuar.")

def playVideo(speed):
    for frame in framesAscii:
        os.system('cls')
        print(frame)
        time.sleep(speed)

while True:
    os.system('cls')
    print("---------------------------------")
    print("1.- Convertir video a ascii")
    print("2.- Cargar frames")
    print("3.- Reproducir video en consola")
    print("4.- Salir")
    print("---------------------------------")

    eleccion = int(input())

    #Python no tiene switch, que cagada
    if(eleccion == 1):
        convertVideo(input("Ingrese ruta del video: "))
    if(eleccion == 2):
        loadFrames()
    if(eleccion == 3):
        if(len(framesAscii) != 0):
            print("Sugerencia: Maximice la ventana.")
            playVideo(float(input("Indique velocidad (en segundos) para cada frame. Ej: 0.014: ")))
        else:
            print("Cargue los frames con la opción 2 antes de reproducir.")
            input("Presione una tecla para continuar.")
    if(eleccion == 4):
        sys.exit()