import re
import unicodedata

def generate_slug(text: str) -> str:
    """
    Erzeugt einen URL-freundlichen Slug aus einem Text-String.
    Entfernt Umlaute, Sonderzeichen und ersetzt Leerzeichen durch Bindestriche.
    
    Args:
        text: Der Text, aus dem ein Slug erzeugt werden soll
        
    Returns:
        Ein URL-freundlicher Slug
    """
    # Zu Kleinbuchstaben konvertieren
    text = text.lower()
    
    # Umlaute und Sonderzeichen durch ASCII-Äquivalente ersetzen
    # (besonders wichtig für deutsche Umlaute: ä, ö, ü, ß)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    
    # Nicht-alphanumerische Zeichen durch Bindestriche ersetzen
    text = re.sub(r'[^a-z0-9]+', '-', text)
    
    # Führende und abschließende Bindestriche entfernen
    text = text.strip('-')
    
    # Mehrfache Bindestriche durch einen einzelnen ersetzen
    text = re.sub(r'-+', '-', text)
    
    return text
