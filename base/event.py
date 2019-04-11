from threading import Event


class EventBase(Event):
    target = None
