# ============================================================
# ZUNO AGENT
# ============================================================

import os
import subprocess
import time
import webbrowser
from urllib.parse import quote_plus

import pyautogui

from google.adk.agents import Agent

from creative_mode import creative_mode

from file_tools import (
    create_folder,
    create_file,
    open_folder,
    open_file_in_pycharm,
    open_folder_in_pycharm,
    rename_file,
    delete_file_or_folder,
    close_application,
)

from selenium_tools import (
    open_chrome_with_selenium,
    search_google_with_selenium,
    search_youtube_with_selenium,
    play_youtube,
    open_youtube_video,
    open_automation_test_site,
    test_selenium_form,
    close_selenium_browser,
)

from communication_tools import (
    send_sms,
    make_call,
    send_whatsapp_message,
)


# ============================================================
# STATUS
# ============================================================

def get_current_status() -> str:
    """Return Zuno's current status."""
    return "Zuno is online and ready."


# ============================================================
# OPEN WEBSITE
# ============================================================

def open_website(url: str) -> str:
    """Open a website."""
    try:
        url = url.strip()
        if not url:
            return "ERROR: Website address is empty."
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        if webbrowser.open(url):
            return f"SUCCESS: Opened {url}"
        return f"ERROR: Could not open {url}"
    except Exception as e:
        return f"ERROR: Could not open website: {type(e).__name__}: {e}"


# ============================================================
# GOOGLE SEARCH
# ============================================================

def search_google(query: str) -> str:
    """Search Google using the normal browser."""
    try:
        query = query.strip()
        if not query:
            return "ERROR: Search query is empty."
        url = "https://www.google.com/search?q=" + quote_plus(query)
        if webbrowser.open(url):
            return f"SUCCESS: Searched Google for '{query}'."
        return "ERROR: Could not open Google."
    except Exception as e:
        return f"ERROR: Could not search Google: {type(e).__name__}: {e}"


# ============================================================
# YOUTUBE SEARCH
# ============================================================

def search_youtube(query: str) -> str:
    """Search YouTube using the normal browser."""
    try:
        query = query.strip()
        if not query:
            return "ERROR: YouTube search query is empty."
        url = "https://www.youtube.com/results?search_query=" + quote_plus(query)
        if webbrowser.open(url):
            return f"SUCCESS: Searched YouTube for '{query}'."
        return "ERROR: Could not open YouTube."
    except Exception as e:
        return f"ERROR: Could not search YouTube: {type(e).__name__}: {e}"


# ============================================================
# OPEN APPLICATION
# ============================================================

def open_application(application: str) -> str:
    """Open a Windows application."""
    try:
        app_name = application.lower().strip()
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "calc": "calc.exe",
            "paint": "mspaint.exe",
            "microsoft paint": "mspaint.exe",
            "explorer": "explorer.exe",
            "file explorer": "explorer.exe",
            "command prompt": "cmd.exe",
            "cmd": "cmd.exe",
            "powershell": "powershell.exe",
            "word": "winword.exe",
            "microsoft word": "winword.exe",
            "excel": "excel.exe",
            "microsoft excel": "excel.exe",
            "powerpoint": "powerpnt.exe",
            "microsoft powerpoint": "powerpnt.exe",
        }

        # Chrome
        if app_name in {"chrome", "google chrome", "browser", "web browser"}:
            return open_chrome_with_selenium()

        # Spotify
        if app_name in {"spotify", "spotify app"}:
            webbrowser.open("https://open.spotify.com/")
            return "SUCCESS: Opened Spotify."

        # PyCharm
        if app_name in {"pycharm", "py charm"}:
            pycharm_path = r"E:\py\PyCharm 2026.2.0.1\bin\pycharm64.exe"
            if not os.path.exists(pycharm_path):
                return f"ERROR: PyCharm was not found at {pycharm_path}"
            subprocess.Popen([pycharm_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            return "SUCCESS: Opened PyCharm."

        if app_name not in apps:
            return f"ERROR: I don't currently know how to open '{application}'."

        process = subprocess.Popen(apps[app_name], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        time.sleep(0.5)
        return f"SUCCESS: Opened {application}. Process ID: {process.pid}"
    except Exception as e:
        return f"ERROR: Could not open {application}: {type(e).__name__}: {e}"


# ============================================================
# TYPE TEXT
# ============================================================

def type_text(text: str) -> str:
    """Paste text into the active application."""
    try:
        if not text:
            return "ERROR: Text is empty."
        import pyperclip
        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")
        return "SUCCESS: Text typed."
    except Exception as e:
        return f"ERROR: Could not type text: {type(e).__name__}: {e}"


# ============================================================
# PRESS KEY
# ============================================================

def press_key(key: str) -> str:
    """Press a keyboard key."""
    try:
        key = key.lower().strip()
        if not key:
            return "ERROR: Key is empty."
        pyautogui.press(key)
        return f"SUCCESS: Pressed {key}."
    except Exception as e:
        return f"ERROR: Could not press {key}: {type(e).__name__}: {e}"


# ============================================================
# HOTKEY
# ============================================================

def hotkey(keys: list[str]) -> str:
    """Press multiple keys together."""
    try:
        if not keys:
            return "ERROR: No keys were provided."
        pyautogui.hotkey(*keys)
        return "SUCCESS: Pressed " + " + ".join(keys) + "."
    except Exception as e:
        return f"ERROR: Could not press shortcut: {type(e).__name__}: {e}"


# ============================================================
# MOUSE CLICK
# ============================================================

def click_mouse(x: int, y: int) -> str:
    """Click at screen coordinates."""
    try:
        pyautogui.click(x, y)
        return f"SUCCESS: Clicked at ({x}, {y})."
    except Exception as e:
        return f"ERROR: Could not click mouse: {type(e).__name__}: {e}"


# ============================================================
# DRAW LINE
# ============================================================

def draw_line(start_x: int, start_y: int, end_x: int, end_y: int) -> str:
    """Draw a line using the mouse."""
    try:
        pyautogui.moveTo(start_x, start_y, duration=0.2)
        pyautogui.dragTo(end_x, end_y, duration=0.7, button="left")
        return f"SUCCESS: Drew a line from ({start_x}, {start_y}) to ({end_x}, {end_y})."
    except Exception as e:
        return f"ERROR: Could not draw line: {type(e).__name__}: {e}"


# ============================================================
# SAVE CURRENT FILE
# ============================================================

def save_current_file(file_name: str = "") -> str:
    """Save the active document."""
    try:
        pyautogui.hotkey("ctrl", "shift", "s")
        time.sleep(1.5)
        if file_name.strip():
            import pyperclip
            pyperclip.copy(file_name.strip())
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.5)
            pyautogui.press("enter")
            time.sleep(1.0)
            return f"SUCCESS: Save command completed for '{file_name}'."
        return "SUCCESS: Save As window opened."
    except Exception as e:
        return f"ERROR: Could not save file: {type(e).__name__}: {e}"


# ============================================================
# MEDIA CONTROL
# ============================================================

def pause_media() -> str:
    from selenium_tools import pause_media as selenium_pause
    return selenium_pause()

def resume_media() -> str:
    from selenium_tools import resume_media as selenium_resume
    return selenium_resume()

def stop_media() -> str:
    from selenium_tools import stop_media as selenium_stop
    return selenium_stop()


# ============================================================
# VOLUME
# ============================================================

def volume_up() -> str:
    try:
        for _ in range(3):
            pyautogui.press("volumeup")
        return "SUCCESS: Increased volume."
    except Exception as e:
        return f"ERROR: Could not increase volume: {type(e).__name__}: {e}"

def volume_down() -> str:
    try:
        for _ in range(3):
            pyautogui.press("volumedown")
        return "SUCCESS: Decreased volume."
    except Exception as e:
        return f"ERROR: Could not decrease volume: {type(e).__name__}: {e}"

def mute_volume() -> str:
    try:
        pyautogui.press("volumemute")
        return "SUCCESS: Toggled mute."
    except Exception as e:
        return f"ERROR: Could not mute volume: {type(e).__name__}: {e}"


# ============================================================
# WINDOW CONTROL
# ============================================================

def close_active_window() -> str:
    try:
        pyautogui.hotkey("alt", "f4")
        return "SUCCESS: Closed the active window."
    except Exception as e:
        return f"ERROR: Could not close window: {type(e).__name__}: {e}"

def minimize_window() -> str:
    try:
        pyautogui.hotkey("win", "down")
        return "SUCCESS: Minimized the window."
    except Exception as e:
        return f"ERROR: Could not minimize window: {type(e).__name__}: {e}"

def maximize_window() -> str:
    try:
        pyautogui.hotkey("win", "up")
        return "SUCCESS: Maximized the window."
    except Exception as e:
        return f"ERROR: Could not maximize window: {type(e).__name__}: {e}"


# ============================================================
# SPOTIFY
# ============================================================

def open_spotify() -> str:
    try:
        webbrowser.open("https://open.spotify.com/")
        return "SUCCESS: Opened Spotify."
    except Exception as e:
        return f"ERROR: Could not open Spotify: {type(e).__name__}: {e}"

def search_spotify(query: str) -> str:
    try:
        query = query.strip()
        if not query:
            return "ERROR: Spotify search query is empty."
        url = "https://open.spotify.com/search/" + quote_plus(query)
        webbrowser.open(url)
        return f"SUCCESS: Searched Spotify for '{query}'."
    except Exception as e:
        return f"ERROR: Could not search Spotify: {type(e).__name__}: {e}"


# ============================================================
# YOUTUBE
# ============================================================

def open_youtube() -> str:
    try:
        webbrowser.open("https://www.youtube.com")
        return "SUCCESS: Opened YouTube."
    except Exception as e:
        return f"ERROR: Could not open YouTube: {type(e).__name__}: {e}"

def selenium_google_search(query: str) -> str:
    return search_google_with_selenium(query)

def selenium_youtube_search(query: str) -> str:
    return search_youtube_with_selenium(query)

def play_youtube_video(query: str) -> str:
    return play_youtube(query)

def open_specific_youtube_video(url: str) -> str:
    return open_youtube_video(url)

def close_chrome() -> str:
    return close_selenium_browser()

def selenium_test() -> str:
    return open_automation_test_site()

def selenium_form_test() -> str:
    return test_selenium_form()


# ============================================================
# ZUNO AGENT
# ============================================================

root_agent = Agent(

    name="zuno",
    
    # 2.0-flash is the best for agents and fixes 429 errors
    model="gemini-3.5-flash-lite",

    description=(
        "Zuno is an intelligent personal AI assistant "
        "that controls the user's Windows computer, "
        "browser, files, applications, media, "
        "WhatsApp, SMS and phone calls, and can create "
        "original creative content."
    ),

    instruction="""

You are Zuno, a practical Windows computer-control
and creative AI assistant.

The user primarily communicates through voice.

============================================================
CORE RULE
============================================================

ACT FIRST.

When a tool can perform the requested action, use the tool.
Never claim success unless the tool reports SUCCESS.
Keep spoken responses short for normal computer actions.

============================================================
CREATIVE MODE
============================================================

You have a tool called creative_mode.
Use creative_mode whenever the user asks you to create,
write, generate, develop, continue, or modify creative content.

Examples:
"write me a story about a robot" → creative_mode
"create a character named Maya" → creative_mode
"continue this story" → creative_mode

For creative requests, call creative_mode instead of trying
to answer using computer-control tools.
Return the generated creative content to the user.

============================================================
APPLICATIONS
============================================================

Use open_application for:
Chrome, Notepad, Calculator, Paint, File Explorer, Word, 
Excel, PowerPoint, PyCharm, Spotify

When the user asks to close an application:
    use close_application

============================================================
YOUTUBE
============================================================

"open YouTube" → open_youtube
"search YouTube for [query]" → selenium_youtube_search
"play [song/video]" → play_youtube_video
"pause" → pause_media
"resume" → resume_media
"stop" → stop_media

IMPORTANT:
"play [specific song/video]" means SEARCH AND PLAY.
"play again" means RESUME CURRENT MEDIA.

============================================================
VOLUME & WINDOWS
============================================================

"volume up" → volume_up
"volume down" → volume_down
"mute" → mute_volume

"close this" → close_active_window
"minimize this" → minimize_window
"maximize this" → maximize_window
"close Selenium Chrome" → close_chrome

============================================================
GOOGLE
============================================================

"search Google for [query]" → selenium_google_search

============================================================
FILES
============================================================

"create a file called test.txt"
→ create_file

"create a folder called Test"
→ create_folder

"open Test folder"
→ open_folder

"rename test.txt to hello.txt"
→ rename_file

"delete test.txt"
→ delete_file_or_folder

CRITICAL RULE: If the user asks to delete, YOU MUST use delete_file_or_folder. NEVER use open_file_in_pycharm. NEVER try to open the file instead. If deletion fails, just tell the user it failed.

============================================================
PYCHARM
============================================================

"open main.py in PyCharm" → open_file_in_pycharm
"open TestZuno in PyCharm" → open_folder_in_pycharm

============================================================
NOTEPAD & KEYBOARD / MOUSE
============================================================

"open Notepad and type hello"
1. open_application("Notepad")
2. type_text("hello")

"write [text] in Notepad" → type_text with the COMPLETE text
"save this as test.txt" → save_current_file("test.txt")
"save" → save_current_file()

"press enter" → press_key("enter")
"ctrl c" → hotkey(["ctrl", "c"])
"click at 500 300" → click_mouse(500, 300)

Never invent coordinates.


============================================================
COMMUNICATION (WHATSAPP, CALLS, SMS)
============================================================

"Send a WhatsApp to Mom saying hello"
→ send_whatsapp_message("mom", "hello")

"Call Rahul"
→ make_call("rahul")

"Text 9876543210 saying I am busy"
→ send_sms("9876543210", "I am busy")

You can accept EITHER a contact name OR a phone number. 
Never invent a contact. If the user doesn't provide the name/number or the message, ask them for it before using the tool.

============================================================
MULTI-ACTION
============================================================

Execute multiple requested actions in order.
Example: "Open Notepad, write hello and save it as test.txt."
1. open_application("Notepad")
2. type_text("hello")
3. save_current_file("test.txt")

============================================================
ERRORS & RESPONSE STYLE
============================================================

If a tool returns ERROR, report the error briefly.
Never pretend it worked.

Normal computer actions should have short responses: "Done.", "Chrome is open."
Creative Mode responses may be long.

FINAL RULE: ACT FIRST. REPORT SECOND. NEVER PRETEND.

""",

    tools=[

        # ====================================================
        # STATUS
        # ====================================================
        get_current_status,

        # ====================================================
        # CREATIVE MODE
        # ====================================================
        creative_mode,

        # ====================================================
        # APPLICATIONS
        # ====================================================
        open_application,
        close_application,

        # ====================================================
        # WEBSITES
        # ====================================================
        open_website,
        search_google,
        search_youtube,
        open_youtube,

        # ====================================================
        # SELENIUM
        # ====================================================
        open_chrome_with_selenium,
        selenium_google_search,
        selenium_youtube_search,
        play_youtube_video,
        open_specific_youtube_video,
        selenium_test,
        selenium_form_test,
        close_chrome,

        # ====================================================
        # SPOTIFY
        # ====================================================
        open_spotify,
        search_spotify,

        # ====================================================
        # KEYBOARD / MOUSE
        # ====================================================
        type_text,
        press_key,
        hotkey,
        click_mouse,
        draw_line,

        # ====================================================
        # SAVE
        # ====================================================
        save_current_file,

        # ====================================================
        # MEDIA
        # ====================================================
        pause_media,
        resume_media,
        stop_media,
        volume_up,
        volume_down,
        mute_volume,

        # ====================================================
        # WINDOWS
        # ====================================================
        close_active_window,
        minimize_window,
        maximize_window,

        # ====================================================
        # FILES
        # ====================================================
        create_folder,
        create_file,
        open_folder,
        rename_file,
        delete_file_or_folder,

        # ====================================================
        # PYCHARM
        # ====================================================
        open_file_in_pycharm,
        open_folder_in_pycharm,

        # ====================================================
        # COMMUNICATION
        # ====================================================
        send_sms,
        make_call,
        send_whatsapp_message,
    ],
)