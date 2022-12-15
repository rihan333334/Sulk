# Libraries
import requests
import os
from config import API_KEY
from config import file

# Colors
class colors:
    HEADER = '\033[1;35m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKCYANL = '\033[1;36m'
    OKGREEN = '\033[92m'
    OKGREENL = '\033[1;32m'
    OKREDL = '\033[1;31m' 
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Functions
def banner():
    clear()
    print(colors.OKBLUE  + """
   ▄▄▄▄▄   ▄   █    █  █▀ 
  █     ▀▄  █  █    █▄█   
▄  ▀▀▀▀▄ █   █ █    █▀▄   
 ▀▄▄▄▄▀  █   █ ███▄ █  █  
         █▄ ▄█     ▀  █   
          ▀▀▀        ▀                                                                                          
    """ + colors.ENDC)
    print(colors.WARNING + "Sulk (SMS Bulk) - Bulk SMS using the textbelt API | " + colors.OKGREEN + "Author: " + colors.WARNING + "pablokbg | " + colors.OKGREEN + "Website: " + colors.WARNING + "https://pablokbg.com\n" + colors.ENDC)

def clear():
    os.system("cls")

def error():
    banner()
    print("[" + colors.FAIL + "x" + colors.ENDC + "] Error, that answer was not expected.")
    exit()

def main():
    banner()
    # Mensaje de texto a enviar
    message = input("[" + colors.OKCYAN + ">" + colors.ENDC + "] Enter the message you want to send: ")
    banner()
    # Mensaje de confirmación de envio
    confirm = input("[" + colors.HEADER + "?" + colors.ENDC + "] Are you sure to send the message [y/n]: ")
    
    if confirm in ['n', 'N', 'No', 'no', 'NO']:
        banner()
        confirm2 = input("[" + colors.HEADER + "?" + colors.ENDC + "] Do you want to leave Sulk [y/n]: ")

        if confirm2 in ['n', 'N', 'No', 'no', 'NO']:
            main()

        elif confirm2 in ['y', 'Y', 'Yes', 'yes', 'YES']:
            exit()

        else:
            error()

    elif confirm in ['y', 'Y', 'Yes', 'yes', 'YES']:
        banner()
        # Ruta donde se encuentra el archivo
        # En este caso, se obtiene el directorio del script y se une
        # con el nombre del archivo
        script_dir = os.path.dirname(__file__)
        path = os.path.join(script_dir, file)

        # Se leen los números de teléfono desde el archivo
        with open(path) as f:
            numbers = [x.strip() for x in f.readlines()]

        true_count = 0
        false_count = 0

        # Se envía una petición POST por cada número de teléfono
        for number in numbers:
            payload = {
                "phone": number, 
                "message": message, 
                "key": API_KEY
                }
            resp = requests.post(
                'https://textbelt.com/text', 
                data = payload
                )

            # Si la respuesta tiene un valor success, aumentar el contador true
            if ['success'] == 'True' in resp.json():
                true_count += 1
            else:
                false_count += 1

            print("[" + colors.OKCYAN + ">" + colors.ENDC + "] " + number + " ({})".format(colors.OKGREEN + 'Success' + colors.ENDC if resp.json()['success']=='True' else colors.FAIL + 'Failed' + colors.ENDC)) 
            
        print('\fTotal: {} ({}: {} | {}: {})'.format(len(numbers), colors.OKGREEN + 'Success' + colors.ENDC, true_count, colors.FAIL + 'Failed' + colors.ENDC, false_count))
        quota = requests.get('https://textbelt.com/quota/'+ API_KEY)
        quota = quota.json()['quotaRemaining']
        print('Remaining quota: {}{}%{}\f'.format(colors.WARNING, quota, colors.ENDC))

    else:
        error()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        banner()
        print("[" + colors.OKREDL + "x" + colors.ENDC + "] Leaving from Sulk ...\n")
        exit()
