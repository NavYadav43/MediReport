# reports/medical_knowledge.py
# WHO/NIH standard medical knowledge base

PARAMETERS = {

    # ── BLOOD (CBC) ──────────────────────────────────────────────
    "hemoglobin": {
        "unit": "g/dL", "category": "blood",
        "aliases": ["hb", "hgb", "haemoglobin"],
        "normal": (12.0, 17.5),
        "low_advice": {
            "name": "Low Hemoglobin (Anemia)",
            "medications": [
                {"name": "Ferrous Sulfate", "purpose": "Iron supplement for anemia", "note": "Take with Vitamin C. Consult doctor first."},
                {"name": "Folic Acid", "purpose": "For folate deficiency anemia", "note": "Prescription required."},
            ],
            "precautions": [
                {"title": "Avoid Strenuous Exercise", "description": "Low hemoglobin reduces oxygen. Avoid heavy workouts."},
                {"title": "Watch for Dizziness", "description": "Sit or lie down if dizzy to avoid falls."},
            ],
            "prevention": [
                {"title": "Iron-Rich Diet", "description": "Eat spinach, lentils, red meat, beans, and fortified cereals."},
                {"title": "Vitamin C with Meals", "description": "Pair iron-rich foods with citrus for better absorption."},
            ],
            "lifestyle": [{"category": "Diet", "advice": "Include spinach, lentils, chicken liver, and fortified cereals daily."}],
            "doctor_signs": ["Extreme fatigue", "Shortness of breath at rest", "Chest pain or palpitations", "Pale or yellowish skin"],
        },
        "high_advice": {
            "name": "High Hemoglobin (Polycythemia)",
            "medications": [
                {"name": "Hydroxyurea", "purpose": "Reduces excess red blood cells (specialist only)", "note": "Never self-medicate. Doctor prescription required."},
            ],
            "precautions": [
                {"title": "Stay Hydrated", "description": "Drink 2-3 liters of water daily to thin the blood."},
                {"title": "Avoid High Altitudes", "description": "High altitude worsens this condition temporarily."},
            ],
            "prevention": [
                {"title": "Quit Smoking", "description": "Smoking raises hemoglobin. Quitting helps normalize it."},
                {"title": "Stay Hydrated", "description": "Adequate water intake keeps blood viscosity normal."},
            ],
            "lifestyle": [{"category": "Exercise", "advice": "Light aerobic activity helps circulation. Avoid extreme exertion."}],
            "doctor_signs": ["Severe headache", "Vision problems", "Redness in face/hands", "Unexplained itching after shower"],
        },
    },

    "wbc": {
        "unit": "cells/µL", "category": "blood",
        "aliases": ["white blood cells", "leukocytes", "tlc", "wbc count"],
        "normal": (4000, 11000),
        "low_advice": {
            "name": "Low WBC (Leukopenia)",
            "medications": [
                {"name": "Filgrastim (G-CSF)", "purpose": "Stimulates WBC production", "note": "Prescription only. Consult immunologist."},
            ],
            "precautions": [
                {"title": "Avoid Infections", "description": "Low WBC weakens immunity. Avoid crowds, wash hands frequently."},
                {"title": "Avoid Raw Foods", "description": "Avoid raw meat and unwashed vegetables to prevent food-borne infections."},
            ],
            "prevention": [
                {"title": "Balanced Nutrition", "description": "Eat zinc-rich foods, Vitamin B12, and folate to support WBC production."},
            ],
            "lifestyle": [{"category": "Other", "advice": "Strict hygiene. Avoid contact with sick individuals."}],
            "doctor_signs": ["Fever above 38°C", "Frequent infections", "Mouth sores or ulcers", "Swollen lymph nodes"],
        },
        "high_advice": {
            "name": "High WBC (Leukocytosis)",
            "medications": [
                {"name": "Antibiotics", "purpose": "If infection is the cause", "note": "Only after doctor determines cause and prescribes."},
            ],
            "precautions": [
                {"title": "Identify the Cause", "description": "High WBC is a symptom — infection, stress, or inflammation may be the cause."},
                {"title": "Rest Adequately", "description": "Allow your body to fight whatever is causing the elevation."},
            ],
            "prevention": [
                {"title": "Manage Stress", "description": "Chronic stress raises WBC. Practice meditation or yoga."},
                {"title": "Treat Infections Early", "description": "Don't ignore minor infections; treat them promptly."},
            ],
            "lifestyle": [{"category": "Stress", "advice": "Practice breathing exercises and adequate sleep to reduce stress-related WBC elevation."}],
            "doctor_signs": ["Persistent fever", "Unexplained weight loss", "Night sweats", "Severe fatigue"],
        },
    },

    "platelets": {
        "unit": "cells/µL", "category": "blood",
        "aliases": ["platelet count", "plt", "thrombocytes"],
        "normal": (150000, 400000),
        "low_advice": {
            "name": "Low Platelets (Thrombocytopenia)",
            "medications": [
                {"name": "Eltrombopag", "purpose": "Stimulates platelet production", "note": "Specialist prescription only."},
            ],
            "precautions": [
                {"title": "Avoid Cuts and Injuries", "description": "Low platelets mean prolonged bleeding. Be extremely careful with sharp objects."},
                {"title": "No Aspirin or NSAIDs", "description": "These thin the blood further. Avoid unless prescribed."},
            ],
            "prevention": [
                {"title": "Papaya Leaf Extract", "description": "May help raise platelet count naturally. Consult doctor before use."},
                {"title": "Avoid Alcohol", "description": "Alcohol suppresses platelet production. Avoid completely."},
            ],
            "lifestyle": [{"category": "Diet", "advice": "Eat papaya, pomegranate, pumpkin, and foods rich in Vitamin K."}],
            "doctor_signs": ["Unexplained bruising", "Prolonged bleeding from cuts", "Blood in urine or stool", "Severe headache"],
        },
        "high_advice": {
            "name": "High Platelets (Thrombocytosis)",
            "medications": [
                {"name": "Aspirin (low dose)", "purpose": "Prevents clot formation", "note": "Only as prescribed by doctor."},
            ],
            "precautions": [
                {"title": "Clot Risk", "description": "High platelets increase clotting risk. Stay active to maintain circulation."},
                {"title": "Stay Hydrated", "description": "Drink plenty of water to reduce blood thickness."},
            ],
            "prevention": [
                {"title": "Regular Exercise", "description": "Light physical activity improves blood flow and reduces clot risk."},
            ],
            "lifestyle": [{"category": "Exercise", "advice": "Walk 30 minutes daily to keep blood flowing well."}],
            "doctor_signs": ["Sudden chest pain", "Leg swelling or pain", "Sudden severe headache", "Vision changes"],
        },
    },

    "rbc": {
        "unit": "million/µL", "category": "blood",
        "aliases": ["red blood cells", "rbc count", "erythrocytes"],
        "normal": (4.2, 5.9),
        "low_advice": {
            "name": "Low RBC Count (Anemia)",
            "medications": [
                {"name": "Iron Supplements", "purpose": "Boost red blood cell production", "note": "Take as prescribed."},
                {"name": "Vitamin B12 Injections", "purpose": "For B12 deficiency anemia", "note": "Doctor prescription required."},
            ],
            "precautions": [
                {"title": "Limit Caffeine", "description": "Coffee and tea inhibit iron absorption. Avoid with iron-rich meals."},
            ],
            "prevention": [
                {"title": "B12-Rich Foods", "description": "Eat eggs, dairy, fish, and meat to maintain healthy RBC production."},
            ],
            "lifestyle": [{"category": "Diet", "advice": "Eat red meat, eggs, dairy, and leafy greens rich in iron and B12."}],
            "doctor_signs": ["Persistent fatigue", "Cold hands and feet", "Pale skin", "Rapid heartbeat"],
        },
        "high_advice": {
            "name": "High RBC Count",
            "medications": [],
            "precautions": [
                {"title": "Avoid Dehydration", "description": "High RBC thickens blood. Drink at least 2-3 liters of water daily."},
            ],
            "prevention": [
                {"title": "Quit Smoking", "description": "Smoking is a leading cause of high RBC count."},
            ],
            "lifestyle": [{"category": "Other", "advice": "Avoid high altitudes. Stay hydrated and quit smoking."}],
            "doctor_signs": ["Headache", "Dizziness", "Shortness of breath", "Flushed skin"],
        },
    },

    # ── BLOOD SUGAR ───────────────────────────────────────────────
    "fasting_glucose": {
        "unit": "mg/dL", "category": "blood",
        "aliases": ["fasting blood sugar", "fbs", "fasting glucose", "blood glucose fasting", "glucose fasting"],
        "normal": (70, 100),
        "low_advice": {
            "name": "Low Blood Sugar (Hypoglycemia)",
            "medications": [
                {"name": "Glucose Tablets", "purpose": "Immediate treatment for low blood sugar", "note": "Carry glucose tablets at all times if diabetic."},
            ],
            "precautions": [
                {"title": "Never Skip Meals", "description": "Skipping meals can dangerously lower blood sugar. Eat every 3-4 hours."},
                {"title": "Carry Fast Sugar", "description": "Always carry juice, glucose tablets, or candy for emergencies."},
            ],
            "prevention": [
                {"title": "Regular Meal Schedule", "description": "Eat balanced meals at regular intervals throughout the day."},
            ],
            "lifestyle": [{"category": "Diet", "advice": "Eat complex carbohydrates like oats, whole grain bread that release sugar slowly."}],
            "doctor_signs": ["Sweating and trembling", "Confusion or difficulty concentrating", "Loss of consciousness", "Extreme hunger with weakness"],
        },
        "high_advice": {
            "name": "High Blood Sugar (Hyperglycemia/Prediabetes/Diabetes)",
            "medications": [
                {"name": "Metformin", "purpose": "First-line medication for Type 2 diabetes", "note": "Prescription required. Do not self-medicate."},
                {"name": "Insulin", "purpose": "For Type 1 or advanced Type 2 diabetes", "note": "Must be prescribed and monitored by endocrinologist."},
            ],
            "precautions": [
                {"title": "Monitor Blood Sugar Daily", "description": "Use a glucometer to track fasting and post-meal sugar levels daily."},
                {"title": "Avoid Sugary Foods", "description": "Cut out soft drinks, sweets, white rice, and refined flour immediately."},
                {"title": "Foot Care", "description": "High sugar damages nerves. Check feet daily for sores or wounds."},
            ],
            "prevention": [
                {"title": "Low Glycemic Diet", "description": "Choose brown rice, whole wheat, oats, and vegetables over refined carbs."},
                {"title": "Exercise Daily", "description": "30 minutes of brisk walking helps cells absorb glucose better."},
                {"title": "Lose Excess Weight", "description": "Even 5-10% weight loss significantly improves blood sugar control."},
            ],
            "lifestyle": [
                {"category": "Diet", "advice": "Avoid sugar, white rice, maida, soft drinks. Choose whole grains and vegetables."},
                {"category": "Exercise", "advice": "Walk 30-45 minutes daily. Exercise helps insulin work more effectively."},
            ],
            "doctor_signs": ["Excessive thirst or urination", "Blurred vision", "Slow healing wounds", "Tingling in hands or feet"],
        },
    },

    # ── LIPID PROFILE ──────────────────────────────────────────────
    "total_cholesterol": {
        "unit": "mg/dL", "category": "lipid",
        "aliases": ["cholesterol", "total cholesterol", "serum cholesterol"],
        "normal": (0, 200),
        "low_advice": {
            "name": "Low Cholesterol",
            "medications": [],
            "precautions": [{"title": "Nutritional Review", "description": "Very low cholesterol may indicate malnutrition or liver disease."}],
            "prevention": [{"title": "Healthy Fat Intake", "description": "Include healthy fats like avocado, nuts, and olive oil in your diet."}],
            "lifestyle": [{"category": "Diet", "advice": "Include healthy fats: nuts, seeds, avocado, olive oil, eggs."}],
            "doctor_signs": ["Unexplained weight loss", "Fatigue", "Hormonal imbalances"],
        },
        "high_advice": {
            "name": "High Cholesterol (Hypercholesterolemia)",
            "medications": [
                {"name": "Atorvastatin (Statin)", "purpose": "Reduces LDL cholesterol", "note": "Prescription required. Take at night as prescribed."},
                {"name": "Ezetimibe", "purpose": "Reduces cholesterol absorption from gut", "note": "Usually combined with statins. Doctor prescription."},
            ],
            "precautions": [
                {"title": "Avoid Saturated Fats", "description": "Cut out butter, red meat, full-fat dairy, and fried foods."},
                {"title": "No Trans Fats", "description": "Avoid processed foods, margarine, and commercial baked goods."},
            ],
            "prevention": [
                {"title": "Heart-Healthy Diet", "description": "Eat oats, fruits, vegetables, fish, and nuts. Avoid fried and processed food."},
                {"title": "Regular Exercise", "description": "Exercise raises good HDL and lowers bad LDL cholesterol."},
                {"title": "Quit Smoking", "description": "Smoking lowers HDL (good cholesterol) and raises cardiovascular risk."},
            ],
            "lifestyle": [
                {"category": "Diet", "advice": "Eat oats, omega-3 rich fish (salmon, mackerel), nuts, and plenty of fiber."},
                {"category": "Exercise", "advice": "Aim for 150 minutes of moderate exercise per week."},
            ],
            "doctor_signs": ["Chest pain or tightness", "Shortness of breath on exertion", "Yellowish skin deposits (xanthomas)", "Family history of heart disease"],
        },
    },

    "hdl": {
        "unit": "mg/dL", "category": "lipid",
        "aliases": ["hdl cholesterol", "good cholesterol", "hdl-c"],
        "normal": (40, 999),
        "low_advice": {
            "name": "Low HDL (Good Cholesterol)",
            "medications": [
                {"name": "Niacin (Vitamin B3)", "purpose": "Raises HDL cholesterol", "note": "High doses require medical supervision."},
            ],
            "precautions": [
                {"title": "Avoid Smoking", "description": "Smoking is the #1 cause of low HDL. Quitting raises it significantly."},
            ],
            "prevention": [
                {"title": "Regular Exercise", "description": "Aerobic exercise is the best way to raise HDL naturally."},
                {"title": "Healthy Fats", "description": "Olive oil, avocado, and nuts raise HDL levels."},
            ],
            "lifestyle": [
                {"category": "Exercise", "advice": "30 minutes of cardio (running, cycling, swimming) 5 days a week raises HDL."},
                {"category": "Diet", "advice": "Use olive oil, eat avocados, nuts, and fatty fish."},
            ],
            "doctor_signs": ["Chest pain", "Known heart disease", "Family history of low HDL"],
        },
        "high_advice": {
            "name": "High HDL (Good Cholesterol) — Generally Positive",
            "medications": [],
            "precautions": [{"title": "Generally Beneficial", "description": "High HDL is usually protective against heart disease."}],
            "prevention": [{"title": "Maintain Healthy Lifestyle", "description": "Continue your current diet and exercise habits."}],
            "lifestyle": [{"category": "Other", "advice": "High HDL is a positive sign. Maintain your healthy lifestyle."}],
            "doctor_signs": ["Very high HDL (above 100) in rare cases may need evaluation"],
        },
    },

    "ldl": {
        "unit": "mg/dL", "category": "lipid",
        "aliases": ["ldl cholesterol", "bad cholesterol", "ldl-c"],
        "normal": (0, 100),
        "low_advice": {
            "name": "Low LDL",
            "medications": [],
            "precautions": [{"title": "Generally Good", "description": "Low LDL is mostly beneficial for heart health."}],
            "prevention": [{"title": "Maintain Current Diet", "description": "Your current lifestyle is keeping LDL in a healthy range."}],
            "lifestyle": [{"category": "Diet", "advice": "Maintain your heart-healthy eating habits."}],
            "doctor_signs": ["Extremely low LDL may rarely indicate other conditions — discuss with doctor"],
        },
        "high_advice": {
            "name": "High LDL (Bad Cholesterol)",
            "medications": [
                {"name": "Rosuvastatin", "purpose": "Powerful LDL-lowering statin", "note": "Doctor prescription required. Regular liver function monitoring needed."},
            ],
            "precautions": [
                {"title": "Strict Dietary Changes", "description": "Eliminate red meat, butter, full-fat dairy, and all fried foods."},
                {"title": "Weight Management", "description": "Excess weight directly raises LDL levels."},
            ],
            "prevention": [
                {"title": "Plant-Based Diet", "description": "More vegetables, fruits, and whole grains lower LDL significantly."},
                {"title": "Daily Exercise", "description": "Exercise lowers LDL and raises protective HDL."},
            ],
            "lifestyle": [
                {"category": "Diet", "advice": "Eat more fiber, fruits, vegetables. Avoid fried, processed, and fatty foods."},
                {"category": "Exercise", "advice": "Minimum 30 minutes brisk walking daily."},
            ],
            "doctor_signs": ["Chest pain or pressure", "Pain radiating to left arm", "Shortness of breath", "High blood pressure"],
        },
    },

    "triglycerides": {
        "unit": "mg/dL", "category": "lipid",
        "aliases": ["triglycerides", "tg", "trigs"],
        "normal": (0, 150),
        "low_advice": {
            "name": "Low Triglycerides",
            "medications": [],
            "precautions": [{"title": "Generally Fine", "description": "Low triglycerides are usually a positive sign."}],
            "prevention": [{"title": "Maintain Balanced Diet", "description": "Continue eating a balanced diet with healthy fats."}],
            "lifestyle": [{"category": "Diet", "advice": "Your lipid levels are well controlled. Maintain current diet."}],
            "doctor_signs": ["Generally no concern at low levels"],
        },
        "high_advice": {
            "name": "High Triglycerides (Hypertriglyceridemia)",
            "medications": [
                {"name": "Fenofibrate", "purpose": "Lowers triglyceride levels", "note": "Prescription required."},
                {"name": "Omega-3 Fatty Acids (Fish Oil)", "purpose": "Naturally lowers triglycerides", "note": "High doses (4g/day) require medical guidance."},
            ],
            "precautions": [
                {"title": "Cut Sugar and Alcohol", "description": "Sugar and alcohol are the top causes of high triglycerides. Eliminate them."},
                {"title": "Avoid Refined Carbs", "description": "White bread, rice, and pasta spike triglycerides rapidly."},
            ],
            "prevention": [
                {"title": "Reduce Sugar Intake", "description": "Sugar converts directly to triglycerides in the liver."},
                {"title": "Omega-3 Rich Foods", "description": "Eat fatty fish (salmon, sardines) 2-3 times per week."},
            ],
            "lifestyle": [
                {"category": "Diet", "advice": "Eliminate sugar, alcohol, and refined carbs. Eat fatty fish and walnuts."},
                {"category": "Exercise", "advice": "Regular aerobic exercise significantly lowers triglycerides."},
            ],
            "doctor_signs": ["Severe abdominal pain (may indicate pancreatitis)", "Xanthomas (fatty deposits under skin)", "Very high reading above 500 mg/dL"],
        },
    },

    # ── THYROID ────────────────────────────────────────────────────
    "tsh": {
        "unit": "µIU/mL", "category": "thyroid",
        "aliases": ["tsh", "thyroid stimulating hormone", "thyrotropin"],
        "normal": (0.4, 4.0),
        "low_advice": {
            "name": "Low TSH (Hyperthyroidism)",
            "medications": [
                {"name": "Methimazole", "purpose": "Reduces thyroid hormone production", "note": "Prescription only. Regular monitoring required."},
                {"name": "Propranolol", "purpose": "Controls heart rate and symptoms", "note": "Temporary symptom relief. Doctor prescription."},
            ],
            "precautions": [
                {"title": "Avoid Excess Iodine", "description": "Too much iodine worsens hyperthyroidism. Limit seaweed and iodine supplements."},
                {"title": "Monitor Heart Rate", "description": "Hyperthyroidism causes rapid heartbeat. Track pulse daily."},
                {"title": "Bone Health", "description": "Hyperthyroidism weakens bones over time. Ensure calcium and Vitamin D intake."},
            ],
            "prevention": [
                {"title": "Regular Thyroid Tests", "description": "Monitor TSH every 3-6 months to track treatment progress."},
                {"title": "Stress Management", "description": "Stress worsens thyroid conditions. Practice meditation and yoga."},
            ],
            "lifestyle": [
                {"category": "Diet", "advice": "Avoid excess caffeine, iodine-rich foods. Focus on calcium-rich foods for bone health."},
                {"category": "Exercise", "advice": "Gentle exercise like yoga. Avoid intense workouts as heart rate is already elevated."},
            ],
            "doctor_signs": ["Rapid or irregular heartbeat", "Unexplained weight loss", "Excessive sweating", "Trembling hands", "Bulging eyes"],
        },
        "high_advice": {
            "name": "High TSH (Hypothyroidism)",
            "medications": [
                {"name": "Levothyroxine (T4)", "purpose": "Thyroid hormone replacement", "note": "Take on empty stomach 30 minutes before breakfast. Lifelong medication usually required."},
            ],
            "precautions": [
                {"title": "Take Medication Consistently", "description": "Take levothyroxine at the same time every day for best results."},
                {"title": "Avoid Certain Foods with Medication", "description": "Calcium, iron, and soy interfere with levothyroxine absorption. Take separately."},
                {"title": "Cold Sensitivity", "description": "Hypothyroidism causes cold intolerance. Dress warmly and maintain room temperature."},
            ],
            "prevention": [
                {"title": "Adequate Iodine Intake", "description": "Use iodized salt. Iodine deficiency is a leading cause of hypothyroidism."},
                {"title": "Selenium-Rich Foods", "description": "Brazil nuts, tuna, and eggs support thyroid function."},
                {"title": "Regular Testing", "description": "Monitor TSH every 6 months once on treatment."},
            ],
            "lifestyle": [
                {"category": "Diet", "advice": "Eat selenium-rich foods (Brazil nuts, tuna). Use iodized salt. Limit goitrogenic foods (raw cabbage, broccoli)."},
                {"category": "Exercise", "advice": "Regular moderate exercise combats fatigue and weight gain from hypothyroidism."},
                {"category": "Sleep", "advice": "Aim for 8 hours of sleep. Hypothyroidism causes fatigue that worsens without adequate rest."},
            ],
            "doctor_signs": ["Extreme fatigue", "Unexplained weight gain", "Severe constipation", "Depression", "Puffy face or swollen ankles"],
        },
    },

    "t3": {
        "unit": "ng/dL", "category": "thyroid",
        "aliases": ["t3", "triiodothyronine", "free t3", "total t3"],
        "normal": (80, 200),
        "low_advice": {
            "name": "Low T3 (Thyroid Hormone Deficiency)",
            "medications": [
                {"name": "Liothyronine (T3)", "purpose": "Direct T3 hormone replacement", "note": "Specialist prescription. Requires careful dose monitoring."},
            ],
            "precautions": [{"title": "Monitor Symptoms", "description": "Low T3 causes fatigue, cold intolerance, weight gain. Track symptoms."}],
            "prevention": [{"title": "Selenium Intake", "description": "Selenium helps convert T4 to active T3. Eat Brazil nuts and seafood."}],
            "lifestyle": [{"category": "Diet", "advice": "Eat selenium-rich foods: Brazil nuts, tuna, eggs, sunflower seeds."}],
            "doctor_signs": ["Severe fatigue", "Hair loss", "Dry skin", "Difficulty concentrating", "Depression"],
        },
        "high_advice": {
            "name": "High T3 (Hyperthyroidism)",
            "medications": [
                {"name": "Methimazole", "purpose": "Reduces thyroid hormone production", "note": "Endocrinologist prescription required."},
            ],
            "precautions": [{"title": "Avoid Stimulants", "description": "Avoid caffeine and energy drinks as they worsen palpitations."}],
            "prevention": [{"title": "Stress Reduction", "description": "Stress can trigger thyroid storms. Practice relaxation techniques."}],
            "lifestyle": [{"category": "Stress", "advice": "Practice meditation, deep breathing, and yoga to manage hyperthyroid symptoms."}],
            "doctor_signs": ["Rapid heartbeat", "Nervousness or anxiety", "Excessive sweating", "Unexplained weight loss"],
        },
    },

    "t4": {
        "unit": "µg/dL", "category": "thyroid",
        "aliases": ["t4", "thyroxine", "free t4", "total t4"],
        "normal": (4.5, 12.5),
        "low_advice": {
            "name": "Low T4 (Hypothyroidism)",
            "medications": [
                {"name": "Levothyroxine", "purpose": "T4 hormone replacement therapy", "note": "Most common thyroid medication. Take daily on empty stomach."},
            ],
            "precautions": [{"title": "Consistent Medication", "description": "Never skip levothyroxine doses. Consistency is critical."}],
            "prevention": [{"title": "Adequate Iodine", "description": "Use iodized salt. Iodine is essential for T4 production."}],
            "lifestyle": [{"category": "Diet", "advice": "Use iodized salt. Eat dairy, seafood, and eggs for iodine and selenium."}],
            "doctor_signs": ["Weight gain", "Fatigue", "Hair thinning", "Constipation", "Feeling cold always"],
        },
        "high_advice": {
            "name": "High T4 (Hyperthyroidism)",
            "medications": [
                {"name": "Carbimazole", "purpose": "Blocks thyroid hormone production", "note": "Prescription only. Blood tests needed during treatment."},
            ],
            "precautions": [{"title": "Bone Protection", "description": "High T4 accelerates bone loss. Ensure calcium and Vitamin D intake."}],
            "prevention": [{"title": "Regular Monitoring", "description": "Check TSH/T4 every 3 months during treatment."}],
            "lifestyle": [{"category": "Diet", "advice": "Ensure adequate calcium and Vitamin D for bone protection."}],
            "doctor_signs": ["Heart palpitations", "Tremors", "Heat intolerance", "Anxiety", "Muscle weakness"],
        },
    },

    # ── URINE TEST ─────────────────────────────────────────────────
    "urine_glucose": {
        "unit": "mg/dL", "category": "urine",
        "aliases": ["urine glucose", "glycosuria", "glucose in urine", "urine sugar"],
        "normal": (0, 0),
        "low_advice": {
            "name": "No Glucose in Urine (Normal)",
            "medications": [],
            "precautions": [{"title": "Normal Finding", "description": "Absence of glucose in urine is normal and healthy."}],
            "prevention": [{"title": "Maintain Blood Sugar", "description": "Continue healthy diet to keep blood sugar in normal range."}],
            "lifestyle": [{"category": "Diet", "advice": "Maintain a low-sugar, balanced diet to keep blood sugar healthy."}],
            "doctor_signs": [],
        },
        "high_advice": {
            "name": "Glucose in Urine (Glycosuria) — Possible Diabetes",
            "medications": [
                {"name": "Metformin", "purpose": "First-line diabetes medication", "note": "Only after confirmed blood glucose testing and doctor prescription."},
            ],
            "precautions": [
                {"title": "Get Blood Sugar Tested", "description": "Glycosuria requires a fasting blood glucose test to rule out diabetes."},
                {"title": "Reduce Sugar Intake", "description": "Immediately cut refined sugar, sweets, and sugary drinks."},
            ],
            "prevention": [
                {"title": "Blood Sugar Monitoring", "description": "Monitor fasting blood sugar regularly."},
                {"title": "Healthy Diet and Exercise", "description": "A low-glycemic diet and daily exercise can prevent diabetic progression."},
            ],
            "lifestyle": [
                {"category": "Diet", "advice": "Avoid sugar, white rice, maida. Eat whole grains, vegetables, and lean protein."},
                {"category": "Exercise", "advice": "30 minutes daily walking is highly effective in managing blood sugar."},
            ],
            "doctor_signs": ["Increased thirst", "Frequent urination", "Unexplained fatigue", "Blurred vision"],
        },
    },

    "urine_protein": {
        "unit": "mg/dL", "category": "urine",
        "aliases": ["urine protein", "proteinuria", "protein in urine", "albumin urine"],
        "normal": (0, 14),
        "low_advice": {
            "name": "Normal Urine Protein",
            "medications": [],
            "precautions": [{"title": "Normal Finding", "description": "Protein levels in urine are within normal limits."}],
            "prevention": [{"title": "Stay Hydrated", "description": "Drink adequate water to maintain kidney health."}],
            "lifestyle": [{"category": "Diet", "advice": "Maintain adequate hydration and a kidney-friendly diet."}],
            "doctor_signs": [],
        },
        "high_advice": {
            "name": "High Urine Protein (Proteinuria) — Kidney Concern",
            "medications": [
                {"name": "ACE Inhibitors (e.g., Enalapril)", "purpose": "Reduces protein leakage and protects kidneys", "note": "Prescription required. Monitor blood pressure and kidney function."},
            ],
            "precautions": [
                {"title": "Reduce Salt Intake", "description": "Excess sodium worsens kidney strain. Limit salt strictly."},
                {"title": "Control Blood Pressure", "description": "High BP damages kidneys. Monitor and manage BP carefully."},
                {"title": "Limit Protein Intake", "description": "Reduce red meat and high-protein foods to ease kidney workload."},
            ],
            "prevention": [
                {"title": "Control Diabetes and BP", "description": "Diabetes and hypertension are the leading causes of proteinuria."},
                {"title": "Stay Hydrated", "description": "Drink 2-3 liters of water daily for kidney health."},
                {"title": "Avoid NSAIDs", "description": "Pain killers like ibuprofen damage kidneys. Use with caution."},
            ],
            "lifestyle": [
                {"category": "Diet", "advice": "Low salt, low protein diet. Avoid red meat, processed foods. Eat kidney-friendly foods."},
                {"category": "Other", "advice": "Avoid strenuous exercise on test days as it can temporarily raise urine protein."},
            ],
            "doctor_signs": ["Foamy or bubbly urine", "Swelling in ankles or face", "Fatigue", "High blood pressure", "Reduced urination"],
        },
    },

    "urine_ph": {
        "unit": "pH", "category": "urine",
        "aliases": ["urine ph", "ph urine", "urinary ph"],
        "normal": (4.5, 8.0),
        "low_advice": {
            "name": "Acidic Urine (Low pH)",
            "medications": [],
            "precautions": [{"title": "Increase Fluid Intake", "description": "Drink more water to dilute acidic urine and prevent kidney stones."}],
            "prevention": [
                {"title": "Alkaline Foods", "description": "Eat more vegetables and fruits to reduce urine acidity."},
                {"title": "Reduce Meat Intake", "description": "High protein diets acidify urine. Balance with vegetables."},
            ],
            "lifestyle": [{"category": "Diet", "advice": "Eat more fruits and vegetables. Reduce red meat and processed foods."}],
            "doctor_signs": ["Burning urination", "Kidney stone history", "Frequent UTIs"],
        },
        "high_advice": {
            "name": "Alkaline Urine (High pH)",
            "medications": [],
            "precautions": [{"title": "Check for UTI", "description": "Alkaline urine can indicate a urinary tract infection. Get urine culture done."}],
            "prevention": [
                {"title": "Stay Hydrated", "description": "Adequate hydration helps maintain normal urine pH."},
            ],
            "lifestyle": [{"category": "Diet", "advice": "Ensure balanced diet. Stay well hydrated throughout the day."}],
            "doctor_signs": ["Burning urination", "Cloudy urine", "Frequent urge to urinate", "Fever with chills"],
        },
    },

    "creatinine": {
        "unit": "mg/dL", "category": "urine",
        "aliases": ["creatinine", "serum creatinine", "creatinine serum", "s. creatinine"],
        "normal": (0.6, 1.2),
        "low_advice": {
            "name": "Low Creatinine",
            "medications": [],
            "precautions": [{"title": "Generally Benign", "description": "Low creatinine may indicate low muscle mass or pregnancy. Usually not concerning."}],
            "prevention": [{"title": "Adequate Protein Intake", "description": "Ensure sufficient protein in diet for muscle maintenance."}],
            "lifestyle": [{"category": "Diet", "advice": "Include lean protein sources: chicken, fish, legumes, and dairy."}],
            "doctor_signs": ["Muscle wasting", "Unexplained weakness"],
        },
        "high_advice": {
            "name": "High Creatinine (Kidney Function Concern)",
            "medications": [
                {"name": "ACE Inhibitors", "purpose": "Protects kidneys and reduces creatinine", "note": "Prescription only. Regular monitoring needed."},
            ],
            "precautions": [
                {"title": "Limit High-Protein Foods", "description": "Reduce red meat and protein supplements to lower kidney load."},
                {"title": "Avoid NSAIDs", "description": "Ibuprofen and similar painkillers worsen kidney function."},
                {"title": "Stay Hydrated", "description": "Drink adequate water to help kidneys filter creatinine."},
            ],
            "prevention": [
                {"title": "Control Diabetes and BP", "description": "Both are the leading causes of kidney damage."},
                {"title": "Adequate Hydration", "description": "2-3 liters of water daily supports kidney function."},
            ],
            "lifestyle": [
                {"category": "Diet", "advice": "Low protein, low salt diet. Avoid red meat, processed foods, and alcohol."},
                {"category": "Other", "advice": "Avoid heavy exercise before kidney tests as it temporarily raises creatinine."},
            ],
            "doctor_signs": ["Reduced urination", "Swelling in legs or face", "Fatigue", "Nausea", "Foamy urine"],
        },
    },
}

# Risk scoring thresholds
RISK_RULES = {
    "critical": 3,   # 3+ abnormal parameters = critical
    "high": 2,       # 2 abnormal = high
    "medium": 1,     # 1 abnormal = medium
    "low": 0,        # 0 abnormal = low
}

# Report type to category mapping
REPORT_CATEGORY_MAP = {
    "blood_test": ["blood"],
    "lipid_profile": ["lipid"],
    "thyroid": ["thyroid"],
    "urine_test": ["urine"],
    "other": ["blood", "lipid", "thyroid", "urine"],
}
