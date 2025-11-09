# In backend/token_utils.py

def get_token_claim(request, claim_name, default=None):
    """
    "Flawless" helper to safely get a claim from the JWT.
    
    This prevents crashes if 'request.auth' or the claim is missing.
    
    Args:
        request: The request object.
        claim_name (str): The name of the claim to get (e.g., 'user_id').
        default: The safe value to return if the claim is not found.
        
    Returns:
        The claim's value or the default.
    """
    
    # 1. Check if request.auth exists and is not None
    if not hasattr(request, 'auth') or request.auth is None:
        return default
    
    # 2. Safely get the claim from the auth token
    # .get() will return 'default' (None) if the claim_name is missing
    return request.auth.get(claim_name, default)