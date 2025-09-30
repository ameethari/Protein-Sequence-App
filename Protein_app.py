import customtkinter as ctk
from Bio import Entrez #Biopython’s tool to connect to NCBI’s databases.
import threading #lets us fetch data in the background so the app doesn’t freeze.
import tkinter as tk
from tkinter import messagebox, filedialog #dialog boxes (pop-ups and file save windows)
import webbrowser #lets you open links in the default browser.
import time




# set up app appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")




#starting the class 
class ProteinSearchApp: #this wraps all code into a class, keeping code organised - a class is a blueprint/template for creating objects(which contain data and functions to handle certain tasks like a software)
    def __init__(self): #this function is an intialiser (a special method), and is the blueprint for how a new object of that class should be set up when it's first created 
        self.root = ctk.CTk() #this makes the main window
        self.root.title("Protein Sequence Finder") #sets the top bar text
        self.root.geometry("900x700")
        self.root.minsize(800, 600) #this prevents the window being squished smaller than this

        #Variables
        self.current_sequence = "" #a placeholder for the FASTA sequence that will be outputted later
        self.current_info = "" #a placeholder for metadata like title, length, organism

        self.setup_ui() #calls another function that build the buttons, inputs and layouts


#1 BUILDING THE GUI - BUILD ALL THE FRAMES, BUTTONS, LABEL, INPUTS AND TEXT AREAS IN THE APP

    def setup_ui(self): #very big and important function
    #main container frame, everything sits in this
        main_frame = ctk.CTkFrame(self.root) #this creates a container inside the main window to hold all the widgets
        main_frame.pack(fill="both", expand=True, padx=20, pady=20) #this makes it fill the space wth some padding around it
    

    #now the title and subtitle
        title_label = ctk.CTkLabel( #this starts defining a label widget
            main_frame, # this specifies that this label should be inside the mainframe container (the parent widget)
            text = "Protein Sequence Finder",
            font = ctk.CTkFont(size=28, weight="bold")
        ) #this closes the CTkLabel function call
        title_label.pack(pady=(20,10)) #uses the pack geometry manager to place the title_label in the GUI, the numbers sets the vertical padding(empty space) above the label to 20 pixels and below the label 10 pixels

        subtitle_label = ctk.CTkLabel(
            main_frame,
            text = "Search NCBI's protein database and retrieve FASTA sequences",
            font = ctk.CTkFont(size=14),
            text_color = "gray"
        )
        subtitle_label.pack(pady=(0,30))


        #now the input section 
        input_frame = ctk.CTkFrame(main_frame) #this creates a new frame inside mainframe to hold inputs -ctk.CTk are the GUI widgets, so ctk.CTkLabel/Font/Button/Entry - this creates the widgets on the page 
        input_frame.pack(fill="x", padx=20, pady=(0,20))

        #now the email input

        #first part creates and places a static text label - this tells the user what the next field is for
         #create the label 
        email_label = ctk.CTkLabel(input_frame, text="Email (Required by NCBI):", anchor="w") #creates email widget containing that text and sets the text alignment within the label widget to 'w', west
        #place the label
        email_label.pack(fill="x", padx=20, pady=(20, 5)) # 'fill = x' means the widget label will stretch horizontally to fill all the available space alloted to it by its parent container after any padding has been applied

        #second part creates and places a user input field - interactive widget where user can actually type in their data
        self.email_entry = ctk.CTkEntry( #called self.email_entry because it stores it as an accessible attribute for the class (makes it referencable), so it can be used by other functions in the future - email info may be needed in future 
            input_frame,
            placeholder_text = "your.email@example.com",
            height=40 # this sets the height of the input box to 40 pixels making it taller than normal
        )
        self.email_entry.pack(fill="x", padx=20, pady=(0,15))

        #now the protein name input
        #create and place label
        protein_label = ctk.CTkLabel(input_frame, text="Protein Name:", anchor="w")
        protein_label.pack(fill="x", padx=20, pady=(0,5))

        #create interactive input box
        self.protein_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text = "e.g., Human Hemoglobin, Insulin, Lysoxyme",
            height=40 
        )
        #place interactive input box
        self.protein_entry.pack(fill="x", padx=20, pady=(0,15))



        #now pressing enter button to trigger search
        self.protein_entry.bind("<Return>", lambda e: self.search_protein()) #the text input field is attached to an event handler (.bind()), which tells it to watch out for a certain event. ie pressing the enter/return button. the lambda function immediatley calls the self.search_protein() method to retrieve the protein sequence. the lambda e: is standard way to define a temp function that accepts the event object 'e' passed by the system

        #now creating a clickable search button in case people don't press enter
        self.search_button = ctk.CTkButton( #the 'self.' makes it accessible by other methodsin the class
            input_frame, 
            text= "Search Protein",
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.search_protein #ACTION LINK - this tells the button what python function ot run when clicked
        )
        self.search_button.pack(pady=(0,20))



        #quick example protein buttons to use in rows
        #create a new container called examples_frame and placing a label inside to introduce a section of example protein buttons - OTHER CONTAINER IS THE INPUT CONTAINER BOX
        examples_frame = ctk.CTkFrame(input_frame)
        examples_frame.pack(fill="x", padx=20, pady=(0,20))

        examples_label = ctk.CTkLabel(examples_frame, text ="Quick Examples:", anchor="w")
        examples_label.pack(fill="x", padx=15, pady=(15,10))

        #producing the types of examples i will show in the examples container
        examples = [
            ("Human hemoglobin", "human hemoglobin"),   #"display name", "search name"
            ("Human Insulin", "human insulin"),
            ("Lysozyme", "lysozyme"),
            ("Human Albumin", "human albumin"),
            ("Cytochrome C", "cytochrome c")
        ]

        #now placing the buttons for each of those proteins - 3 in row 1 and 2 in row 2
        button_frame1 = ctk.CTkFrame(examples_frame, fg_color="transparent") #this means the buttons frame is placed inside the examples frame
        button_frame1.pack(fill="x", padx=15, pady=(0,10))
    
        button_frame2 = ctk.CTkFrame(examples_frame, fg_color="transparent") #this means the buttons frame is placed inside the examples frame
        button_frame2.pack(fill="x", padx=15, pady=(0,15)) #this means buttonframe 1 will be slightly above buttonframe 2


        #for loop to automatically create several small, pre-set example buttons and arrange them
        for i, (display_name, search_term) in enumerate(examples): #sets up for loop that goes through each item in examples list and unpacks each item into two values - display name and search name - Enumerate(examples) gives the iterable list an index, starting at 0
            parent = button_frame1 if i < 3 else button_frame2 #uses if statement so if the buttons assigned the index value of 1,2,3 then will be put in buttonframe1 above and the rest go in buttonframe2 below
            btn=ctk.CTkButton( #creates a new button widget
                parent, #this puts btn in the parent container (which is made of buttonframe1/2)
                text=display_name, #sets the text shown on the button as the display name from the examples list
                width = 120,
                height = 30, #sets width and height of button
                command = lambda term=search_term: self.set_example(term) #when the button is clicked (command) it calls the self.set_example() method passing the search_term into the search query
            ) #closes the button creation call
            btn.pack(side="left", padx=5, pady=2) #places the button, the padding is for the padding between each button 
        

        #progress bar + status
        self.progress_bar = ctk.CTkProgressBar(main_frame)
        self.progress_bar.pack(fill="x", padx=20, pady=(0,10))
        self.root.update()
        #self.progress_bar.pack_forget() # to hide the progress bar initially 

        self.status_label = ctk.CTkLabel(main_frame, text="", text_color="gray")
        self.status_label.pack(pady=(0,10))



        #now results section
        self.results_frame = ctk.CTkFrame(main_frame) #just created the results_frame, that is within the main_frame
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))

        results_header = ctk.CTkFrame(self.results_frame)
        results_header.pack(fill="x", padx=15, pady=15)

        results_title = ctk.CTkLabel(
            results_header,
            text="Results",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor = "w"
        )
        results_title.pack(side="left", padx=10)


        #now create a copy button to copy the results
        self.copy_button = ctk.CTkButton( #using self here makes the copy_button a permenant attribute of the application object allowing it to be controlled, modified and managed by the rest of the class' logic - like i might want to disable the copy button if there are no search results for example
            results_header,
            text = "Copy",
            width = 80,
            command=self.copy_sequence
        )
        self.copy_button.pack(side="right", padx=5)
    

        #now create a save button to save the results
        self.save_button = ctk.CTkButton(
            results_header,
            text = "Save",
            width = 80,
            command=self.save_sequence  #i will create this method(basically function) later
        )
        self.save_button.pack(side="right", padx=5)
    

        #now create protein metadata box (like title, length of amino acid chain, organsim...)
        self.info_textbox = ctk.CTkTextbox(
            self.results_frame,
            height=100,
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.info_textbox.pack(fill="x", padx=15, pady=(0,10))


        #now create a protein sequence box
        self.results_textbox= ctk.CTkTextbox(
            self.results_frame,
            font=ctk.CTkFont(family="Consolas", size=11),
            wrap="char" #this is a setting for a text box that determines how long lines of text are broke up - in this case, the text will break and move to the next line after any single character if the line runs out of space - as the DNA/Protein sequence wont have any natural gaps in it - instead of word wrap, which will wait for a whole word before moving to next line - this is done by the CHARacter
        )
        self.results_textbox.pack(fill="both", expand=True, padx=15, pady=(0,15)) #fill both means fill extra space in both the horizontal and vertical directions. Expand=True tells the textbox to absorb any extra space allocated to its parent frame, allowing the widget to grow if the user enlarges the application window


        #disable copy button and save button until data appears
        self.copy_button.configure(state="disabled")
        self.save_button.configure(state="disabled")


        #footer
        footer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        footer_frame.pack(fill="x", padx=20, pady=(0,10))

        #footer label
        footer_label = ctk.CTkLabel(
            footer_frame,
            text="Powered by Biopython & NCBI Entrez | Made with CustomTkinter",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        footer_label.pack() #no arguments to allow default pack() settings - placed in centre of parent container, makes label just big enough to fit text and not bigger, no padding/extra space needed as default for padx/pady is 0

    #the function (defproteinsearchapp) stops here





    #2 - INPUT HANDLING 
    def set_example(self, protein_name): #the set_example function only takes these two arguments
        #set protein name when quick button clicked
        self.protein_entry.delete(0, tk.END) #this tells the protein entry box to delete all existing text when the button is pressed
        self.protein_entry.insert(0, protein_name) #which allows this to input the name of the protein into the protein entry box when the button is pressed 


    def validate_inputs(self):
        #check if email and protein name are valid
        email = self.email_entry.get().strip() #this retrieves the email and strips out of any leading or tailing white space like spaces or tabs
        protein_name = self.protein_entry.get().strip()

    #Guard clause - 
        if not email: #not email would be true when the string is empty because it represents nothing - if just email and it was empty then it would be false(y) - Since "" is a falsy value, not "" evaluates to True.
            messagebox.showerror("Input Error", "Please enter your email address.") #function that is good for user experience
            return False #as soon as an error is found, it executes return False and stops and tells the computer that the input is not valid
        if "@" not in email or "." not in email:
            messagebox.showerror("Input Error", "Please enter your email address.")
            return False
        if not protein_name:
            messagebox.showerror("Input Error", "Please enter a protein name.")
            return False
        return True #if the code reaches here and all checks are passed, then function returns true, meaning the validation has succeeded
    #uses a series of independant if statements to check conditions one by one - if any condition is met, it immediately stops and shows an error


    def search_protein(self):  #this is the method we used earlier and now we are actually making what it does
        #start protein search (runs in background thread)
        if not self.validate_inputs(): #the function calls the self.validate_inputs method which checks the email and protein input fields - if any of the if statements in validate_inputs code block finds an error then returns false, if not then the operator flips it to True, so the if condition is met. 
            return #if the if condition is true(meaning the validation failed), this command exits the search_protein method
        #the if statement is designed to be True only when the validation failed(false) - due to the operator of not flipping it, so the code can execute the stop(return)

    #so this function is the primary method that controls the rest of the workflow - called when the user presses enter or clicks search button - this method was used earlier and now coding what it does now

    #now make a disable button and show progress bar for when the search button/enter has been pressed
        self.search_button.configure(state="disabled", text="Searching...") #disable the button so it can't be pressed again and change the text to searching...
        self.progress_bar.pack(fill="x", padx=20, pady=(0,10)) #this actually displays the progress bar now which was hidden before
        self.progress_bar.set(0) #this sets the initial value of the progress bar to 0 before it starts moving up
        self.status_label.configure(text="Connecting to NCBI...") #this changes the text shown in the status label to show that, giving user immediate confirmation that the search is happening

    #now the code to clear all the old results - cleanup sequence before a new search begins
        self.info_textbox.delete("1.0", tk.END) #delete clears all metadata/accession number text in info_textbox - 1.0 refers to clearing from beginning of the text at line 1 - tk.END ensures the clearing occurs till the end of the text
        self.results_textbox.delete("1.0", tk.END) #same for clearing the sequence_textbox
        self.copy_button.configure(state="disabled") #prevents user copying old or non-existent results
        self.save_button.configure(state="disabled") ##prevents user saving old or non-existent results

    #this makes the code run in thread (run in the background so the UI doesn't freeze while waiting for NCBI)
        email = self.email_entry.get().strip()
        protein_name = self.protein_entry.get().strip() #reassigning same values again to email and protein_name

        search_thread = threading.Thread( #creates a new thread from pythons threading module - a thread is a parallel worker inside the programme
            target=self.perform_search, #this specifies the function the new thread should run - run the method self.perform_search which we will code later on to do the actual ncbi search
            args=(email, protein_name), #this passes these arguments into the self.perform_search method as it needs this info to carry out the ncbi search
            daemon=True #this marks this thread as a daemon thread, so the programm won't wait for this thread to finish when the main application is closed, it will shut down too contemporaneously
        )
        search_thread.start() #this immediately starts the thread, causing self.perform_search function to run in the background, allowing the main UI to remain responsive 





    #3 - CREATING CODE FOR THE NCBI SEARCH (BACKGROUND THREAD)
    def perform_search(self, email, protein_name): #it accepts the application instance 'self' as an argument as well as the other 2
        try: #try is used to start the try block as it ensures that if any network communication errors occur, it wont crask straightaway  
            Entrez.email = email #tell NCBI who is using it, needed for the NCBI API

            #step one = search
            self.root.after(0, lambda: self.progress_bar.set(0.2)) #because this is running in a thread, the method cannot directly access the GUI widgets, so self.root.after schedules an update to run 0ms on the main GUI thread, pushing the progress bar to 20%
            self.root.after(0, lambda: self.status_label.configure(text="Searching protein database..."))#this schedules an update to change the status label text, giving the user live feedback
            handle = Entrez.esearch(db="protein", term = protein_name, retmax=5) #start of the actual NCBI request
            search_results = Entrez.read(handle)
            handle.close()
            id_list = search_results["IdList"]
            
            #another Guard Clause 
            if not id_list: #this checks if id_list is empty - if it is empty. then 'no id_list' condition is true
                self.root.after(0, lambda: self.show_no_results(protein_name)) #if no ids were found, it schedules a call to the self.show_no_results method to run on the main thread to show the reader an error message 
                return #immediately exits the perform search method, stopping the background thread as no data to retrieve in next steps
            

            #step two = get summary
            self.root.after(0, lambda: self.progress_bar.set(0.5)) #this technique updates the GUI from a background thread - only main thread can modify any GUI widget, no side threats or else crash. self.root = main window application, after(0), makes it run 0ms after (it tells the main thread, when you get a chance, run this function next). the lambda function wraps up the unsafe code and scheduling it with 'after' to just after, changing the progress bar from 20% to 50%
            self.root.after(0, lambda: self.status_label.configure(text="Retrieving sequence information..."))
            handle = Entrez.esummary(db="protein", id=id_list[0])
        
            summary = Entrez.read(handle)
            handle.close()

            #step 3 = fetch FASTA sequence
            self.root.after(0, lambda: self.progress_bar.set(0.8))
            self.root.after(0, lambda: self.status_label.configure(text="Downloading sequence..."))
            handle=Entrez.efetch(db="protein", id=id_list[0], rettype="fasta", retmode="text")
            sequence= handle.read()
            handle.close()

            #step 4 = display results
            self.root.after(0, lambda: self.progress_bar.set(1.0))
            self.root.after(0, lambda: self.display_results(summary, sequence)) #this lambda function is telling the main application thread to display the search results immediately. this method will update the GUIs with the summary info and the sequence

        except Exception as e: #error handler - catch errors from the preceding 'try' block like a network failure, the programme jumps here and teh specific error message is captured in the variable - the 'e' contains the error message given by NCBI which will get displayed
            error_msg = f"Error searching for protein: {str(e)}" #appends this error message with the error message given by NCBI
            self.root.after(0, lambda: self.show_error(error_msg)) #this calls the method - self.show_error passing the actual error_msg - the show_error method will then update the GUI with the erro_msg




    #4 DISPLAY RESULTS AND ERROR HANDLING
    def show_no_results(self, protein_name):
        #no results found
        self.status_label.configure(text=f"No results were found for '{protein_name}'")
        self.info_textbox.insert("1.0", f"No protein sequences found for '{protein_name}'.")
        self.reset_search_button() #enable this and change its text back to "search protein" and hide the progress bar

    def show_error(self, error_msg):
        #show error if something goes wrong - this runs on the main application thread still
        self.status_label.configure(text="Error occured during search")
        self.info_textbox.insert("1.0", f"Error: {error_msg}") #displays more detailed error message
        messagebox.showerror("Search Error", error_msg) #this opens a modal pop up window on the screen, with title "search error" and the body displays the error message - ensures the user notices the failure immediately
        self.reset_search_button()

    def display_results(self, summary, sequence):
        #shows results in the UI - NOT ERROR HANDLING

        #store values
          # Clear old content
        self.info_textbox.delete("1.0", tk.END)
        self.results_textbox.delete("1.0", tk.END)

        record = summary[0]

    # Show summary information
        self.info_textbox.insert(
            tk.END,
            f"Title: {record.get('Title', 'N/A')}\n"
            f"Organism: {record.get('Organism', 'N/A')}\n"
            f"Length: {record.get('Length', 'N/A')} aa\n"
            f"Accession: {record.get('AccessionVersion', 'N/A')}\n"
        )

    # Show sequence in the results box
        self.results_textbox.insert(tk.END, sequence) #this final organism bit uses the python dictionary method.get(key, default_value), in case the organism info is missing from the search results
        

        #show results in text boxes
        self.info_textbox.insert("1.0", self.current_info) #start insertion of info at line 1, character 0
        self.results_textbox.insert("1.0", sequence)

        self.status_label.configure(text="Search completed succesfully.")

        #enable buttons
        self.copy_button.configure(state="normal")
        self.save_button.configure(state="normal")
        self.reset_search_button()

    def reset_search_button(self): #resets buttons for next user input
        #restore button and hide progress bar
        self.search_button.configure(state="normal", text="Search Protein") #restores the button - state back to normal so it can be clicked again and changes text back from 'searching' to its original label
        self.progress_bar.pack_forget() #removes the progress bar from the main window, but is ready to be shown again, thanks to .pack()



    #5 - COPY + SAVE
    def copy_sequence(self): #finally making the method that copies the sequence that is assigned to the button from above
        #copy to clipboard
        if self.current_sequence: #another guard clause - this first line is checking if self.current_sequence has a value, ie a sequence that has been stored in it, preventing user copying an empty search result
            self.root.clipboard_clear() #this clears any previous content from the OSs clipboard
            self.root.clipboard_append(self.current_sequence)
            self.status_label.configure(text="Sequence copied to clipboard!") #immediate user feedback given

    def save_sequence(self):
        #save FASTA file
        if not self.current_sequence:
            return
        
        protein_name = self.protein_entry.get().strip() #uses the protein name entered by the user earlier and cleans it
        default_filename =f"{protein_name.replace(" ", "_")}_sequence.fasta" #creates suggested filename

        file_path = filedialog.asksaveasfilename( #this calles the asksaveasfilename function from the filedialog module to open the OS's save as window
            defaultextension=".fasta",
            initialfilename=default_filename, #prefills the filename box with cleaned user version from above
            filetypes=[("FASTA files", "*.fasta"), ("Text files", "*.txt"), ("All files", "*.*")] #this defines the list of file types seen in the OS's save as window that the user can choose from
        )

        if file_path: #checks user has provided a valid file path
            try: #starts a try block again - involves any code that involves writing to external operations like the disc - put in try block so if it fails it doesnt crash the app
                with open(file_path, "w") as f: #this opens the file located at file_path. 'w' specifies writing mode, meaning the file will be created/overwritten. 'as f' assigs the file variable to f. the 'with' statement automatically ensures the file is close via f.close()
                    f.write(f"# Protein Information: \n# {self.current_info.replace(chr(10), chr(10)+'#')}\n\n") #this writes all the protein's info like title, length and organsim to the file as a header. the code replaces every new line in the info string with a newline plus a # symbol to comment out every line of the metadata, out of the FASTA file
                    f.write(self.current_sequence) #this writes the actual protein sequence(core data) to the file immediatley after the header
                self.status_label.configure(text=f"Sequence saved to {file_path}") #if the saving is a success, it will update the status_label with success message
            except Exception as e: #if any error from saving process occurs, it's captured in e variable
                messagebox.showerror("Save Error", f"Could not save file: {str(e)}") #and displays a pop up window with specific error message
        


#6- RUN APP
    def run(self): #this defines the 'run' method for the app
        self.root.mainloop() #this calls the crucial mainloop() method on the main window object(self.root) - puts the window on the screen and starts the event loop



    #7- MAIN ENTRY POINT
if __name__ == "__main__": #standard python guard clause - ensures the code block only runs when the script is executed directly
    try: #starts try block to attempt the necessary imports
        import tkinter as tk
        from tkinter import messagebox, filedialog
        from Bio import Entrez
        import threading


    except ImportError as e: #if either of the imports fail, execution jumps here and the specific missing package is stored in e
        print(f"Missing required package: {e}")
        print("Install them with: pip install customtkinter biopython")
        exit(1) #this causes the app to close due to an error of missing packages#

    app = ProteinSearchApp()
    app.run()
        

