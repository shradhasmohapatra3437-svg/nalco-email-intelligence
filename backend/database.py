import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError

# Read connection string from environment (Railway will inject this automatically in production)
# Fallback to local SQLite file for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./nalco_emails.db")

# SQLite needs a specific configuration for multithreading in FastAPI
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Initialize SQLAlchemy core components
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Email ORM Model
class EmailModel(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    gmail_id = Column(String, unique=True, index=True, nullable=False)
    sender = Column(String, nullable=True)
    subject = Column(String, nullable=True)
    body_preview = Column(Text, nullable=True)
    category = Column(String, nullable=True)
    urgency = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    processed_at = Column(String, default=lambda: datetime.now().isoformat())

# Helper 1: Initialize the database tables
def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully via SQLAlchemy.")

# Helper 2: Save a new email (with duplicate checks)
def save_email(gmail_id, sender, subject, body, category, urgency, summary):
    db = SessionLocal()
    try:
        new_email = EmailModel(
            gmail_id=gmail_id,
            sender=sender,
            subject=subject,
            body_preview=body[:500],
            category=category,
            urgency=urgency,
            summary=summary
        )
        db.add(new_email)
        db.commit()
        print(f"Saved: {subject}")
    except IntegrityError:
        db.rollback()  # Rollback session on conflict
        print(f"Already exists, skipping: {subject}")
    finally:
        db.close()

# Helper 3: Fetch all emails (formatted as tuples for backward compatibility)
def get_all_emails():
    db = SessionLocal()
    try:
        emails = db.query(EmailModel).order_by(EmailModel.processed_at.desc()).all()
        # Convert SQLAlchemy objects to tuples to ensure main.py doesn't break
        return [
            (
                email.id,
                email.gmail_id,
                email.sender,
                email.subject,
                email.body_preview,
                email.category,
                email.urgency,
                email.summary,
                email.processed_at
            )
            for email in emails
        ]
    finally:
        db.close()

if __name__ == '__main__':
    init_db()
    