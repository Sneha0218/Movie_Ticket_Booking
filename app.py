from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {}  # Temporary in-memory store

# Movie data
movies = [
   
    {'id': 1, 'title': 'The King of Kings', 'desc': 'An animated film by Angel Studios depicting the life of Jesus Christ.', 'image_url': 'https://tse3.mm.bing.net/th?id=OIP.uh8jeYnGvOgSEJNnc7M1ZQHaKy&w=200&h=291&c=7', 'slots': ['10:00 AM', '1:00 PM', '5:00 PM']},
    {'id': 2, 'title': 'The Accountant 2', 'desc': 'A sequel to the 2016 action thriller,  story of Christian Wolff', 'image_url': 'https://tse4.mm.bing.net/th?id=OIP.jNyhYqevD22yLjaGl8p3GgHaK-&w=200&h=296&c=7', 'slots': ['11:00 AM', '2:00 PM', '6:00 PM']},
    {'id': 3, 'title': 'Avengers: Endgame', 'desc': 'After the devastating events...', 'image_url': 'https://tse3.mm.bing.net/th?id=OIP.KNfIqaD92jvecpbxNWWQ4wHaJ4&pid=Api&P=0&h=180', 'slots': ['9:00 AM', '12:00 PM', '4:00 PM']},
    {'id': 4, 'title': 'Fog of War', 'desc': 'A gripping mystery film that explores the complexities of warfare and the human psyche.', 'image_url': 'https://m.media-amazon.com/images/M/MV5BYjBjMjRmMzItYzgzYy00NzgwLWI1M2MtODQ0NzdmOWU5YWZhXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg','slots': ['10:30 AM', '1:30 PM', '5:30 PM']},
    {'id': 5, 'title': '825 Forest Road', 'desc': 'A horror film set in a secluded cabin, where a group of friends encounters supernatural entities', 'image_url': 'https://tse4.mm.bing.net/th/id/OIP.XEgc_041ElhLzxAUZX22NgAAAA?w=200&h=254&c=7', 'slots': ['10:00 AM', '3:00 PM', '6:00 PM']},
    {'id': 6, 'title': 'Spider-Man: No Way Home', 'desc': 'Spider-Man navigates a multiverse...', 'image_url': 'https://tse1.mm.bing.net/th?id=OIP.mRd08ZT4CLccOUp4T5k_GAHaF7&pid=Api&rs=1&c=1&qlt=95&w=139&h=111', 'slots': ['11:30 AM', '2:30 PM', '7:00 PM']},
    {'id': 7, 'title': 'Joker', 'desc': 'The origin of the Joker...', 'image_url': 'https://tse1.mm.bing.net/th?id=OIP.bYfp-wydS6fE2hO1JMWsmgHaLH&pid=Api&rs=1&c=1&qlt=95&w=83&h=124', 'slots': ['10:00 AM', '1:00 PM', '5:00 PM']},
    {'id': 8, 'title': 'Tenet', 'desc': 'Time inversion and espionage...', 'image_url': 'https://tse1.mm.bing.net/th?id=OIP.J4jXElNBv8Es1SJncO6xigHaLH&pid=Api&rs=1&c=1&qlt=95&w=75&h=112', 'slots': ['12:00 PM', '3:00 PM', '6:00 PM']},
    {'id': 9, 'title': 'Avatar', 'desc': 'A marine on an alien planet...','image_url': 'https://tse1.mm.bing.net/th?id=OIP.QZIRZKUSWt1HBifjDRKGzAHaFj&pid=Api&rs=1&c=1&qlt=95&w=152&h=114', 'slots': ['9:00 AM', '12:00 PM', '3:00 PM']},
    {'id': 10, 'title': 'Sacramento', 'desc': 'A road trip comedy starring Michael Angarano, Maya Erskine, Kristen Stewart, and Michael Cera.', 'image_url': 'https://tse3.mm.bing.net/th?id=OIP.guk8-l05E2Zdb6Ah7dw4UgHaLH&w=200&h=300&c=7', 'slots': ['10:30 AM', '1:30 PM', '4:30 PM']},
     {'id': 11, 'title': 'The Friend', 'desc': 'A drama exploring the complexities of friendship and loss, featuring an ensemble cast.', 'image_url': 'https://tse1.mm.bing.net/th?id=OIP.IzIKCQtRP-IlkP29Iwt4YgHaKk&w=200&h=285&c=7', 'slots': ['10:30 AM', '1:30 PM', '4:30 PM']},
      {'id': 11, 'title': 'Mufasa: The Lion King', 'desc': 'A prequel to the beloved Lion King story', 'image_url': 'https://tse1.mm.bing.net/th?id=OIP.Z0t9-c0U6y-M1AuRBvj3IQHaKk&w=200&h=285&c=7', 'slots': ['10:30 AM', '1:30 PM', '4:30 PM']},
]
upcoming_movies = [
    {'title': 'Deadpool 3', 'desc': 'Deadpool teams up with Wolverine in the multiverse.', 'image_url': 'https://tse1.mm.bing.net/th?id=OIP.KmuC9RsdDaNidNulY9cZ-wHaJC&pid=Api&rs=1&c=1&qlt=95&w=92&h=112'},
    {'title': 'Inside Out 2', 'desc': 'Riley faces new emotions as a teenager.', 'image_url': 'https://tse1.mm.bing.net/th?id=OIP.i61m3bfsgHgNTTtapyhi7QHaJT&pid=Api&rs=1&c=1&qlt=95&w=96&h=121'},
    {'title': 'The Batman: Part II', 'desc': 'Batman returns to face darker threats.', 'image_url': 'https://tse1.mm.bing.net/th?id=OIP.T2wZJNMzEq9LnpTOtliKuQHaKe&pid=Api&rs=1&c=1&qlt=95&w=87&h=123'},
    {'title': 'Kung Fu Panda 4', 'desc': 'Po embarks on a new kung fu adventure.', 'image_url': 'https://tse1.mm.bing.net/th?id=OIP.33vqLk9fObEmMgTHctk6MAHaLo&pid=Api&rs=1&c=1&qlt=95&w=69&h=109'},
    {'title': 'Avatar 3', 'desc': 'The next chapter in Pandora\'s saga.', 'image_url': 'https://tse1.mm.bing.net/th?id=OIP.6FVsFBf-pL5lYgd9hojShgHaJQ&pid=Api&rs=1&c=1&qlt=95&w=85&h=107'},
    {'title': 'Fantastic Four', 'desc': 'Marvel’s first family joins the MCU.', 'image_url': 'https://tse1.mm.bing.net/th?id=OIP.aHCWhtfyh4eYcyM56OnOqgHaLH&pid=Api&rs=1&c=1&qlt=95&w=67&h=101'},
]

@app.route('/')
def home():
    return render_template('home.html', movies=movies)

@app.route('/upcoming')
def upcoming():
    return render_template('upcoming.html', movies=upcoming_movies)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if username in users:
            flash('User already exists!', 'error')
        else:
            users[username] = password
            flash('Registered successfully!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['user'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        flash('Invalid credentials!', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out!', 'info')
    return redirect(url_for('home'))

@app.route('/book/<int:movie_id>', methods=['GET', 'POST'])
def book(movie_id):
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if not movie:
        return redirect(url_for('home'))
    if request.method == 'POST':
        slot = request.form['slot']
        flash(f'Ticket booked for {movie["title"]} at {slot}', 'success')
        return redirect(url_for('home'))
    return render_template('book.html', movie=movie)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        flash(f'Thank you {name}, we’ll get back to you shortly!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)

