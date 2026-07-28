from typing import Optional

INDUSTRIES = {
    "all": {
        "label": "All Industries",
        "emoji": "🌐",
        "subreddits": ["smallbusiness", "entrepreneur", "Entrepreneur", "automation", "business", "operations", "productivity", "nocode", "zapier"],
        "keywords": ["founder", "small business", "manual work", "workflow", "operations", "automation", "sop", "burnout", "delegation", "process", "efficiency", "outsourcing", "scaling", "smb", "systems", "bottleneck", "overhead", "admin", "repetitive", "streamline"],
        "pain_signals": ["drowning", "nightmare", "frustrated", "killing me", "overwhelmed", "burned out", "exhausted", "lost clients", "losing money", "can't scale", "manually", "by hand", "takes forever", "tedious", "worn out", "stretched thin", "can't keep up", "doing everything myself"],
        "yt_queries": ["small business automation 2025", "founder burnout entrepreneur", "business operations systems", "workflow automation small business"],
        "bsky_queries": ["small business automation", "founder burnout", "business operations", "workflow automation SMB"],
    },
    "wellness": {
        "label": "Wellness",
        "emoji": "🧘",
        "subreddits": ["smallbusiness", "entrepreneur", "personaltraining", "yoga", "massage", "fitness", "crossfit"],
        "keywords": ["yoga studio", "gym", "wellness", "personal trainer", "massage therapist", "spa", "fitness studio", "instructor", "class scheduling", "membership", "booking", "no-show", "client retention", "pilates", "crossfit owner"],
        "pain_signals": ["no-show", "cancellation", "filling classes", "membership dropped", "overbooked", "retention problem", "booking system", "can't keep clients", "burned out trainer"],
        "yt_queries": ["yoga studio owner problems 2025", "fitness studio management challenges", "gym owner burnout", "wellness business operations struggles"],
        "bsky_queries": ["yoga studio owner", "fitness business owner", "gym owner", "wellness entrepreneur problems"],
    },
    "healthcare": {
        "label": "Healthcare Admin",
        "emoji": "🏥",
        "subreddits": ["medicine", "nursing", "smallbusiness", "HealthIT", "Dentistry", "medicaloffice"],
        "keywords": ["medical practice", "dental office", "clinic", "ehr", "billing", "insurance", "patient scheduling", "hipaa", "prior auth", "prior authorization", "administrative burden", "medical billing", "copay", "referral"],
        "pain_signals": ["prior authorization", "insurance denied", "billing nightmare", "staffing shortage", "administrative burden", "documentation overload", "patient no-show", "claim denied", "credentialing", "ehr frustration"],
        "yt_queries": ["medical office management problems 2025", "healthcare admin burnout", "dental practice management challenges", "medical billing nightmare"],
        "bsky_queries": ["medical practice management", "healthcare admin", "dental office owner", "prior authorization nightmare"],
    },
    "restaurant": {
        "label": "Restaurant & Hospitality",
        "emoji": "🍽️",
        "subreddits": ["restaurantowners", "KitchenConfidential", "bartenders", "smallbusiness", "Entrepreneur"],
        "keywords": ["restaurant", "cafe", "hospitality", "kitchen", "chef", "front of house", "inventory", "pos system", "food cost", "staffing", "server", "line cook", "catering", "bar owner", "menu costing"],
        "pain_signals": ["staff turnover", "can't find staff", "food waste", "margins too thin", "labor cost", "food cost out of control", "quit without notice", "understaffed", "overworked kitchen"],
        "yt_queries": ["restaurant owner problems 2025", "restaurant management challenges", "food service burnout", "hospitality staffing crisis"],
        "bsky_queries": ["restaurant owner", "chef owner problems", "hospitality burnout", "food service management"],
    },
    "legal": {
        "label": "Legal (Solo/Small Firm)",
        "emoji": "⚖️",
        "subreddits": ["Lawyertalk", "smallbusiness", "LegalAdvice", "Entrepreneur"],
        "keywords": ["law firm", "solo attorney", "paralegal", "legal billing", "case management", "billable hours", "client intake", "document management", "court deadline", "discovery", "solo practitioner", "small firm"],
        "pain_signals": ["non-billable time", "chasing invoices", "client ghosting", "document chaos", "overwhelmed with cases", "time tracking nightmare", "admin eating my day", "can't get paid"],
        "yt_queries": ["solo lawyer practice management 2025", "law firm automation", "legal admin problems", "attorney burnout small firm"],
        "bsky_queries": ["solo attorney problems", "law firm management", "legal billing frustration", "attorney burnout"],
    },
    "realestate": {
        "label": "Real Estate",
        "emoji": "🏠",
        "subreddits": ["realtors", "PropertyManagement", "RealEstate", "landlord", "smallbusiness"],
        "keywords": ["realtor", "property management", "landlord", "tenant", "listing", "crm", "lead generation", "commission", "showing", "property manager", "rental", "eviction", "maintenance request"],
        "pain_signals": ["tenant issues", "chasing rent", "vacancy problem", "maintenance nightmare", "lead follow-up", "can't keep up with showings", "eviction process", "paperwork overload", "manual tracking"],
        "yt_queries": ["real estate agent problems 2025", "property management challenges", "realtor burnout", "real estate business systems"],
        "bsky_queries": ["realtor problems", "property management frustration", "real estate business", "landlord issues"],
    },
    "trades": {
        "label": "Trades & Contractors",
        "emoji": "🔧",
        "subreddits": ["Plumbing", "electricians", "HVAC", "Construction", "smallbusiness", "Entrepreneur"],
        "keywords": ["contractor", "plumber", "electrician", "hvac", "handyman", "scheduling", "invoicing", "job costing", "field service", "service business", "dispatch", "estimate", "service call", "crew management"],
        "pain_signals": ["scheduling nightmare", "chasing payment", "customers ghosting", "labor shortage", "material costs", "overbooked", "can't scale crews", "invoicing chaos", "no-show customer"],
        "yt_queries": ["contractor business problems 2025", "trades business management", "field service management challenges", "plumbing business owner burnout"],
        "bsky_queries": ["contractor business owner", "trades business problems", "electrician business owner", "hvac business management"],
    },
    "retail": {
        "label": "Retail & Boutique",
        "emoji": "🛍️",
        "subreddits": ["retailbusiness", "smallbusiness", "ecommerce", "Entrepreneur"],
        "keywords": ["retail", "boutique", "inventory management", "pos", "brick and mortar", "shopify", "e-commerce", "customer returns", "shrinkage", "foot traffic", "seasonal", "retail store"],
        "pain_signals": ["shrinkage", "returns nightmare", "foot traffic down", "margins too thin", "online competition killing", "inventory nightmare", "shoplifting", "can't compete with amazon", "slow season"],
        "yt_queries": ["retail store owner problems 2025", "boutique owner challenges", "small retail business management", "brick and mortar struggles"],
        "bsky_queries": ["retail store owner", "boutique owner problems", "small retail business", "brick and mortar"],
    },
}

GLOBAL_PAIN_PHRASES = [
    "can't keep up", "drowning in", "nightmare", "so frustrated", "killing me",
    "too much to handle", "overwhelmed", "burned out", "exhausted",
    "losing money", "can't scale", "manually", "by hand", "takes forever",
    "so tedious", "hate doing this", "sick of", "fed up", "time consuming",
    "not sustainable", "breaking point", "stretched thin", "wearing too many hats",
    "do everything myself", "can't afford to hire", "understaffed",
    "staff quit", "chasing payment", "nobody shows up", "wasted hours",
]


def detect_pain_signal(text: str) -> Optional[str]:
    text_lower = text.lower()
    for phrase in GLOBAL_PAIN_PHRASES:
        if phrase in text_lower:
            return phrase
    return None


def get_industry(key: str) -> dict:
    return INDUSTRIES.get(key, INDUSTRIES["all"])
