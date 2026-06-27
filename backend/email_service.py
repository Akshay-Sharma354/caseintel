from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

def send_analysis_email(recipient_email: str, analysis: str, document_type: str):
    """Send analysis results via email using SendGrid"""
    
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    
    subject = f"CaseIntel Analysis - {document_type}"
    
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2>📄 CaseIntel Analysis Results</h2>
            <p><strong>Document Type:</strong> {document_type}</p>
            <hr>
            <div style="background: #f5f5f5; padding: 15px; border-radius: 5px;">
                {analysis}
            </div>
            <hr>
            <p style="color: #666; font-size: 12px;">
                Sent from <a href="https://caseintel-rho.vercel.app/">CaseIntel</a>
            </p>
        </body>
    </html>
    """
    
    message = Mail(
        from_email='akysha354@gmail.com',
        to_emails=recipient_email,
        subject=subject,
        html_content=html_content
    )
    
    try:
        response = sg.send(message)
        return {"success": True, "status": response.status_code}
    except Exception as e:
        return {"success": False, "error": str(e)}
