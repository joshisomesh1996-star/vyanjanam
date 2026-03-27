# utils/emails.py

import smtplib
import ssl
from email.message import EmailMessage
from typing import List, Optional
import mimetypes
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class EmailSender:
    """
    Low-level email sender using SMTP (Gmail by default)
    """

    def __init__(
        self,
        smtp_server: str,
        port: int,
        username: str,
        password: str,
        use_tls: bool = True,
    ):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls

    def send_email(
        self,
        subject: str,
        body: str,
        to_emails: List[str] | str,
        from_email: Optional[str] = None,
        html: bool = False,
        attachments: Optional[List[str]] = None,
    ) -> None:
        """
        Send an email
        """

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = from_email or self.username

        if isinstance(to_emails, list):
            msg["To"] = ", ".join(to_emails)
        else:
            msg["To"] = to_emails

        # Content
        msg.set_content(body, subtype="html" if html else "plain")

        # Attachments (optional)
        if attachments:
            for file_path in attachments:
                if not os.path.isfile(file_path):
                    raise FileNotFoundError(f"Attachment not found: {file_path}")

                mime_type, _ = mimetypes.guess_type(file_path)
                mime_type = mime_type or "application/octet-stream"
                maintype, subtype = mime_type.split("/", 1)

                with open(file_path, "rb") as f:
                    msg.add_attachment(
                        f.read(),
                        maintype=maintype,
                        subtype=subtype,
                        filename=os.path.basename(file_path),
                    )

        # Secure connection
        context = ssl.create_default_context()

        # Send email
        if self.use_tls:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls(context=context)
                server.login(self.username, self.password)
                server.send_message(msg)
        else:
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
                server.login(self.username, self.password)
                server.send_message(msg)


# ==============================
# 🔥 TEST BLOCK
# ==============================
if __name__ == "__main__":

    sender = EmailSender(
        smtp_server="smtp.gmail.com",
        port=587,
        username=os.getenv("EMAIL"),
        password=os.getenv("EMAIL_PWD"),
        use_tls=True
    )

    sender.send_email(
        subject="🚀 Test Email from Vyanjanam",
        body="Your email system is working correctly!",
        to_emails=os.getenv("EMAIL")  # send to yourself
    )

    print("✅ Test email sent successfully")