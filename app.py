import network
import socket
import ure
import time
import gc
import widget

sta = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)

machine_id = ""
data_host = ""
data_path = ""
key_path = ""
data_addr = ""
last_message = ""
message_ack = False
error_count = 0
request_count = 0

# ------------------------------------------------------
# helper routines for doConfigWork()
# ------------------------------------------------------

def send_response(client, payload, status_code=200):
    client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    client.sendall("Content-Type: text/html\r\n")
    client.sendall("Content-Length: {}\r\n".format(len(payload)))
    client.sendall("\r\n")
    
    if len(payload) > 0:
        client.sendall(payload)

# --------------------------------------------------------

def handle_root(client):
    response_header = """
        <h1>ESPWidget Wi-Fi Setup</h1>
        <form action="configure" method="post">
          <label for="ssid">SSID</label>
          <select name="ssid" id="ssid">
    """
    
    response_variable = ""
    turned_on = False
    if not sta.active():
        sta.active(True)
        turned_on = True
    for ssid, *_ in sta.scan():
        response_variable += '<option value="{0}">{0}</option>'.format(ssid.decode("utf-8"))
    if turned_on:
        sta.active(False)

    response_footer = """
           </select> <br/>
           Password: <input name="password" type="password"></input> <br />
           <input type="submit" value="Submit">
         </form>
    """
    send_response(client, response_header + response_variable + response_footer)

# --------------------------------------------------------

def handle_configure(client, request):
    match = ure.search("ssid=([^&]*)&password=(.*)", request)
    
    if match is None:
        send_response(client, "Parameters not found", status_code=400)
        return
    
    ssid = match.group(1)
    password = match.group(2)
    
    if len(ssid) == 0:
        send_response(client, "SSID must be provided", status_code=400)
        return
    
    sta.active(True)
    sta.connect(ssid, password)
    
    send_response(client, "Wi-Fi configured for SSID {}<br />Your widget should now connect...".format(ssid))
    return

# --------------------------------------------------------

def handle_not_found(client, url):
    send_response(client, "Path not found: {}".format(url), status_code=404)

# ------------------------------------------------------
# will run the AP and the web server to get the SSID and password
# ------------------------------------------------------

def doConfigWork():

    widget.pixel_color(64, 0, 0)

    sta.active(False)
    ap.active(True)
    ap.config(essid="ESPWidget", password="thereisnospoon")

    server_socket = socket.socket()
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(addr)
    server_socket.listen(1)

    widget.oled_clear()
    widget.oled_text("Connect to...", 0, 0)
    widget.oled_text("ESPWidget", 16, 12)
    widget.oled_text("Browse to...", 0, 24)
    widget.oled_text("192.168.4.1", 16, 36)
    
    while True:
        client, addr = server_socket.accept()
        client.settimeout(5.0)
        
        request = b""
        try:
            while not "\r\n\r\n" in request:
                request += client.recv(512)
        except OSError:
            pass
        
        if "HTTP" not in request:
            client.close()
            continue
        
        url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).rstrip("/")

        finished = False
        if url == "":
            handle_root(client)
        elif url == "configure":
            handle_configure(client, request)
            finished = True
        else:
            handle_not_found(client, url)
        
        client.close()

        if finished:
            break

    server_socket = None
    client = None
    addr = None
    request = None
    url = None
    finished = None
    gc.collect()

# ------------------------------------------------------
# helper routines for doWidgetWork()
# ------------------------------------------------------

def setupWidget():
    global data_host
    global data_addr
    global machine_id
    global data_path
    global key_path

    data_host = "wezensky.no-ip.org"
    try:
        data_addr = socket.getaddrinfo(data_host, 80)[0][-1]
    except:
        widget.oled_text("Failed...", 16, 24)

    import machine
    from ubinascii import hexlify
    machine_id = hexlify(machine.unique_id()).decode("utf-8")
    data_path = machine_id + "/data.txt"
    key_path = machine_id + "/key.txt"

# --------------------------------------------------------

def updateWidget():
    
    global data_addr
    global data_host
    global data_path
    global message_ack
    global error_count
    global last_message
    global request_count

    request_count += 1

    quit = False

    widget.pixel_color(0, 64, 0)

    resp = ""
    try:
        s = socket.socket()
        s.connect(data_addr)
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (data_path, data_host), 'utf8'))
        while True:
            data = s.recv(100)
            if data:
                resp += str(data, 'utf8')
            else:
                break
        s.close()
    except:
        print("HTTP Get failed.")

    if message_ack:
        widget.pixel_color(0, 0, 0)
    else:
        widget.pixel_color(0, 0, 64)

    if resp == "":
        print("No content retrieved")        
        error_count += 1
        if (error_count > 5):
            #print("Resetting....")
            #quit = True
            print("Sleeping...")
            time.sleep(120)
            error_count = 0
    else:
        print(resp)
        error_count = 0
        lines = resp.split("\r\n")
        linecount = len(lines)
        content = "No content"
        if linecount > 0:
            content = ""
            found = False
            for line in range(linecount):
                if lines[line] == "":
                    found = True
                else:
                    if found:
                        content += lines[line]

        if last_message == "":
            last_message = content
            new_content = True
        else:
            if content == last_message:            
                new_content = False
            else:
                last_message = content
                new_content = True

        if new_content:
            message_ack = False
            widget.pixel_color(0, 0, 64)
            widget.oled_clear()
            lines = content.split("/")
            for line in range(len(lines)):
                widget.oled_text(lines[line], 0, 8 * line)

    s = None
    data = None
    resp = None
    line = None
    lines = None
    linecount = None
    content = None
    new_content = None
    gc.collect()
    print(gc.mem_free())
    print(request_count)

    return quit

# --------------------------------------------------------
# will handle the display and the UI for the main function
#---------------------------------------------------------

def doWidgetWork():

    setupWidget()

    finished = False
    refresh_deadline = 0
    while True:
        if time.time() > refresh_deadline:
            finished = updateWidget()
            refresh_deadline = time.time() + 30

        if widget.button1_pressed():
            global last_message
            last_message = ""
            finished = updateWidget()

        if finished:
            break

        if widget.button2_pressed():
            widget.pixel_color(64, 64, 64)
            sta.disconnect()
            sta.connect("dummy", "")
            sta.active(False)
            break            

        if widget.button3_pressed():
            widget.pixel_color(0, 0, 0)
            global message_ack
            message_ack = True

        gc.collect()
    
    finished = None
    refresh_deadline = None
    gc.collect()

# --------------------------------------------------------

def main():

    gc.enable()

    widget.oled_clear()
    widget.oled_text("Starting...", 16, 24)
    widget.pixel_color(64, 0, 64)

    global last_message
    last_message = ""

    while True:
        sta.active(True)
        starting_time = time.time()
        while not sta.isconnected() and (time.time() - starting_time) < 10:
            pass
        if not sta.isconnected():
            time.sleep(5)
            doConfigWork()
            ap.active(False)
        else:
            time.sleep(5)
            doWidgetWork()
        
        gc.collect()
