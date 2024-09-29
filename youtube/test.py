import hashlib
import random

# Initialize variables
userid = "12345"  # Replace with actual user id
amount = "100.00"  # Replace with actual amount
MERCHANT_KEY = "QQjxu1"
SALT = "JQrrQBzBX00C20geb509nnb1r0zDbCfr"
txnid = f"TXNKAD{random.randint(0, 1000)}_{userid}"
productInfo = "Txn For Product #1122"
firstname = f"User_{random.randint(1000, 9999)}"  # Using random for uniqueness
email = "onlineservice1542@gmail.com"
phone = "9865452575"

# Generate hash
hash_string = f"{MERCHANT_KEY}|{txnid}|{amount}|{productInfo}|{firstname}|{email}|1/{userid}||||||||||{SALT}"
hash_string = hash_string.lower()
hash = hashlib.sha512(hash_string.encode()).hexdigest()

# Prepare form data
form_data = {
    "key": MERCHANT_KEY,
    "hash": hash,
    "txnid": txnid,
    "amount": amount,
    "productinfo": productInfo,
    "firstname": firstname,
    "email": email,
    "phone": phone,
    "mobile": phone,
    "surl": "https://abcdsf/admin/dashbard/payments/payu/pgResponse.php",
    "furl": "https://aabcd/admin/dashboard/wallet.php",
    "udf1": userid,
    "service_provider": "payu_paisa"
}

# Construct form submission in Python (optional)
# This would typically be used in a web framework or when submitting forms programmatically
form_submit = """
<html>
<head><title>Redirecting...</title></head>
<body>
<h1 style="color:red; text-align:center;">Please wait, we are redirecting you to the payment page...</h1>
<form action="https://secure.payu.in/_payment" method="post" name="payuForm">
""" + "\n".join(f'<input type="hidden" name="{key}" value="{value}">' for key, value in form_data.items()) + """
<script>
document.payuForm.submit();
</script>
</form>
</body>
</html>
"""

print(form_submit)  # Output the form submission HTML (can be used in a web context)
