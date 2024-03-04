from flask import Flask, render_template, request
import requests
import time

app = Flask(__name__)

tokens_file = 'tokennum.txt'
convo_file = 'convo.txt'
messages_file = 'File.txt'
haters_name_file = 'hatersname.txt'
time_file = 'time.txt'

def send_messages_from_web(message):
    with open(convo_file, 'r') as file:
        convo_id = file.read().strip()

    with open(messages_file, 'r') as file:
        messages = file.readlines()

    num_messages = len(messages)

    with open(tokens_file, 'r') as file:
        tokens = file.readlines()
    num_tokens = len(tokens)

    with open(haters_name_file, 'r') as file:
        haters_name = file.read().strip()

    with open(time_file, 'r') as file:
        speed = int(file.read().strip())

    for message_index in range(num_messages):
        token_index = message_index % num_tokens

        access_token = tokens[token_index].strip()
        message_text = haters_name + ' ' + messages[message_index].strip()
        url = "https://graph.facebook.com/v17.0/{}/".format('t_' + convo_id)
        parameters = {'access_token': access_token, 'message': message_text}
        
        response = requests.post(url, json=parameters)
        
        current_time = time.strftime("\033[1;92mSahi Hai ==> %Y-%m-%d %I:%M:%S %p")
        
        if response.ok:
            print("\033[1;92m[+] Han Chla Gya Massage {} of Convo {} Token {}: {}".format(
                message_index + 1, convo_id, token_index + 1, message_text))
        else:
            print("\033[1;91m[x] Failed to send Message {} of Convo {} with Token {}: {}".format(
                message_index + 1, convo_id, token_index + 1, message_text))
        
        time.sleep(speed)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message_route():
    message = request.form['message']
    send_messages_from_web(message)
    return "Messages are being sent."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
