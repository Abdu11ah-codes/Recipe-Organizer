#  Python Recipe Organizer with customtkinter (Biggest Project so far)
import _tkinter
from customtkinter import *
from PIL import Image
from playsound import playsound
import json
import os

start_icon = Image.open('recipe photos/start.png')
stop_icon = Image.open('recipe photos/stop.png')
start_ctk = CTkImage(light_image=start_icon,dark_image=start_icon,size=(25,25))
stop_ctk = CTkImage(light_image=stop_icon,dark_image=stop_icon,size=(25,25))

running = True
time_displayed = None
duration_entered = None
y_ing = 115
y_stp = 80
y_tmr = 55
steps_list = []
ing_list = []
timer_list = []
duration_entry = None
add_btn = None

ing_entries = []
steps_entries = []
timer_durations = []
recipe = {
    "ingredients":ing_entries,
    "steps":steps_entries,
    "timers":timer_durations
}

remaining_time = 0

ing_count = 0
step_count = 0
timer_count = 0
# Functions
def add_recipe():
    # Functions
    def save():
        os.makedirs('recipes', exist_ok=True)
        file_path = f'recipes/{recipe_name.get()}.json'
        with open(file_path,'w',encoding='utf-8') as file:
            json.dump(recipe, file,indent=4,ensure_ascii=False)

    def delete():
        global y_stp, y_tmr, y_ing, running, time_displayed, duration_entered, steps_list, ing_list, timer_list, duration_entry, add_btn
        running = True
        time_displayed = None
        duration_entered = None
        y_tmr = 55
        y_stp = 80
        y_ing = 115
        steps_list = []
        ing_list = []
        timer_list = []
        duration_entry = None
        add_btn = None
        # Loop through all widgets in steps_frame and destroy the ones that are not in the keep list
        for widget in steps_frame.winfo_children():
            if widget not in [steps_title, steps_add_btn, steps_entry]:  # Compare with the actual widget objects
                widget.destroy()

        # Loop through all widgets in ingredient_frame and destroy the ones that are not in the keep list
        for widget in ingredient_frame.winfo_children():
            if widget not in [ing_title, amount_entry, ingredient_entry, unit_OM,ing_add_btn]:  # Compare with actual widget objects
                widget.destroy()

        # Loop through all widgets in timers_frame and destroy the ones that are not in the keep list
        for widget in timers_frame.winfo_children():
            if widget not in [timer_title]:  # Compare with the actual widget objects
                widget.destroy()

    # Frame functions
    def add_ing():
        global y_ing,ing_list, ing_count
        ing_count += 1
        if ing_count < 19:
            ing_entries.append(f" {ingredient_entry.get()}     {amount_entry.get()}{unit_OM.get()}")
            ingredient_label = CTkLabel(ingredient_frame, text=f"• {ingredient_entry.get()}     {amount_entry.get()}{unit_OM.get()}", font=("arial", 20))
            ingredient_label.place(x=10, y=y_ing)
            y_ing+=25
            amount_entry.delete(0, 'end')
            ingredient_entry.delete(0,'end')
            delete_btn = CTkButton(
                ingredient_frame,
                text="X",
                fg_color="red",
                width=20,
                height=20,
                font=("arial", 16),
                command=lambda: delete_ing(ingredient_label, delete_btn)
            )
            delete_btn.place(x=370, y=y_ing-25)

            # Add to ingredients list
            ing_list.append((ingredient_label, delete_btn))
        else:
            ing_popup = CTkToplevel(window)  # Creates a new pop-up window
            ing_popup.geometry("300x175+500+500")
            ing_popup.resizable(0, 0)
            ing_popup.title("ERROR")
            ing_popup.attributes("-topmost", True)
            CTkLabel(ing_popup, text="Can't add more than 18 ingredients", text_color="red", font=("Arial", 18)).pack(pady=20)
            CTkButton(ing_popup, text="OK", command=ing_popup.destroy).pack(pady=10)

    # Added delete_ing() function
    def delete_ing(label, button):
        global y_ing, ing_count
        ing_count -= 1
        # Get the index of the ingredient to be deleted
        index = ing_list.index((label, button))

        # Destroy the label and button
        label.destroy()
        button.destroy()
        del ing_list[index]

        # Reposition remaining ingredients
        y_ing -= 25
        for i in range(index, len(ing_list)):
            # Get the original y-coordinate for the current ingredient
            y = 115 + (i * 25)  # Start from the initial y-coordinate and increment by 25 for each ingredient
            ing_list[i][0].place(x=10, y=y)  # Update label position
            ing_list[i][1].place(x=370, y=y)  # Update delete button position
    def add_step():
        global y_stp,steps_list, step_count
        step_count += 1
        if step_count < 13:
            steps_entries.append(steps_entry.get())
            steps_label = CTkLabel(steps_frame, text=f" • {steps_entry.get()}", font=("arial", 20))
            steps_label.place(x=6, y=y_stp)
            steps_entry.delete(0, 'end')
            delete_btn = CTkButton(
                steps_frame,
                text="X",
                fg_color="red",
                width=20,
                height=20,
                font=("arial", 16),
                command=lambda: delete_step(steps_label, delete_btn,timer_btn)
            )
            timer = Image.open('recipe photos/timer.png')
            timer_ctk = CTkImage(light_image=timer,dark_image=timer,size=(25,25))
            timer_btn = CTkButton(steps_frame,image=timer_ctk,text="",fg_color='transparent',width=30,command=add_duration)
            delete_btn.place(x=460, y=y_stp)
            timer_btn.place(x=410,y=y_stp-5)

            # Add to steps list
            steps_list.append((steps_label, delete_btn,timer_btn))
            y_stp += 27
        else:
            stp_popup = CTkToplevel(window)  # Creates a new pop-up window
            stp_popup.geometry("300x175+500+500")
            stp_popup.resizable(0, 0)
            stp_popup.title("ERROR")
            stp_popup.attributes("-topmost", True)
            CTkLabel(stp_popup, text="Can't add more than 12 steps", text_color="red", font=("Arial", 18)).pack(pady=20)
            CTkButton(stp_popup, text="OK", command=stp_popup.destroy).pack(pady=10)
        # Added delete_step() function
    def delete_step(label, button,btn2):
        global y_stp, step_count
        step_count -= 1
        # Get the index of the step to be deleted
        index = steps_list.index((label, button,btn2))

        # Destroy the label and button
        label.destroy()
        button.destroy()
        btn2.destroy()
        del steps_list[index]

        # Reposition remaining steps
        y_stp -= 27
        for i in range(index, len(steps_list)):
            # Get the original y-coordinate for the current step
            y = 80 + (i * 27)  # Start from the initial y-coordinate and increment by 25 for each step
            steps_list[i][0].place(x=6, y=y)  # Update label position
            steps_list[i][1].place(x=460, y=y)  # Update delete button position
            steps_list[i][2].place(x=410, y=y-5)  # Update timer button position

    def add_timer():
        global duration_entry, y_tmr, add_btn, running, time_displayed, duration_entered, timer_count, start_ctk, stop_ctk
        timer_count += 1
        if timer_count < 8:
            timer_durations.append(duration_entry.get())
            try:
                duration_entered = int(duration_entry.get()) * 60
            except ValueError:
                y_tmr -= 29
            duration_entry.destroy()
            add_btn.destroy()
            # Create a duration label
            try:
                duration_label = CTkLabel(timers_frame, text=f'{int(duration_entered/60):02}:00', font=('arial', 20))
            except TypeError:
                pass
            try:
                duration_label.place(x=20, y=y_tmr)
            except UnboundLocalError:
                pass

            def start_timer():
                global running
                running = True
                countdown(duration_entered, duration_label)

            def stop_timer():
                global running
                running = False
                duration_label.configure(text=time_displayed)

            start_btn = CTkButton(
                timers_frame,
                width=30,
                command=start_timer,  # Start countdown
                text="",
                fg_color='transparent',
                text_color='black',
                image = start_ctk
            )
            stop_btn = CTkButton(
                timers_frame,
                width=30,
                command=stop_timer,  # Stop action
                text='',
                fg_color='transparent',
                text_color='black',
                image= stop_ctk
            )
            delete_btn = CTkButton(
                timers_frame,
                text="X",
                fg_color="red",
                width=20,
                height=20,
                font=("arial", 16),
                command=lambda: delete_timer(duration_label, start_btn,stop_btn,delete_btn))

            start_btn.place(x=300, y=y_tmr)
            stop_btn.place(x=350, y=y_tmr)
            delete_btn.place(x=460,y=y_tmr)
            try:
                timer_list.append((duration_label,start_btn,stop_btn,delete_btn))
            except UnboundLocalError:
                stop_btn.destroy()
                start_btn.destroy()
                delete_btn.destroy()
            y_tmr += 29
        else:
            stp_popup = CTkToplevel(window)  # Creates a new pop-up window
            stp_popup.geometry("300x175+500+500")
            stp_popup.resizable(0, 0)
            stp_popup.title("ERROR")
            stp_popup.attributes("-topmost", True)
            CTkLabel(stp_popup, text="Can't add more than 7 timers", text_color="red", font=("Arial", 18)).pack(pady=20)
            CTkButton(stp_popup, text="OK", command=stp_popup.destroy).pack(pady=10)
    
    def delete_timer(label, start_button, stop_button, delete_button):
        global y_tmr, timer_count
        timer_count -= 1
        # Get the index of the step to be deleted
        index = timer_list.index((label, start_button, stop_button, delete_button))

        # Destroy the label and button
        label.destroy()
        start_button.destroy()
        stop_button.destroy()
        delete_button.destroy()
        del timer_list[index]

        # Reposition remaining steps
        y_tmr -= 29
        for i in range(index, len(timer_list)):
            # Get the original y-coordinate for the current step
            y = 55 + (i * 29)  # Start from the initial y-coordinate and increment by 29 for each step
            timer_list[i][0].place(x=20, y=y)  # Update label position
            timer_list[i][1].place(x=300, y=y)  # Update start button position
            timer_list[i][2].place(x=350, y=y)  # Update stop button position
            timer_list[i][3].place(x=460, y=y)  # Update delete button position

    def countdown(duration, duration_label):
        """Simple countdown function using after() for non-blocking updates."""
        global running, time_displayed, duration_entered
        if duration > 0 and running:
            minutes, seconds = divmod(duration, 60)
            time_displayed = f"{minutes:02}:{seconds:02}"
            try:
                duration_label.configure(text=time_displayed)
            except _tkinter.TclError:
                pass
            timers_frame.after(1000, countdown, duration - 1, duration_label)  # Schedule next update
            try:
                duration_entered-=1
            except TypeError:
                pass
        elif duration == 0:
            duration_label.configure(text="Time's up!")  # Display when finished
            playsound('C:/Users/Lenovo/PycharmProjects/pythonProject/External Projects/wav/Alarm.wav')
            running = False
    def add_duration():
        global duration_entry, add_btn
        empty_label.destroy()
        duration_entry = CTkEntry(timers_frame,font=('Times new roman',15),placeholder_text='Duration (in Minutes)')
        add_btn = CTkButton(timers_frame,text="+",font=('impact',20,'bold'),fg_color='green', corner_radius=8, width=10, command=add_timer)
        duration_entry.place(x=230,y=20)
        add_btn.place(x=400,y=20)
    def back():
        for widget in window.winfo_children():
            widget.destroy()
        main()
    for widget in window.winfo_children():
        widget.destroy()
    CTkLabel(window,text="Add a Recipe",font=('georgian',60,'bold'),text_color='green').place(x=45,y=15)

    # Frames
    ingredient_frame = CTkFrame(window,border_color='white',border_width=5,width=420,height=580)
    steps_frame = CTkFrame(window,border_color='white',border_width=5,width=510,height=415)
    timers_frame = CTkFrame(window,border_color='white',border_width=5,width=510,height=265)

    ingredient_frame.place(x=30,y=115)
    timers_frame.place(x=475,y=430)
    steps_frame.place(x=475,y=5)

    # Buttons
    back_btn = CTkButton(window, text='Back', text_color='white', font=('arial', 25), border_color='black',border_width=3, corner_radius=5, fg_color='grey', command=back)
    CTkButton(window,text='Save',text_color='black',font=('arial',25),border_color='black',border_width=3,corner_radius=5,fg_color='green',command=save).place(x=650,y=710)
    CTkButton(window, text='Delete', text_color='black', font=('arial', 25), border_color='black', border_width=3,hover_color='orange',corner_radius=5, fg_color='red',command=delete).place(x=825, y=710)
    back_btn.place(x=150,y=710)
    # Entry
    recipe_name = CTkEntry(window,placeholder_text='Recipe name',font=('Times new roman',25),text_color='cyan',width=180)
    recipe_name.place(x=340,y=710)
    # Frame insides
    ing_title = CTkLabel(ingredient_frame,text='Ingredients',font=('Times new roman',30,'underline'),text_color='orange')
    ing_title.place(x=50,y=15)
    ingredient_entry = CTkEntry(ingredient_frame,placeholder_text="Add an ingredient",font=('arial',20),corner_radius=20,width=200)
    amount_entry = CTkEntry(ingredient_frame,placeholder_text='Amount',font=('arial',15),width=70)
    ingredient_entry.place(x=13, y=70)
    amount_entry.place(x=217,y=70)
    units = ["g", "kg",'pcs', "tbsp", "tsp", "cup",'ml','l']
    unit_OM = CTkOptionMenu(ingredient_frame, values=units, text_color="white", font=("Arial", 20), width=40, height=15)
    unit_OM.place(x=290, y=73)
    ing_add_btn = CTkButton(ingredient_frame,text='+',font=('impact',25,'bold'),fg_color='green',corner_radius=8,width=10,command=add_ing)
    ing_add_btn.place(x=360,y=60)

    steps_title = CTkLabel(steps_frame, text='Steps', font=('Times new roman', 30, 'underline'),text_color='orange')
    steps_entry = CTkEntry(steps_frame, placeholder_text="Add a Step", font=('arial', 20),corner_radius=20, width=200)
    steps_add_btn = CTkButton(steps_frame, text='+', font=('impact', 25, 'bold'), fg_color='green', corner_radius=8, width=10,command=add_step)
    steps_title.place(x=50, y=5)
    steps_entry.place(x=13, y=45)
    steps_add_btn.place(x=230, y=38)

    timer_title = CTkLabel(timers_frame,text='Timers', font=('Times new roman', 30, 'underline'),text_color='orange')
    empty_label = CTkLabel(timers_frame,text='No Timers Have Been\nAdded Yet',font=("Times new roman",37,'bold'),text_color='grey')
    timer_title.place(x=50, y=15)
    empty_label.place(x=70,y=95)


def saved_recipes():
    def open_recipe():
        if len(recipe_names) >0:
            def countdown(duration, drtn_lbl):
                """Simple countdown function using after() for non-blocking updates."""
                global running, time_displayed, remaining_time
                nonlocal timer
                timer = int(timer)
                if duration > 0 and running:
                    minutes, seconds = divmod(duration, 60)
                    time_displayed = f"{minutes:02}:{seconds:02}"
                    try:
                        drtn_lbl.configure(text=time_displayed)
                    except _tkinter.TclError:
                        pass
                    new_timers_frame.after(1000, countdown, duration - 1, drtn_lbl)  # Schedule next update
                    remaining_time = duration - 1
                elif duration == 0:
                    drtn_lbl.configure(text="Time's up!")  # Display when finished
                    playsound('C:/Users/Lenovo/PycharmProjects/pythonProject/External Projects/wav/Alarm.wav')
                    running = False
            def start_timer():
                global running, remaining_time
                running = True
                if remaining_time == 0:
                    remaining_time = int(timer) * 60
                countdown(remaining_time, duration_label)

            def stop_timer():
                global running
                running = False
                duration_label.configure(text=time_displayed)

            file_path = f'recipes/{recipes_OM.get()}.json'
            with open(file_path,'r') as file:
                content = json.load(file)
                ingredients = content['ingredients']
                steps = content['steps']
                timers = content['timers']
            def back_to_saved_recipes():
                for wgt in window.winfo_children():
                    wgt.destroy()
                saved_recipes()

            for wdg in window.winfo_children():
                wdg.destroy()
            # Window
            CTkLabel(window, text=recipes_OM.get(), font=('impact', 50), text_color="cyan").place(x=65,y=20)
            back_btn = CTkButton(window, text='Back', text_color='white', font=('arial', 25), border_color='black', border_width=3,corner_radius=5, fg_color='grey',command=back_to_saved_recipes)
            unsave_btn = CTkButton(window, text='Unsave', text_color='black', font=('arial', 25), border_color='black', border_width=3,hover_color='orange',corner_radius=5, fg_color='red',command=lambda: os.remove(f'recipes/{recipes_OM.get()}.json'))
            back_btn.place(x=150,y=710)
            unsave_btn.place(x=825, y=710)
            # Frames
            new_ingredient_frame = CTkFrame(window, border_color='white', border_width=5, width=420, height=580)
            new_steps_frame = CTkFrame(window, border_color='white', border_width=5, width=510, height=415)
            new_timers_frame = CTkFrame(window, border_color='white', border_width=5, width=510, height=265)
            new_ingredient_frame.place(x=30, y=115)
            new_timers_frame.place(x=475, y=430)
            new_steps_frame.place(x=475, y=5)

            y_new_ing = 65
            y_new_stp = 60
            y_new_tmr = 60
            step_number = 1
            ing_number = 1
            # Frame insides
            ing_title = CTkLabel(new_ingredient_frame, text='Ingredients', font=('Times new roman', 30, 'underline'),text_color='orange')
            ing_title.place(x=50, y=15)
            for ingredient in ingredients:
                CTkLabel(new_ingredient_frame,text=f"{ing_number}. {ingredient}", font=('arial',20)).place(x=13,y=y_new_ing)
                y_new_ing += 30
                ing_number += 1

            steps_title = CTkLabel(new_steps_frame, text='Steps', font=('Times new roman', 30, 'underline'),text_color='orange')
            steps_title.place(x=50, y=5)
            for step in steps:
                CTkLabel(new_steps_frame,text=f"{step_number}. {step}", font=('arial',20)).place(x=13,y=y_new_stp)
                y_new_stp += 27
                step_number += 1

            timer_title = CTkLabel(new_timers_frame, text='Timers', font=('Times new roman', 30, 'underline'),text_color='orange')
            timer_title.place(x=50, y=15)
            start_btn = CTkButton(
                new_timers_frame,
                width=30,
                command=start_timer,  # Start countdown
                text="",
                fg_color='transparent',
                text_color='black',
                image= start_ctk
            )
            stop_btn = CTkButton(
                new_timers_frame,
                width=30,
                command=stop_timer,  # Stop action
                fg_color='transparent',
                text_color='black',
                image= stop_ctk
            )
            for timer in timers:
                duration_label = CTkLabel(new_timers_frame, text=f"{timer}:00", font=('arial', 20))
                duration_label.place(x=13,y=y_new_tmr)

                stop_btn.place(x=350,y=y_new_tmr)
                start_btn.place(x=300,y=y_new_tmr)
                y_new_tmr += 29
        else:
            file_popup = CTkToplevel(window)  # Creates a new pop-up window
            file_popup.geometry("300x175+500+500")
            file_popup.resizable(0, 0)
            file_popup.title("ERROR")
            file_popup.attributes("-topmost", True)
            CTkLabel(file_popup, text="File not found", text_color="red", font=("Arial", 18)).pack(pady=20)
            CTkButton(file_popup, text="OK", command=file_popup.destroy).pack(pady=10)
    def back():
        for widget in window.winfo_children():
            widget.destroy()
        main()

    for widget in window.winfo_children():
        widget.destroy()
    saved_recipes_title = CTkLabel(window, text="Saved Recipes", font=('georgian', 60, 'bold'), text_color='green')
    back_btn = CTkButton(window, text='Back', text_color='white', font=('arial', 25), border_color='black',border_width=3, corner_radius=5, fg_color='grey', command=back)
    open_btn = CTkButton(window,text='OPEN',fg_color='green',border_color='black',corner_radius=10,border_width=3,font=('robotic',40,'underline'),text_color='white',command=open_recipe)
    recipe_names = []
    for file in os.listdir('recipes'):
        recipe_names.append(file.split('.')[0])
    recipes_OM = CTkOptionMenu(window,width=300,height=70,values=recipe_names,text_color='cyan', font=('impact',35))
    open_btn.place(x=650,y=100)
    saved_recipes_title.place(x=45, y=15)
    recipes_OM.place(x=550,y=20)
    back_btn.place(x=150, y=710)

# Window
window = CTk()
window.geometry("1000x760")
window.title("Recipe Organizer")
window.resizable(0, 0)
set_appearance_mode('dark')
set_default_color_theme('green')
def main():
    # Home Page
    CTkLabel(window,text="Recipe Organizer",font=("impact",60,"bold"),text_color="cyan").place(y=50,x=40)
    # Photo
    cookbook_image = Image.open("recipe photos/photo for hompage.png")
    ctk_cookbook_image = CTkImage(light_image=cookbook_image,dark_image=cookbook_image,size=(225,225))
    CTkLabel(window,image=ctk_cookbook_image,text="").place(x=620,y=10)
    # frames
    saved_recipes_frame = CTkFrame(window,width=330,height=400,border_color='white',border_width=5)
    add_recipe_frame = CTkFrame(window,width=330,height=400,border_color='white',border_width=5)

    saved_recipes_frame.place(x=100,y=275)
    add_recipe_frame.place(x=580,y=275)
    # Frame insides
    save_image = Image.open("recipe photos/save.png")
    ctk_save_image = CTkImage(light_image=save_image,dark_image=save_image,size=(150,150))
    CTkButton(saved_recipes_frame,image=ctk_save_image,text="",command=saved_recipes).place(x=82,y=160)
    CTkLabel(saved_recipes_frame,text="Saved Recipes",font=('Times new roman',40),text_color="orange").place(x=58,y=20)

    add_image = Image.open("recipe photos/add.png")
    ctk_add_image = CTkImage(light_image=add_image,dark_image=add_image,size=(150,150))
    CTkButton(add_recipe_frame,image=ctk_add_image,text="",command=add_recipe).place(x=82,y=160)
    CTkLabel(add_recipe_frame,text="Add a Recipe",font=('Times new roman',40),text_color="orange").place(x=58,y=20)
main()
window.mainloop() #run
