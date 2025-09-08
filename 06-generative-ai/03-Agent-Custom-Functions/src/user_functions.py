import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Optional

# Directory for storing tickets
TICKETS_DIR = Path(__file__).parent.parent / "data" / "tickets"
TICKETS_DIR.mkdir(parents=True, exist_ok=True)

def submit_support_ticket(email_address: str, description: str, priority: str = "medium") -> str:
    """
    Submit a technical support ticket.
    
    Args:
        email_address: Customer's email address
        description: Detailed description of the issue
        priority: Ticket priority (low, medium, high, critical)
    
    Returns:
        JSON string with ticket submission confirmation
    """
    # Generate unique ticket number
    ticket_number = str(uuid.uuid4()).replace('-', '')[:8].upper()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create ticket content
    ticket_content = f"""Support Ticket: {ticket_number}
Submitted: {timestamp}
Priority: {priority.upper()}
Submitted by: {email_address}

Issue Description:
{description}

Status: Open
Assigned to: Support Team
"""
    
    # Save ticket to file
    file_name = f"ticket-{ticket_number}.txt"
    file_path = TICKETS_DIR / file_name
    file_path.write_text(ticket_content)
    
    # Return confirmation
    response = {
        "status": "success",
        "ticket_number": ticket_number,
        "message": f"Support ticket {ticket_number} has been submitted successfully. A support engineer will contact you at {email_address} within 24 hours.",
        "priority": priority,
        "timestamp": timestamp
    }
    
    return json.dumps(response)


def check_ticket_status(ticket_number: str) -> str:
    """
    Check the status of an existing support ticket.
    
    Args:
        ticket_number: The ticket number to check
    
    Returns:
        JSON string with ticket status information
    """
    # Look for ticket file
    file_name = f"ticket-{ticket_number.upper()}.txt"
    file_path = TICKETS_DIR / file_name
    
    if file_path.exists():
        content = file_path.read_text()
        
        # Extract status from content
        status = "Open"  # Default status
        if "Status:" in content:
            status_line = [line for line in content.split('\n') if line.startswith("Status:")][0]
            status = status_line.split(":", 1)[1].strip()
        
        response = {
            "status": "found",
            "ticket_number": ticket_number.upper(),
            "ticket_status": status,
            "message": f"Ticket {ticket_number.upper()} is currently {status}."
        }
    else:
        response = {
            "status": "not_found",
            "ticket_number": ticket_number.upper(),
            "message": f"No ticket found with number {ticket_number.upper()}. Please check the ticket number and try again."
        }
    
    return json.dumps(response)


def escalate_ticket(ticket_number: str, reason: str) -> str:
    """
    Escalate a support ticket to higher priority.
    
    Args:
        ticket_number: The ticket number to escalate
        reason: Reason for escalation
    
    Returns:
        JSON string with escalation confirmation
    """
    file_name = f"ticket-{ticket_number.upper()}.txt"
    file_path = TICKETS_DIR / file_name
    
    if file_path.exists():
        # Read current content
        content = file_path.read_text()
        
        # Add escalation note
        escalation_note = f"\n\nESCALATION: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nReason: {reason}\nPriority updated to: CRITICAL\n"
        
        # Update priority in content
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith("Priority:"):
                lines[i] = "Priority: CRITICAL"
                break
        
        # Write updated content
        updated_content = '\n'.join(lines) + escalation_note
        file_path.write_text(updated_content)
        
        response = {
            "status": "success",
            "ticket_number": ticket_number.upper(),
            "message": f"Ticket {ticket_number.upper()} has been escalated to CRITICAL priority. A senior engineer will review it immediately.",
            "escalation_reason": reason
        }
    else:
        response = {
            "status": "error",
            "ticket_number": ticket_number.upper(),
            "message": f"Cannot escalate: No ticket found with number {ticket_number.upper()}."
        }
    
    return json.dumps(response)


def get_knowledge_base_article(topic: str) -> str:
    """
    Retrieve a knowledge base article on a specific topic.
    
    Args:
        topic: The topic to search for
    
    Returns:
        JSON string with article content or search results
    """
    # Simulated knowledge base
    knowledge_base = {
        "password_reset": {
            "title": "How to Reset Your Password",
            "content": "1. Go to the login page\n2. Click 'Forgot Password'\n3. Enter your email address\n4. Check your email for reset instructions\n5. Follow the link to create a new password"
        },
        "vpn_setup": {
            "title": "VPN Configuration Guide",
            "content": "1. Download the VPN client from the company portal\n2. Install the application\n3. Enter server address: vpn.company.com\n4. Use your corporate credentials to log in\n5. Select your region and connect"
        },
        "email_setup": {
            "title": "Email Client Configuration",
            "content": "Server: mail.company.com\nPort: 993 (IMAP) / 587 (SMTP)\nSecurity: SSL/TLS\nUsername: your.email@company.com\nPassword: Your corporate password"
        },
        "printer_issues": {
            "title": "Common Printer Problems",
            "content": "1. Check printer is powered on and connected\n2. Verify correct printer is selected\n3. Clear print queue and try again\n4. Update printer drivers if needed\n5. Contact IT if issues persist"
        }
    }
    
    # Search for topic
    topic_lower = topic.lower()
    matching_articles = []
    
    for key, article in knowledge_base.items():
        if topic_lower in key or topic_lower in article['title'].lower():
            matching_articles.append({
                "id": key,
                "title": article['title'],
                "preview": article['content'][:100] + "..."
            })
    
    if matching_articles:
        # If exact match, return full article
        for key, article in knowledge_base.items():
            if key == topic_lower:
                return json.dumps({
                    "status": "found",
                    "article": article
                })
        
        # Otherwise return search results
        return json.dumps({
            "status": "search_results",
            "results": matching_articles,
            "message": f"Found {len(matching_articles)} article(s) related to '{topic}'"
        })
    else:
        return json.dumps({
            "status": "not_found",
            "message": f"No knowledge base articles found for '{topic}'. Please submit a support ticket for assistance."
        })