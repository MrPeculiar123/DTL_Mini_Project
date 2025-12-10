# backend/src/services/matching_engine.py
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- MOCK INVENTORY (Replace this with a DB query later) ---
MOCK_PRODUCT_DB = [
    {
        "sku": "CBL-3PH-50A",
        "name": "Industrial Power Cable 50A",
        "specs": "3-phase, 415V, 50 Amps, Copper Core, PVC Insulation",
        "price": 2500
    },
    {
        "sku": "CBL-3PH-100A",
        "name": "Heavy Duty Cable 100A",
        "specs": "3-phase, 415V, 100 Amps, Armored, XLPE",
        "price": 4500
    },
    {
        "sku": "SWG-1PH-16A",
        "name": "Domestic Switchgear 16A",
        "specs": "1-phase, 230V, 16 Amps, Plastic Housing",
        "price": 450
    },
    {
        "sku": "TRN-500KVA",
        "name": "Distribution Transformer 500kVA",
        "specs": "11kV/433V, Oil Cooled, 500 kVA rating",
        "price": 450000
    }
]

def extract_key_specs(text: str):
    """
    Uses Regex to pull hard numbers (Voltage, Amperage) from RFP text.
    """
    specs = {
        "voltage": None,
        "amperage": None
    }
    
    # Regex to find patterns like "415V", "415 Volts", "50A", "50 Amps"
    volt_match = re.search(r'(\d+)\s*[vV](?:olts?)?', text, re.IGNORECASE)
    amp_match = re.search(r'(\d+)\s*[aA](?:mps?)?', text, re.IGNORECASE)
    
    if volt_match:
        specs['voltage'] = int(volt_match.group(1))
    if amp_match:
        specs['amperage'] = int(amp_match.group(1))
        
    return specs

def find_best_matches(rfp_text: str, top_n=3):
    """
    1. TF-IDF Vectorization to find text similarity.
    2. Boosts score if Hard Specs (Volts/Amps) match.
    """
    # Prepare Data
    product_descriptions = [p['specs'] + " " + p['name'] for p in MOCK_PRODUCT_DB]
    documents = [rfp_text] + product_descriptions
    
    # Calculate Similarity
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    
    # Cosine Similarity between RFP (index 0) and Products (index 1 to N)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    # Extract hard specs for "Boosting"
    rfp_specs = extract_key_specs(rfp_text)
    
    results = []
    for i, score in enumerate(cosine_sim):
        product = MOCK_PRODUCT_DB[i]
        final_score = score
        
        # --- LOGIC: BOOST SCORE FOR HARD SPEC MATCH ---
        prod_specs = extract_key_specs(product['specs'])
        
        if rfp_specs['voltage'] and prod_specs['voltage']:
            # Allow 10% tolerance
            if 0.9 <= rfp_specs['voltage'] / prod_specs['voltage'] <= 1.1:
                final_score += 0.3  # Huge boost for voltage match
                
        if rfp_specs['amperage'] and prod_specs['amperage']:
            if rfp_specs['amperage'] == prod_specs['amperage']:
                final_score += 0.3 # Huge boost for amp match
                
        results.append({
            "sku": product['sku'],
            "name": product['name'],
            "match_score": round(min(final_score, 0.99), 2), # Cap at 0.99
            "reason": f"Text Sim: {round(score,2)}"
        })
    
    # Sort by score descending and return top N
    results.sort(key=lambda x: x['match_score'], reverse=True)
    return results[:top_n]