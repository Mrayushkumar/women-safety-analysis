import tkinter as tk
from tkinter import *
from tkinter.font import BOLD, Font
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pandas as pd
from tkinter import filedialog
from tkinter import messagebox
from textblob import TextBlob
import matplotlib.pyplot as plt


## Create the DynamicGUI class for User Interface use Tkinter library.

class DynamicGUI(tk.Frame):
   
    
    def __init__(self,master=None):
       
        super().__init__(master)
        
       
        self.create_widgets()
        self.create_buttons()
        self.text()
        
        self.master = master
    
       
    ## Creating the function of WIdgets for GUI .

    def create_widgets(self):
        self.bold25 = Font(self.master, size=25, weight=BOLD,underline=True,slant="italic")
        self.bold20 = Font(self.master,family= "Times", size=12, weight=BOLD,underline=True,slant="italic")
        
        self.label1 = tk.Label(self.master,height=3,width=90, bg='aquamarine1',text="WOMEN SAFETY ANALYSIS ACCODING TO TWITTER DATA",compound='center',font=self.bold25)
        self.label1.pack(ipadx=100)
    
    ## Create text box for user interface.
    
    def text(self):
        
        self.textbox = tk.Text(self.master)
        self.textbox.pack(padx=10,pady=0,ipadx=800,ipady=1000)
        Scroll= tk.Scrollbar(self.textbox)
        Scroll.pack(side =RIGHT, fill=Y)
        Scroll.config(command=self.textbox.yview)
        self.textbox.config(yscrollcommand=Scroll.set)
        
          
    ##Creating buttons for GUI with tkinter .
    
    def create_buttons(self):   
        self.label=tk.Label(self.master,bg='red',bd='17 pixel' ,width=200,height=8)
        self.label.place(x=5,y=40)
        
        self.button_frame=tk.Frame(self.label,height=5,width=2)
        self.button_frame.place(x=50,y=70)
        self.button_frame.pack()
        
        self.button = tk.Button(self.button_frame, text="Upload and Read tweets data",font=self.bold20,bg="dark slate grey", fg="white", command=lambda:upload_data(self.textbox))
        self.button.place(x=50, y=50)
        
        self.button.pack(side="left",padx=15,pady=5,ipadx=15,ipady=10)
        self.button_frame.pack(ipadx=10,ipady=5)
        self.label.pack()
        
        # self.button = tk.Button(self.button_frame, text="Read tweets",font=self.bold20, bg="dark slate grey", fg="white", command=read_tweets)
        # self.button.pack(side="left",padx=15,pady=5,ipadx=15,ipady=10)
        
        self.button = tk.Button(self.button_frame, text="Tweet cleaning",font=self.bold20, bg="dark slate grey", fg="white", command=lambda: tweet_cleaning(self.textbox))
        self.button.pack(side="left",padx=15,pady=5,ipadx=15,ipady=10)
        
        self.button = tk.Button(self.button_frame, text="Run machine learning algorithm", font=self.bold20, bg="dark slate grey", fg="white", command=lambda: run_algorithm(self.textbox))
        self.button.pack(side="left",padx=15,pady=5,ipadx=15,ipady=10)
        
        self.button = tk.Button(self.button_frame, text="Analysis graph",font=self.bold20, bg="dark slate grey", fg="white", command=lambda: analysis_graph(self.textbox))
        self.button.pack(side="left",padx=15,pady=5,ipadx=15,ipady=10)
        
        
        self.label.pack(ipadx=20,ipady=5,padx=10,pady=15)

##Creating the function for the module upload data .

def upload_data(text_widget):
      file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
      if file_path:
        try:
            df = pd.read_csv(file_path)
            messagebox.showinfo("Success", "Dataset uploaded successfully!")
            text_widget.insert(tk.END, df.to_string())  # Display the dataframe in the textbox
        except:
            messagebox.showerror("Error", "Failed to upload the dataset!")

## Creating the function of Tweet Cleaning module.

def tweet_cleaning(text_widget):
    text_data = text_widget.get("1.0", "end-1c")  # Get the content of the textbox
    
    # Clean duplicates
    unique_tweets = list(set(text_data.split("\n")))
    cleaned_data = "\n".join(unique_tweets)
    
    # Clean null data
    cleaned_data = cleaned_data.replace("null", "")
    
    # Clean incomplete data
    
    cleaned_data = cleaned_data.replace("...", "")
   
    # Clean special characters and unnecessary data
    
    special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=', '[', ']', '{', '}', '|',
                     '\\', ':', ';', '<', '>', ',', '.', '?', '/', '~', '`']
    for char in special_chars:
        cleaned_data = cleaned_data.replace(char, "")
    ##arrange data in ascending format
    
    cleaned_data = "\n".join(sorted(cleaned_data.split("\n"), key=str.lower))
    text_widget.delete("1.0", "end")  # Clear the existing content
    text_widget.insert("1.0", cleaned_data)  # Insert the cleaned and sorted data


## Creating the function of Run Algorithm Module.

## Creating the function of Run Algorithm Module.
def run_algorithm(text_widget):
    global positive_count, negative_count, neutral_count 
    text_data = text_widget.get("1.0", "end-1c")  # Get the content of the textbox
    corpus = text_data.split("\n")
    sentiment_scores = []
    
    for tweet in corpus:
        analysis = TextBlob(tweet)
        sentiment_scores.append(analysis.sentiment.polarity)

    positive_count = sum(score > 0 for score in sentiment_scores)
    negative_count = sum(score < 0 for score in sentiment_scores)
    neutral_count = sum(score == 0 for score in sentiment_scores)

    analysis_result = f"Positive Tweets: {positive_count}\n"
    analysis_result += f"Negative Tweets: {negative_count}\n"
    analysis_result += f"Neutral Tweets: {neutral_count}\n"

    text_widget.delete("1.0", "end")  # Clear the existing content
    text_widget.insert("1.0", analysis_result)  # Insert the analysis result


def analysis_graph(text_widget):
    text_data = text_widget.get("1.0", "end-1c")  # Get the content of the textbox

    # Calculate percentage values
    total_count = positive_count + negative_count + neutral_count
    positive_percentage = (positive_count / total_count) * 100
    negative_percentage = (negative_count / total_count) * 100
    neutral_percentage = (neutral_count / total_count) * 100

    # Create the labels and values for the pie chart
    labels = ["Positive", "Negative", "Neutral"]
    values = [positive_percentage, negative_percentage, neutral_percentage]
    
    # Define custom colors
    colors = ['#34A853', '#EA4335', 'orange']
    fig = plt.figure(figsize=(9, 5))

    # Plot the pie chart
    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title("Sentiment Analysis", fontweight='bold', fontsize=14)
    
    # Add a legend
    legend_labels = [f"{label}: {value:.1f}%" for label, value in zip(labels, values)]
    plt.legend(legend_labels, loc='best', bbox_to_anchor=(1, 1))

    plt.show()


root = tk.Tk()
root.geometry('1030x500')


# if __name__ == "__main__":
app = DynamicGUI(master=root)

app.mainloop()

