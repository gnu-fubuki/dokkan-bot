from colorama import init, Fore, Back
import utils.funcs as funcs
init(autoreset=True)


def render(text):
    settings = funcs.get_settings()
    texts = ['command', 'description', 'error', 'success', 'message', 'drops']
    colors = ['red', 'green', 'cyan', 'blue', 'yellow', 'white', 'purple']
    for i in texts:
        if settings['colors'][str(i)] == 'red':
            text = text.replace('{' + str(i) + '}', Fore.LIGHTRED_EX)
        if settings['colors'][str(i)] == 'green':
            text = text.replace('{' + str(i) + '}', Fore.LIGHTGREEN_EX)
        if settings['colors'][str(i)] == 'cyan':
            text = text.replace('{' + str(i) + '}', Fore.CYAN)
        if settings['colors'][str(i)] == 'blue':
            text = text.replace('{' + str(i) + '}', Fore.BLUE)
        if settings['colors'][str(i)] == 'yellow':
            text = text.replace('{' + str(i) + '}', Fore.LIGHTYELLOW_EX)
        if settings['colors'][str(i)] == 'white':
            text = text.replace('{' + str(i) + '}', Fore.RESET)
        if settings['colors'][str(i)] == 'purple':
            text = text.replace('{' + str(i) + '}', Fore.LIGHTMAGENTA_EX)
    return text
