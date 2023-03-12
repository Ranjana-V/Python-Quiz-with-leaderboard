import pandas as pd
import pygame
import math
from tkinter import *
from tkinter import messagebox as mb
from PIL import ImageTk, Image
from prettytable import from_csv

question = ['Q1. What house is Ron in?',
            "Q2. What is hermoine's last name?",
            'Q3. How  many HP movies are there?',
            "Q4. What is Hagrid's first name?"]

answer = [1, 2, 3, 2]

options = [['Gryffindor', 'Slytherin', 'Hufflepuff', 'Ravenclaw'],
           ['Griffin', 'Granger', 'Gilbert', 'Gertrude'],
           ['6', '9', '8', '7'],
           ['Robbie', 'Rubeus', 'Robert', 'Rhett']]

root = Tk()
root.title("You're a wizzard harry")
root.geometry("800x500")

# Background Image
bg = ImageTk.PhotoImage(file="hp.jpg")
my_canvas = Canvas(root, width=800, height=500)
my_canvas.pack(fill="both", expand=True)
my_canvas.create_image(0, 0, image=bg, anchor="nw")

# Resizing Background Image


def resizer(e):
    global b1, resized_bg, new_bg
    bg1 = Image.open("hp.jpg")
    resized_bg = bg1.resize((e.width, e.height), Image.ANTIALIAS)
    new_bg = ImageTk.PhotoImage(resized_bg)
    my_canvas.create_image(0, 0, image=new_bg, anchor="nw")
    my_canvas.create_text(400, 200, text="You're a Quizzard Harry!", font=(
        "Imprint MT Shadow", 40), fill="white")


root.bind('<Configure>', resizer)

# Start Quiz Function


def start():
    global final_name
    final_name = name_entry.get()
    root.destroy()

    class Quiz:
        def __init__(self):

            self.q_no = 0

            self.display_title()
            self.display_question()

            self.opt_selected = IntVar()

            self.opts = self.radio_buttons()

            self.display_options()

            self.buttons()

            self.data_size = len(question)

            self.correct = 0

            self.countdown(60)

        def display(self):

            # calculates the wrong count
            wrong_ans = self.data_size - self.correct
            correct = f"Correct: {self.correct}"
            wrong = f"Wrong: {wrong_ans}"

            # calcultaes the percentage of correct answers
            score = int(self.correct / self.data_size * 100)
            result = f"Score: {score}%"

            # Shows a message box to display the result
            mb.showinfo("Result", f"{result}\n{correct}\n{wrong}")

        def check_ans(self, q_no):

            # checks for if the selected option is correct
            if self.opt_selected.get() == answer[q_no]:
                # if the option is correct it return true
                return True

        def next_btn(self):
            # Check if the answer is correct
            if self.check_ans(self.q_no):

                # if the answer is correct it increments the correct by 1
                self.correct += 1

            # Moves to next Question by incrementing the q_no counter
            self.q_no += 1

            # checks if the q_no size is equal to the data size
            if self.q_no == self.data_size:

                # if it is correct then it displays the score
                self.display()
                lead_data = {
                    'Name': [final_name],
                    'Score': [self.correct],
                    'Time Left': [final_count]
                }
                df = pd.DataFrame(lead_data)
                df.to_csv('leader.csv', mode='a', index=False, header=False)
                print("Data appended successfully.")
                quiz_window.destroy()

                leader = Tk()
                dfa = pd.read_csv("leader.csv")
                dfa.sort_values(["Score", "Time Left"], axis=0,
                                ascending=False, inplace=True, na_position='first')
                dfa.to_csv('leader.csv', mode='w+', index=False)
                with open("leader.csv") as fp:
                    mytable = from_csv(fp)
                leader.geometry("500x400")
                output_text = Text(leader, height=100,
                                   width=100, bg="#C996CC",fg="#3D2C8D",border="0",pady=30,padx=125)
                output_text.insert(END, mytable)
                output_text.place(x=1, y=1)
                leader.mainloop()
            else:
                # shows the next question
                self.display_question()
                self.display_options()

        def buttons(self):

            # The first button is the Next button to move to the
            # next Question
            nextbtn = Button(quiz_window, text="Next", command=self.next_btn,
                             width=10, bg="#3D2C8D", fg="#916BBF", font=("ariel", 16, "bold"),activebackground="#3D2C8D",activeforeground="#C996CC")

            # palcing the button on the screen
            nextbtn.place(x=340, y=420)

            # This is the second button which is used to Quit the GUI
            quitbtn = Button(quiz_window, text="Quit", command=quiz_window.destroy,
                             width=5, bg="#3D2C8D", fg="#916BBF", font=("ariel", 16, " bold"),activebackground="#3D2C8D",activeforeground="#C996CC")

            # placing the Quit button on the screen
            quitbtn.place(x=700, y=50)
        def display_options(self):
            val = 0

            # deselecting the options
            self.opt_selected.set(0)

            # looping over the options to be displayed for the
            # text of the radio buttons.
            for i in options[self.q_no]:
                self.opts[val]['text'] = i
                val += 1

        # This method shows the current Question on the screen

        def display_question(self):

            # setting the Question properties
            q_no = Label(quiz_window, text=question[self.q_no], width=60,
                         font=('ariel', 21, 'bold'), anchor='w', bg="#C996CC", fg="#3D2C8D")

            # placing the option on the screen
            q_no.place(x=100, y=120)

        # This method is used to Display Title

        def display_title(self):

            # The title to be shown
            title = Label(quiz_window, text="A Harry Potter Quiz",
                          width=100, bg="#916BBF", fg="#3D2C8D", font=("Cooper Black", 20))

            # place of the title
            title.place(x=-480, y=0)

        def radio_buttons(self):

            # initialize the list with an empty list of options
            queslst = []

            # position of the first option
            y_pos = 200

            # adding the options to the list
            while len(queslst) < 4:

                # setting the radio button properties
                radio_btn = Radiobutton(quiz_window, text=" ", variable=self.opt_selected,
                                        value=len(queslst)+1, font=("ariel", 19),bg="#C996CC", fg="#3D2C8D",activebackground="#c996cc",activeforeground="#3D2C8D")

                # adding the button to the list
                queslst.append(radio_btn)

                # placing the button
                radio_btn.place(x=100, y=y_pos)

                # incrementing the y-axis position by 40
                y_pos += 40

            # return the radio buttons
            return queslst

        def countdown(self, count):
            count_min = math.floor(count/60)
            count_sec = count % 60

            if count_sec < 10:
                count_sec = f"0{count_sec}"

            timer_label = Label(quiz_window, text="1:00", font=(
                "Helvetica", 24), fg="#3D2C8D", bg="#C996CC")
            timer_label.place(x=20, y=50)

            timer_label.config(text=f"{count_min}:{count_sec}")
            if count > 0:
                root.after(1000, self.countdown, count - 1)
            if count == 0:
                wrong_ans = self.data_size - self.correct
                correct = f"Correct: {self.correct}"
                wrong = f"Wrong: {wrong_ans}"

                # calcultaes the percentage of correct answers
                score = int(self.correct / self.data_size * 100)
                result = f"Score: {score}%"

                # Shows a message box to display the result
                mb.showinfo(
                    "Result", f"Your time is up!\n\n{result}\n{correct}\n{wrong}")
                lead_data = {
                    'Name': [final_name],
                    'Score': [self.correct],
                    'Time Left': [count]
                }
                df = pd.DataFrame(lead_data)
                df.to_csv('leader.csv', mode='a', index=False, header=False)
                print("Data appended successfully.")
                quiz_window.destroy()

                leader = Tk()
                dfa = pd.read_csv("leader.csv")
                dfa.sort_values(["Score", "Time Left"], axis=0,
                                ascending=False, inplace=True, na_position='first')
                dfa.to_csv('leader.csv', mode='w+', index=False)
                with open("leader.csv") as fp:
                    mytable = from_csv(fp)
                leader.geometry("500x400")
                output_text = Text(leader, height=100,
                                   width=100, bg="#C996CC",fg="#3D2C8D",border="0",pady=30,padx=125)
                output_text.insert(END, mytable)
                output_text.place(x=1, y=1)
                leader.mainloop()

            if self.q_no == self.data_size:
                global final_count
                final_count = count

    # Create a GUI Window
    quiz_window = Tk()

    # set the size of the GUI Window
    quiz_window.geometry("800x500")
    quiz_window.configure(bg="#C996CC")

    # set the title of the Window
    quiz_window.title("You're a Quizzard Harry")

    quiz = Quiz()

    quiz_window.mainloop()


# Create Main Buttons
start_button = Button(root, text="Start", height=2, width=8, font=(
    "Helvetica", 24), bg="#012626", fg="white", border=0, command=start,activeforeground="#B6E7F2",activebackground="#012626")
exit_button = Button(root, text="Exit", height=1, width=6, font=(
    "Helvetica", 16), bg="#012626", fg="white", border=0, command=root.destroy,activeforeground="#B6E7F2",activebackground="#012626")
name_label = Label(root, text="Enter Name", height=1, width=12, font=(
    "Helvetica", 16), bg="#012626", fg="white", border=0)
name_entry = Entry(root, width=20, border=0, font=(
    "Helvetica", 16), bg="#012626", fg="white")
# Display Main Buttons
my_canvas.create_window(330, 260, anchor="nw", window=start_button)
my_canvas.create_window(370, 380, anchor="nw", window=exit_button)
my_canvas.create_window(340, 50, anchor='nw', window=name_label)
my_canvas.create_window(295, 100, anchor='nw', window=name_entry)

# Music Functions
pygame.mixer.init()


def play():
    pygame.mixer.music.load("harry-potter-ringtone.mp3")
    pygame.mixer.music.play()


def stop():
    pygame.mixer.music.stop()


# Create Music Buttons
play_button = Button(root, text="Play", height=1, width=4, font=(
    "Helvetica", 10), bg="#012626", fg="white", border=0, command=play,activeforeground="#B6E7F2",activebackground="#012626")
stop_button = Button(root, text="Stop", height=1, width=4, font=(
    "Helvetica", 10), bg="#012626", fg="white", border=0, command=stop,activeforeground="#B6E7F2",activebackground="#012626")
# Display Music Buttons
my_canvas.create_window(640, 440,
                        anchor="nw",
                        window=play_button)

my_canvas.create_window(690, 440,
                        anchor="nw",
                        window=stop_button)

# Open GUI Window
root.mainloop()
