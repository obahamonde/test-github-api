from typing import *
import asyncio
from aioboto3 import Session
from aiohttp.web import FileField
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pydantic import Field as Data  # pylint: disable=no-name-in-module

from ..config import credentials, env
from ..schemas import *

session = Session(**credentials)


class UploadRequest(BaseModel):
    """
    UploadRequest
        - key:str
        - size:int
        - user:str
        - file:FileField
    """

    key: str = Data(...)
    size: int = Data(...)
    user: str = Data(...)
    file: FileField = Data(...)

    class Config:
        arbitrary_types_allowed = True


EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Welcome to our Newsletter!</title>
    <style>
      /* Add your custom styles here */
    </style>
  </head>
  <body>
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto;">
      <tr>
        <td align="center" style="padding: 10px 0;">
          <h1 style="color: #008080;font-family: Arial, Helvetica, sans-serif;">Welcome to AioFauna!</h1>
          <p>Thank you for subscribing to our newsletter. We're excited to have you on board!</p>
        </td>
      </tr>
      <tr>
        <td align="center" style="padding: 10px 0;">
          <img src="https://aiofauna.netlify.app/logo.png" alt="Company Logo" style="max-width: 100px;">
        </td>
      </tr>
      <tr>
        <td align="center">
          <p>Stay tuned for the latest updates, news, and exclusive content.</p>
        </td>
      </tr>
      <tr>
        <td align="center" style="padding: 40px 0;">
          <a href="https://www.aiofauna.com/api/unsubscribe" style="text-decoration: none; color: #ffffff; background-color: #008080; padding: 10px 20px; border-radius: 4px;">Unsubscribe</a>
        </td>
      </tr>
    </table>
  </body>
</html>
"""


class Email(Chainable):
    """
    Email
        - to:str
        - subject:str
        - html:str
    """

    to: str = Data(...)
    subject: str = Data(...)
    html: str = Data(...)


class AmazonWebServices:
    """
    Amazon Web Services
    """

    async def upload(self, request: UploadRequest):
        """
        Upload Endpoint
        """
        key, size, user, file = request.key, request.size, request.user, request.file
        async with session.client("s3") as s3:  # type: ignore
            key_ = f"{key}/{file.filename}"  # type: ignore
            await s3.put_object(
                Bucket=env.AWS_S3_BUCKET,
                Key=key_,
                Body=file.file.read(),
                ContentType=file.content_type,
                ACL="public-read",
            )
            url = f"https://s3.amazonaws.com/{env.AWS_S3_BUCKET}/{key_}"
            response = await Upload(
                user=user,
                key=key_,
                name=file.filename,
                size=size,
                type=file.content_type,
                url=url,
            ).save()
            assert isinstance(response, Upload)
            return response

    async def verify_email(self, request: Email):
        """
        Verify Email Endpoint
        """
        async with session.client("ses", region_name="us-east-1") as ses:
            await ses.verify_email_identity(EmailAddress=request.to)
            return {
                "message": "Verification link sent successfully, please check your inbox."
            }

    async def send_email(self, request: Email):
        """
        Send Email Endpoint
        """
        async with session.client("ses", region_name="us-east-1") as ses:
            await ses.send_email(
                Source="oscar.bahamonde.dev@gmail.com",
                Destination={
                    "ToAddresses": [
                        request.to,
                    ],
                },
                Message={
                    "Subject": {
                        "Data": request.subject,
                    },
                    "Body": {
                        "Html": {
                            "Data": request.html,
                        }
                    },
                },
            )
            return {"message": "Email sent successfully, please check your inbox."}

    async def list_verified_emails(self):
        """
        List Verified Emails Endpoint
        """
        async with session.client("ses") as ses:
            response = await ses.list_identities(IdentityType="EmailAddress")
            return response["Identities"]

    async def suscribe(self, email: str):
        """
        Suscribe Endpoint
        """
        verified_emails = await self.list_verified_emails()
        is_verified = email in verified_emails
        if is_verified:
            await self.send_email(
                Email(
                    to=email, subject="Welcome to our Newsletter!", html=EMAIL_TEMPLATE
                )
            )
        else:
            await self.verify_email(
                Email(
                    to=email,
                )
            )
            while not is_verified:
                verified_emails = await self.list_verified_emails()
                is_verified = email in verified_emails
                await asyncio.sleep(1)

            await self.send_email(
                Email(
                    to=email, subject="Welcome to our Newsletter!", html=EMAIL_TEMPLATE
                )
            )
        return {"message": "Email suscribed successfully, please check your inbox."}

    async def unsubscribe(self, email: str):
        """
        Unsubscribe Endpoint
        """
        async with session.client("ses", region_name="us-east-1") as ses:
            await ses.delete_identity(Identity=email)
            return {"message": "Email unsubscribed successfully."}
