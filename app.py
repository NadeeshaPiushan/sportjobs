from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to create a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('jobs.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to get all job listings from the database
def get_jobs():
    conn = get_db_connection()
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    return jobs

# Route for the home page
@app.route('/')
def index():
    jobs = get_jobs()
    return render_template('index.html', jobs=jobs)

# Route to add a new job listing
@app.route('/add_job', methods=['POST'])
def add_job():
    title = request.form['title']
    description = request.form['description']
    conn = get_db_connection()
    conn.execute('INSERT INTO jobs (title, description) VALUES (?, ?)', (title, description))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Route to delete a job listing
@app.route('/delete_job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM jobs WHERE id = ?', (job_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Create the jobs table if it doesn't exist
    conn = sqlite3.connect('jobs.db')
    conn.execute('CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, title TEXT, description TEXT)')
    conn.close()
    
    # Run the Flask app
    app.run(debug=True)
