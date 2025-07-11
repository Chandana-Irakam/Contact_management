from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
DATA_FILE = 'contacts.json'

def load_contacts():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_contacts(contacts):
    with open(DATA_FILE, 'w') as f:
        json.dump(contacts, f, indent=4)

@app.route('/')
def index():
    contacts = load_contacts()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['POST'])
def add_contact():
    new_contact = {
        'id': os.urandom(4).hex(),
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'phone': request.form['phone']
    }
    contacts = load_contacts()
    contacts.append(new_contact)
    save_contacts(contacts)
    return redirect('/')

@app.route('/delete/<contact_id>')
def delete_contact(contact_id):
    contacts = load_contacts()
    contacts = [c for c in contacts if c['id'] != contact_id]
    save_contacts(contacts)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
