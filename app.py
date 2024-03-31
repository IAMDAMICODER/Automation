from flask import Flask, render_template, request, redirect, url_for
from googleapiclient.discovery import build

app = Flask(__name__)

# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey='YOUR_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    title = request.form['title']
    description = request.form['description']
    video_path = request.files['file']
    response = upload_video(title, description, video_path)
    video_id = response['id']
    return redirect(url_for('watch', video_id=video_id))

def upload_video(title, description, video_path):
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["tag1", "tag2"]  # Add your tags here
            },
            "status": {
                "privacyStatus": "private"  # Set privacy status as required
            }
        },
        media_body=video_path
    )
    response = request.execute()
    return response

@app.route('/watch/<video_id>')
def watch(video_id):
    return render_template('watch.html', video_id=video_id)

if __name__ == '__main__':
    app.run(debug=True)
