#User-facing message strings.
#Keyed by language code, then by message key.
#Falls back to English if a key is missing in another language

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
        "recommend_impersonation": "This website may be impersonating an official bank.",
        "never_share_otp": "Never share OTP or SMS verification codes.",
        "check_ssl": "Verify the SSL certificate before logging in.",
        "contact_bank": "Contact your bank using official channels if unsure.",

        # Report labels
        "table_scan_summary": "Scan Summary",
        "table_url_info": "URL Information",
        "table_connection": "Website Connection",
        "table_ssl": "SSL Certificate",
        "table_domain_info": "Domain Information",
        "table_bank_verification": "Official Domain Verification",
        "table_payment_verification": "Official Payment Processor Verification",
        "table_keywords": "Detected Keywords",
        "table_risk_analysis": "Risk Analysis",
        "table_recommendations": "Security Recommendations",

        "label_property": "Property",
        "label_value": "Value",
        "label_scan_time": "Scan Time",
        "label_risk_score": "Risk Score",
        "label_risk_level": "Risk Level",
        "label_recommendation": "Recommendation",
        "label_status": "Status",
        "label_bank": "Bank",
        "label_processor": "Processor",
        "label_official_domain": "Official Domain",
        "label_closest_domain": "Closest Domain",
        "label_similarity": "Similarity",
        "label_possible_impersonation": "Possible Impersonation",
        "label_field": "Field",
        "label_original_url": "Original URL",
        "label_protocol": "Protocol",
        "label_domain": "Domain",
        "label_path": "Path",
        "label_query": "Query",
        "label_fragment": "Fragment",
        "label_reachable": "Reachable",
        "label_http_status": "HTTP Status",
        "label_issuer": "Issuer",
        "label_expires": "Expires",
        "label_days_remaining": "Days Remaining",
        "label_whois_data": "WHOIS Data",
        "label_registrar": "Registrar",
        "label_created": "Created",
        "label_domain_age": "Domain Age",
        "label_security_check": "Security Check",
        "label_result": "Result",
        "label_keyword": "Keyword",
        "label_days_suffix": "days",
        "label_ssl_certificate": "SSL Certificate",
        "label_suspicious_tld": "Suspicious TLD",
        "label_detected_keywords": "Detected Keywords",
        "value_not_detected": "Not Detected",
        "value_detected": "Detected",
        "panel_security_score": "Security Score",

        # Result values
        "value_pass": "PASS",
        "value_fail": "FAIL",
        "value_warning": "WARNING",
        "value_not_checked": "Not Checked",
        "value_yes": "Yes",
        "value_no": "No",
        "value_none": "None",
        "value_available": "Available",
        "value_not_available": "Not Available",
        "value_valid": "Valid",
        "value_invalid": "Invalid",

        # Banner
        "banner_subtitle": "Cybersecurity URL Analysis Toolkit",
        "banner_status_ready": "Ready",

        # CLI prompts
        "prompt_enter_url": "Enter a website URL: "
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
        "recommend_impersonation": "Этот сайт может имитировать официальный банк.",
        "never_share_otp": "Никогда не сообщайте код подтверждения (OTP) или SMS-код.",
        "check_ssl": "Проверьте SSL-сертификат перед входом в систему.",
        "contact_bank": "Если сомневаетесь, свяжитесь с банком по официальным каналам.",

        # Report labels
        "table_scan_summary": "Сводка сканирования",
        "table_url_info": "Информация об URL",
        "table_connection": "Соединение с сайтом",
        "table_ssl": "SSL-сертификат",
        "table_domain_info": "Информация о домене",
        "table_bank_verification": "Проверка официального домена банка",
        "table_payment_verification": "Проверка официального платёжного сервиса",
        "table_keywords": "Обнаруженные ключевые слова",
        "table_risk_analysis": "Анализ рисков",
        "table_recommendations": "Рекомендации по безопасности",

        "label_property": "Параметр",
        "label_value": "Значение",
        "label_scan_time": "Время сканирования",
        "label_risk_score": "Оценка риска",
        "label_risk_level": "Уровень риска",
        "label_recommendation": "Рекомендация",
        "label_status": "Статус",
        "label_bank": "Банк",
        "label_processor": "Платёжный сервис",
        "label_official_domain": "Официальный домен",
        "label_closest_domain": "Ближайший домен",
        "label_similarity": "Схожесть",
        "label_possible_impersonation": "Возможная имитация",
        "label_field": "Поле",
        "label_original_url": "Исходный URL",
        "label_protocol": "Протокол",
        "label_domain": "Домен",
        "label_path": "Путь",
        "label_query": "Запрос",
        "label_fragment": "Фрагмент",
        "label_reachable": "Доступен",
        "label_http_status": "HTTP статус",
        "label_issuer": "Издатель",
        "label_expires": "Истекает",
        "label_days_remaining": "Осталось дней",
        "label_whois_data": "Данные WHOIS",
        "label_registrar": "Регистратор",
        "label_created": "Создан",
        "label_domain_age": "Возраст домена",
        "label_security_check": "Проверка безопасности",
        "label_result": "Результат",
        "label_keyword": "Ключевое слово",
        "label_days_suffix": "дней",
        "label_ssl_certificate": "SSL-сертификат",
        "label_suspicious_tld": "Подозрительный TLD",
        "label_detected_keywords": "Обнаруженные ключевые слова",
        "value_not_detected": "Не обнаружено",
        "value_detected": "Обнаружено",
        "panel_security_score": "Оценка безопасности",

        # Result values
        "value_pass": "ПРОЙДЕНО",
        "value_fail": "НЕ ПРОЙДЕНО",
        "value_warning": "ПРЕДУПРЕЖДЕНИЕ",
        "value_not_checked": "Не проверено",
        "value_yes": "Да",
        "value_no": "Нет",
        "value_none": "Нет",
        "value_available": "Доступно",
        "value_not_available": "Недоступно",
        "value_valid": "Действителен",
        "value_invalid": "Недействителен",

        # Banner
        "banner_subtitle": "Инструмент анализа URL для кибербезопасности",
        "banner_status_ready": "Готово",

        # CLI prompts
        "prompt_enter_url": "Введите URL сайта: "
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
        "recommend_impersonation": "Ushbu veb-sayt rasmiy bankka o'xshatilgan bo'lishi mumkin.",
        "never_share_otp": "OTP yoki SMS tasdiqlash kodini hech kimga bermang.",
        "check_ssl": "Tizimga kirishdan oldin SSL sertifikatini tekshiring.",
        "contact_bank": "Shubha bo'lsa, bank bilan rasmiy kanallar orqali bog'laning.",

        # Report labels
        "table_scan_summary": "Skanerlash xulosasi",
        "table_url_info": "URL haqida ma'lumot",
        "table_connection": "Veb-sayt ulanishi",
        "table_ssl": "SSL sertifikati",
        "table_domain_info": "Domen haqida ma'lumot",
        "table_bank_verification": "Rasmiy bank domeni tekshiruvi",
        "table_payment_verification": "Rasmiy to'lov tizimi tekshiruvi",
        "table_keywords": "Aniqlangan kalit so'zlar",
        "table_risk_analysis": "Xavf tahlili",
        "table_recommendations": "Xavfsizlik tavsiyalari",

        "label_property": "Xususiyat",
        "label_value": "Qiymat",
        "label_scan_time": "Skanerlash vaqti",
        "label_risk_score": "Xavf bahosi",
        "label_risk_level": "Xavf darajasi",
        "label_recommendation": "Tavsiya",
        "label_status": "Holat",
        "label_bank": "Bank",
        "label_processor": "To'lov tizimi",
        "label_official_domain": "Rasmiy domen",
        "label_closest_domain": "Eng yaqin domen",
        "label_similarity": "O'xshashlik",
        "label_possible_impersonation": "Mumkin bo'lgan taqlid",
        "label_field": "Maydon",
        "label_original_url": "Asl URL",
        "label_protocol": "Protokol",
        "label_domain": "Domen",
        "label_path": "Yo'l",
        "label_query": "So'rov",
        "label_fragment": "Fragment",
        "label_reachable": "Ochiq",
        "label_http_status": "HTTP holati",
        "label_issuer": "Beruvchi",
        "label_expires": "Amal qiladi",
        "label_days_remaining": "Qolgan kunlar",
        "label_whois_data": "WHOIS ma'lumotlari",
        "label_registrar": "Registrator",
        "label_created": "Yaratilgan",
        "label_domain_age": "Domen yoshi",
        "label_security_check": "Xavfsizlik tekshiruvi",
        "label_result": "Natija",
        "label_keyword": "Kalit so'z",
        "label_days_suffix": "kun",
        "label_ssl_certificate": "SSL sertifikati",
        "label_suspicious_tld": "Shubhali TLD",
        "label_detected_keywords": "Aniqlangan kalit so'zlar",
        "value_not_detected": "Aniqlanmadi",
        "value_detected": "Aniqlandi",
        "panel_security_score": "Xavfsizlik bahosi",

        # Result values
        "value_pass": "O'TDI",
        "value_fail": "O'TMADI",
        "value_warning": "OGOHLANTIRISH",
        "value_not_checked": "Tekshirilmagan",
        "value_yes": "Ha",
        "value_no": "Yo'q",
        "value_none": "Yo'q",
        "value_available": "Mavjud",
        "value_not_available": "Mavjud emas",
        "value_valid": "Yaroqli",
        "value_invalid": "Yaroqsiz",

        # Banner
        "banner_subtitle": "Kiberxavfsizlik URL tahlil vositasi",
        "banner_status_ready": "Tayyor",

        # CLI prompts
        "prompt_enter_url": "Veb-sayt URL manzilini kiriting: "
    }

}


def get_message(key, language="en"):

    language_messages = MESSAGES.get(language, MESSAGES["en"])

    if key in language_messages:
        return language_messages[key]

    return MESSAGES["en"].get(key, key)