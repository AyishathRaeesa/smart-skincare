import re

# Detailed skincare recommendations with product info and image URLs
BASE_RECS = {
    "acne": [
        {
            "product": "Salicylic Acid Cleanser (0.5-2%)",
            "description": "Exfoliates inside pores to reduce acne and blackheads.",
            "image_url": "https://example.com/images/salicylic_acid_cleanser.jpg"
        },
        {
            "product": "Benzoyl Peroxide 2.5-5% (spot or wash)",
            "description": "Kills acne-causing bacteria and reduces inflammation.",
            "image_url": "https://example.com/images/benzoyl_peroxide.jpg"
        },
        {
            "product": "Adapalene 0.1% Gel (night)",
            "description": "A retinoid that helps clear acne and prevents new breakouts.",
            "image_url": "https://example.com/images/adapalene_gel.jpg"
        },
        {
            "product": "Niacinamide Serum 4-10%",
            "description": "Reduces inflammation, redness, and regulates oil production.",
            "image_url": "https://example.com/images/niacinamide_serum.jpg"
        },
        {
            "product": "Oil-free, Non-comedogenic Moisturizer",
            "description": "Keeps skin hydrated without clogging pores.",
            "image_url": "https://example.com/images/oil_free_moisturizer.jpg"
        },
    ],
    "pigment|hyperpigmentation|dark spots": [
        {
            "product": "Vitamin C Serum (10-20%)",
            "description": "Brightens skin and reduces melanin production to fade dark spots.",
            "image_url": "https://example.com/images/vitamin_c_serum.jpg"
        },
        {
            "product": "Niacinamide 4-10%",
            "description": "Helps lighten hyperpigmentation and strengthens skin barrier.",
            "image_url": "https://example.com/images/niacinamide_serum.jpg"
        },
        {
            "product": "Azelaic Acid 10-20%",
            "description": "Treats pigmentation, redness and evens skin tone.",
            "image_url": "https://example.com/images/azelaic_acid.jpg"
        },
        {
            "product": "Retinol 0.2-0.5% (night)",
            "description": "Speeds skin renewal to reduce pigmentation patches.",
            "image_url": "https://example.com/images/retinol.jpg"
        },
        {
            "product": "Broad-spectrum Sunscreen SPF 50+",
            "description": "Protects against UV rays to prevent worsening pigmentation.",
            "image_url": "https://example.com/images/sunscreen.jpg"
        }
    ],
    "wrinkle|aging|age": [
        {
            "product": "Retinol 0.2-0.5% (night, buffer as needed)",
            "description": "Boosts collagen and reduces wrinkles over time.",
            "image_url": "https://example.com/images/retinol.jpg"
        },
        {
            "product": "Peptide Serum",
            "description": "Supports skin repair and firmness.",
            "image_url": "https://example.com/images/peptide_serum.jpg"
        },
        {
            "product": "Hyaluronic Acid Serum",
            "description": "Deeply hydrates and plumps the skin.",
            "image_url": "https://example.com/images/hyaluronic_acid.jpg"
        },
        {
            "product": "Ceramide Moisturizer",
            "description": "Restores skin barrier and locks in moisture.",
            "image_url": "https://example.com/images/ceramide_moisturizer.jpg"
        },
        {
            "product": "Daily Sunscreen SPF 50+",
            "description": "Protects skin from photoaging caused by UV exposure.",
            "image_url": "https://example.com/images/sunscreen.jpg"
        }
    ],
    "eczema|dermatitis": [
        {
            "product": "Fragrance-Free Ceramide Moisturizer (thick)",
            "description": "Calms inflammation and restores skin barrier.",
            "image_url": "https://example.com/images/ceramide_moisturizer.jpg"
        },
        {
            "product": "Hydrocortisone 1% (short courses if advised)",
            "description": "Reduces inflammation; use under medical supervision.",
            "image_url": "https://example.com/images/hydrocortisone.jpg"
        },
        {
            "product": "Gentle, non-soap Cleanser",
            "description": "Avoids irritation while keeping skin clean.",
            "image_url": "https://example.com/images/gentle_cleanser.jpg"
        },
        {
            "product": "Occlusives (e.g., petrolatum) for flare areas",
            "description": "Helps lock moisture in and protect damaged skin.",
            "image_url": "https://example.com/images/petrolatum_ointment.jpg"
        }
    ],
    "psoriasis": [
        {
            "product": "Urea/Lactic Acid Keratolytics (hands/feet)",
            "description": "Softens thickened skin and scales.",
            "image_url": "https://example.com/images/urea_cream.jpg"
        },
        {
            "product": "Coal Tar or Salicylic Acid shampoos for scalp",
            "description": "Relieves scalp scaling and itching.",
            "image_url": "https://example.com/images/coal_tar_shampoo.jpg"
        },
        {
            "product": "Moisturize after bathing",
            "description": "Prevents dryness and cracking.",
            "image_url": "https://example.com/images/moisturizer.jpg"
        },
        {
            "product": "Daily Sunscreen SPF 50+",
            "description": "Protects sensitive skin from UV damage.",
            "image_url": "https://example.com/images/sunscreen.jpg"
        }
    ],
    "rosacea": [
        {
            "product": "Gentle, fragrance-free cleanser",
            "description": "Prevents irritation and redness flare-ups.",
            "image_url": "https://example.com/images/gentle_cleanser.jpg"
        },
        {
            "product": "Azelaic Acid 10-15%",
            "description": "Reduces redness and bumps.",
            "image_url": "https://example.com/images/azelaic_acid.jpg"
        },
        {
            "product": "Mineral Sunscreen SPF 50+",
            "description": "Prevents sun-induced flare-ups with physical blockers.",
            "image_url": "https://example.com/images/mineral_sunscreen.jpg"
        },
        {
            "product": "Avoid Triggers: Heat, Spicy Food, Alcohol",
            "description": "Lifestyle changes to reduce flare frequency.",
            "image_url": "https://example.com/images/avoid_triggers.jpg"
        }
    ],
    "vitiligo": [
        {
            "product": "Broad-spectrum Sunscreen SPF 50+",
            "description": "Protects depigmented patches from sun damage.",
            "image_url": "https://example.com/images/sunscreen.jpg"
        },
        {
            "product": "Gentle Ceramide Moisturizer",
            "description": "Keeps skin hydrated and maintains barrier function.",
            "image_url": "https://example.com/images/ceramide_moisturizer.jpg"
        },
        {
            "product": "Use Lightening or Repigmentation Therapies (consult doctor)",
            "description": "Medical treatments to manage vitiligo.",
            "image_url": "https://example.com/images/consult_doctor.jpg"
        }
    ],
    "melanoma|cancer|carcinoma": [
        {
            "product": "Regular Dermatology Screening",
            "description": "Essential for early detection and treatment.",
            "image_url": "https://example.com/images/dermatologist.jpg"
        },
        {
            "product": "Avoid Self-Treatment",
            "description": "Follow professional medical advice strictly.",
            "image_url": "https://example.com/images/medical_care.jpg"
        }
    ],
    "nail|onych": [
        {
            "product": "Protective Gloves for Wet Work",
            "description": "Prevents nail damage and infections.",
            "image_url": "https://example.com/images/protective_gloves.jpg"
        },
        {
            "product": "Barrier Creams",
            "description": "Moisturizes and protects nail skin.",
            "image_url": "https://example.com/images/barrier_cream.jpg"
        },
        {
            "product": "Dermatology Consult for Nail Therapy",
            "description": "Specialist treatment advice recommended.",
            "image_url": "https://example.com/images/consult_doctor.jpg"
        }
    ],
    "fung|tinea|ringworm|pityria": [
        {
            "product": "Topical Antifungal (Clotrimazole/Ketoconazole)",
            "description": "Treats fungal infections effectively.",
            "image_url": "https://example.com/images/antifungal_cream.jpg"
        },
        {
            "product": "Keep Area Dry; Avoid Occlusion",
            "description": "Prevents fungal growth environment.",
            "image_url": "https://example.com/images/dry_skin.jpg"
        },
        {
            "product": "Continue Treatment 2 Weeks After Clearing",
            "description": "Prevents recurrence of infection.",
            "image_url": "https://example.com/images/complete_treatment.jpg"
        }
    ],
    "ulcer|sjs|stevens|necrol|bullous": [
        {
            "product": "Fragrance-Free Gentle Cleanser",
            "description": "Cleanses without irritating sensitive skin.",
            "image_url": "https://example.com/images/gentle_cleanser.jpg"
        },
        {
            "product": "Thick Ceramide Moisturizer",
            "description": "Protects and restores the skin barrier.",
            "image_url": "https://example.com/images/ceramide_moisturizer.jpg"
        },
        {
            "product": "Barrier Repair Ointments (e.g., Petrolatum)",
            "description": "Creates protective layer to lock moisture and protect skin.",
            "image_url": "https://example.com/images/petrolatum_ointment.jpg"
        },
        {
            "product": "Broad-spectrum Sunscreen SPF 50+ (suitable for sensitive skin)",
            "description": "Prevents UV damage and worsens symptoms.",
            "image_url": "https://example.com/images/sunscreen.jpg"
        },
    ],
}

GENERIC_FALLBACK = [
    {
        "product": "Gentle Cleanser",
        "description": "Use twice daily to maintain clean skin without irritation.",
        "image_url": "https://example.com/images/gentle_cleanser.jpg"
    },
    {
        "product": "Ceramide Moisturizer",
        "description": "Supports skin barrier repair and hydration.",
        "image_url": "https://example.com/images/ceramide_moisturizer.jpg"
    },
    {
        "product": "Broad-spectrum Sunscreen SPF 50+",
        "description": "Essential daily protection from harmful UV rays.",
        "image_url": "https://example.com/images/sunscreen.jpg"
    }
]

def recommend_for_label(label: str):
    name = label.lower().strip()
    for pattern, recs in BASE_RECS.items():
        if re.search(pattern, name):
            return recs
    return GENERIC_FALLBACK

# Example usage:
if __name__ == "__main__":
    label = "bullous"
    recs = recommend_for_label(label)
    for rec in recs:
        print(f"Product: {rec['product']}")
        print(f"Description: {rec['description']}")
        print(f"Image URL: {rec['image_url']}\n")
