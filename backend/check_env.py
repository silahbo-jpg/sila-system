from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    
    print("Environment Variables Check:")
    print("=" * 80)
    
    # Database
    print("\n[Database]")
    print(f"DATABASE_URL: {'Set' if os.getenv('DATABASE_URL') else 'Not set'}")
    
    # Environment
    print("\n[Environment]")
    print(f"ENVIRONMENT: {os.getenv('ENVIRONMENT', 'Not set')}")
    
    # Security
    print("\n[Security]")
    print(f"SECRET_KEY_PLACEHOLDER: {'Set' if os.getenv('SECRET_KEY_PLACEHOLDER') else 'Not set'}")
    
    # API Keys
    print("\n[External Services]")
    print(f"SOME_API_KEY: {'Set' if os.getenv('SOME_API_KEY') else 'Not set'}")
    
    print("\n" + "=" * 80)
    print("Environment check completed.")

if __name__ == "__main__":
    main()

