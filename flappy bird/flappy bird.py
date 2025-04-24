from PIL import Image, ImageTk  # Importing images for the game elements
import tkinter as tk
import random

window = tk.Tk()
window.geometry('1920x1080')  # Set window size
window.config(bg='lightblue')  # Background color for the window

canvas = tk.Canvas(window, height=1080, width=1920, highlightthickness=0)  # Create a canvas
canvas.pack()

mylist = [0, 100, 200, 300, 400]

gameover = False  # Flag for game over status
gamestart = False  # Flag for game start status

bg1 = Image.open('bg.png')  # Open background image
bg1 = bg1.resize((1920, 1080))  # Resize to fit the window
bg = ImageTk.PhotoImage(bg1)  # Convert to PhotoImage for tkinter
lbg = canvas.create_image(600, 300, image=bg)  # Place background on canvas

bird = Image.open('bird.png')  # Open bird image
bird = bird.resize((60, 60))  # Resize to proper size
birdtk = ImageTk.PhotoImage(bird)
birdid = canvas.create_image(100, 400, image=birdtk)

pipey = random.choice(mylist) * 0.1  # Random vertical position for pipes
pipe = Image.open('pipe.png')  # Open pipe image
pipe_width, pipe_height = pipe.size  # Get pipe dimensions
pipe = pipe.resize((100, 1000))  # Resize pipe image
pipetk = ImageTk.PhotoImage(pipe)
pipeid = canvas.create_image(300, 1000, image=pipetk)

pipe1y = random.choice(mylist) * 0.1
pipe1 = Image.open('pipe.png')
pipe1 = pipe1.resize((100, 1000))
pipe1tk = ImageTk.PhotoImage(pipe1)
pipe1id = canvas.create_image(800, 1000, image=pipe1tk)

pipe2y = random.choice(mylist) * 0.1
pipe2 = Image.open('pipe.png')
pipe2 = pipe2.resize((100, 1000))
pipe2tk = ImageTk.PhotoImage(pipe2)
pipe2id = canvas.create_image(1300, 1000, image=pipe2tk)

pipeup = Image.open('pipeup.png')  # Open top pipe image
pipeup = pipeup.resize((100, 1000))  # Resize top pipe image
pipeuptk = ImageTk.PhotoImage(pipeup)
pipeupid = canvas.create_image(300, -200, image=pipeuptk)

pipeup1 = Image.open('pipeup.png')
pipeup1 = pipeup1.resize((100, 1000))
pipeup1tk = ImageTk.PhotoImage(pipeup1)
pipeup1id = canvas.create_image(800, -200, image=pipeup1tk)

pipeup2 = Image.open('pipeup.png')
pipeup2 = pipeup2.resize((100, 1000))
pipeup2tk = ImageTk.PhotoImage(pipeup2)
pipeup2id = canvas.create_image(1300, -200, image=pipeup2tk)

score = 0
record = 0

def del_score():
    canvas.delete('score_text')  # Delete the score text

def scor():
    canvas.create_text(750, 100, text=score, tags='score_text', font=('Arial', 20))  # Display score
    window.after(1000, del_score)  # Update every second
    window.after(1000, scor)

def pipemove():
    global score
    if gameover:
        score = 0
        return

    canvas.move(pipeid, -10, 0)  # Move pipes horizontally
    canvas.move(pipe1id, -10, 0)
    canvas.move(pipe2id, -10, 0)
    canvas.move(pipeupid, -10, 0)
    canvas.move(pipeup1id, -10, 0)
    canvas.move(pipeup2id, -10, 0)

    if canvas.coords(pipeid)[0] < 0:  # Reset pipe position
        canvas.move(pipeid, 1500, pipey)
        canvas.move(pipeupid, 1500, pipey)
        score += 1

    if canvas.coords(pipe1id)[0] < 0:
        canvas.move(pipe1id, 1500, pipe1y)
        canvas.move(pipeup1id, 1500, pipe1y)
        score += 1

    if canvas.coords(pipe2id)[0] < 0:
        canvas.move(pipe2id, 1500, pipe2y)
        canvas.move(pipeup2id, 1500, pipe2y)
        score += 1

    window.after(40, pipemove)

def move(event):  # Function for bird movement based on user input
    global gamestart, gameover, birdid
    if gameover:
        gameover = False
        gamestart = False
        
        canvas.delete('gameover_text')
        
        canvas.delete(birdid)
        birdid = canvas.create_image(100, 400, image=birdtk)
        
        canvas.coords(pipeid, 300, 1000)
        canvas.coords(pipeupid, 300, -200)
        canvas.coords(pipe1id, 800, 1000)
        canvas.coords(pipeup1id, 800, -200)
        canvas.coords(pipe2id, 1300, 1000)
        canvas.coords(pipeup2id, 1300, -200)
        
    if not gamestart:
        gamestart = True
        jazebeh()
        pipemove()
        
    if not gameover:
        check()
        
    canvas.move(birdid, 0, -100)  # Move bird upward

def jazebeh():
    if gameover:
        return
    canvas.move(birdid, 0, 10)  # Simulate gravity (bird falling)

    window.after(50, jazebeh)

def check():
    global gameover
    x1, y1, x2, y2 = canvas.bbox(birdid)  # Get bounding box for bird
    if y2 >= 1080 or y1 <= 0:  # Check collision with ground or ceiling
        gameover = True
    for pipe, pipeup in [(pipeid, pipeupid), (pipe1id, pipeup1id), (pipe2id, pipeup2id)]:  # Check collisions with pipes
        px1, py1, px2, py2 = canvas.bbox(pipe)
        px1u, py1u, px2u, py2u = canvas.bbox(pipeup)

        if (x2 > px1 and x1 < px2 and y2 > py1 and y1 < py2) or (x2 > px1u and x1 < px2u and y2 > py1u and y1 < py2u):
            gameover = True
    if gameover:
        records()
        canvas.delete(birdid)
        canvas.create_text(750, 400, text='GAME OVER', fill='red', font=("Arial", 50, "bold"), tags='gameover_text')
        return
    if not gameover:
        window.after(50, check)

def records():
    global score, record
    try:
        with open('record.txt', 'r+') as file:
            content = file.read().strip()
            if content.isdigit():
                record = int(content)
            else:
                record = 0

            if score > record:
                record = score
                file.seek(0)
                file.write(str(record))
                file.truncate()
    except FileNotFoundError:
        with open('record.txt', 'w') as file:
            file.write(str(score))
        record = score

def calrecord():
    global record
    canvas.delete('record_text')
    canvas.create_text(750, 50, text=f"record: {record}", tags='record_text', font=('Arial', 30))
    window.after(100, calrecord)

calrecord()
check()
scor()

canvas.bind_all('<space>', move)  # Bind space bar to bird movement
canvas.bind_all('<Button-1>', move)  # Bind mouse click to bird movement

window.mainloop()
