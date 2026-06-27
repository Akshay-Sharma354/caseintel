from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

def send_analysis_email(recipient_email: str, analysis: str, document_type: str):
    """Send analysis results via email using SendGrid with professional design"""
    
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    
    subject = f"CaseIntel Analysis - {document_type}"
    
    # Get icon based on document type
    icons = {
        "CONTRACT": "⚖️",
        "CASE": "🏛️",
        "COMPLIANCE": "✅",
        "NOTICE": "📋"
    }
    icon = icons.get(document_type.upper(), "🤖")
    
    html_content = f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    padding: 20px;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 650px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 40px 30px;
                    text-align: center;
                }}
                .header h1 {{
                    font-size: 32px;
                    margin-bottom: 10px;
                    font-weight: 700;
                }}
                .header p {{
                    font-size: 16px;
                    opacity: 0.95;
                    font-weight: 500;
                }}
                .content {{
                    padding: 40px 30px;
                }}
                .doc-type-badge {{
                    display: inline-block;
                    background: #f0f4ff;
                    color: #667eea;
                    padding: 12px 20px;
                    border-radius: 8px;
                    font-weight: 600;
                    margin-bottom: 30px;
                    font-size: 14px;
                    border: 2px solid #667eea;
                }}
                .section {{
                    margin-bottom: 30px;
                    padding: 25px;
                    background: #f9fafb;
                    border-radius: 8px;
                    border-left: 4px solid #667eea;
                }}
                .section-title {{
                    font-size: 16px;
                    font-weight: 700;
                    color: #1a1a1a;
                    margin-bottom: 15px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }}
                .analysis-text {{
                    color: #555;
                    font-size: 14px;
                    line-height: 1.8;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                    background: white;
                    padding: 15px;
                    border-radius: 6px;
                    border: 1px solid #e5e7eb;
                }}
                .cta-button {{
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white !important;
                    padding: 14px 32px;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: 600;
                    font-size: 14px;
                    margin-top: 20px;
                    transition: transform 0.2s;
                }}
                .cta-button:hover {{
                    transform: translateY(-2px);
                }}
                .footer {{
                    background: #f9fafb;
                    padding: 25px 30px;
                    border-top: 1px solid #e5e7eb;
                    text-align: center;
                    font-size: 12px;
                    color: #6b7280;
                }}
                .footer a {{
                    color: #667eea;
                    text-decoration: none;
                    font-weight: 600;
                }}
                .badge {{
                    display: inline-block;
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: 600;
                    margin-right: 8px;
                }}
                .badge-critical {{ background: #fee2e2; color: #991b1b; }}
                .badge-warning {{ background: #fef3c7; color: #92400e; }}
                .badge-success {{ background: #dcfce7; color: #166534; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{icon} CaseIntel Analysis</h1>
                    <p>Professional Legal Document Review</p>
                </div>
                
                <div class="content">
                    <div class="doc-type-badge">
                        📄 {document_type.upper()}
                    </div>
                    
                    <div class="section">
                        <div class="section-title">
                            📋 Analysis Results
                        </div>
                        <div class="analysis-text">{analysis}</div>
                    </div>
                    
                    <div style="margin-top: 30px;">
                        <a href="https://caseintel-rho.vercel.app/" class="cta-button">
                            View Full Analysis →
                        </a>
                    </div>
                </div>
                
                <div class="footer">
                    <p>This analysis was generated by <strong>CaseIntel</strong>, an AI-powered legal document analysis platform.</p>
                    <p style="margin-top: 12px;">
                        <a href="https://caseintel-rho.vercel.app/">Visit CaseIntel</a> | 
                        <a href="https://github.com/Akshay-Sharma354/caseintel">GitHub</a>
                    </p>
                    <p style="margin-top: 12px; opacity: 0.7;">© 2026 CaseIntel. All rights reserved.</p>
                </div>
            </div>
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
