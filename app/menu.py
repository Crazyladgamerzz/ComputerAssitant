
from enum import Enum
import os

class Screen(Enum):
    MAIN_MENU = 0
    CONFIG = 1
    START = 2
    EXIT = 3

class MenuAction(Enum):
    SET_MAXITERATIONS_ACTION = 0
    SET_HUMAN_CONFIRMATION_ACTION = 1

    REQUEST_AGENT_ACTION = 2
    EXIT_ACTION = 3
    NO_ACTION = (None,None)

class Menu:
    def __init__(self):
        self.current_screen = Screen.MAIN_MENU
        self.is_running = True

    def display_menu(self):
        self.clear_console()
        if self.current_screen == Screen.MAIN_MENU:
            return self.show_main_menu()
        elif self.current_screen == Screen.CONFIG:
            return self.show_config()
        elif self.current_screen == Screen.START:
            return self.show_start()
        elif self.current_screen == Screen.EXIT:
            return self.show_exit()
        return MenuAction.NO_ACTION.value
    

    def show_main_menu(self):
        print(
            (f"1- Start\n"
            f"2- Change config\n"
            f"3- Exit\n" )
        )
        option=input('Pick an option: ')

        if option == '1':
            self.current_screen = Screen.START
        elif option == '2':
            self.current_screen = Screen.CONFIG
        elif option == '3':
            self.current_screen = Screen.EXIT
        
        return MenuAction.NO_ACTION.value
    
    def show_config(self):
        print(
            (f"1- Set human confirmation\n"
            f"2- Set maximun iterations\n" 
            f"3- Return\n" )
        )
        option = input('Pick an option: ')
        print()

        if option == '3':
            self.current_screen = Screen.MAIN_MENU
        elif option == '1':
            print(
            (f"1- Enable human confirmation\n"
            f"2- Disable human confirmation\n" 
            f"3- Cancel\n" )
            )
            option = input('Pick an option: ')
            if option in ['1','2']: return MenuAction.SET_HUMAN_CONFIRMATION_ACTION,option == '1'
        elif option == '2':
            option = input('Type the maximun iterations (-1 to disable): ')
            return MenuAction.SET_MAXITERATIONS_ACTION,option

        return MenuAction.NO_ACTION.value
    

    def show_start(self):
        user_intput = input('Type your request or ("back" to return): ')
        if self.return_screen(user_intput,Screen.MAIN_MENU):
            return MenuAction.NO_ACTION.value
        return MenuAction.REQUEST_AGENT_ACTION,user_intput

    def show_exit(self):
        self.is_running = False
        print('Successfully exited the application...')
        return MenuAction.EXIT_ACTION,None
    
    
    def return_screen(self,user_intput,screen:Screen):
        if user_intput.strip() == 'back':
            self.current_screen = screen
            return True
        return False

    
    def clear_console(self):
        if os.name == 'nt': # Windows
            _ = os.system('cls')
        else: # macOS; Linux
            _ = os.system('clear')
    
    def request_enter(self,msg):
        input(f'{msg}\nEnter to continue...')
