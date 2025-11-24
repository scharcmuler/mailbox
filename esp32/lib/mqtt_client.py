"""
Dummy-MQTT-Client. Kann später durch echten MQTT-Publisher ersetzt werden.
"""


def setup(broker=None, topic=None):
    # Platzhalter: hier würde man einen Client instanziieren und verbinden.
    if not broker:
        print("mqtt: kein Broker konfiguriert, laufe im Dummy-Modus.")
    else:
        print("mqtt: Verbinde zu Broker '{}', Topic '{}' (Dummy-Ausgabe)".format(broker, topic))


def publish_mail_state(has_mail, topic=None):
    # Platzhalter-Publish
    state = "has_mail" if has_mail else "empty"
    if topic:
        print("mqtt: Publish -> {}: {}".format(topic, state))
    else:
        print("mqtt: Publish -> (kein Topic gesetzt): {}".format(state))
