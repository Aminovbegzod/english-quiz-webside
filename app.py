from  flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  


def get_db_connection():
    conn = sqlite3.connect('questions.db')
    conn.row_factory = sqlite3.Row
    return conn

# Homepage
@app.route('/')
def index():
    return render_template('index.html')
import sqlite3

# Bazani yaratish
conn = sqlite3.connect('questions.db')
c = conn.cursor()

# Jadvalni yaratish
c.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,
        correct_option TEXT NOT NULL
    )
''')

# Savollarni qo‘shish
questions = [
    ("What is the plural of 'child'?", "childs", "childes", "children", "childen", "C"),
    ("Which one is a verb?", "happy", "quickly", "run", "blue", "C"),
    ("Choose the correct article: ___ apple", "a", "an", "the", "no article", "B"),
    ("What is the opposite of 'hot'?", "warm", "cold", "cool", "fire", "B"),
    ("Which sentence is correct?", "She go to school", "She goes to school", "She going school", "She goed school", "B"),
    ("What is the capital of France?", "London", "Paris", "Berlin", "Madrid", "B"),
    ("What is the largest planet in our solar system?", "Earth", "Mars", "Jupiter", "Saturn", "C"),
    ("Who wrote the play 'Romeo and Juliet'?", "Charles Dickens", "William Shakespeare", "Mark Twain", "Jane Austen", "B"),
    ("What is the smallest prime number?", "0", "1", "2", "3", "C"),
    ("Which element has the chemical symbol 'O'?", "Oxygen", "Osmium", "Ozone", "Oganesson", "A"),
    ("Who painted the Mona Lisa?", "Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Claude Monet", "C"),
    ("Which country is known as the Land of the Rising Sun?", "China", "South Korea", "Japan", "Thailand", "C"),
    ("What is the square root of 64?", "6", "7", "8", "9", "C"),
    ("What is the main ingredient in guacamole?", "Tomato", "Avocado", "Onion", "Garlic", "B"),
    ("Which continent is the Sahara Desert located in?", "Asia", "Africa", "Europe", "Australia", "B"),
    ("How many continents are there on Earth?", "5", "6", "7", "8", "C"),
    ("Which animal is known as the King of the Jungle?", "Elephant", "Lion", "Tiger", "Bear", "B"),
        
]

# c.executemany('''
#     INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_option)
#     VALUES (?, ?, ?, ?, ?, ?)
# ''', questions)

conn.commit()
conn.close()


print("✅ savol bazaga qo‘shildi.")
# Quiz page
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    conn = get_db_connection()
    questions = conn.execute('SELECT * FROM questions').fetchall()
    conn.close()
    session['questions'] = [dict(q) for q in questions]  
    return render_template('quiz.html', questions=questions)
 
# Result page
@app.route('/result', methods=['POST'])
def result():
    questions = session.get('questions', [])

    score = 0
    total = len(questions)

    for question in questions:
        selected = request.form.get(str(question['id']))
        if selected == question['correct_option']:
            score += 1

    session['score'] = score  # Store score in session if needed later
    session['total'] = total

    return render_template('result.html', score=score, total=total)


if __name__ == '__main__':
    app.run(debug=True)