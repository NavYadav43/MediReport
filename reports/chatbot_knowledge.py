# reports/chatbot_knowledge.py
# Medical Q&A knowledge base for TF-IDF ML chatbot

QA_PAIRS = [
    # BLOOD TEST
    ("what does high hemoglobin mean", "High hemoglobin (above 17.5 g/dL in men, 15.5 in women) is called polycythemia. It thickens your blood, increasing clot risk. Common causes include smoking, dehydration, and lung disease. Stay well hydrated, quit smoking, and consult your doctor."),
    ("what does low hemoglobin mean", "Low hemoglobin indicates anemia. Symptoms include fatigue, pale skin, shortness of breath, and dizziness. Most common cause is iron deficiency. Eat iron-rich foods like spinach, lentils, red meat. Take iron supplements if prescribed by your doctor."),
    ("what is normal hemoglobin level", "Normal hemoglobin: Men 13.5–17.5 g/dL, Women 12.0–15.5 g/dL, Children 11–16 g/dL. Values below these indicate anemia; values above suggest polycythemia."),
    ("what does high wbc mean", "High WBC (above 11,000 cells/µL) is called leukocytosis. It usually means your body is fighting an infection, inflammation, or stress. Less commonly it can indicate leukemia. See your doctor to find the underlying cause."),
    ("what does low wbc mean", "Low WBC (below 4,000 cells/µL) is leukopenia. It weakens your immune system, making you prone to infections. Causes include viral infections, autoimmune conditions, and certain medications. Avoid crowded places and practice strict hygiene."),
    ("what does low platelet count mean", "Low platelets (below 150,000) is thrombocytopenia. It causes easy bruising, prolonged bleeding, and petechiae (red spots on skin). Common causes in India include dengue fever. Avoid NSAIDs, eat papaya, and see a doctor immediately if count drops below 50,000."),
    ("what does high platelet count mean", "High platelets (above 400,000) is thrombocytosis. It increases blood clot risk. Stay hydrated, exercise regularly, and avoid prolonged sitting. See your doctor if platelets are above 600,000."),

    # BLOOD SUGAR
    ("what is normal blood sugar level", "Normal fasting blood sugar: 70–100 mg/dL. Prediabetes: 100–125 mg/dL. Diabetes: 126 mg/dL or above. Post-meal (2 hours): below 140 mg/dL is normal, 140–199 is prediabetes, 200+ is diabetes."),
    ("what does high blood sugar mean", "High fasting blood sugar (above 126 mg/dL) indicates diabetes. Between 100–125 is prediabetes. Manage with low-sugar diet, daily exercise, weight loss, and medication if prescribed. Avoid white rice, maida, sweets, and soft drinks."),
    ("what does low blood sugar mean", "Low blood sugar (below 70 mg/dL) is hypoglycemia. Symptoms: sweating, trembling, confusion, hunger. Immediately eat glucose tablets, fruit juice, or candy. Never skip meals. If you're diabetic, carry glucose tablets at all times."),
    ("what is hba1c", "HbA1c measures your average blood sugar over the past 3 months. Normal: below 5.7%. Prediabetes: 5.7–6.4%. Diabetes: 6.5% or above. Target for diabetics: below 7.0%. Get tested every 3 months if diabetic."),

    # CHOLESTEROL / LIPID
    ("what is normal cholesterol level", "Total cholesterol should be below 200 mg/dL. LDL (bad cholesterol): below 100 mg/dL. HDL (good cholesterol): above 40 mg/dL for men, above 50 for women. Triglycerides: below 150 mg/dL."),
    ("what does high cholesterol mean", "High total cholesterol (above 200 mg/dL) increases heart disease and stroke risk. Cut saturated fats (butter, red meat, fried food). Exercise 30 minutes daily. Your doctor may prescribe statins like atorvastatin."),
    ("what does high ldl mean", "High LDL (bad cholesterol above 100 mg/dL) builds up in artery walls causing heart disease. Avoid fried foods, processed meats, and full-fat dairy. Eat oats, nuts, olive oil, and fatty fish. Exercise regularly."),
    ("what does low hdl mean", "Low HDL (good cholesterol below 40 mg/dL) increases heart risk. Raise it by exercising regularly (best method), quitting smoking, losing weight, and eating healthy fats like olive oil, avocado, and nuts."),
    ("what does high triglycerides mean", "High triglycerides (above 150 mg/dL) increase heart and pancreatitis risk. Main causes: excess sugar, refined carbs, and alcohol. Cut sugar and alcohol completely, exercise daily, eat fatty fish and walnuts."),

    # THYROID
    ("what does high tsh mean", "High TSH (above 4.0 µIU/mL) indicates hypothyroidism — your thyroid is underactive. Symptoms: fatigue, weight gain, feeling cold, constipation, hair loss. Treatment is daily levothyroxine tablet on an empty stomach."),
    ("what does low tsh mean", "Low TSH (below 0.4 µIU/mL) indicates hyperthyroidism — your thyroid is overactive. Symptoms: weight loss, rapid heartbeat, anxiety, tremors, sweating. Treatment includes antithyroid medications like methimazole."),
    ("what is normal tsh level", "Normal TSH range is 0.4–4.0 µIU/mL. Below 0.4 suggests hyperthyroidism (overactive). Above 4.0 suggests hypothyroidism (underactive). Pregnant women have different ranges — consult your doctor."),
    ("what is hypothyroidism", "Hypothyroidism means your thyroid gland produces too little hormone. TSH rises above 4.0. Symptoms: fatigue, weight gain, cold intolerance, constipation, hair loss, depression. Treated with daily levothyroxine. Very manageable with medication."),
    ("what is hyperthyroidism", "Hyperthyroidism means your thyroid produces too much hormone. TSH drops below 0.4. Symptoms: weight loss, palpitations, anxiety, tremors, heat intolerance. Graves disease is the most common cause. Treated with methimazole or radioactive iodine."),

    # KIDNEY
    ("what does high creatinine mean", "High creatinine (above 1.2 mg/dL in men, 1.0 in women) suggests reduced kidney function. Causes: diabetes, hypertension, dehydration, NSAIDs overuse. Drink 2–3 liters of water daily, reduce salt and protein intake, avoid ibuprofen."),
    ("what is normal creatinine level", "Normal creatinine: Men 0.7–1.2 mg/dL, Women 0.5–1.0 mg/dL. Above these values suggests kidney stress. Below is usually fine, often indicating low muscle mass."),
    ("what does protein in urine mean", "Protein in urine (proteinuria) suggests kidney damage or stress. Normally kidneys filter out protein — finding it in urine means filters are leaking. Causes: diabetes, hypertension, kidney disease. Reduce salt, control BP and blood sugar."),
    ("what does glucose in urine mean", "Glucose in urine (glycosuria) usually indicates diabetes or prediabetes — blood sugar is too high for kidneys to reabsorb. Get a fasting blood glucose test immediately. Reduce sugar and refined carbs, exercise daily."),

    # BLOOD PRESSURE
    ("what is normal blood pressure", "Normal blood pressure is below 120/80 mmHg. Elevated: 120–129/below 80. Stage 1 hypertension: 130–139/80–89. Stage 2 hypertension: 140+/90+. Hypertensive crisis (emergency): above 180/120."),
    ("what does high blood pressure mean", "High blood pressure (hypertension, above 130/80) damages blood vessels over time, causing heart attack, stroke, and kidney failure. Reduce salt, exercise daily, lose weight, quit smoking, and take prescribed medication consistently."),
    ("how to lower blood pressure naturally", "To lower blood pressure naturally: reduce salt to less than 2300mg/day, exercise 30 minutes daily, lose weight, quit smoking, limit alcohol, eat potassium-rich foods (bananas, spinach), manage stress with meditation, and get 7–8 hours of sleep."),

    # VITAMINS
    ("what does low vitamin d mean", "Low Vitamin D (below 20 ng/mL) causes fatigue, bone pain, muscle weakness, frequent infections, and depression. Get 15–20 minutes of sunlight daily. Take Vitamin D3 supplements — 60,000 IU weekly for 8–12 weeks if severely deficient."),
    ("what does low vitamin b12 mean", "Low Vitamin B12 (below 200 pg/mL) causes fatigue, tingling in hands/feet, memory problems, and anemia. Very common in vegetarians. Take methylcobalamin 500–1500 mcg daily. Eat dairy, eggs, and fish if possible."),
    ("what foods are rich in iron", "Iron-rich foods: Red meat, chicken liver, spinach, lentils, chickpeas, kidney beans, tofu, pumpkin seeds, fortified cereals. Always pair with Vitamin C (lemon juice, orange) to double iron absorption. Avoid tea/coffee with iron-rich meals."),
    ("what foods increase vitamin d", "Vitamin D food sources: Fatty fish (salmon, mackerel, sardines), egg yolks, fortified milk, mushrooms exposed to sunlight. But food alone is usually not enough — get daily sunlight (15–20 minutes) and supplement if deficient."),

    # GENERAL HEALTH
    ("what is anemia", "Anemia means low hemoglobin or red blood cells, reducing oxygen delivery to your body. Symptoms: fatigue, pale skin, shortness of breath, dizziness. Most common cause is iron deficiency. Treat with iron-rich diet and supplements as prescribed."),
    ("what is diabetes", "Diabetes is a condition where blood sugar stays too high because the body can't produce or use insulin properly. Type 2 is most common. Managed with diet, exercise, weight loss, and medications like metformin. HbA1c above 6.5% confirms diabetes."),
    ("what is hypertension", "Hypertension (high blood pressure, above 130/80) is called the silent killer because it has no symptoms but damages heart, kidneys, and brain over time. Managed with low-salt diet, exercise, weight loss, stress reduction, and medication."),
    ("what is anemia symptoms", "Anemia symptoms: persistent fatigue and weakness, pale or yellowish skin, shortness of breath on exertion, dizziness, cold hands and feet, brittle nails, hair loss, rapid heartbeat, headaches. See a doctor if hemoglobin is below 10 g/dL."),
    ("how to improve kidney health", "To protect kidney health: drink 2–3 liters of water daily, control blood sugar and blood pressure, avoid NSAIDs (ibuprofen, diclofenac) — use paracetamol instead, reduce salt and protein intake, quit smoking, and get annual kidney function tests."),
    ("how to reduce cholesterol", "To reduce cholesterol: eat oats, fatty fish, nuts, olive oil, and lots of fiber. Avoid fried foods, butter, red meat, and processed foods. Exercise 30 minutes daily. Lose excess weight. If LDL remains high, your doctor may prescribe statins."),
    ("what is normal urine test", "Normal urine test: No glucose, No protein (below 14 mg/dL), pH 4.5–8.0, No blood, No bacteria, No ketones. Presence of glucose suggests diabetes. Protein suggests kidney issues. Blood suggests UTI or kidney stones."),
    ("how to control diabetes", "Control diabetes with: daily 30–45 minute walk, low-carb diet (avoid white rice, maida, sugar, soft drinks), weight loss, blood sugar monitoring, HbA1c testing every 3 months, and medications as prescribed. Target fasting sugar below 100, HbA1c below 7%."),
    ("what is dengue", "Dengue is a mosquito-borne viral fever causing high fever, severe headache, body aches, and low platelet count. No specific antiviral treatment — rest, hydration, paracetamol for fever (NOT aspirin or ibuprofen). Hospitalize if platelets drop below 50,000."),
    ("how to increase platelet count", "To increase platelet count: eat papaya leaf extract, pomegranate, pumpkin, kiwi, and Vitamin C-rich foods. Avoid alcohol completely. Avoid aspirin and NSAIDs. Rest adequately. If count drops below 20,000, hospital treatment is needed."),
    ("what is uti", "UTI (urinary tract infection) is a bacterial infection causing burning urination, frequent urge to urinate, cloudy urine, and pelvic pain. Treated with antibiotics. Drink 2–3 liters of water daily, urinate after sex, and don't hold urine for long."),
    ("what is bmi", "BMI (Body Mass Index) = weight (kg) ÷ height² (m²). For Indians: Normal 18.5–22.9, Overweight 23–24.9, Obese 25+. High BMI increases risk of diabetes, hypertension, and heart disease. Lose weight with diet and exercise."),
    ("how to lose weight", "To lose weight safely: reduce calorie intake by 500/day, eat more protein and fiber, cut sugar and refined carbs, exercise 150–300 minutes per week, drink water before meals, sleep 7–8 hours (poor sleep increases hunger hormones), and track your food intake."),
    ("what is good food for heart", "Heart-healthy foods: oats, fatty fish (salmon, mackerel), walnuts, almonds, olive oil, avocado, berries, dark leafy greens, legumes. Avoid: fried foods, processed meats, full-fat dairy, excess salt, sugary drinks, and trans fats."),
    ("what is metformin used for", "Metformin is the most prescribed Type 2 diabetes medication. It reduces glucose production in the liver and improves insulin sensitivity. Take with meals to avoid nausea. Take on empty stomach if using for weight management. Monitor B12 levels annually."),
    ("what is levothyroxine", "Levothyroxine is the standard treatment for hypothyroidism (underactive thyroid). It replaces the missing thyroid hormone. Take every morning on an empty stomach, 30–60 minutes before breakfast. Never miss a dose. TSH should be rechecked every 6 months."),
    ("how to improve immune system", "To boost immunity: sleep 7–8 hours, exercise regularly, eat Vitamin C-rich foods (citrus, bell peppers), take Vitamin D supplements, reduce stress, quit smoking, limit alcohol, maintain healthy weight, and wash hands frequently."),
    ("what causes fatigue", "Common causes of fatigue: anemia (low hemoglobin), hypothyroidism (high TSH), Vitamin D or B12 deficiency, diabetes, sleep disorders, depression, dehydration. Get a CBC, thyroid function, Vitamin D, and B12 blood test if fatigue persists."),
    ("what is normal kidney function", "Normal kidney function tests: Creatinine 0.6–1.2 mg/dL, BUN 7–20 mg/dL, eGFR above 90 mL/min/1.73m², Urine protein below 14 mg/dL. Values outside these ranges need medical evaluation, especially if you have diabetes or hypertension."),
]
