from setuptools import setup, find_packages

setup(
    name="moontrip-backend",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "pydantic==2.4.2",
        "python-multipart==0.0.6",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-dotenv==1.0.0",
        "firebase-admin==6.2.0",
        "google-cloud-storage==2.13.0",
        "google-cloud-firestore==2.13.1"
    ],
    python_requires=">=3.8",
) 