import commands_handler
import os

startInfo = lambda: print('Type "help" for help\n')                        
                         
startInfo()

def clear():
    startInfo()

try:
    while True:
        inp = input('> ')
        match(inp):
            case 'exit':
                break
            case 'cls':
                clear()
            case 'chelp':
                startInfo()
                commands_handler.commands_handler('help')
            case '':
                print ("\033[A                             \033[A")
            case _:
                commands_handler.commands_handler(inp)
except Exception as ex:
    print(ex, '\n')

input('\nВведите, чтобы продолжить...')
