import websocket
from threading import Thread
import time
import sys
import json
import sense_hat

initvalue = 0
close = False
time=3
sense = sense_hat.SenseHat()
sense.set_rotation(90)
sense.low_light = True

X = [255, 0, 0]  # Red
O = [0, 0, 0]  # Black
G = [255,215,0]

question_mark = [
    O, O, O, X, X, O, O, O,
    O, O, X, O, O, X, O, O,
    O, O, O, O, O, X, O, O,
    O, O, O, O, X, O, O, O,
    O, O, O, X, O, O, O, O,
    O, O, O, X, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, X, O, O, O, O
]

exclamation_mark = [
    O, O, O, X, O, O, O, O,
    O, O, O, X, O, O, O, O,
    O, O, O, X, O, O, O, O,
    O, O, O, X, O, O, O, O,
    O, O, O, X, O, O, O, O,
    O, O, O, X, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, X, O, O, O, O
]

bitcoin = [
    O, O, G, O, G, O, O, O,
    O, G, G, G, G, G, O, O,
    O, O, G, O, G, O, G, O,
    O, O, G, O, G, O, G, O,
    O, O, G, G, G, G, O, O,
    O, O, G, O, G, O, G, O,
    O, O, G, O, G, O, G, O,
    O, G, G, G, G, G, O, O
]

def on_message(ws, message):
    # print(message)
    # Receive messages in a loop and print them out
    if message.find("lastPrice") > 0:
        jsonMessage = json.loads(message)
        if jsonMessage.get("data"):
            if (jsonMessage.get("data")[0].get("lastPrice")):
                lastvalueSTR = int(jsonMessage.get("data")[0].get("lastPrice"))
                lastvalue = int(float(lastvalueSTR))
                allowed_error = 3
                global initvalue
                difff = lastvalue - initvalue
                absdifff = abs(lastvalue - initvalue)
                # print(difff)

                if absdifff >= allowed_error:
                    initvalue = lastvalue
                    if difff >= 0:
                        sense.show_message(str(lastvalueSTR), text_colour=(0, 255, 0), back_colour=(0, 0, 0))
                        print("GREEN")
                    else:
                        sense.show_message(str(lastvalueSTR), text_colour=(255, 0, 0), back_colour=(0, 0, 0))
                        print("RED")

                    print(lastvalueSTR)

        else:
            print("?")


def on_error(ws, error):
    print(error)
    sense.set_pixels(question_mark)


def on_close(ws):
    print("### closed ###")
    sense.set_pixels(exclamation_mark)


def on_open(ws):
    def run(*args):
        #for i in range(50):
        while True:
            # send the message, then wait
            # so thread doesn't exit and socket
            # isn't closed
            msg = {
                "op": "subscribe",
                "args": ["instrument:XBTUSD"]
            }
            ws.send(json.dumps(msg))
            time.sleep(time)

        ws.close()
        print("Thread terminating...")

    Thread(target=run).start()


if __name__ == "__main__":
    while True:
        sense.set_pixels(bitcoin)
        websocket.enableTrace(True)
        if len(sys.argv) < 2:
            host = "wss://www.bitmex.com/realtime"
        else:
            host = sys.argv[1]
        ws = websocket.WebSocketApp(host,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()
