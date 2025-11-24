class MailStateMachine:
    """
    Einfache Zustandsmaschine zur Post-Erkennung per Ultraschallsensor.
    - empty_distance_cm: Distanz bei leerem Briefkasten (Kalibrierwert)
    - delta_cm: Ab wann gilt "etwas liegt drin" (Distanz größer als leer+delta)
    - consecutive_required: Anzahl aufeinander folgender Treffer, um Rauschen zu filtern
    """

    def __init__(self, empty_distance_cm, delta_cm=5.0, consecutive_required=3):
        self.empty_distance_cm = empty_distance_cm
        self.delta_cm = delta_cm
        self.consecutive_required = consecutive_required
        self.has_mail = False
        self._hits = 0

    def update(self, measurement_cm):
        """
        Nimmt eine neue Messung (cm oder None) entgegen.
        Gibt Tuple (has_mail, changed) zurück.
        """
        if measurement_cm is None:
            # Messfehler: Zähler zurücksetzen, Zustand unverändert
            self._hits = 0
            return self.has_mail, False

        mail_detected = measurement_cm > (self.empty_distance_cm + self.delta_cm)

        if mail_detected:
            if self._hits < self.consecutive_required:
                self._hits += 1
        else:
            self._hits = 0

        changed = False

        if mail_detected and self._hits >= self.consecutive_required and not self.has_mail:
            self.has_mail = True
            changed = True

        return self.has_mail, changed

    def reset(self):
        """
        Setzt den Status auf "leer" zurück.
        Gibt Tuple (has_mail, changed) zurück.
        """
        was_mail = self.has_mail
        self.has_mail = False
        self._hits = 0
        changed = was_mail  # nur "changed", wenn vorher Post erkannt war
        return self.has_mail, changed
