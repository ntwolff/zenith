import usaddress
import hashlib

# TODO Refactor - extension of CustomerEvent

class FuzzyMatching:
    def __init__(self):
        pass

    def standardize_email(self, email):
        return email.lower()

    def standardize_ssn(self, ssn):
        return ssn.replace("-", "")

    def hash_ssn(self, ssn):
        return hash(ssn)

    def standardize_phone_number(self, phone_number):
        return phone_number.replace("-", "").replace(" ", "")

    def standardize_address(self, address):
        return " ".join([address.street, address.city, address.state, address.zip_code, address.country]
        ).replace(" ", "").lower()

    def hash_address(self, address):
        standardized_address = self.standardize_address(address)
        parsed_address = usaddress.tag(standardized_address)[0]

        street_hash = hashlib.sha256(parsed_address.get("AddressNumber", "").encode()).hexdigest()
        city_hash = hashlib.sha256(parsed_address.get("PlaceName", "").encode()).hexdigest()
        state_hash = hashlib.sha256(parsed_address.get("StateName", "").encode()).hexdigest()
        zip_hash = hashlib.sha256(parsed_address.get("ZipCode", "").encode()).hexdigest()

        composite_hash = street_hash + city_hash + state_hash + zip_hash
        fuzzy_match_hash = composite_hash[:16]

        return fuzzy_match_hash