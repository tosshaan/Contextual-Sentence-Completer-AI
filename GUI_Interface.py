from tkinter import *
import tkinter
from word_prediction import *
from tkinter.scrolledtext import ScrolledText

LABELS_DICT = {0: "1st options", 1: "2nd options", 2: "3rd options"}
class GUIInterface:
    def __init__(self):
        #self.value = 0
        self.categories_dict = generate_categories_dict()

    def add_text(self,message):
        message += " "
        self.scrolling_window.insert(END,message)
        self.get_predictions(None)

    def get_predictions(self, event):
        whole_text = self.scrolling_window.get(1.0,END)
        whole_text = whole_text.strip()
        word_wise = whole_text.split(" ")
        evidence = word_wise[-4:]
        print(whole_text)
        print(evidence)
        next_words = ["example","example","example"]
        # Getting next prediction
        if( len(evidence) > 3):
            next_words = predictNextWord(evidence, self.categories_dict, "politics", probsUnigram(self.categories_dict, "politics"))
        self.update_buttons([ [word] * 5 for word in next_words])

    def update_buttons(self, new_predictions):
        print(new_predictions)
        for i,button in enumerate(self.buttons):
            button.config(text = new_predictions[i//5][i % 5], command = lambda i=i: self.add_text(new_predictions[i//5][i%5]))

    def predict_category(self):
        print("Prediction coming right up!")
        self.top_frame_label.config( text = "Category changed TODO")

    def handleGUI(self):
        main_window = Tk()
        # Creating scrolling window and adding callback
        self.topFrame = Frame(main_window)
        self.topFrame.pack()
        self.top_frame_label = Label(self.topFrame, text = "Current category is: ")
        self.top_frame_label.pack(side = LEFT, padx = 50)
        self.top_frame_button = Button(self.topFrame, text = "Predict category", command = self.predict_category)
        self.top_frame_button.pack( side = RIGHT, padx = 50)
        self.scrolling_window = ScrolledText(main_window, width=100, height=20)
        self.scrolling_window.pack()
        main_window.wm_title("Categorized text predicter")
        #main_window.bind_all("<space>", lambda scrolling_window=scrolling_window: print_words(scrolling_window))
        main_window.bind_all("<space>", self.get_predictions)

        # Creating frames to keep buttons for suggestions
        options_frame = []
        messages = ["example", "example example", "example example example", "example example example example","example example example example example"]
        labels = []
        self.buttons = []
        for j in range(0,3):
            options_frame.append(Frame(main_window))
            options_frame[j].pack()
            options =[]
            label = Label(options_frame[j], text=LABELS_DICT[j])
            label.pack()
            for i in range(0,5):
                temp_button = tkinter.Button(options_frame[j])
                self.buttons.append(temp_button)
                #options.append(tkinter.Button( options_frame[j], text = messages[i], command = lambda i=i: self.add_text(messages[i])))
                #options[i].pack(side = LEFT)
                temp_button.pack(side = LEFT)

        main_window.mainloop()


# For testing purposes
if __name__ == '__main__':
    g = GUIInterface()
    g.handleGUI()
