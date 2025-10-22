from authentication.models import CustomUser

# Find all users with empty string phone numbers and set to None
users_with_empty_phone = CustomUser.objects.filter(phone_number='')
count = users_with_empty_phone.count()
print(f"Found {count} users with empty phone numbers")

if count > 0:
    users_with_empty_phone.update(phone_number=None)
    print(f"Updated {count} users to have NULL phone numbers")
else:
    print("No users to update")

# Show all users
print("\nAll users:")
for user in CustomUser.objects.all():
    print(f"  {user.username}: phone={user.phone_number}, email={user.email}")
