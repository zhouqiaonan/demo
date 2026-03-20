"""
Address Normalization Module for Django ERP System

Converts international shipping addresses to standardized, shortened formats
to meet carrier label constraints (35 character limit per field).

Includes intelligent house number extraction for carrier APIs that require
separate street and house number fields.

Usage:
    from address_normalizer import Address
    
    address = Address(
        address1="123 BUSINESS PARK ROAD",
        address2="Building 5",
        company="",
        country="GB",
        phone="+44 123-456/789",
        house_no="",
        contact_person="John Smith"
    )
    address.normalize()
    
    # Access normalized fields
    print(address.address1)   # Street name
    print(address.house_no)   # Extracted house number
"""

import re
from dataclasses import dataclass
from typing import Optional, Tuple


# =============================================================================
# CONFIGURATION
# =============================================================================

# Word replacement mappings by country type
WORD_REPLACEMENTS = {
    1: [  # UK (GB)
        ("ROAD", "Rd"),
        ("STREET", "St"),
        ("BUSINESS", "BUSI"),
        ("PARK", "PK"),
        ("Avenue", "Ave"),
        ("Company", "Co."),
        ("Department", "Dept."),
        ("Gymnasium", "GYM"),
        ("Headquarters", "HQ"),
        ("Limited", "Ltd."),
        ("Room", "rm"),
        ("Court", "ct"),
        ("University", "Univ"),
        ("Number", "No."),
        ("Building", "Bldg"),
        ("Floor", "Fl"),
        ("Drive", "Dr"),
        ("Lane", "Ln"),
        ("Tanjung", "Tg"),
        ("APARTMENT", "APT"),
    ],
    2: [  # FR, BE
        ("Appartement", "apt"),
        ("Bâtiment", "bat"),
        ("Batiment", "bat"),
        ("Résidence", "res"),
        ("Residence", "res"),
    ],
    3: [  # "IT", "ES", "PT"
    ], 
    4: [  # "DE", "NL", "AT", "LU"
        ("Straße", "Str."),
        ("Strasse", "Str.")
    ]
}

# Country groupings for processing rules
COUNTRY_GROUPS = {
    "UK": {"GB"},
    "FR_BE": {"FR", "BE"},
    "IT_ES_PT": {"IT", "ES", "PT"},
    "DE_NL_AT_LU": {"DE", "NL", "AT", "LU"},
}

# Countries where house number typically comes BEFORE street name
# e.g., "123 High Street", "45A Baker Street"
HOUSE_NUMBER_FIRST_COUNTRIES = {"GB", "US", "CA", "AU", "NZ", "IE"}

# Countries where house number typically comes AFTER street name
# e.g., "Hauptstrasse 123", "Rue de Paris 45"
HOUSE_NUMBER_LAST_COUNTRIES = {"DE", "NL", "AT", "LU", "CH", "BE", "FR", "IT", "ES", "PT", "PL", "CZ", "SE", "NO", "DK", "FI"}

# Maximum field length for carrier labels
MAX_FIELD_LENGTH = 35


# =============================================================================
# HOUSE NUMBER PATTERNS
# =============================================================================

# Pattern for house number at START of string (UK/US style)
# Matches: 123, 45A, 7b, 12-14, 10/12, 5-7A
HOUSE_NUMBER_START_PATTERN = re.compile(
    r'^(\d+[a-zA-Z]?(?:\s*[-–/]\s*\d+[a-zA-Z]?)?)\s+',
    re.IGNORECASE
)

# Pattern for house number at END of string (German/Dutch style)
# Matches: 123, 45A, 7b, 12-14, 10/12
# Requires either whitespace OR a dot before the number
HOUSE_NUMBER_END_PATTERN = re.compile(
    r'(?:\s+|\.(?=\d))(\d+[a-zA-Z]?(?:\s*[-–/]\s*\d+[a-zA-Z]?)?)$',
    re.IGNORECASE
)

# Patterns for number prefixes to clean up (N°, No., Nr., #)
# Captures the prefix and replaces with just the number
NUMBER_PREFIX_PATTERN = re.compile(
    r'\b(n[°ºo.]?\s*|no\.?\s*|nr\.?\s*|#\s*)(?=\d)',
    re.IGNORECASE
)


# =============================================================================
# ADDRESS CLASS
# =============================================================================

@dataclass
class Address:
    """
    Represents a shipping address with normalization capabilities.
    
    Handles country-specific address formatting rules and intelligent
    house number extraction for carrier APIs.
    """
    
    address1: str = ""
    address2: str = ""
    company: str = ""
    country: str = ""
    phone: str = ""
    house_no: str = ""
    contact_person: str = ""
    
    def __post_init__(self):
        """Ensure all string fields are never None."""
        self.address1 = self.address1 or ""
        self.address2 = self.address2 or ""
        self.company = self.company or ""
        self.country = (self.country or "").upper()
        self.phone = self.phone or ""
        self.house_no = self.house_no or ""
        self.contact_person = self.contact_person or ""
    
    def normalize(self, extract_house_number: bool = True) -> "Address":
        """
        Normalize the address based on country-specific rules.
        
        Args:
            extract_house_number: If True, extract house number from address1
                                  when house_no is empty.
        
        Returns:
            self for method chaining
        """
        # Trim address2
        self.address2 = self.address2.strip()
        
        # Clean phone: remove spaces, hyphens, slashes
        self.phone = re.sub(r"[\s\-/]", "", self.phone)
        
        # Apply country-specific rules (basic normalization, no aggressive spacing yet)
        if self.country in COUNTRY_GROUPS["UK"]:
            self._normalize_uk()
        elif self.country in COUNTRY_GROUPS["FR_BE"]:
            self._normalize_fr_be()
        elif self.country in COUNTRY_GROUPS["IT_ES_PT"]:
            self._normalize_it_es_pt()
        elif self.country in COUNTRY_GROUPS["DE_NL_AT_LU"]:
            self._normalize_de_nl_at_lu()
        else:
            # Unknown country: at least do basic spacing normalization
            self._normalize_spacing()
        
        # Extract house number AFTER basic normalization but BEFORE aggressive spacing
        if extract_house_number and not self.house_no.strip():
            self._extract_house_number()
        
        # Only apply aggressive spacing (removing spaces around punctuation) 
        # if fields exceed the max length - this is a last resort to fit carrier limits
        if len(self.address1) > MAX_FIELD_LENGTH:
            self.address1 = self._aggressive_clean_spacing(self.address1)
        if len(self.address2) > MAX_FIELD_LENGTH:
            self.address2 = self._aggressive_clean_spacing(self.address2)
        if len(self.company) > MAX_FIELD_LENGTH:
            self.company = self._aggressive_clean_spacing(self.company)
        
        return self
    
    # =========================================================================
    # HOUSE NUMBER EXTRACTION
    # =========================================================================
    
    def _extract_house_number(self) -> None:
        """
        Extract house number from address1 based on country conventions.
        
        - UK/US/AU style: Number at START ("123 High Street")
        - DE/NL/FR style: Number at END ("Hauptstrasse 123")
        
        Special handling for N°/No./Nr. prefixes which always indicate
        number-first format regardless of country.
        """
        if not self.address1:
            return
        
        # Check if address has a number prefix (N°, No., Nr., #)
        # These always indicate number-first format
        has_number_prefix = bool(NUMBER_PREFIX_PATTERN.search(self.address1))
        
        # Clean any number prefixes first (N°, No., Nr., #)
        self.address1 = NUMBER_PREFIX_PATTERN.sub('', self.address1).strip()
        
        # If we had a number prefix, try start extraction first
        if has_number_prefix:
            if self._extract_house_number_from_start():
                return
            self._extract_house_number_from_end()
        # Otherwise use country-based logic
        elif self.country in HOUSE_NUMBER_FIRST_COUNTRIES:
            self._extract_house_number_from_start()
        elif self.country in HOUSE_NUMBER_LAST_COUNTRIES:
            self._extract_house_number_from_end()
        else:
            # Unknown country: try end first (more common globally), then start
            if not self._extract_house_number_from_end():
                self._extract_house_number_from_start()
    
    def _extract_house_number_from_start(self) -> bool:
        """
        Extract house number from the beginning of address1.
        
        Examples:
            "123 High Street" -> house_no="123", address1="High Street"
            "45A Baker Street" -> house_no="45A", address1="Baker Street"
            "12-14 Main Road" -> house_no="12-14", address1="Main Road"
        
        Returns:
            True if extraction was successful
        """
        match = HOUSE_NUMBER_START_PATTERN.match(self.address1)
        if match:
            potential_number = match.group(1).strip()
            remaining = self.address1[match.end():].strip()
            
            # Only extract if there's a meaningful remaining street name
            if remaining and len(remaining) > 1:
                self.house_no = potential_number
                self.address1 = remaining
                return True
        
        return False
    
    def _extract_house_number_from_end(self) -> bool:
        """
        Extract house number from the end of address1.
        
        Examples:
            "Hauptstrasse 123" -> house_no="123", address1="Hauptstrasse"
            "Rue de Paris 45A" -> house_no="45A", address1="Rue de Paris"
            "Berliner Weg 10-12" -> house_no="10-12", address1="Berliner Weg"
            "Grosse Str.65" -> house_no="65", address1="Grosse Str."
        
        Returns:
            True if extraction was successful
        """
        match = HOUSE_NUMBER_END_PATTERN.search(self.address1)
        if match:
            potential_number = match.group(1).strip()
            # Get the part before the match
            remaining = self.address1[:match.start()].strip()
            
            # Check if the match was after a dot (no space case)
            # In that case, we need to keep the dot with the street name
            full_match = match.group(0)
            if full_match.startswith('.'):
                remaining = self.address1[:match.start() + 1].strip()  # Include the dot
            
            # Only extract if there's a meaningful remaining street name
            if remaining and len(remaining) > 1:
                self.house_no = potential_number
                self.address1 = remaining
                return True
        
        return False
    
    # =========================================================================
    # COUNTRY-SPECIFIC NORMALIZATION
    # =========================================================================
    
    def _normalize_uk(self) -> None:
        """UK (GB) specific normalization."""
        # 1. Apply word abbreviations
        self._apply_word_replacements(1)
        
        # 2-3. Normalize spacing
        self._normalize_spacing()
        
        # 4. Remove duplicate address2 if exact match
        if self.address1 == self.address2:
            self.address2 = ""
        
        # 5. If address1 is single word with digits, append address2
        words = self.address1.split()
        if len(words) == 1 and re.search(r"\d+", words[0]):
            self.address1 = f"{self.address1} {self.address2}".strip()
            self.address2 = ""
        
        # 6. If address1 > 35 and address2 empty, extract overflow to address2
        if len(self.address1) > MAX_FIELD_LENGTH and not self.address2:
            self._extract_overflow(target="address2")
    
    def _normalize_fr_be(self) -> None:
        """France (FR) and Belgium (BE) specific normalization."""
        # 1. Apply word abbreviations
        self._apply_word_replacements(2)
        
        # 2. Normalize spacing
        self._normalize_spacing()
        
        # 3. If address1 > 35 and company empty, extract overflow to company
        if len(self.address1) > MAX_FIELD_LENGTH and not self.company:
            self._extract_overflow(target="company")
    
    def _normalize_it_es_pt(self) -> None:
        """Italy (IT), Spain (ES), Portugal (PT) specific normalization."""
        # 1. Apply word abbreviations
        self._apply_word_replacements(3)
        
        # 2. Normalize spacing
        self._normalize_spacing()
        
        # 3. If company equals contact person (case-insensitive), clear company (remove duplicate)
        if self.company and self.contact_person and self.company.lower() == self.contact_person.lower():
            self.company = ""
        
        # 4. If address1 > 35 and company empty, extract overflow to company
        if not self.company and len(self.address1) > MAX_FIELD_LENGTH:
            self._extract_overflow(target="company")
    
    def _normalize_de_nl_at_lu(self) -> None:
        """Germany (DE), Netherlands (NL), Austria (AT), Luxembourg (LU) normalization."""
        # 1. Apply word abbreviations
        self._apply_word_replacements(4)
        
        # 2. If address2 is pure digits, it's likely a house number
        if self.address2.isdigit():
            if not self.house_no:
                self.house_no = self.address2
            self.address2 = ""
        
        # 3. If address1 == address2 (case-insensitive), clear address2 (remove duplicate)
        if self.address1 and self.address2 and self.address1.lower() == self.address2.lower():
            self.address2 = ""
        
        # 4. Normalize spacing
        self._normalize_spacing()
        
        # 5. If company > 35 chars, remove German company suffixes
        if len(self.company) > MAX_FIELD_LENGTH:
            self.company = re.sub(r"GmbH|&|Co\.?\s*KG", "", self.company, flags=re.IGNORECASE).strip()
            self.company = re.sub(r"\s{2,}", " ", self.company)
    
    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    
    def _apply_word_replacements(self, replacement_type: int) -> None:
        """Apply word abbreviations based on country type."""
        replacements = WORD_REPLACEMENTS.get(replacement_type, [])
        for long_word, short_word in replacements:
            pattern = re.compile(re.escape(long_word), re.IGNORECASE)
            self.address1 = pattern.sub(short_word, self.address1)
            self.address2 = pattern.sub(short_word, self.address2)
    
    def _normalize_spacing(self) -> None:
        """Normalize spacing in address fields."""
        self.address1 = self._clean_spacing(self.address1)
        self.address2 = self._clean_spacing(self.address2)
        self.company = self._clean_spacing(self.company)
    
    @staticmethod
    def _clean_spacing(text: str) -> str:
        """Clean spacing in a single string."""
        if not text:
            return text
        # Only collapse multiple spaces into one
        text = re.sub(r"\s{2,}", " ", text)
        return text.strip()
    
    @staticmethod
    def _aggressive_clean_spacing(text: str) -> str:
        """
        Aggressively clean spacing for fields that exceed length limits.
        Removes spaces around -, ,, . to save characters.
        """
        if not text:
            return text
        # Remove spaces around -, ,, .
        text = re.sub(r"\s*([-,.])\s*", r"\1", text)
        # Collapse multiple spaces
        text = re.sub(r"\s{2,}", " ", text)
        return text.strip()
    
    def _extract_overflow(self, target: str) -> None:
        """
        Extract overflow content from address1 when it exceeds MAX_FIELD_LENGTH.
        
        Tries in order:
        1. Content in parentheses ()
        2. Content after slash /
        3. Remove N°/n° prefixes
        4. Content after last comma
        """
        # Try parentheses extraction
        match = re.search(r"\(.*?\)", self.address1)
        if match:
            extracted = match.group()
            self.address1 = re.sub(r"\s*\(.*?\)\s*", " ", self.address1).strip()
            if extracted:
                self._set_field(target, extracted)
                return
        
        # Try slash extraction
        slash_idx = self.address1.find("/")
        if slash_idx != -1:
            extracted = self.address1[slash_idx + 1:].strip()
            self.address1 = self.address1[:slash_idx].strip()
            if extracted:
                self._set_field(target, extracted)
                return
        
        # Remove N°/n° prefixes
        if re.search(r"n[°ºo]", self.address1, re.IGNORECASE):
            self.address1 = re.sub(r"(?i)n[°ºo]\s*", "", self.address1).strip()
        
        # Try last comma extraction
        last_comma = self.address1.rfind(",")
        if last_comma != -1:
            extracted = self.address1[last_comma + 1:].strip()
            self.address1 = self.address1[:last_comma].strip()
            if extracted:
                self._set_field(target, extracted)
    
    def _set_field(self, field: str, value: str) -> None:
        """Set a field by name."""
        setattr(self, field, value)
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def to_dict(self) -> dict:
        """Return address fields as a dictionary."""
        return {
            "address1": self.address1,
            "address2": self.address2,
            "company": self.company,
            "country": self.country,
            "phone": self.phone,
            "house_no": self.house_no,
            "contact_person": self.contact_person,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Address":
        """Create an Address instance from a dictionary."""
        return cls(
            address1=data.get("address1", ""),
            address2=data.get("address2", ""),
            company=data.get("company", ""),
            country=data.get("country", ""),
            phone=data.get("phone", ""),
            house_no=data.get("house_no", ""),
            contact_person=data.get("contact_person", ""),
        )
    
    @classmethod
    def from_model(cls, instance) -> "Address":
        """Create an Address from a Django model instance."""
        return cls(
            address1=getattr(instance, "address1", "") or "",
            address2=getattr(instance, "address2", "") or "",
            company=getattr(instance, "company", "") or "",
            country=getattr(instance, "country", "") or "",
            phone=getattr(instance, "phone", "") or "",
            house_no=getattr(instance, "house_no", "") or getattr(instance, "houseNo", "") or "",
            contact_person=getattr(instance, "contact_person", "") or getattr(instance, "contactPerson", "") or "",
        )
    
    def update_model(self, instance) -> None:
        """Update a Django model instance with normalized address fields."""
        instance.address1 = self.address1
        instance.address2 = self.address2
        instance.company = self.company
        instance.phone = self.phone
        
        if hasattr(instance, "house_no"):
            instance.house_no = self.house_no
        elif hasattr(instance, "houseNo"):
            instance.houseNo = self.house_no


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def normalize_sale_order_address(sale_order, extract_house_number: bool = True) -> None:
    """
    Normalize address fields on a SaleOrder model instance in place.
    
    Args:
        sale_order: Django model instance with address fields
        extract_house_number: Whether to extract house number from address1
    """
    address = Address.from_model(sale_order)
    address.normalize(extract_house_number=extract_house_number)
    address.update_model(sale_order)


def extract_house_number(address_string: str, country: str = "") -> Tuple[str, str]:
    """
    Standalone function to extract house number from an address string.
    
    Args:
        address_string: Full address string
        country: ISO 2-letter country code (helps determine format)
    
    Returns:
        Tuple of (street_name, house_number)
    
    Examples:
        >>> extract_house_number("123 High Street", "GB")
        ('High Street', '123')
        
        >>> extract_house_number("Hauptstrasse 45A", "DE")
        ('Hauptstrasse', '45A')
    """
    addr = Address(address1=address_string, country=country)
    addr._extract_house_number()
    return addr.address1, addr.house_no


# =============================================================================
# DJANGO MODEL MIXIN
# =============================================================================

class AddressNormalizationMixin:
    """
    Mixin for Django models that need address normalization.
    
    Usage:
        class MySaleOrder(AddressNormalizationMixin, models.Model):
            address1 = models.CharField(max_length=100)
            address2 = models.CharField(max_length=100, blank=True)
            company = models.CharField(max_length=100, blank=True)
            country = models.CharField(max_length=2)
            phone = models.CharField(max_length=50)
            house_no = models.CharField(max_length=20, blank=True)
            contact_person = models.CharField(max_length=100, blank=True)
            
            def save(self, *args, **kwargs):
                self.normalize_address()
                super().save(*args, **kwargs)
    """
    
    def normalize_address(self, extract_house_number: bool = True) -> None:
        """Normalize address fields on this model instance."""
        normalize_sale_order_address(self, extract_house_number=extract_house_number)