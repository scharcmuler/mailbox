import time
from machine import Pin

import config
from lib.sensors import UltrasonicSensor
from lib.state import MailStateMachine
from lib import wifi, mqtt_client


def init_components():
    sensor = UltrasonicSensor(trig_pin=32, echo_pin=13)
    fsm = MailStateMachine(
        empty_distance_cm=config.MAILBOX_EMPTY_DISTANCE_CM,
        delta_cm=config.MAIL_DETECTION_DELTA_CM,
        consecutive_required=config.MAIL_CONSECUTIVE_HITS,
    )
    pull_cfg = Pin.PULL_UP if config.BACK_DOR_ACTIVE_LOW else Pin.PULL_DOWN
    dor_pin = Pin(config.BACK_DOR_PIN, Pin.IN, pull_cfg)
    return sensor, fsm, dor_pin


def main():
    sensor, fsm, dor_pin = init_components()

    wifi.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
    mqtt_client.setup(broker=config.MQTT_BROKER, topic=config.MQTT_TOPIC)

    last_dor_open = dor_opened(dor_pin)
    print("Initiale Klappenstellung: offen={}".format(last_dor_open))

    while True:
        dor_open = dor_opened(dor_pin)
        if dor_open != last_dor_open:
            last_dor_open = dor_open
            if dor_open:
                has_mail, changed_reset = fsm.reset()
                print("Klappe offen -> Reset auf 'leer'")
                mqtt_client.publish_mail_state(has_mail, topic=config.MQTT_TOPIC)
            else:
                print("Klappe geschlossen")
            time.sleep(0.2)  # einfache Entprellung

        dist = sensor.distance_cm()
        has_mail, changed = fsm.update(dist)

        if dist is None:
            print("Messung: keine Antwort (Timeout)")
        else:
            print("Messung: {:.1f} cm".format(dist))

        # Statuszeile: Flappe offen/zu und Postzustand
        print(
            "Status: dor_open={}, has_mail={}".format(
                dor_open, has_mail
            )
        )

        if changed:
            print("Statuswechsel: has_mail =", has_mail)
            mqtt_client.publish_mail_state(has_mail, topic=config.MQTT_TOPIC)

        time.sleep(config.MEASURE_INTERVAL_SEC)


def dor_opened(dor_pin):
    val = dor_pin.value()
    if config.BACK_DOR_ACTIVE_LOW:
        return val == 1  # Pull-up: offen = 1, gedrückt = 0
    return val == 0


if __name__ == "__main__":
    main()
