CLASSIFICATION_PROMPT = """
You are a legal query classifier for an Indian legal AI system.

Analyze the user's question and classify it.

Return ONLY valid JSON.

Allowed legal categories:
- constitutional_law
- criminal_law
- property_law
- family_law
- consumer_law
- employment_law
- contract_law
- cyber_law
- tax_law
- labour_law
- company_law
- intellectual_property
- environmental_law
- human_rights
- civil_law

Intent can be:
- legal_advice
- document_question
- case_question
- legal_research
- general_information

Determine whether the user needs their uploaded document
to answer the question.

Return this JSON structure:

{{
    "category": "...",
    "issue": "...",
    "intent": "...",
    "keywords": ["...", "..."],
    "requires_user_document": true
}}

User question:

{question}
"""