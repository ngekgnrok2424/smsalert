from flask import Flask, json, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/sendsms', methods=['POST'])
def send_sms():
    comma_separated_numbers = request.form.get('comma_separated_numbers')
    message = request.form['message']
    
    api_token = '870|h05YLghELQ8xSwBYKosPFx3w6svYs4EckHpQvsf9'
    
    url = 'https://app.philsms.com/api/v3/sms/send'
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    if comma_separated_numbers:
        numbers = comma_separated_numbers.split(',')

    
    responses = []
    for number in numbers:
        payload = {
            'recipient': number.strip(),
            'sender_id': 'PhilSMS',  # Replace with your actual sender ID
            'type': 'plain',
            'message': message
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        responses.append({
            'number': number.strip(),
            'status_code': response.status_code,
            'response_text': response.text
        })
    
    success = all(r['status_code'] == 200 for r in responses)
    if success:
        return render_template('index.html', status='success', message='SMS sent successfully!', responses=responses)
    else:
        return render_template('index.html', status='failure', message='Failed to send some messages.', responses=responses)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)