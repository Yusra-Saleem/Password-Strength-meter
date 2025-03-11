"""
Password insights module with funny comments and additional security insights.
"""
import random
import datetime

def get_funny_comment(score, time_to_crack):
    """
    Returns a funny comment based on password strength score and crack time.
    
    Args:
        score (int): Password strength score (0-4)
        time_to_crack (str): Human-readable crack time
        
    Returns:
        str: A funny comment
    """
    very_weak_comments = [
        "Even my grandma could crack this password! 👵",
        "This password is like leaving your front door wide open with a sign saying 'Welcome Hackers!' 🚪",
        "Your password is more exposed than a celebrity on social media. 📸",
        "If passwords were cars, yours would be a broken-down bicycle. 🚲",
        "This password is about as secure as a chocolate teapot. 🍫",
    ]
    
    weak_comments = [
        "Your password and a paper lock have about the same security level. 📝",
        "Hackers would find cracking this password more boring than challenging. 😴",
        "This password is like using a pool noodle as home security. 🏊",
        "Your password should consider going to the gym to get stronger. 💪",
        "The 90s called, they want their weak password back. 📞",
    ]
    
    medium_comments = [
        "Not bad! Your password is like a guard dog who sometimes falls asleep on duty. 🐕",
        "Your password security is the equivalent of a door with three locks but one is broken. 🔒",
        "Hackers would need to put in some effort - like getting up from their chair. 💺",
        "Your password is the digital equivalent of 'good enough' - like store-brand cereal. 🥣",
        "This password is like a fence that's tall but has a few holes in it. 🧀",
    ]
    
    strong_comments = [
        "Impressive! Hackers would need to pack a lunch to crack this one. 🍱",
        "Your password is like Fort Knox, but with better WiFi. 🏰",
        "Hackers see your password and suddenly 'remember' they have other things to do. 🏃",
        "This password is stronger than my coffee on Monday morning, and that's saying something! ☕",
        "Hackers trying to crack this would age like they looked into the wrong Holy Grail. 👴",
    ]
    
    very_strong_comments = [
        "Wow! This password is stronger than a bodybuilder who does CrossFit and is vegan (and tells everyone). 🏋",
        "Aliens might evolve, visit Earth, and leave before this password gets cracked. 👽",
        "Your password is so secure, even you might forget it! 🤔",
        "Hackers would retire, take up knitting, and finish a sweater before cracking this. 🧶",
        "The heat death of the universe will occur before this password is compromised. 🌌",
    ]
    
    if score == 0:
        return random.choice(very_weak_comments)
    elif score == 1:
        return random.choice(weak_comments)
    elif score == 2:
        return random.choice(medium_comments)
    elif score == 3:
        return random.choice(strong_comments)
    else:  # score == 4
        return random.choice(very_strong_comments)

def get_historical_insight(score, password):
    """
    Returns a historical insight based on password characteristics.
    
    Args:
        score (int): Password strength score (0-4)
        password (str): The password to analyze
        
    Returns:
        str: A historical insight
    """
    insights = [
        "Did you know? The first computer password was implemented at MIT in 1961.",
        "In 2019, '123456' was still the most commonly used password, followed by '123456789' and 'qwerty'.",
        "Biometric security (fingerprints, face recognition) doesn't replace passwords—it just adds another layer of security.",
        "The average person has to remember around 70-80 passwords across various services.",
        "Password managers were first introduced in the late 1990s to help combat password fatigue.",
        "The NIST (National Institute of Standards and Technology) now recommends using long passphrases instead of complex, hard-to-remember passwords.",
        "The concept of a 'brute force attack' on passwords was first formalized in the 1970s.",
        "Password composition rules (requiring uppercase, numbers, etc.) were first standardized in the 1980s.",
        "Two-factor authentication was developed in the early 1980s but didn't become widely used until the 2010s.",
        "The first known computer 'worm' that used password cracking was the Morris Worm in 1988."
    ]
    
    return random.choice(insights)

def get_password_strength_description(score):
    """
    Returns a descriptive text about what the password strength score means.
    
    Args:
        score (int): Password strength score (0-4)
        
    Returns:
        dict: A dictionary with title and content describing the score
    """
    descriptions = {
        0: {
            "title": "Very Weak Password",
            "content": "This password can be cracked almost instantly. It's likely a common password, too short, or uses very predictable patterns."
        },
        1: {
            "title": "Weak Password",
            "content": "This password doesn't provide adequate protection. It would be vulnerable to common cracking methods and could be breached quickly."
        },
        2: {
            "title": "Medium Strength Password",
            "content": "This password offers moderate protection. While not immediately vulnerable, it could still be cracked with dedicated effort."
        },
        3: {
            "title": "Strong Password",
            "content": "This password provides good protection against most attack methods. It would require significant time and resources to crack."
        },
        4: {
            "title": "Very Strong Password",
            "content": "Excellent! This password offers exceptional protection. It would be extremely difficult to crack through brute force methods."
        }
    }
    
    return descriptions.get(score, {"title": "Unknown", "content": "Could not determine password strength."})

def get_security_strategy(score):
    """
    Returns a security strategy based on the password strength score.
    
    Args:
        score (int): Password strength score (0-4)
        
    Returns:
        list: A list of security strategies
    """
    base_strategies = [
        "Use a password manager to generate and store complex passwords",
        "Enable two-factor authentication whenever possible",
        "Never reuse passwords across different accounts",
        "Change passwords periodically, especially for sensitive accounts",
        "Be cautious of phishing attempts asking for your password"
    ]
    
    low_score_strategies = [
        "Increase your password length to at least 12 characters",
        "Use a combination of uppercase, lowercase, numbers, and special characters",
        "Avoid using personal information in your passwords",
        "Don't use sequential patterns like '12345' or 'qwerty'",
        "Consider using a passphrase (a sequence of random words)"
    ]
    
    if score <= 2:
        # Return both base strategies and low score specific advice
        return base_strategies + low_score_strategies
    else:
        # Return just the base strategies
        return base_strategies

def get_password_hash_preview(password):
    """
    Returns a masked preview of what the password hash might look like.
    Not a real hash, just for illustration.
    
    Args:
        password (str): The password to visualize
        
    Returns:
        str: A fake hash visualization
    """
    # This is NOT a real hash - just a visual representation for educational purposes
    import hashlib
    real_hash = hashlib.sha256(password.encode()).hexdigest()
    return f"{real_hash[:6]}...{real_hash[-6:]}"