from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

from database import get_db
import models, security
from pydantic import BaseModel, EmailStr

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class OTPVerify(BaseModel):
    email: EmailStr
    otp_code: str

# Token validation dependency
def get_current_user(token: str = Depends(security.oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def generate_otp():
    return str(random.randint(100000, 999999))

def build_otp_html(otp_code: str, expire_minutes: int) -> str:
    """Returns a premium HTML email body for OTP verification."""
    digits = list(otp_code)
    digit_boxes = "".join([
        f'<td style="width:52px;height:64px;background:#1e293b;border:2px solid #3b82f6;border-radius:12px;'
        f'text-align:center;vertical-align:middle;font-size:32px;font-weight:800;color:#60a5fa;'
        f'font-family:monospace;letter-spacing:0;padding:0 4px;">{d}</td>'
        f'<td style="width:8px;"></td>'
        for d in digits
    ])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>GeoPredict Verification</title>
</head>
<body style="margin:0;padding:0;background:#020617;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#020617;padding:40px 0;">
    <tr>
      <td align="center">
        <table width="560" cellpadding="0" cellspacing="0" style="max-width:560px;width:100%;">

          <!-- Header -->
          <tr>
            <td align="center" style="padding-bottom:32px;">
              <table cellpadding="0" cellspacing="0">
                <tr>
                  <td style="background:linear-gradient(135deg,#1d4ed8,#4f46e5);border-radius:16px;padding:12px 28px;">
                    <span style="font-size:22px;font-weight:900;color:#fff;letter-spacing:-0.5px;">&#127760; GeoPredict</span>
                    <span style="font-size:11px;color:#93c5fd;display:block;text-align:center;letter-spacing:3px;margin-top:2px;">EARLY WARNING SYSTEM</span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Card -->
          <tr>
            <td style="background:linear-gradient(160deg,#0f172a 0%,#1e293b 100%);border-radius:24px;border:1px solid #1e3a5f;overflow:hidden;">

              <!-- Top accent bar -->
              <tr>
                <td style="height:4px;background:linear-gradient(90deg,#1d4ed8,#7c3aed,#06b6d4);"></td>
              </tr>

              <!-- Body -->
              <tr>
                <td style="padding:48px 48px 40px;">

                  <!-- Icon -->
                  <table cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
                    <tr>
                      <td style="background:rgba(59,130,246,0.15);border:1px solid rgba(59,130,246,0.3);border-radius:16px;padding:16px;width:56px;height:56px;text-align:center;vertical-align:middle;">
                        <span style="font-size:28px;">&#128274;</span>
                      </td>
                    </tr>
                  </table>

                  <!-- Title -->
                  <p style="margin:0 0 8px;font-size:28px;font-weight:800;color:#f1f5f9;line-height:1.2;">Verify Your Account</p>
                  <p style="margin:0 0 32px;font-size:15px;color:#94a3b8;line-height:1.6;">
                    Welcome to GeoPredict! Enter the verification code below to activate your account and gain access to the AI-powered landslide early warning dashboard.
                  </p>

                  <!-- OTP Digit Boxes -->
                  <table cellpadding="0" cellspacing="0" style="margin:0 0 32px;">
                    <tr>
                      {digit_boxes}
                    </tr>
                  </table>

                  <!-- Expiry notice -->
                  <table cellpadding="0" cellspacing="0" style="margin-bottom:36px;">
                    <tr>
                      <td style="background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.3);border-radius:10px;padding:12px 16px;">
                        <span style="font-size:13px;color:#fbbf24;">&#9203; </span>
                        <span style="font-size:13px;color:#fcd34d;font-weight:600;">This code expires in {expire_minutes} minutes.</span>
                        <span style="font-size:13px;color:#94a3b8;"> Do not share it with anyone.</span>
                      </td>
                    </tr>
                  </table>

                  <!-- Divider -->
                  <hr style="border:none;border-top:1px solid #1e3a5f;margin:0 0 28px;" />

                  <!-- Security note -->
                  <p style="margin:0;font-size:13px;color:#64748b;line-height:1.7;">
                    &#128737; If you did not create a GeoPredict account, you can safely ignore this email.
                    Someone may have entered your email address by mistake.
                  </p>

                </td>
              </tr>

            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td align="center" style="padding-top:28px;">
              <p style="margin:0 0 6px;font-size:13px;color:#334155;">GeoPredict &mdash; Predictive Intelligence for Landslide Disaster Prevention</p>
              <p style="margin:0;font-size:12px;color:#1e3a5f;">&#169; 2025 GeoPredict. All rights reserved.</p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

def send_otp_email(to_email: str, otp_code: str):
    """Sends OTP via SMTP with a rich HTML template. Falls back to console print."""
    smtp_pwd  = os.getenv("SMTP_PASSWORD", "")
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    expire_minutes = security.OTP_EXPIRE_MINUTES

    if smtp_pwd and smtp_pwd != "your_app_password" and smtp_user:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "🔐 GeoPredict — Your Verification Code"
            msg["From"]    = f"GeoPredict EWS <{smtp_user}>"
            msg["To"]      = to_email

            # Plain-text fallback
            plain = (
                f"Your GeoPredict verification code is: {otp_code}\n"
                f"Valid for {expire_minutes} minutes. Do not share this code."
            )
            msg.attach(MIMEText(plain, "plain"))

            # Rich HTML version
            html_body = build_otp_html(otp_code, expire_minutes)
            msg.attach(MIMEText(html_body, "html"))

            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(smtp_user, smtp_pwd)
                server.sendmail(smtp_user, to_email, msg.as_string())

            logger.info(f"OTP email sent successfully to {to_email}")

        except smtplib.SMTPAuthenticationError:
            logger.error(
                "SMTP Authentication failed! Your Gmail App Password is incorrect or not set.\n"
                "Fix: Go to myaccount.google.com → Security → 2-Step Verification → App passwords\n"
                f"Then update SMTP_PASSWORD in backend/.env"
            )
            # Still print OTP to console so dev work isn't blocked
            _print_otp_console(to_email, otp_code, expire_minutes)
        except Exception as e:
            logger.error(f"Failed to send OTP email to {to_email}: {e}")
            _print_otp_console(to_email, otp_code, expire_minutes)
    else:
        logger.warning(
            "SMTP_PASSWORD not configured in .env — printing OTP to console.\n"
            "To enable real emails, add your Gmail App Password to SMTP_PASSWORD in backend/.env"
        )
        _print_otp_console(to_email, otp_code, expire_minutes)

def _print_otp_console(to_email: str, otp_code: str, expire_minutes: int):
    print(f"\n{'='*50}")
    print(f"  📧  SIMULATED OTP EMAIL")
    print(f"{'='*50}")
    print(f"  To:      {to_email}")
    print(f"  Code:    {otp_code}")
    print(f"  Expires: {expire_minutes} minutes")
    print(f"{'='*50}\n")


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pass = security.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_pass, is_active=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate and assign OTP
    otp_code = generate_otp()
    expires = datetime.utcnow() + timedelta(minutes=security.OTP_EXPIRE_MINUTES)
    otp_entry = models.OTP(user_id=new_user.id, otp_code=otp_code, expires_at=expires, purpose="registration")
    db.add(otp_entry)
    
    # Initialize empty profile
    profile_entry = models.Profile(user_id=new_user.id)
    db.add(profile_entry)
    db.commit()

    # Send OTP email
    send_otp_email(new_user.email, otp_code)

    return {"message": "User registered successfully. Check email for OTP to activate account.", "email": new_user.email}

@router.post("/verify-otp")
def verify_otp(payload: OTPVerify, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    otp_entry = db.query(models.OTP).filter(
        models.OTP.user_id == user.id,
        models.OTP.otp_code == payload.otp_code
    ).first()

    if not otp_entry or otp_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    user.is_active = True
    db.delete(otp_entry)
    db.commit()

    return {"message": "Account successfully activated. You can now login."}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account not activated. Please verify OTP.")

    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email, "is_admin": user.is_admin}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer", "is_admin": user.is_admin}

@router.get("/me")
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "is_admin": current_user.is_admin, "is_active": current_user.is_active}
