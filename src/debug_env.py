import os
import dotenv

# Path to .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
print(f"Loading .env from: {env_path}")

# Load env
loaded = dotenv.load_dotenv(dotenv_path=env_path, override=True)
print(f"dotenv.load_dotenv returned: {loaded}")

required_keys = [
    "AZURE_API_KEY",
    "AZURE_API_VERSION",
    "AZURE_API_ENDPOINT",
    "AZURE_DEPLOYMENT_NAME"
]

print("\n--- Environment Variable Check ---")
all_present = True
for key in required_keys:
    value = os.getenv(key)
    if value:
        # Mask the value for security
        masked_value = value[:4] + "*" * (len(value) - 8) + value[-4:] if len(value) > 8 else "****"
        print(f"✅ {key}: Found (Value: {masked_value})")
    else:
        print(f"❌ {key}: MISSING")
        all_present = False

if all_present:
    print("\nAll required Azure environment variables are set.")
else:
    print("\nSome variables are missing. Please check your src/.env file.")
