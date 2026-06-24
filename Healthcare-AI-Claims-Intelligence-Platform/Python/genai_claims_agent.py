import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
import json


# Load API key from .env

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def investigate_claim_with_ai(claim):
    print(f"\nDEBUG: Processing Claim ID: {claim['Claim_ID']}")

    prompt = f"""

You are a Healthcare Claims Investigation AI Agent.

Analyze this claim:

Claim ID:
{claim["Claim_ID"]}

Billed Amount:
${claim["Billed_Amount"]}

Paid Amount:
${claim["Paid_Amount"]}

Denial Reason:
{claim["Denial_Reason"]}

Claim Status:
{claim["Claim_Status"]}


Return only JSON format:

Return only JSON format:

{{
"Risk_Level":"",
"Investigation_Explanation":"",
"Possible_Issue":"",
"Recommended_Action":""
}}


Respond clearly for a healthcare investigator.

"""


    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )
    print("DEBUG: AI Response received")


    ai_result = response.choices[0].message.content
    print("AI RAW OUTPUT:")
    print(ai_result)
    ai_result = ai_result.replace("```json", "")
    ai_result = ai_result.replace("```", "")

    return json.loads(ai_result)





# Read claims file

df = pd.read_excel(
    "Mock_Claims_Data.xlsx"
)

df["Revenue_Leakage"] = (
    df["Billed_Amount"] - df["Paid_Amount"]
)


df = df.sort_values(
    by="Revenue_Leakage",
    ascending=False
)


df = df.head(50)

df["Denial_Reason"] = df["Denial_Reason"].fillna("No Denial Recorded")
# Test one claim first

results = []

for index, claim in df.iterrows():

    ai_response = investigate_claim_with_ai(claim)

    results.append({
        "Claim_ID": claim["Claim_ID"],
        "Risk_Level": ai_response["Risk_Level"],
        "Investigation_Explanation": ai_response["Investigation_Explanation"],
        "Possible_Issue": ai_response["Possible_Issue"],
        "Recommended_Action": ai_response["Recommended_Action"]
   
})


output = pd.DataFrame(results)


output.to_excel(
    "AI_GenAI_Investigation_Structured.xlsx",
    index=False
)


print("AI_GenAI_Investigation_Structured Created Successfully")
