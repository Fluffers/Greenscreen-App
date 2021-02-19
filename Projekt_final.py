from tkinter import *
import cv2
import numpy as np
import time

root = Tk()

# rozmiar okna
root.title("Greenscreen App")
root.geometry("310x620")

# polecenie - film
header = Label(root, text="Greenscreen App", font=('Calibri', 15, 'bold'))
text1 = Label(root, text=" Podaj ścieżkę do filmu: ", font=('Calibri', 12))
subtext1 = Label(root, text=" razem z rozszerzeniem ", font=('Calibri', 8, 'italic'))
header.pack(padx=20, pady=10)
text1.pack(padx=20, pady=4)
subtext1.pack(padx=20, pady=4)

# input filmu
video_name = Entry(root, width=100)
video_name.pack(anchor=W, padx=20)

# polecenie - tło
text2 = Label(root, text=" Podaj ścieżkę do tła: ", font=('Calibri', 12))
subtext2 = Label(root, text=" razem z rozszerzeniem  ", font=('Calibri', 8, 'italic'))
text2.pack(padx=20, pady=4)
subtext2.pack(padx=20, pady=4)

# input tła
img = Entry(root, width=100)
img.pack(padx=20, pady=10)

# polecenie - kolorek
color_pick = Label(root, text=" Wybierz kolor do wycięcia ", font=('Calibri', 12))
color_pick.pack(padx=20, pady=10)

# wybieranie kolorka
c = IntVar()
c1 = Radiobutton(root, text="Zielony", variable=c, value=1)
c2 = Radiobutton(root, text="Czerwony", variable=c, value=2)
c3 = Radiobutton(root, text="Niebieski", variable=c, value=3)
c1.pack()
c2.pack()
c3.pack()

# uruchomienie maleństwa
butt = Button(root, text="  Zaczynamy!  ", command=lambda: green_screen(video_name.get(), img.get(), c.get()))
butt.pack(side=BOTTOM, pady=100)

def zielona(count, background, video):
    try:
        while (video.isOpened()):
            ret, movie = video.read()
            movie = cv2.resize(movie, (640, 480))
            background = cv2.resize(background, (640, 480))

            if not ret:
                break
            count += 1

            # Zamiana rgb na hsv
            hsv = cv2.cvtColor(movie, cv2.COLOR_BGR2HSV)

            # Zielona maska
            lower_green = np.array([35, 40, 40])
            upper_green = np.array([86, 255, 255])
            gmask1 = cv2.inRange(hsv, lower_green, upper_green)

            # Fuzja i przetwarzanie maski
            gmask1 = cv2.morphologyEx(gmask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
            gmask1 = cv2.dilate(gmask1, np.ones((3, 3), np.uint8), iterations=1)
            gmask2 = cv2.bitwise_not(gmask1)

            # Widok wyjściowy
            res1 = cv2.bitwise_and(background, background, mask=gmask1)
            res2 = cv2.bitwise_and(movie, movie, mask=gmask2)
            final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

            cv2.imshow('Aby zakonczyc, nacisnij ESC', final_output)

            # kończymy z Esc
            k = cv2.waitKey(25)
            if k == 27:
                exit()
    except():
        print("Exit")
        exit()

def czerwona(count, background, video):
    try:
        while (video.isOpened()):
            ret, movie2 = video.read()
            movie2 = cv2.resize(movie2, (640, 480))
            background = cv2.resize(background, (640, 480))

            if not ret:
                break
            count += 1

            hsv = cv2.cvtColor(movie2, cv2.COLOR_BGR2HSV)

            # Czerwona maska
            lower_red = np.array([170, 40, 40])
            upper_red = np.array([179, 255, 255])
            rmask1 = cv2.inRange(hsv, lower_red, upper_red)

            lower_red2 = np.array([0, 40, 40])
            upper_red2 = np.array([13, 255, 255])
            rmask2 = cv2.inRange(hsv, lower_red2, upper_red2)

            rmask = rmask1 + rmask2

            rmask = cv2.morphologyEx(rmask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
            rmask = cv2.dilate(rmask, np.ones((3, 3), np.uint8), iterations=1)
            rmask3 = cv2.bitwise_not(rmask)

            res1 = cv2.bitwise_and(background, background, mask=rmask)
            res2 = cv2.bitwise_and(movie2, movie2, mask=rmask3)
            final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

            cv2.imshow('Aby zakonczyc, nacisnij ESC', final_output)

            k = cv2.waitKey(25)
            if k == 27:
                exit()
            else:
                continue
    except:
        print("Exit")
        exit()

def niebieska(count, background, video):
    try:
        while (video.isOpened()):
            ret, movie3 = video.read()
            movie3 = cv2.resize(movie3, (640, 480))
            background = cv2.resize(background, (640, 480))

            if not ret:
                break
            count += 1

            hsv = cv2.cvtColor(movie3, cv2.COLOR_BGR2HSV)

            # Niebieska maska
            lower_blue = np.array([95, 40, 40])
            upper_blue = np.array([135, 255, 255])
            bmask1 = cv2.inRange(hsv, lower_blue, upper_blue)

            bmask1 = cv2.morphologyEx(bmask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
            bmask1 = cv2.dilate(bmask1, np.ones((3, 3), np.uint8), iterations=1)
            bmask2 = cv2.bitwise_not(bmask1)

            res1 = cv2.bitwise_and(background, background, mask=bmask1)
            res2 = cv2.bitwise_and(movie3, movie3, mask=bmask2)
            final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

            cv2.imshow('Aby zakonczyc, nacisnij ESC', final_output)

            k = cv2.waitKey(25)
            if k == 27:
                exit()
            else:
                continue
    except:
        print("Exit")
        exit()

def green_screen(video_name, img, c):
    video = cv2.VideoCapture(video_name)
    background = cv2.imread(img)
    # Czas dla kamery
    time.sleep(2)
    count = 0

    if c == 1:
        print(zielona(count, background, video))
    if c == 2:
        print(czerwona(count, background, video))
    if c == 3:
        print(niebieska(count, background, video))

    video.release()
    cv2.destroyAllWindows()

root.mainloop()
