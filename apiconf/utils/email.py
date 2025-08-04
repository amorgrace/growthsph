from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from apiconf.models import UserWallet

def send_withdrawal_email(user, network, amount, address):
    try:
        wallet = UserWallet.objects.get(user=user, network=network)
        address = wallet.address
    except UserWallet.DoesNotExist:
        address = "Not Available"

    subject = 'Withdrawal Request - Pending Approval'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [user.email, settings.ADMIN_EMAIL]

    text_content = (
        f"User: {user.email or user.username}\n"
        f"Network: {network}\n"
        f"Address: {address}\n"
        f"Amount: {amount}\n"
        f"Status: Pending"
    )

    html_content = f"""
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <style>
        body {{
          margin: 0;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          background: #f9f9f9;
          color: #333;
        }}
        .wrapper {{
          max-width: 600px;
          margin: 40px auto;
          background: #fff;
          border-radius: 10px;
          box-shadow: 0 4px 12px rgba(0,0,0,0.05);
          overflow: hidden;
        }}
        .header {{
          background: #111827;
          color: #fff;
          padding: 20px 30px;
          text-align: center;
        }}
        .logo {{
          margin-bottom: 10px;
        }}
        .logo img {{
          height: 60px;
        }}
        .header h1 {{
          margin: 0;
          font-size: 22px;
          letter-spacing: 0.5px;
        }}
        .content {{
          padding: 30px;
        }}
        .row {{
          margin-bottom: 15px;
        }}
        .label {{
          font-weight: 600;
          display: inline-block;
          width: 100px;
        }}
        .value {{
          display: inline-block;
        }}
        .status {{
          display: inline-block;
          background: #f59e0b;
          color: #fff;
          padding: 5px 10px;
          border-radius: 5px;
          font-weight: 600;
        }}
        .footer {{
          background: #f3f4f6;
          text-align: center;
          padding: 20px;
          font-size: 14px;
          color: #555;
        }}
        @media only screen and (max-width: 600px) {{
          .content, .header {{
            padding: 20px;
          }}
          .label {{
            width: auto;
            display: block;
            margin-bottom: 5px;
          }}
        }}
      </style>
    </head>
    <body>
      <div class="wrapper">
        <div class="header">
          <div class="logo">
            <img src="https://img.icons8.com/?size=100&id=6U-iMUbTRTf-&format=png&color=000000" alt="Logo">
          </div>
          <h1>Withdrawal Request</h1>
        </div>
        <div class="content">
          <div class="row"><span class="label">User:</span><span class="value">{user.email or user.username}</span></div>
          <div class="row"><span class="label">Network:</span><span class="value">{network}</span></div>
          <div class="row"><span class="label">Address:</span><span class="value">{address}</span></div>
          <div class="row"><span class="label">Amount:</span><span class="value">{amount}</span></div>
          <div class="row"><span class="label">Status:</span><span class="status">Pending</span></div>
        </div>
        <div class="footer">
          This is an automated message. Do not reply.
        </div>
      </div>
    </body>
    </html>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
