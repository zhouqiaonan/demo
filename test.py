from address_normalizer import Address, extract_house_number

# Full normalization with house number extraction
addr = Address(
    address1="Grosse Straße 65",
    address2="Tür 5",
    country="DE",
    phone="+44 123-456/789",
    house_no="",
    contact_person="John Smith"
)
addr = Address(
    address1="Atlantik 1",
    address2="",
    country="DE",
    phone="",
    house_no="",
    contact_person="Yanran Dong"
)
addr.normalize()
print(f"address1: {addr.address1}")
print(f"address2: {addr.address2}")
print(f"company: {addr.company}")
print(f"house_no: {addr.house_no}")
print(f"phone: {addr.phone}")

# Standalone extraction
# street, number = extract_house_number("123 High Street", "GB")
# # street="High Street", number="123"
# print(f"street: {street}, number: {number}")
#
# # Disable extraction if not needed
# addr.normalize(extract_house_number=False)