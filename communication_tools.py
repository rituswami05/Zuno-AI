import os
import json
import time
import webbrowser
from urllib.parse import quote
import pyautogui
import difflib
import re

# ============================================================
# TWILIO SETUP (FOR REAL PHONE CALLS & SMS)
# ============================================================
# To make real phone calls or standard SMS, you need a free account from twilio.com
# (WhatsApp works entirely for free without this!)


# ============================================================
# SMART CONTACT BOOK (WORKS ON ANYONE'S PC)
# ============================================================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONTACTS_FILE = os.path.join(CURRENT_DIR, "contacts.json")

def load_contacts():
    """Loads contacts from contacts.json, creating a template if missing."""
    if not os.path.exists(CONTACTS_FILE):
        template = {
            "mom": "+919876543210",
            "mother": "+919876543210",
            "dad": "+918765432109",
            "father": "+918765432109",
            "test": "+910000000000"
        }
        with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
            json.dump(template, f, indent=4)
        return template

    try:
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def resolve_phone_number(contact_name_or_number: str) -> str:
    """Matches a spoken name using smart Fuzzy Matching."""
    
    query = re.sub(r'[^a-z0-9]', '', contact_name_or_number.lower())
    contacts = load_contacts()
    
    # Clean the contact book keys
    normalized_contacts = {re.sub(r'[^a-z0-9]', '', k.lower()): v for k, v in contacts.items()}

    # 1. Try an EXACT match first
    if query in normalized_contacts:
        return normalized_contacts[query]

    # 2. Try a FUZZY match (The "Did you mean?" feature)
    # It looks for names that are at least 60% similar to what the microphone heard
    possible_matches = difflib.get_close_matches(query, normalized_contacts.keys(), n=1, cutoff=0.6)
    
    if possible_matches:
        best_guess = possible_matches[0]
        print(f"--- DEBUG: STT heard '{query}', but Fuzzy Match auto-corrected to '{best_guess}'! ---")
        return normalized_contacts[best_guess]

    # 3. If it fails, assume it's a raw phone number
    cleaned_number = query
    if any(char.isalpha() for char in cleaned_number):
        raise ValueError(f"'{contact_name_or_number}' is not in your contacts.json file.")

    if not cleaned_number.startswith("+"):
        cleaned_number = "+91" + cleaned_number

    return cleaned_number


# ============================================================
# WHATSAPP (FREE - USES DESKTOP APP)
# ============================================================

def send_whatsapp_message(contact_name_or_number: str, message: str) -> str:
    """
    CRITICAL: Sends a WhatsApp message. 
    You MUST accept contact names (like 'mom', 'dad') OR raw phone numbers. 
    DO NOT ask the user for a phone number if they provide a name. Just pass the name directly into this tool!
    """
    try:
        phone_number = resolve_phone_number(contact_name_or_number)

        url = f"whatsapp://send?phone={phone_number}&text={quote(message)}"
        webbrowser.open(url)
        
        time.sleep(4)
        pyautogui.press("enter")
        
        return f"SUCCESS: WhatsApp message sent to {contact_name_or_number}."
    except ValueError as ve:
        return f"ERROR: {ve}"
    except Exception as e:
        return f"ERROR: Could not send WhatsApp message: {e}"


# ============================================================
# PHONE CALLS (REQUIRES TWILIO)
# ============================================================

def make_call(contact_name_or_number: str) -> str:
    """
    CRITICAL: Makes a phone call. 
    You MUST accept contact names (like 'mom') OR raw phone numbers. 
    DO NOT ask the user for a phone number if they provide a name. Pass the name directly!
    """
    try:
        phone_number = resolve_phone_number(contact_name_or_number)

        from twilio.rest import Client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        call = client.calls.create(
            twiml='<Response><Say>Hello! This is Zuno calling on behalf of my creator. Have a great day!</Say></Response>',
            to=phone_number,
            from_=TWILIO_PHONE_NUMBER
        )
        
        return f"SUCCESS: Call initiated to {contact_name_or_number}."
    except ValueError as ve:
        return f"ERROR: {ve}"
    except Exception as e:
        return f"ERROR: Could not make phone call. Did you install Twilio? {e}"


# ============================================================
# SMS TEXT MESSAGES (REQUIRES TWILIO)
# ============================================================

def send_sms(contact_name_or_number: str, message: str) -> str:
    """
    CRITICAL: Sends an SMS text message. 
    You MUST accept contact names (like 'mom') OR raw phone numbers. 
    DO NOT ask the user for a phone number if they provide a name. Pass the name directly!
    """
    try:
        phone_number = resolve_phone_number(contact_name_or_number)

        from twilio.rest import Client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        message_obj = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        
        return f"SUCCESS: SMS sent to {contact_name_or_number}."
    except ValueError as ve:
        return f"ERROR: {ve}"
    except Exception as e:
        return f"ERROR: Could not send SMS: {e}"

# ============================================================
# INITIALIZATION
# ============================================================
# This forces the contacts file to generate the second the app boots up!
load_contacts()