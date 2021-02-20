from tkinter import *
import cv2
import numpy as np
import time

root = Tk()

# rozmiar okna
root.title("Greenscreen App")
root.geometry("310x420")
root.resizable(False, False)

# polecenie - film
header = Label(root, text="Greenscreen App", font=('Calibri', 15, 'bold'))
text1 = Label(root, text=" Podaj ścieżkę do filmu: ", font=('Calibri', 12))
subtext1 = Label(root, text=" brak ścieżki będzie oznaczać kamerę urządzenia ", font=('Calibri', 8, 'italic'))
header.pack(padx=20, pady=10)
text1.pack(padx=20, pady=4)
subtext1.pack(padx=20, pady=4)

# input filmu
video_name = Entry(root, width=100)
video_name.insert(END, 'example-video.mp4')
video_name.pack(anchor=W, padx=20)

# polecenie - tło
text2 = Label(root, text=" Podaj ścieżkę do tła: ", font=('Calibri', 12))
text2.pack(padx=20, pady=4)

# input tła
img = Entry(root, width=100)
img.insert(END, 'example-image.jpg')
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
butt.pack(padx=20, pady=30)

def show_video(video, background, color, fps):

    while (video.isOpened()):
        ret, movie = video.read()

        if ret:
            movie = cv2.resize(movie, (640, 480))
            background = cv2.resize(background, (640, 480))
            # Zamiana rgb na hsv
            hsv = cv2.cvtColor(movie, cv2.COLOR_BGR2HSV)

            if color == 1:
                lower_green = np.array([35, 40, 40])
                upper_green = np.array([86, 255, 255])
                mask1 = cv2.inRange(hsv, lower_green, upper_green)

            elif color == 2:

                lower_red = np.array([170, 40, 40])
                upper_red = np.array([179, 255, 255])
                mask1 = cv2.inRange(hsv, lower_red, upper_red)

                lower_red2 = np.array([0, 40, 40])
                upper_red2 = np.array([13, 255, 255])
                mask_2 = cv2.inRange(hsv, lower_red2, upper_red2)

                mask1 = mask1 + mask_2
            else:
                lower_blue = np.array([95, 40, 40])
                upper_blue = np.array([135, 255, 255])
                mask1 = cv2.inRange(hsv, lower_blue, upper_blue)

            mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
            mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations=1)
            mask2 = cv2.bitwise_not(mask1)

            # Widok wyjściowy
            res1 = cv2.bitwise_and(background, background, mask=mask1)
            res2 = cv2.bitwise_and(movie, movie, mask=mask2)
            final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

            cv2.imshow('Aby zakonczyc, nacisnij ESC', final_output)

            # Wychodzimy wciskając 'q' // jedna klatka trwa tyle, na ile pozwala wideo na wejściu
            if cv2.waitKey(int((1 / int(fps)) * 1000)) & 0xFF == ord('q'):
                break
        else:
            break

def green_screen(video_name, img, color):
    if video_name == '':
        video_name = 0
    video = cv2.VideoCapture(video_name)
    fps = video.get(cv2.CAP_PROP_FPS)
    background = cv2.imread(img)

    # Czas dla kamery
    time.sleep(2)
    count = 0

    show_video(video, background, color, fps)


    video.release()
    cv2.destroyAllWindows()

root.mainloop()
