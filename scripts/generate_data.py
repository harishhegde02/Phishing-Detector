import pandas as pd
import random

# Templates for different attack patterns
data = [
    # Urgency + Fear
    ("Urgent: Your account will be locked in 1 hour if you don't verify.", 1, 0, 1, 0),
    ("Final warning: Security breach detected. Reset your password now.", 1, 0, 1, 0),
    ("Action Required: Unusual login attempt from Russia. Secure your account.", 1, 0, 1, 0),
    ("IMMEDIATE: Your subscription is cancelled. Pay now to avoid data loss.", 1, 0, 1, 0),
    ("Suspicious activity on your credit card. Verify recent transactions immediately.", 1, 0, 1, 0),
    
    # Authority + Impersonation
    ("Dear Employee, This is the CEO. Please wire $5000 to this account for a secret project.", 1, 1, 0, 1),
    ("Internal Memo: HR requires your SSN for the new benefits portal.", 0, 1, 0, 1),
    ("This is IT support. We need your password to fix your mailbox.", 0, 1, 0, 1),
    ("Hi, this is Mark from Finance. Can you send me the Q4 revenue report?", 0, 1, 0, 1),
    ("From the Office of the Director: Required security training documentation attached.", 0, 1, 0, 1),
    
    # Impersonation + Urgency
    ("Hi mom, I lost my phone. Can you send me some money for a new one?", 1, 0, 0, 1),
    ("Hey buddy, I'm stuck at the airport. Can you Zelle me $50 for a cab?", 1, 0, 0, 1),
    ("This is your Netflix account manager. Update payment to keep streaming.", 1, 0, 0, 1),
    ("Urgent message from your bank: Claim your reward now.", 1, 0, 0, 1),
    
    # Fear + Authority
    ("Your IRS tax return is overdue. Legal action will be taken.", 1, 1, 1, 0),
    ("Department of Justice: You are subpoenaed. View the case file here.", 1, 1, 1, 0),
    ("Police Dept: Unpaid traffic violation found. Pay or face arrest.", 1, 1, 1, 0),
    
    # Benign
    ("Hello, would you like to grab coffee next Tuesday?", 0, 0, 0, 0),
    ("You have a new voicemail. Listen here.", 0, 0, 0, 0),
    ("Meeting reminder: Weekly Sync at 10 AM.", 0, 0, 0, 0),
    ("Happy Birthday! Have a great day ahead.", 0, 0, 0, 0),
    ("Your order has been shipped. Track it here.", 0, 0, 0, 0),
    ("Don't forget the milk on your way home.", 0, 0, 0, 0),
    ("The project documentation has been updated on the wiki.", 0, 0, 0, 0),
    ("Can you review this pull request when you have a moment?", 0, 0, 0, 0),
    ("Hey, are we still on for the movie tonight?", 0, 0, 0, 0),
    ("Please find the attached agenda for tomorrow's meeting.", 0, 0, 0, 0),
]

# Multiply samples to have a decent starting point
# We'll add some noise/variation manually if needed, but for baseline this is fine.
df = pd.DataFrame(data * 10, columns=['text', 'urgency', 'authority', 'fear', 'impersonation'])

# Shuffle
df = df.sample(frac=1).reset_index(drop=True)

df.to_csv('data/raw/synthetic_data.csv', index=False)
print(f"Generated {len(df)} samples in data/raw/synthetic_data.csv")
