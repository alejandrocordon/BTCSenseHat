import websockets
import asyncio
import json
import numpy
import sense_hat

initvalue = 0
close = False
sense = sense_hat.SenseHat()
sense.set_rotation(90)
sense.low_light = True


async def main():
    try:
        uri = "wss://www.bitmex.com/realtime"
        async with websockets.connect(uri) as websocket:
            # Send a message to subscribe to XBTUSD updates
            msg = {
                "op": "subscribe",
                "args": ["instrument:XBTUSD"]
            }
            await websocket.send(json.dumps(msg))

            # Receive messages in a loop and print them out
            while True:
                result = await websocket.recv()
                data = json.loads(result)
                if data.get("data"):
                    if (data.get("data")[0].get("lastPrice")):
                        lastvalueSTR = int(data.get("data")[0].get("lastPrice"))
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

                        # else:
                        #   print("---")
                    # else:
                    #   print("data")

                    '''isclose = numpy.isclose(lastvalue, initvalue)

                    if not isclose:
                        initvalue = lastvalue
                        print(lastvalueSTR)
    '''

                else:
                    print("-")
    except:
        print("--")


if __name__ == "__main__":
    # Run the 'main' function in an asyncio event loop
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

