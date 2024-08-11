import os

from flask import Flask, request, jsonify
import google.generativeai as genai

api_key = "your_gemini_api_key"
genai.configure(api_key=api_key)
client_private_key = (
        "fEHKmlyeJHOQgVuDYJQkpRbyXQcRpsmeLKMsnIcITcnbIJBKQXjioMrJdopBiUdlwbEkjfhem" +
        "gcPZJcskdpZOkBgNfezeLMCXejk")

app = Flask(__name__)

process_audio_request_count = 0
process_text_request_count = 0
process_video_request_count = 0


@app.route('/process_audio', methods=['POST'])
def process_audio():
    # Ensure both prompt and file are present
    if 'prompt' not in request.form or 'audio' not in request.files:
        return jsonify({"error": "Missing data"}), 400

    key = request.form['key']
    if key != client_private_key:
        return jsonify({"error": "Invalid key"}), 403
    prompt = request.form['prompt']
    audio = request.files['audio']
    global process_audio_request_count
    process_audio_request_count += 1

    # Save audio file
    audio_path = f"audio_{process_audio_request_count}.wav"
    audio.save(audio_path)

    # Process audio
    audio_file = genai.upload_file(path=audio_path)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([prompt, audio_file])
    response_text = response.text
    os.remove(audio_path)

    return jsonify({"response": response_text})


@app.route('/process_text', methods=['POST'])
def process_text():
    # Ensure both prompt and file are present
    if 'prompt' not in request.form:
        return jsonify({"error": "Missing data"}), 400

    key = request.form['key']
    if key != client_private_key:
        print("return invalid key user key is: ", key)
        print("but the api key is: ", client_private_key)
        return jsonify({"error": "Invalid key"}), 403
    prompt = request.form['prompt']
    global process_text_request_count
    process_text_request_count += 1

    # Process text
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([prompt])

    print("response: ", response)

    response_text = response.text

    return jsonify({"response": response_text})


@app.route('/process_video', methods=['POST'])
def process_video():
    # Ensure both prompt and file are present
    if 'prompt' not in request.form or 'video' not in request.files:
        return jsonify({"error": "Missing data"}), 400

    key = request.form['key']
    if key != client_private_key:
        return jsonify({"error": "Invalid key"}), 403
    prompt = request.form['prompt']
    video = request.files['video']
    global process_video_request_count
    process_video_request_count += 1

    # Save audio file
    video_path = f"video_{process_audio_request_count}.mp4"
    video.save(video_path)

    # Process audio
    video_file = genai.upload_file(path=video_path)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([prompt, video_file])
    response_text = response.text
    os.remove(video_path)

    return jsonify({"response": response_text})

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"response": "test successful"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
