import random
import string

def process_payment(amount: float, card_number: str = "4242424242424242") -> dict:
    """
    Simulira procesiranje plaćanja.
    Test kartica 4000000000000002 uvek vraća neuspeh, sve ostale uspeh.
    """
    if card_number == "4000000000000002":
        return {"status": "failed", "reason": "Card declined"}

    transaction_id = "mock_" + "".join(random.choices(string.digits, k=10))
    return {"status": "success", "transaction_id": transaction_id}