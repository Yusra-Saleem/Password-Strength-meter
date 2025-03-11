import re
import zxcvbn

def analyze_password(password):
    """
    Analyzes a password using zxcvbn and custom criteria.
    
    Args:
        password (str): The password to analyze
        
    Returns:
        dict: Analysis results including score, feedback, and details
    """
    # Use zxcvbn for comprehensive analysis
    result = zxcvbn.zxcvbn(password)
    
    # Extract relevant information
    score = result['score']  # 0-4, with 4 being the strongest
    crack_time_seconds = result['crack_times_seconds']['offline_fast_hashing_1e10_per_second']
    crack_time_display = result['crack_times_display']['offline_fast_hashing_1e10_per_second']
    warnings = result['feedback']['warning']
    suggestions = result['feedback']['suggestions']
    
    # Perform additional specific checks
    strength_details = {
        "Length": check_length(password),
        "Uppercase letters": check_uppercase(password),
        "Lowercase letters": check_lowercase(password),
        "Numbers": check_numbers(password),
        "Special characters": check_special_chars(password),
        "Common patterns": check_common_patterns(password),
        "Repetition": check_repetition(password)
    }
    
    # Format the final analysis
    analysis = {
        'score': score,
        'crack_time_seconds': crack_time_seconds,
        'crack_time_display': crack_time_display,
        'warnings': warnings,
        'suggestions': suggestions,
        'strength_details': strength_details,
        'feedback': generate_feedback(score)
    }
    
    return analysis

def check_length(password):
    """Check if password meets minimum length requirements."""
    min_length = 8
    recommended_length = 12
    
    if len(password) < min_length:
        return {
            'pass': False,
            'message': f"Password is too short (minimum {min_length} characters)"
        }
    elif len(password) < recommended_length:
        return {
            'pass': True,
            'message': f"Password meets minimum length, but {recommended_length}+ characters is recommended"
        }
    else:
        return {
            'pass': True,
            'message': "Password has good length"
        }

def check_uppercase(password):
    """Check if password contains uppercase letters."""
    if re.search(r'[A-Z]', password):
        return {
            'pass': True,
            'message': "Contains uppercase letters"
        }
    else:
        return {
            'pass': False,
            'message': "No uppercase letters found"
        }

def check_lowercase(password):
    """Check if password contains lowercase letters."""
    if re.search(r'[a-z]', password):
        return {
            'pass': True,
            'message': "Contains lowercase letters"
        }
    else:
        return {
            'pass': False,
            'message': "No lowercase letters found"
        }

def check_numbers(password):
    """Check if password contains numbers."""
    if re.search(r'\d', password):
        return {
            'pass': True,
            'message': "Contains numbers"
        }
    else:
        return {
            'pass': False,
            'message': "No numbers found"
        }

def check_special_chars(password):
    """Check if password contains special characters."""
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return {
            'pass': True,
            'message': "Contains special characters"
        }
    else:
        return {
            'pass': False,
            'message': "No special characters found"
        }

def check_common_patterns(password):
    """Check for common patterns like sequences or keyboard patterns."""
    common_sequences = ['123', 'abc', 'qwerty', 'password', 'admin']
    lower_password = password.lower()
    
    for seq in common_sequences:
        if seq in lower_password:
            return {
                'pass': False,
                'message': "Contains common patterns or sequences"
            }
    
    return {
        'pass': True,
        'message': "No obvious patterns detected"
    }

def check_repetition(password):
    """Check for character repetition."""
    if re.search(r'(.)\1{2,}', password):  # Same character repeated 3+ times
        return {
            'pass': False,
            'message': "Contains repeated characters"
        }
    else:
        return {
            'pass': True,
            'message': "No excessive character repetition"
        }

def generate_feedback(score):
    """Generate general feedback based on the score."""
    if score == 0:
        return "Very weak password. Easily guessable."
    elif score == 1:
        return "Weak password. Could be cracked quickly."
    elif score == 2:
        return "Medium strength password. Could be better."
    elif score == 3:
        return "Strong password. Good job!"
    else:  # score == 4
        return "Very strong password. Excellent!"