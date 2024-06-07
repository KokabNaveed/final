import os
import sqlite3
import pymysql
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from Bitrate import get_bitrate
from DR import calculate_decibels_with_sampling_rate, plot_waveform_with_sampling_rate
from loudness import get_loudness, plot_loudness
from peak_level import plot_waveform_with_peak
from silence_speech import get_silence_speech_ratio, plot_silence_speech_ratio_pie
from file_utils import calculate_file_size
from harmonicity import get_harmonicity, plot_harmonicity
from frequency import plot_frequency_spectrum
from tempo import estimate_tempo


app = Flask(__name__)
app.secret_key = os.urandom(24)

# Ensure the database and uploads directories exist
if not os.path.exists('database'):
    os.makedirs('database')
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Initialize the MySQL database
def init_db():
    conn = pymysql.connect(
        host='localhost',
        user='root',       
        password='',  
        db='audio',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    # Check if the tables exist, if not, create them
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255) UNIQUE NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS uploads (
                        audio_id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT,
                        filename VARCHAR(255) NOT NULL,
                        bitrate INT NOT NULL,
                        loudness_plot_path VARCHAR(255) NOT NULL,
                        waveform_plot_path VARCHAR(255) NOT NULL,
                        silence_speech_ratio_plot_path VARCHAR(255) NOT NULL,
                        plot_path_decibels VARCHAR(255) NOT NULL,
                        plot_path_sr VARCHAR(255) NOT NULL,
                        harmonicity_plot_path VARCHAR(255) NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

# Call init_db() only once when the application starts
init_db()


#Home
@app.route('/')
def index():
    return render_template('index.html')
#signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the username, email, and password from the form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Connect to the database
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='audio',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()
        
        try:
            # Insert new user into the database
            cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
            conn.commit()

            # Set the session value
            session['username'] = username

            conn.close()
            return redirect(url_for('index'))
        except pymysql.MySQLError as e:
            flash("Username already exists")
            conn.close()
    
    return render_template('signup.html')

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form['username']
        password = request.form['password']
        
          # Connect to the database
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='audio',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()
        
        # Fetch user details from the database
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        
                # Check if user exists and passwords match
        if user and user['password'] == password:  # Check password without hashing
            session['username'] = username
            conn.close()
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password")
            conn.close()
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    # Remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    # Remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part")
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)
        
        if not (file.filename.lower().endswith('.mp3') or file.filename.lower().endswith('.wav')):
            flash("Unsupported file format. Only .mp3 and .wav are allowed.")
            return redirect(request.url)
        
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)
        
        # Check if the file is saved successfully
        if not os.path.exists(file_path):
            flash("Error saving the file")
            return redirect(request.url)

        # Calculate the bitrate using the get_bitrate function
        bitrate = get_bitrate(file_path)
        
        # Check if bitrate calculation is successful
        if bitrate is None:
            flash("Error calculating bitrate")
            return redirect(request.url)
        
        # Plot the waveform with sampling rate and save the plot
        plot_path_sr = plot_waveform_with_sampling_rate(file_path)

        # Calculate decibels with sampling rate
        decibels_value = calculate_decibels_with_sampling_rate(file_path, bitrate)
        decibels_with_units = f"{decibels_value:.2f} dB"

        # Plot the loudness and save the plot
        loudness_plot_path = plot_loudness(file_path)
        
        # Plot the waveform with peak and save the plot
        waveform_plot_path = plot_waveform_with_peak(file_path)

        # Plot the silence speech ratio pie chart and save the plot
        silence_speech_ratio_plot_path = plot_silence_speech_ratio_pie(file_path)

        # Plot harmonicity and save the plot
        harmonicity_plot_path = plot_harmonicity(file_path)

        # Plot the frequency spectrum and save the plot
        frequency_plot_path = plot_frequency_spectrum(file_path)

        # Estimate tempo and save the tempo value
        tempo = estimate_tempo(file_path)

        # Calculate the file size
        file_size_mb = calculate_file_size(file_path)
        
        # Connect to MySQL database
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='audio',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()
        
        try:
            # Insert upload details into MySQL database
            cursor.execute('INSERT INTO uploads (filename, bitrate, loudness_plot_path, waveform_plot_path, silence_speech_ratio_plot_path, plot_path_decibels, plot_path_sr, harmonicity_plot_path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', 
                           (filename, bitrate, loudness_plot_path, waveform_plot_path, silence_speech_ratio_plot_path, decibels_with_units, plot_path_sr, harmonicity_plot_path))
            conn.commit()
            flash(f"File uploaded successfully with bitrate: {bitrate} kbps")
        except pymysql.MySQLError as e:
            flash("Error uploading file to database")
            print(e)
        finally:
            conn.close()
        
        # Pass the paths of the generated graph images and tempo value to the template
        return render_template('upload.html', plot_path_sr_var=plot_path_sr, plot_path_decibels_var=decibels_with_units, loudness_plot_path=loudness_plot_path, waveform_plot_path=waveform_plot_path, silence_speech_ratio_plot_path=silence_speech_ratio_plot_path, file_size_var=f"{file_size_mb:.2f} MB", bitrate_var=f"{bitrate} kbps", harmonicity_plot_path=harmonicity_plot_path, frequency_plot_path=frequency_plot_path, tempo=tempo)

    return render_template('upload.html')


@app.route('/history')
def history():
    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT filename, bitrate, loudness_plot_path, waveform_plot_path, silence_speech_ratio_plot_path, plot_path_decibels, plot_path_sr, harmonicity_plot_path FROM uploads')
    uploads = cursor.fetchall()
    conn.close()
    
    return render_template('history.html', uploads=uploads)

if __name__ == '__main__':
    app.run(debug=True)
