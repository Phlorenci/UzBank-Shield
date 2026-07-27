MESSAGES = {

    "en": {
        # Validation
        "invalid_url": "Invalid URL format.",
        "empty_url": "URL cannot be empty.",

        # Verification
        "verified": "Official bank domain verified.",
        "not_verified": "Domain not found in the official database.",
        "unknown": "Unknown",

        # Recommendations
        "recommend_verified": "This website matches an official bank domain.",
        "recommend_unverified": "This domain is not present in the official database.",
        "never_share_otp": "Never share OTP or SMS verification codes.",
        "check_ssl": "Verify the SSL certificate before logging in.",
        "contact_bank": "Contact your bank using official channels if unsure."
    },

    "ru": {
        # Validation
        "invalid_url": "Неверный формат URL.",
        "empty_url": "URL не может быть пустым.",

        # Verification
        "verified": "Официальный домен банка подтверждён.",
        "not_verified": "Домен не найден в официальной базе данных.",
        "unknown": "Неизвестно",

        # Recommendations
        "recommend_verified": "Этот сайт соответствует официальному домену банка.",
        "recommend_unverified": "Этот домен отсутствует в официальной базе данных.",
        "never_share_otp": "Никогда не сообщайте код подтверждения (OTP) или SMS-код.",
        "check_ssl": "Проверьте SSL-сертификат перед входом в систему.",
        "contact_bank": "Если сомневаетесь, свяжитесь с банком по официальным каналам."
    },

    "uz": {
        # Validation
        "invalid_url": "URL formati noto'g'ri.",
        "empty_url": "URL bo'sh bo'lishi mumkin emas.",

        # Verification
        "verified": "Bankning rasmiy domeni tasdiqlandi.",
        "not_verified": "Domen rasmiy ma'lumotlar bazasida topilmadi.",
        "unknown": "Noma'lum",

        # Recommendations
        "recommend_verified": "Ushbu veb-sayt rasmiy bank domeniga mos keladi.",
        "recommend_unverified": "Ushbu domen rasmiy ma'lumotlar bazasida mavjud emas.",
        "never_share_otp": "OTP yoki SMS tasdiqlash kodini hech kimga bermang.",
        "check_ssl": "Tizimga kirishdan oldin SSL sertifikatini tekshiring.",
        "contact_bank": "Shubha bo'lsa, bank bilan rasmiy kanallar orqali bog'laning."
    }

}


def get_message(key, language="en"):
    language_messages = MESSAGES.get(language, MESSAGES["en"])

    if key in language_messages:
        return language_messages[key]

    return MESSAGES["en"].get(key, key)