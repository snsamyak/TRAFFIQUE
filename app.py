# import os
# import pickle
# from flask import Flask, render_template, request,session, redirect, url_for, send_from_directory, jsonify, Response
# import cv2
# import random
# from twilio.rest import Client
# import numpy as np
# import subprocess
# import threading
# from ultralytics import YOLO
# from google.oauth2 import id_token
# # from google.auth.transport import requests
# from google.auth.transport import requests as google_requests  # for Google ID token
# import requests as http_requests  # for regular HTTP calls like Gemini API

# from datetime import datetime
# from werkzeug.utils import secure_filename
# import re
# import base64
# import json
# import uuid
# from flask import flash
# from flask_mail import Mail, Message


# app = Flask(__name__)
# status={}
# app.secret_key = "super_secret_key"
# # Twilio credentials (replace with your own)
# TWILIO_SID = "ACf1c4c663a0c464568e7dd106efaec506"
# TWILIO_AUTH_TOKEN = "676ee1d85d4a38dd02e6ed99fecb0bfd"
# TWILIO_PHONE = "+1 318 252 8449"  # your Twilio number"
# client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = "aniketsinghal876@gmail.com"   # your Gmail
# app.config['MAIL_PASSWORD'] = "wdxb ewub ehge mkue"     # App Password, not Gmail pwd
# app.config['MAIL_DEFAULT_SENDER'] = ("Traffic & Management Portal", "yourgmail@gmail.com")
# mail = Mail(app)
# CLIENT_ID = "260197927815-bthjovm9cn7qkueribkg1hkojnr2nerg.apps.googleusercontent.com"
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
# PROCESSED_FOLDER = os.path.join(BASE_DIR, "processed")
# LANES_FOLDER = os.path.join(BASE_DIR, "lanes")
# for d in (UPLOAD_FOLDER, PROCESSED_FOLDER, LANES_FOLDER):
#     os.makedirs(d, exist_ok=True)

# # Load YOLO model once
# model = YOLO('yolov8n.pt')

# @app.route('/')
# def index():
#     return render_template('upload.html')

# @app.route("/start_simulation")
# def start_simulation():
#     # Launch simu.py as a separate process
#     subprocess.Popen(["python", "simu.py"])
#     return redirect(url_for("simulation"))

# @app.route("/simulation")
# def simulation():
#     return render_template("simulation.html")

# @app.route('/complaint')
# def complaint():
#     return render_template('complaint.html')  # Your complaint page

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')


# @app.route('/chat')
# def chat():
#     return render_template('chat.html')

# @app.route('/team')
# def team():
#     return render_template('team.html')

# @app.route("/send_otp", methods=["POST"])
# def send_otp():
#     phone = request.form.get("phone")
#     if not phone:
#         flash("❌ Phone number is required", "danger")
#         return redirect(url_for("complaint"))

#     otp = str(random.randint(1000, 9999))
#     session["otp"] = otp
#     session["pending_phone"] = phone

#     try:
#         # Send OTP via Twilio SMS
#         client.messages.create(
#             body=f"Your OTP for complaint login is {otp}",
#             from_=TWILIO_PHONE,
#             to=phone
#         )
#         flash("📩 OTP sent to your phone!", "info")
#     except Exception as e:
#         print("Twilio error:", e)
#         flash("⚠ Could not send OTP. Check Twilio settings.", "danger")

#     return redirect(url_for("complaint"))

# @app.route("/verify_otp", methods=["POST"])
# def verify_otp():
#     user_otp = request.form.get("otp")
#     if user_otp == session.get("otp"):
#         phone = session.get("pending_phone")
#         # ✅ Only now user is logged in
#         session["phone"] = phone
#         session["name"] = f"User-{phone[-4:]}" if phone else "User"
#         session["email"] = f"{phone}@user.com"
#         session["picture"] = "/static/images/images.png"

#         # clear temp
#         session.pop("otp", None)
#         session.pop("pending_phone", None)

#         flash("✅ OTP verified! You are logged in.", "success")
#     else:
#         flash("❌ Wrong OTP, try again.", "danger")

#     return redirect(url_for("complaint"))

    
# @app.route("/logout")
# def logout():
#     session.clear()
#     flash("You have been logged out.", "info")
#     return redirect(url_for("complaint"))

# @app.route('/upload', methods=['POST'])
# def upload():
#     f = request.files.get('video')
#     if not f:
#         return 'No file', 400
#     filename = f.filename
#     save_path = os.path.join(UPLOAD_FOLDER, filename)
#     f.save(save_path)
#     return redirect(url_for('draw_lanes', filename=filename))

# @app.route('/draw_lanes/<filename>')
# def draw_lanes(filename):
#     return render_template('draw_lanes.html', filename=filename)

# @app.route('/frame/<filename>')
# def frame_image(filename):
#     # Return the first frame as JPEG for canvas background
#     path = os.path.join(UPLOAD_FOLDER, filename)
#     if not os.path.exists(path):
#         return 'Not found', 404
#     cap = cv2.VideoCapture(path)
#     ret, frame = cap.read()
#     cap.release()
#     if not ret:
#         return 'Cannot read', 500
#     _, buf = cv2.imencode('.jpg', frame)
#     return Response(buf.tobytes(), mimetype='image/jpeg')

# @app.route('/save_lanes', methods=['POST'])
# def save_lanes():
#     data = request.get_json()
#     filename = data.get('filename')
#     lanes = data.get('lanes')
#     if not filename or lanes is None:
#         return jsonify({'status': 'error', 'message': 'missing'}), 400

#     # Convert lanes to numpy arrays and save as pickle
#     lanes_np = {name: np.array(points, dtype=np.int32) for name, points in lanes.items()}
#     ppath = os.path.join(LANES_FOLDER, filename + '.pkl')
#     with open(ppath, 'wb') as f:
#         pickle.dump(lanes_np, f)
#     return jsonify({'status': 'ok'})

# @app.route('/process/<filename>')
# def process(filename):
#     video_path = os.path.join(UPLOAD_FOLDER, filename)
#     lanes_path = os.path.join(LANES_FOLDER, filename + '.pkl')
#     if not os.path.exists(video_path) or not os.path.exists(lanes_path):
#         return 'Missing video or lanes', 404

#     with open(lanes_path, 'rb') as f:
#         lanes = pickle.load(f)

#     cap = cv2.VideoCapture(video_path)
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps = cap.get(cv2.CAP_PROP_FPS) or 20.0

#     out_path = os.path.join(PROCESSED_FOLDER, filename)
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

#     # Process frame-by-frame
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         results = model(frame, verbose=False)[0]
#         lane_counts = {lane: {"car": 0, "truck": 0, "bus": 0} for lane in lanes}

#         for lane_name, poly in lanes.items():
#             cv2.polylines(frame, [poly], True, (0, 255, 255), 2)
#             cv2.putText(frame, lane_name, tuple(poly[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

#         for box in results.boxes:
#             cls = int(box.cls[0])
#             label = model.names[cls]
#             if label not in ["car", "truck", "bus"]:
#                 continue
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

#             # color coding
#             color = (255, 0, 0) if label == 'car' else ((0, 255, 0) if label == 'truck' else (0, 165, 255))
#             cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
#             cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

#             for lane_name, poly in lanes.items():
#                 if cv2.pointPolygonTest(poly, (cx, cy), False) >= 0:
#                     lane_counts[lane_name][label] += 1
#                     break

#         y_offset = 30
#         for lane_name, counts in lane_counts.items():
#             text = f"{lane_name} - Cars: {counts['car']} | Trucks: {counts['truck']} | Buses: {counts['bus']}"
#             cv2.putText(frame, text, (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
#             y_offset += 30

#         out.write(frame)

#     cap.release()
#     out.release()
#     return redirect(url_for('result', filename=filename))

# @app.route('/status/<filename>')
# def check_status(filename):
#     return jsonify({"done": status.get(filename, False)})

# @app.route('/result/<filename>')
# def result(filename):
#     return render_template('result.html', filename=filename)

# def save_base64_file(base64_str, upload_folder):
#     # Extract header and data parts
#     match = re.match(r'data:(.?);base64,(.)', base64_str)
#     if not match:
#         return None, "Invalid base64 data"
#     mime_type, b64data = match.groups()
#     # Determine file extension from mime type
#     ext = mime_type.split('/')[-1]
#     filename = f"media_{datetime.now().strftime('%Y%m%d%H%M%S%f')}.{ext}"
#     filepath = os.path.join(upload_folder, filename)
#     with open(filepath, 'wb') as f:
#         f.write(base64.b64decode(b64data))
#     return filename, None

# @app.route('/complaint', methods=['POST'])
# def save_complaint():
#     complaint = request.form.get("complaint")
#     date = request.form.get("date")
#     time = request.form.get("time")
#     location = request.form.get("location")

#     name = session.get("name", "Anonymous")
#     email = session.get("email", session.get("phone", "Unknown"))
#     phone = session.get("phone", "")

#     media_file = request.files.get("media")
#     media_filename = None
#     if media_file and media_file.filename != "":
#         os.makedirs(UPLOAD_FOLDER, exist_ok=True)
#         media_filename = os.path.join(UPLOAD_FOLDER, media_file.filename)
#         media_file.save(media_filename)

#     # --- Save complaint ---
#     timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     complaint_entry = {
#         "id": str(uuid.uuid4()),
#         "timestamp": timestamp,
#         "name": name,
#         "email": email,
#         "phone": phone,
#         "date": date,
#         "time": time,
#         "location": location,
#         "complaint": complaint,
#         "media_file": media_filename
#     }

#     with open('complaints.txt', 'a', encoding='utf-8') as f:
#         f.write(json.dumps(complaint_entry) + "\n")

#     # --- Send confirmation email ---
#     msg = Message(
#         subject="Your Complaint Has Been Submitted",
#         recipients=[email],
#         body=f"""Hello {name},

# Your complaint has been successfully submitted on {timestamp}.

# Details:
# Location: {location}
# Date: {date} {time}
# Complaint: {complaint}

# We will review it as soon as possible.

# Regards,
# Smart Traffic Management System"""
#     )
#     mail.send(msg)

#     # Instead of JSON → show alert and redirect
#     return '''
#     <script>
#         alert("Complaint saved and confirmation email sent!");
#         window.history.back();
#     </script>
#     '''


# # Optional: A route to read and show all complaints
# @app.route('/complaints', methods=['GET'])
# def get_complaints():
#     try:
#         with open('complaint.txt', 'r', encoding='utf-8') as f:
#             lines = f.readlines()
#         return jsonify({"complaints": [line.strip() for line in lines]})
#     except FileNotFoundError:
#         return jsonify({"complaints": []})

# @app.route('/videos/<folder>/<filename>')
# def serve_video(folder, filename):
#     if folder not in ('uploads', 'processed'):
#         return 'Invalid', 400
#     folder_path = UPLOAD_FOLDER if folder == 'uploads' else PROCESSED_FOLDER
#     return send_from_directory(folder_path, filename)

# @app.route("/delete_complaint/<complaint_id>", methods=["POST"])
# def delete_complaint(complaint_id):
#     if "email" not in session:
#         return jsonify({"message": "Not logged in"}), 401

#     deleted_entry = {"email": session["email"], "id": complaint_id}
#     with open("deleted.txt", "a", encoding="utf-8") as f:
#         f.write(json.dumps(deleted_entry) + "\n")

#     flash("Complaint deleted successfully!", "success")
#     return redirect("/my_complaints")

# # Show only MY complaints
# @app.route("/my_complaints")
# def my_complaints():
#     identifier = session.get("email") or session.get("phone")
#     if not identifier:
#         return redirect("/complaint")

#     user_complaints = []
#     deleted_ids = set()

#     # load deleted complaint IDs
#     try:
#         with open("deleted.txt", "r", encoding="utf-8") as f:
#             for line in f:
#                 if line.strip():
#                     d = json.loads(line.strip())
#                     if d.get("email") == identifier or d.get("phone") == identifier:
#                         deleted_ids.add(d["id"])
#     except FileNotFoundError:
#         pass

#     # load complaints
#     try:
#         with open("complaints.txt", "r", encoding="utf-8") as f:
#             for line in f:
#                 if line.strip():
#                     c = json.loads(line.strip())
#                     if (c.get("email") == identifier or c.get("phone") == identifier) and c.get("id") not in deleted_ids:
#                         user_complaints.append(c)
#     except FileNotFoundError:
#         pass

#     user = {
#         "email": session.get("email"),
#         "phone": session.get("phone"),
#         "name": session.get("name"),
#         "picture": session.get("picture")
#     }

#     return render_template("my_complaints.html", user=user, complaints=user_complaints)

# # ---------------- Gemini API ---------------- #
# GEMINI_API_KEY = "AIzaSyCOaSDELq5J9kof6WSsiDy_6osN5Yo1FGE"  # Replace with your key
# # GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
# GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"


# @app.route("/chatbot", methods=["POST"])
# def chatbot():
#     data = request.get_json()
#     user_msg = data.get("message", "").strip()

#     if not user_msg:
#         return jsonify({"reply": "Please type something!"})

#     # Greeting handling
#     greetings = ["hello", "hi", "hey", "good morning", "good evening"]
#     if user_msg.lower() in greetings:
#         return jsonify({"reply": "Hello! How can I help you with traffic today?"})

#     # Traffic-only restriction
#     traffic_keywords = ["traffic", "road", "signal", "jam", "congestion", "accident"]
#     if not any(k in user_msg.lower() for k in traffic_keywords):
#         return jsonify({"reply": "⚠ I am only a traffic management assistant. Please ask about traffic only."})

#     # Gemini request
#     payload = {
#     "contents": [
#         {
#             "role": "user",
#             "parts": [
#                 {"text": f"You are a traffic assistant bot. Answer clearly.\nUser: {user_msg}"}
#             ]
#         }
#     ]
# }

#     headers = {
#         "Content-Type": "application/json",
#         "X-goog-api-key": GEMINI_API_KEY
#     }

#     try:
#         # response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
#         # response = http_requests.post("https://api.gemini.com/v1/orders", json=payload)
#         response = http_requests.post(GEMINI_API_URL, headers=headers, json=payload)

#         result = response.json()
#         print("[DEBUG] Gemini Response:", json.dumps(result, indent=2))  # log full response
#         print("==== RAW GEMINI RESPONSE ====")
#         print(json.dumps(result, indent=2))
#         print("================================")

#         reply = None

#         # Case 1: new style
#         if "candidates" in result and len(result["candidates"]) > 0:
#             parts = result["candidates"][0].get("content", {}).get("parts", [])
#             if parts and "text" in parts[0]:
#                 reply = parts[0]["text"]

#         # Case 2: older style
#         if not reply and "candidates" in result:
#             reply = result["candidates"][0].get("output")

#         if not reply:
#             reply = "Sorry, I couldn't generate a response."

#     except Exception as e:
#         print(f"[ERROR] Gemini API call failed: {str(e)}")
#         reply = "⚠ Sorry, something went wrong. Please try again later."

#     return jsonify({"reply": reply})


# # ---------------- GOOGLE LOGIN ---------------- #

# @app.route("/google-login", methods=["POST"])
# def google_login():
#     token = request.json.get("token")
#     try:
#         # idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
#         idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), CLIENT_ID)

#         user = {
#             "id": idinfo["sub"],
#             "email": idinfo.get("email"),
#             "name": idinfo.get("name"),
#             "picture": idinfo.get("picture")
#         }
#         session["id"] = user["id"]
#         session["email"] = user["email"]
#         session["name"] = user["name"]
#         session["picture"] = user["picture"]
#         return jsonify(user)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400

# # ---------------- MAIN ---------------- #

# if __name__ == '__main__':
#     app.run(debug=True)