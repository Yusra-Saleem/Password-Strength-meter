def get_strength_color(score):
    """
    Returns a color based on the password strength score.
    
    Args:
        score (int): Password strength score (0-4)
        
    Returns:
        str: Color hex code
    """
    colors = {
        0: "#FF4B4B",  # Very Weak - Red (as per style guide)
        1: "#FF4B4B",  # Weak - Red (as per style guide)
        2: "#FFA500",  # Medium - Orange (as per style guide)
        3: "#00CC66",  # Strong - Green (as per style guide)
        4: "#00CC66"   # Very Strong - Green (as per style guide)
    }
    
    return colors.get(score, "#607D8B")  # Default to gray if score is invalid

def get_emoji_rating(score):
    """
    Returns a descriptive emoji and text rating based on the password strength score.
    
    Args:
        score (int): Password strength score (0-4)
        
    Returns:
        str: Rating text with emoji
    """
    ratings = {
        0: "😱 Very Weak",
        1: "😟 Weak",
        2: "😐 Medium",
        3: "😊 Strong",
        4: "🔒 Very Strong"
    }
    
    return ratings.get(score, "❓ Unknown")

def format_crack_time(seconds):
    """
    Formats seconds into a human-readable time format.
    
    Args:
        seconds (float): Time in seconds
        
    Returns:
        str: Formatted time string
    """
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return f"{seconds / 60:.1f} minutes"
    elif seconds < 86400:
        return f"{seconds / 3600:.1f} hours"
    elif seconds < 2592000:  # 30 days
        return f"{seconds / 86400:.1f} days"
    elif seconds < 31536000:  # 365 days
        return f"{seconds / 2592000:.1f} months"
    elif seconds < 315360000:  # 10 years
        return f"{seconds / 31536000:.1f} years"
    elif seconds < 3153600000:  # 100 years
        return f"{seconds / 31536000:.1f} years"
    else:
        return "centuries"
