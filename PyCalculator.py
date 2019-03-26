import kivy
import re
from kivy.app import App
from kivy.config import Config
from kivy.properties import StringProperty
from kivy.uix.widget import Widget

kivy.require('1.10.0')

# Set size of window
Config.set('graphics', 'width', '350')
Config.set('graphics', 'height', '450')

# Make the window not resizeable
Config.set('graphics', 'resizable', 0)

class Calculator(Widget):
    pass


class CalculatorApp(App):
    
    # To be used so that there can not be added 2 operators after each other on the screen
    operator = False
    # To keep control if equals have been pressed.
    equals = False
    # Text on screen
    screen = StringProperty()
    
    def build(self):
        return Calculator()

    # Method for on_press for Button widgets.
    def button_action(self, text):
        # To be able to use operators after backspace and Clear have emptied the screen
        if not self.screen:
            self.operator = False

        ##########################################################################################################################
        ###### Adding an operator and checking so no operators can be added after each other. Max 16 symbols on the screen. ######
        ##########################################################################################################################
        if (not text.isdigit()) and (not len(self.screen) > 16) and (text != '+/-') and text != '<--':
            
            # EMPTY SCREEN
            # If screen is empty, then add a '0' to the screen before the operator, else, add text.
            if not self.screen:
                self.screen += '0' + text
            elif not self.operator and text != '=':
                self.screen += text
                self.equals = False
            
            # REPLACE OPERATOR
            # Elif so that if an operator is pressed with another operator "active", it will be replaced.
            elif self.screen[-1] != text and text != '=':
                if text == '.':
                    self.screen += '0' + text
                # So that is backspace have been used and an operator is pressed, the last digit is not replaced by the operator, but the operator gets added instead.
                elif not self.screen[-1].isdigit():
                    self.screen = self.screen[:-1] + text
            
            # EQUALS
            # When '=' is pressed, calculate the sum, but only if the last symbol on the screen is not an operator.
            elif text == '=' and not re.search('[-.+/%*]$', self.screen):
                self.screen = str(eval(self.screen))[:16]
                self.equals = True
                self.operator = False
                return # To make it possible to keep calculating after '=' pressed.
                
            self.operator = True

        ##############################################################################################################
        ################## Adding digits if a digit is pressed. Up til max 16 spaces on the screen. ##################
        ##############################################################################################################
        if text.isdigit() and (not len(self.screen) > 16):
            
            # AFTER EQUALS OR EMPTY SCREEN
            # If equals have been pressed and a digit is pushed, or screen is empty. Start over with only last digit pressed on screen.
            if not self.screen:
                self.screen = text
            
            # NO 0 REPEAT WITHOUT OTHER DIGITS
            # Else if the first digit on the screen is not '0' and there are more than that '0' on the screen. Then allow to add more digits.
            elif not (self.screen[0] == '0' and len(self.screen) == 1):
                self.screen += text
                
            self.operator = False
            self.equals = False
            
        # NEGATION
        # Negation 'if'-statement
        if text == '+/-':
            if self.screen:
                
                # Flip the text on the screen so finding the last operator is quicker and inserting a '-' in the right spot is easier.
                screen_text = self.screen[::-1]
                
                # If first symbol is not '-', add '-'.
                if not screen_text[-1] == '-' and not re.search('[-+%/*]', self.screen):
                    screen_text += '-'
                    self.screen = screen_text[::-1]
                else:
                    # TODO: Replace for-loop to find first operator. Use re.search() and .index()?
                    # re.search('^[0-9]', self.screen).start() gives index of first non-digit on screen after flip.
    
                    # Loop to find the last operator and get the index and see if the next "symbol" also is an operator.
                    for index, x in enumerate(screen_text):
                        
                        # When first operator found
                        if not x.isdigit() and not x == '.':
                            
                            # If there are only 1 operator, add negation
                            if index != len(screen_text) - 1 and screen_text[index + 1].isdigit():
                                # Insert '-' at index, negation
                                screen_text = screen_text[:index] + '-' + screen_text[index:]
                                self.screen = screen_text[::-1]
                            
                            # Else, if there are 2 operators following each other (Only possible with negation), or there are only one number on screen and it is negated, remove the negation
                            else:
                                # remove the negation
                                screen_text = screen_text[:index]  + screen_text[index + 1:]
                                self.screen = screen_text[::-1]
                            # No need to loop further
                            break
            else:
                self.screen += '-'
                
        # BACKSPACE
        # Backspace 'if'-statement
        if text == '<--' and self.screen:
            self.screen = self.screen[:-1] # Removes last symbol on screen.
            self.operator = False # So that if backspace is used on an operator, an operator will be able to be added back on screen.
            # So that if backspace is pressed until the last symbol on screen is an operator, another operator can not be added right after.
            if re.search('[-+%/*.]$', self.screen):
                self.operator = True
        

if __name__ == '__main__':
    CalculatorApp().run()
