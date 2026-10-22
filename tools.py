import re
from pathlib import Path

CORPUS_PATH = Path(__file__).parent/"corpus.txt"
#1renew_online_eligibility
def check_online_renewal_eligibility(days_to_expiry: int) -> dict:
    """Positive = days until expiry. Negative = days since it expired."""
    if days_to_expiry >= 0:
        eligible = days_to_expiry <= 90
        reason = "within 90 days before expiry" if eligible else "more than 90 days before expiry"
    else:
        eligible = -days_to_expiry <= 365
        reason = "within 12 months after expiry" if eligible else "more than 12 months after expiry"
    return {
        "eligible_online": eligible,
        "reason": reason,
        "note": "Other online eligibility requirements may still apply.",
    }





#2 get_signal_meaning
SIGNALS = {
    "solid_red": "STOP at the stop or limit line. After stopping, you may turn right on red if no NO TURN ON RED sign is posted and the turn is safe.",
    "red_arrow": "STOP. Do not turn against a red arrow. Remain stopped until a green signal or green arrow appears.",
    "flashing_red": "STOP. After stopping, you may proceed when it is safe.",
    "solid_yellow": "CAUTION. The signal is about to turn red. Stop if you can do so safely; otherwise cross the intersection cautiously.",
    "flashing_yellow": "PROCEED WITH CAUTION. Slow down and stay alert. You do not need to stop.",
    "solid_green": "GO, but yield to vehicles, bicyclists and pedestrians already in the intersection. Do not enter if you cannot completely cross before the light turns red.",
    "green_arrow": "A protected turn in the direction of the arrow. Oncoming traffic is stopped by a red signal.",
    "not_working": "Treat the intersection as if it has STOP signs in all directions. Stop, then proceed cautiously when it is safe.",
}

def get_signal_meaning(signal:str)->dict:
    if signal not in SIGNALS:
        return {"error":"Invalid signal name."}
    else:
        return {"signal":signal, "meaning": SIGNALS[signal]}


    
#3search_handbook

STOPWORDS = {"the", "a", "an", "is", "are", "do", "does", "i", "my", "to", "of", "in", "on",
             "for", "what", "how", "can", "must", "should", "when", "it", "be", "at", "or",
             "and", "if", "you", "your", "need", "much", "far"}

def _words(text: str) -> set:
    return set(re.findall(r"[a-z0-9']+", text.lower()))

def search_handbook(query: str, top_k: int = 3) -> dict:
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", CORPUS_PATH.read_text(encoding="utf-8")) if p.strip()]
    q = _words(query) - STOPWORDS
    scored = [(len(q & _words(p)), p) for p in paragraphs]
    scored = [s for s in scored if s[0] > 0]
    scored.sort(key=lambda s: s[0], reverse=True)
    return {"query": query, "results": [p for _, p in scored[:top_k]]}


REGISTRY = {
    "check_online_renewal_eligibility":check_online_renewal_eligibility,
    "get_signal_meaning":get_signal_meaning,
    "search_handbook":search_handbook
}

def _tool(name, description, props, required):
    return {
        "type":"function",
        "function":{
        "name":name,
        "description": description,
        "parameters":{
            "type":"object",
            "properties":props,
            "required": required
        }
 }}

TOOLS_PRECISE = [
    _tool(
        "check_online_renewal_eligibility",
        "Check whether a California driver's license can be renewed online, based on how many "
        "days remain until it expires. Use it only when the user asks about renewing online AND "
        "says or clearly implies when the license expires. If the timing is not given, ask the "
        "user for it instead of calling this tool. Do not use it for fees, in-person renewal, "
        "or vehicle registration.",
        {"days_to_expiry": {
            "type": "integer",
            "description": "Days until the license expires. Use a negative number if it has already "
                           "expired (-30 means it expired 30 days ago). Convert phrases like "
                           "'6 months ago' to days, using about 30 days per month."}},
        ["days_to_expiry"],
    ),
    _tool(
        "get_signal_meaning",
        "Explain what one specific traffic signal means and what a driver must do, for example a "
        "red arrow or a flashing yellow light. Use it when the user asks about a signal type. "
        "Do not use it for turning lanes, parking, or license questions.",
        {"signal": {
            "type": "string",
            "enum": list(SIGNALS.keys()),
            "description": "The signal type. Choose the closest match."}},
        ["signal"],
    ),
    _tool(
        "search_handbook",
        "Search a short California DMV handbook excerpt for rules about turning, parking, traffic "
        "signals, driver's license renewal, and vehicle registration. Use it for general rules "
        "questions that the other tools do not cover. The excerpt contains no fees, no office "
        "locations, and no phone numbers.",
        {"query": {
            "type": "string",
            "description": "A short search phrase using the key words of the question, "
                           "for example 'parking distance from curb'."}},
        ["query"],
    ),
]

TOOLS_VAGUE = [
    _tool("check_online_renewal_eligibility", "Checks license renewal.",
          {"days_to_expiry": {"type": "integer"}}, ["days_to_expiry"]),
    _tool("get_signal_meaning", "Gets signal information.",
          {"signal": {"type": "string", "enum": list(SIGNALS.keys())}}, ["signal"]),
    _tool("search_handbook", "Searches the handbook.",
          {"query": {"type": "string"}}, ["query"]),
]
