import pandas as pd


def investigate_claim(claim):

    billed = claim["Billed_Amount"]
    paid = claim["Paid_Amount"]
    denial = claim["Denial_Reason"]
    status = claim["Claim_Status"]

    leakage = billed - paid


    if leakage > 5000:
        risk = "HIGH"
    elif leakage > 2000:
        risk = "MEDIUM"
    else:
        risk = "LOW"


    if denial == "Coding Error":
        action = "Review CPT coding and provider documentation."

    elif denial == "Duplicate Claim":
        action = "Check duplicate billing history."

    elif denial == "Medical Necessity":
        action = "Validate medical documentation."

    else:
        action = "Perform standard claim review."


    return {

        "Claim_ID": claim["Claim_ID"],
        "Risk_Level": risk,
        "Revenue_Leakage": leakage,
        "Denial_Reason": denial,
        "Recommendation": action

    }



# Read Excel file

df = pd.read_excel("Mock_Claims_Data.xlsx")


results = []


for index, row in df.iterrows():

    result = investigate_claim(row)

    results.append(result)



# Convert output to dataframe

output = pd.DataFrame(results)


# Save AI output

output.to_excel(
    "AI_Investigation_Output.xlsx",
    index=False
)


print("AI Investigation Completed Successfully")

print(output.head())