import network
import time
import gc
import hardware

def main():

    gc.enable()

    hw = hardware.Hardware()

    hw.oled_clear()
    hw.oled_graphic('start.txt', 0, 8)
    hw.oled_show()
    hw.pixel_color(64, 64, 64)    

    sta = network.WLAN(network.STA_IF)
    ap = network.WLAN(network.AP_IF)

    while True:
        sta.active(True)
        starting_time = time.time()
        while not sta.isconnected() and (time.time() - starting_time) < 10:
            pass
        if not sta.isconnected():
            time.sleep(5)
            gc.collect()
            import config
            config.Work(hw)
            ap.active(False)
        else:
            time.sleep(5)
            gc.collect()
            import widget
            widget.Work(hw)

        gc.collect()
