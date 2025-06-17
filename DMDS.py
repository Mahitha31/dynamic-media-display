import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from threading import Thread, Event, Lock

imagePath = "/home/pi/media"
slideshowDelay = 5
stop_event = Event()
update_event = Event()
lock = Lock()

webpageBody = '''
<html>
<head>
    <title>Slideshow Control Panel</title>
    <style>
        body {
            background-color: #304573;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 20px;
        }
        .button {
            background-color: #7A8AAC;
            padding: 10px 20px;
            color: white;
            font-size: 20px;
            border: none;
            cursor: pointer;
            margin: 10px;
        }
        .button:hover {
            background-color: #9B9B9B;
        }
        input, label {
            font-size: 18px;
            margin: 10px;
        }
    </style>
</head>
<body>
    <h1>Slideshow Control Panel</h1>
    <form action="/" method="get">
        <label for="dir">Image Directory:</label><br>
        <input type="text" id="dir" name="dir" placeholder="/path/to/images" required><br><br>
        <label for="delay">Delay Time (seconds):</label><br>
        <input type="number" id="delay" name="delay" value="5" min="1" required><br><br>
        <input type="submit" value="Start Slideshow" class="button">
    </form>
    <br>
    <a href="?action=stop" class="button">Stop Slideshow</a>
</body>
</html>
'''

class SlideshowHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global imagePath, slideshowDelay, stop_event, update_event

        parsed_path = urlparse(self.path)
        qs = parse_qs(parsed_path.query)

        if 'dir' in qs:
            new_path = qs['dir'][0]
            if os.path.isdir(new_path):
                with lock:
                    imagePath = new_path
                    update_event.set()
            else:
                self._respond("<h1>Invalid directory. Please try again.</h1>")
                return

        if 'delay' in qs:
            try:
                new_delay = max(1, int(qs['delay'][0]))
                with lock:
                    slideshowDelay = new_delay
                    update_event.set()
            except ValueError:
                self._respond("<h1>Invalid delay value. Please try again.</h1>")
                return

        if 'action' in qs and qs['action'][0] == 'stop':
            stop_event.set()
            self._respond("<h1>Slideshow Stopped</h1>")
            return

        self._respond(webpageBody)

    def _respond(self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

def run_web_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SlideshowHTTPRequestHandler)
    print("Web server running at http://192.168.1.102:8000")
    httpd.serve_forever()

def start_slideshow():
    global imagePath, slideshowDelay, stop_event, update_event

    os.environ['DISPLAY'] = ':0'

    while True:
        stop_event.wait()
        update_event.clear()

        try:
            with lock:
                images = [f for f in os.listdir(imagePath) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                if not images:
                    print("No images found in the directory.")
                    time.sleep(5)
                    continue

                command = f"feh --zoom fill -F -Y -D {slideshowDelay} --auto-zoom {' '.join(os.path.join(imagePath, img) for img in images)}"
                print(f"Running slideshow command: {command}")
                os.system(command)

        except Exception as e:
            print(f"Error in slideshow: {e}")

        update_event.wait()

if __name__ == "__main__":
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()

    try:
        start_slideshow()
    except KeyboardInterrupt:
        print("Exiting...")
        stop_event.set()
