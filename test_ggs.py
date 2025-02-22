"""
Test Google search
"""

import requests

from config_private import GG_API_KEY, GG_CX


def google_search(query, num_results=5):
    """Effettua una ricerca su Google e restituisce i risultati"""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": GG_API_KEY,
        "cx": GG_CX,
        "num": num_results,  # Numero di risultati desiderati (massimo 10 per richiesta)
    }

    response = requests.get(url, params=params, timeout=30)
    results = response.json()

    if "items" not in results:
        print("Nessun risultato trovato o limite API superato!")
        return []

    search_results = []
    for item in results["items"]:
        search_results.append(
            {
                "title": item["title"],
                "link": item["link"],
                "snippet": item.get("snippet", "Nessuna descrizione disponibile"),
            }
        )

    return search_results


# 🔎 Esegui una ricerca
query = "pricing di Oracle OCI AI Agents?"
results = google_search(query, num_results=5)

# 📜 Mostra i risultati
for i, result in enumerate(results, 1):
    print(f"{i}. {result['title']}")
    print(f"   {result['link']}")
    print(f"   {result['snippet']}\n")
