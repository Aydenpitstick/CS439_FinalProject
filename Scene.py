from tkinter import *
import random

class Game:
    def __init__(self):
        self.width = 500
        self.height = 500
        self.speed = 200
        self.cell = 20
        self.body = 2
        
        self.snakeColor = "#00FF00"
        self.foodColor = "#FF0000"
        self.bg = "#000000"

        self.score = 0
        self.direction = 'right'

        self.root = Tk()
        self.root.title("Final Project")

        self.button_frame = Frame(self.root)
        self.button_frame.pack(side=BOTTOM, pady=20)

        self.main_frame = Frame(self.root)
        self.main_frame.pack()

        self.label = Label(self.main_frame, text=f"Points: {self.score}", font=('consolas', 20))
        self.label.pack()

        self.canvas = Canvas(self.main_frame, bg = self.bg, height=self.height - 100, width=self.width)
        self.canvas.pack()

        self.center_window()

        self.root.bind('<Left>', lambda e: self.change_direction('left'))
        self.root.bind('<Right>', lambda e: self.change_direction('right'))
        self.root.bind('<Up>', lambda e: self.change_direction('up'))
        self.root.bind('<Down>', lambda e: self.change_direction('down'))
        
        self.start_button = Button(self.button_frame, text="Start", font=('consolas', 14), command=self.start_game)
        self.start_button.pack(side=LEFT, padx=10)
       
        self.restart_button = Button(self.button_frame, text="Restart", font=('consolas', 14), command=self.start_game)


        self.root.mainloop()

    def center_window(self):
        self.root.update()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        x = int((sw - self.width) / 2)
        y = int((sh - self.height) / 2)
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
    
    def reset_game(self):
        self.snake = [(100,100),(80,100)]
        self.squares = [self.draw_square(*c, self.snakeColor) for c in self.snake]
        self.food = self.create_food()
        self.score = 0
        self.label.config(text=f"Points: {self.score}")
        self.direction = 'right'


    def draw_square(self, x, y, color):
        return self.canvas.create_rectangle(x, y, x+self.cell, y+self.cell, fill=color)

    def create_food(self):
        x = random.randrange(0, self.width // self.cell) * self.cell
        y = random.randrange(0, (self.height - 100) // self.cell) * self.cell
        return self.draw_square(x, y, self.foodColor), (x,y)

    def change_direction(self, new_direction):
        opposites = {'up':'down', 'down':'up','left':'right','right':'left'}
        if new_direction != opposites[self.direction]:
            self.direction = new_direction
        

    def next_frame(self):
        head_x, head_y = self.snake[0]

        if self.direction == "up":
            head_y -= self.cell
        elif self.direction == "down":
            head_y += self.cell
        elif self.direction == "left":
            head_x -= self.cell
        elif self.direction == "right":
            head_x += self.cell

        new_head = (head_x, head_y)

        if(head_x < 0 or head_x >= self.width or 
            head_y < 0 or head_y >= (self.height - 120) or 
            new_head in self.snake):
            return self.game_over()

        self.snake.insert(0, new_head)
        self.squares.insert(0, self.draw_square(head_x, head_y, self.snakeColor))

        if new_head == self.food[1]:
            self.score += 1
            self.label.config(text=f"Points: {self.score}")
            self.canvas.delete(self.food[0])
            self.food = self.create_food()
        else:
            tail_square = self.squares.pop()
            self.canvas.delete(tail_square)
            self.snake.pop()
    
        self.root.after(self.speed, self.next_frame)

    def game_over(self):
        self.canvas.delete("all")
        self.canvas.create_text(self.width/2, (self.height - 100)/2, font=('consolas', 40), text="GAME OVER", fill="red")
        self.show_restart()

    def show_restart(self):
        self.restart_button.pack(side=LEFT, padx=10)
        self.start_button.pack_forget()

    def show_start(self):
        self.start_button.pack(side=LEFT, padx=10)
        self.restart_button.pack_forget()

    def hide_buttons(self):
        self.start_button.pack_forget()
        self.restart_button.pack_forget()
    
    def start_game(self):
        self.hide_buttons()
        self.canvas.delete("all")        
        self.reset_game()
        self.next_frame()
Game()
