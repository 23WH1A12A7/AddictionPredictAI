from app import app

if __name__ == "__main__":
    app.run()
else:
    # Vercel serverless handler
    app = app
