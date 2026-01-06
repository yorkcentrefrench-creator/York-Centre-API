import requests

def get_cad_to_inr_rate() -> float:
    try:
        url = "https://api.exchangerate.host/latest"
        params = {"base": "CAD", "symbols": "INR"}
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return float(data["rates"]["INR"])
    except Exception:
        return 62.0