def connect(ssid=None, password=None, retries=3, delay_s=2):
    """
    Platzhalter für WLAN-Verbindung.
    Gibt True zurück, wenn (scheinbar) verbunden.
    """
    try:
        import network  # type: ignore
    except ImportError:
        print("wifi: network-Modul nicht verfügbar (Dummy-Modus).")
        return False

    if not ssid:
        print("wifi: kein SSID gesetzt, überspringe Verbindung (Dummy-Modus).")
        return False

    sta = network.WLAN(network.STA_IF)
    if not sta.active():
        sta.active(True)

    for attempt in range(1, retries + 1):
        print("wifi: Verbinde mit SSID '{}', Versuch {}/{} ...".format(ssid, attempt, retries))
        sta.connect(ssid, password)
        for _ in range(10):
            if sta.isconnected():
                print("wifi: verbunden, IP:", sta.ifconfig()[0])
                return True
            time.sleep_ms(200)

        time.sleep(delay_s)

    print("wifi: keine Verbindung hergestellt.")
    return False
import time
