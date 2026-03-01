import sys
from ai_engine.anomaly_detector import predict_risk
from ai_engine.research_rag import load_secure_index, secure_query

# Simulated Blockchain Status (In a real app, this calls Identity.sol)
def check_blockchain_identity(user_address):
    # Mocking the isAuthorized() call from your Solidity contract
    authorized_wallets = ["0x123", "0x456"]
    return user_address in authorized_wallets

def run_university_access_demo(user_wallet, hour, volume, location, query, dept):
    print(f"\n--- Access Request from {user_wallet} ---")
    
    # Step 1: Zero Trust Identity Check (Blockchain)
    if not check_blockchain_identity(user_wallet):
        return " Access Denied: Invalid Blockchain Identity."
    print(" Identity Verified via Smart Contract.")

    # Step 2: Continuous Behavioral Monitoring (AI UEBA)
    # This runs locally on AMD Ryzen AI for maximum privacy
    risk_assessment = predict_risk(hour, volume, location)
    if risk_assessment == " HIGH RISK":
        return f" Access Blocked: {risk_assessment}. Suspicious behavior detected."
    print(f" Behavioral Analysis: {risk_assessment}.")

    # Step 3: Secure Knowledge Retrieval (RAG)
    print(f" Fetching research data for {dept} department...")
    index = load_secure_index()
    response = secure_query(index, query, dept)
    return f" AI Response: {response}"

if __name__ == "__main__":
    # Scenario A: Valid Student during school hours
    print(run_university_access_demo("0x123", 10, 15, 1, "Latest physics labs", "Physics"))
    
    # Scenario B: Insider Threat (Valid ID but suspicious 3 AM bulk download)
    print(run_university_access_demo("0x456", 3, 950, 9, "All student records", "Admin"))
