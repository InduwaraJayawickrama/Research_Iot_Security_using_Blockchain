from . import crypto_utils

# Alias functions for edge devices
generate_keys = crypto_utils.generate_ecdsa_keys
sign_data = crypto_utils.sign_data
encrypt_data = crypto_utils.encrypt_aes