from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, LCD_FONT, TINY_FONT

from time import sleep
from datetime import datetime

import requests

import multiprocessing

class MatrixLed:
    LCD_FONT[49] = [0x40, 0x42, 0x7f, 0x40, 0x40, 0x00, 0x00, 0x00]  # '1'
    def __init__(self):
        serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(serial, width=64, height=8, block_orientation=-90)
        self.device.contrast(10)
        self.virtual = viewport(self.device, width=64, height=8)
        self.clockProcess = None
        self.biuro_temp = None
        self.biuro_hum = None

    def showMessage(self, message, delay=0.04):
        show_message(self.device, message, fill="white", font=proportional(LCD_FONT), scroll_delay=delay)

    def clockLoop(self):
        step = 10
        step_now = 1

        date_temp = False
        temp_hum = True

        self.get_biuro_data()

        point = True
        move_right = True
        margin = 0
        second = datetime.now().strftime('%S')
        while True:
            with canvas(self.virtual) as draw:
                second_now = datetime.now().strftime('%S')
                if second!=second_now:
                    point = not point
                    second=second_now

                    if int(second)%10 == 0:
                        date_temp = not date_temp

                    if int(second)%5 == 0:
                        temp_hum = not temp_hum

                text(draw, (0+margin, 1 if move_right else 0), datetime.now().strftime('%H'), fill="white", font=proportional(LCD_FONT))
                text(draw, (12+margin, 1 if move_right else 0), ':' if point else ' ', fill="white", font=proportional(TINY_FONT))
                text(draw, (14+margin, 1 if move_right else 0), datetime.now().strftime('%M'), fill="white", font=proportional(LCD_FONT))
                text(draw, (26+margin, 1 if move_right else 0), ' ' if point else ':', fill="white", font=proportional(TINY_FONT))
                text(draw, (28+margin, 1 if move_right else 0), datetime.now().strftime('%S'), fill="white", font=proportional(LCD_FONT))

                if date_temp:
                    if margin < 8:
                        text(draw, (47, 1 if move_right else 0), datetime.now().strftime('%d.%m'), fill="white", font=proportional(TINY_FONT))
                    if margin > 17:
                        text(draw, (0, 1 if move_right else 0), datetime.now().strftime('%d.%m'), fill="white", font=proportional(TINY_FONT))

                    if margin >=8 and margin <=17:
                        text(draw, (0, 1 if move_right else 0), datetime.now().strftime('%d'), fill="white", font=proportional(TINY_FONT))
                        text(draw, (57, 1 if move_right else 0), datetime.now().strftime('%m'), fill="white", font=proportional(TINY_FONT))

                elif self.biuro_temp is not None:
                    if temp_hum:
                        if margin <= 12:
                            text(draw, (51, 1 if move_right else 0), f'{self.biuro_temp}', fill="white", font=proportional(TINY_FONT))
                        if margin > 12:
                            text(draw, (0, 1 if move_right else 0), f'{self.biuro_temp}', fill="white", font=proportional(TINY_FONT))

                        if margin >=0 and margin <=8:
                            text(draw, (47, 1 if move_right else 0), 'T', fill="white", font=proportional(TINY_FONT))
                        if margin > 8 and margin <=12:
                            text(draw, (0, 1 if move_right else 0), 'T', fill="white", font=proportional(TINY_FONT))
                        if margin > 12 and margin < 22:
                            text(draw, (61, 1 if move_right else 0), 'T', fill="white", font=proportional(TINY_FONT))
                        if margin >= 22:
                            text(draw, (14, 1 if move_right else 0), 'T', fill="white", font=proportional(TINY_FONT))
                
                    else:
                        if margin <= 12:
                            text(draw, (51, 1 if move_right else 0), f'{self.biuro_hum}', fill="white", font=proportional(TINY_FONT))
                        if margin > 12:
                            text(draw, (0, 1 if move_right else 0), f'{self.biuro_hum}', fill="white", font=proportional(TINY_FONT))

                        if margin >=0 and margin <=8:
                            text(draw, (47, 1 if move_right else 0), 'H', fill="white", font=proportional(TINY_FONT))
                        if margin > 8 and margin <=12:
                            text(draw, (0, 1 if move_right else 0), 'H', fill="white", font=proportional(TINY_FONT))
                        if margin > 12 and margin < 22:
                            text(draw, (61, 1 if move_right else 0), 'H', fill="white", font=proportional(TINY_FONT))
                        if margin >= 22:
                            text(draw, (14, 1 if move_right else 0), 'H', fill="white", font=proportional(TINY_FONT))


                if step_now == step:
                    step_now = 1

                    self.get_biuro_data()

                    if move_right:
                        margin += 1
                    else:
                        margin -= 1

                    if margin > 24 or margin == 0:
                        move_right = not move_right
                else:
                    step_now += 1


                sleep(0.1)
                # self.showText(margin)

    def showText(self, showText):
        with canvas(self.virtual) as draw:
            text(draw, (0, 1), showText, fill="white", font=proportional(LCD_FONT))
    
    def clockStart(self):
        self.clockProcess = multiprocessing.Process(target=self.clockLoop)
        self.clockProcess.start()

    def clockStop(self):
        self.clockProcess.terminate()

    def get_biuro_data(self):
        bearer = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyMWJlOTU4MGNlMzc0N2ExODI3ZWY1ZTY3ZjQ5MGU4NiIsImlhdCI6MTcxOTU3OTI2NiwiZXhwIjoyMDM0OTM5MjY2fQ.N1XXNWb68e6VZe1LOtrVEpylCA5fLTmnJZFfzTf9Bz4"
        headers = {"Authorization" : f"Bearer {bearer}" }

        response = requests.get("http://homeassistant.local:8123/api/states", headers=headers) 
        if response.status_code == 200:
            res = response.json()

            for r in res:
                if r['entity_id'] == "sensor.czujnik_temperatury_biuro_temperature":
                    self.biuro_temp = r['state']
                if r['entity_id'] == "sensor.czujnik_temperatury_biuro_humidity":
                    self.biuro_hum = r['state']
        else:
            self.biuro_temp = None
            self.biuro_hum = None
