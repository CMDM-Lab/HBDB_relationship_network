from openai import OpenAI
import os

# Ensure API key is set
# os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
# print(os.getenv('OPENAI_API_KEY'))

os.environ["OPENAI_API_KEY"] = "Your API KEY"

client = OpenAI()
# Path to save the response of gpt4o
# save_path = "./results/tmp"

def get_relationship_summary_and_score(context, term_a, term_b):
    # Define the prompt for GPT-4o-mini
    prompt = f"""
    You are tasked with evaluating the relationship between term_A and term_B in the context.
    Given a chemical or biological context, summarize the relationship between term_A and term_B, then provide a score reason and relevance score between 1 and 5. 

    **Key Fields of Interest:** Physiology, Biochemistry, Medicine, and Metabolism.

    **Score Definition:**
    - **Score 1**: term_A and term_B are mentioned, but there is no subsequent discussion of their relationship. They appear coincidentally in the context with no direct relevance.
    - **Score 2**: term_A and term_B are connected indirectly, sharing a general category or function, but their relationship is not detailed.
    - **Score 3**: term_A and term_B are moderately related, with some discussion of their interaction or shared significance in the context.
    - **Score 4**: term_A and term_B have a significant connection, backed by evidence or quantitative data, showing a clear relationship within the context.
    - **Score 5**: term_A and term_B are directly and highly relevant to each other, forming a critical relationship with strong contextual support, particularly in physiology, biochemistry, medicine, or metabolism.

    **Evaluation Steps:**
    1. Summarize the relationship between term_A and term_B in **100 words** based on the context.
    2. Explain your relevance score reason in **50 words**.
    3. Provide a relevance score between 1 and 5 for term_A and term_B.

    Score Examples:
    ### Score 1 example
    - **term_A**: acetone
    - **term_B**: toluene
    - **context**: We also hope to establish the relationships between molecule properties of VOCs and their adsorption on MIL-101, and to explore the underlying adsorption mechanisms. Chemicals Chromium nitrate nonahydrates (99+%), terephthalic acid (TPA) (99+%) and fluorhydric acid (HF) (40+%) were purchased from Sinopharm Chemical Reagent Co., Ltd. (China), Acros organic (USA) and Juhua Reagent Co., Ltd. (China), respectively; acetone (98+%), benzene (98+%), toluene (98+%) and ethylbenzene (98+%) were purchased from Hangzhou Chemical Reagent Co., Ltd (China); o-xylene (98+%), p-xylene (98+%) and m-xylene (98+%) were purchased from Sinopharm Chemical Reagent Co., Ltd. (China). These chemicals were used without any further purification. Selected properties of the VOCs are listed in Table 1 .Synthesis of MIL-101 MIL-101, the highly crystallized green powder of the chromium terephthalate, was synthesized according to the method described in the literature.
    - **summary**: In this context, acetone and toluene are mentioned as chemicals purchased from the same supplier, Hangzhou Chemical Reagent Co., Ltd (China), and both are specified to have a purity of 98+%. They are part of a list of chemicals used in the study, with no additional direct interactions or specific functional relationships described between them.
    - **score reason**: The score of 1 reflects a very low relationship because acetone and toluene are merely listed as chemicals purchased from the same supplier with similar purity, without any functional, chemical, or experimental relationship described in the context.

    ### Score 2 example
    - **term_A**: acetone
    - **term_B**: toluene
    - **context**: Very limited studies have demonstrated the feasibility of treating gas streams contaminated with chlorinated solvents using bioreactors. Wilson et al. (1988) performed a detailed study on biodegradation of TCE and 1,1,1-trichloroethane (TCA), in presence of n-butane, using mixed culture. Speitel and McLay (1993) investigated the suitability of biofilm reactors for the treatment of gas streams containing chlorinated solvents. Yoon and Park (2002) evaluated the performance of a biofilter packed with peat compost for treatment of a VOC mixture with concentration as follows (g/m3): benzene (4.5), toluene (15), m-xylene (15), o-xylene (15), styrene (15), chloroform (7.5), TCE (10), isoprene (4.5), and dimethyl sulfide (5). At an EBRT of 1.5 min and 32 °C, the removal efficiency was highest for isoprene (93%), and lowest for chloroform (84%). Earlier, Todd et al. (1996) also reported similar results. Den et al. (2003) investigated the transient and steady-state performance of a bench-scale biotrickling filter for the removal of an organic mixture of acetone, toluene, and trichloroethylene. Although many studies have been carried to improve the performance of BTF treating various pollutants, comprehensive studies have not been conducted for the performance evaluation of BTF treating mixtures of VOCs in pharmaceutical emissions. Also, the effect of chlorinated compounds such as chloroform on the performance of BTF treating hydrophobic and hydrophilic VOCs has not been studied.
    - **summary**: In this context, acetone and toluene are mentioned as components of an organic mixture treated in a biotrickling filter (BTF) by Den et al. (2003), along with trichloroethylene (TCE). Both acetone and toluene are volatile organic compounds (VOCs) targeted for removal in gas-phase biological treatment systems. The specific interaction or comparison between acetone and toluene was not deeply explored beyond their inclusion in a mixture for removal testing.
    - **score reason**: The score of 2 reflects a low to moderate relevance, as acetone and toluene are simply listed in the same sentence, indicating they are both volatile organic compounds (VOCs) present in the same study, but without any direct chemical or functional relationship to each other. Their relationship is more about their co-treatment rather than a significant chemical interaction.
    
    ### Score 3 example
    - **term_A**: acetone
    - **term_B**: cystic fibrosis 
    - **context**: Inflammatory mediators in the exhaled breath are receiving growing medical interest as noninvasive disease markers. Volatile organic compounds have been investigated in this context, but clinical information and methodological standards are limited. The levels of ethane, propane, n-pentane, methanol, ethanol, 2-propanol, acetone, isoprene, benzene, toluene, dimethyl sulphide (DMS) and limonene were measured in repeated breath samples from 20 cystic fibrosis patients and 20 healthy controls (aged 8-29 yrs). Three end-exhaled and one ambient air sample were collected per person and analysed on a customised gas chromatography system. Intra-subject coefficients of variation ranged between 9 and 34%, and hydrocarbon breath levels were influenced by their inspired concentrations. The alveolar gradient for pentane was higher in cystic fibrosis patients than in healthy controls (0.36 versus 0.21 ppb) and inversely proportional to forced expiratory volume in one second; highest values were observed in patients with pulmonary exacerbations (0.73 versus 0.24 ppb). Cystic fibrosis patients also exhibited a lower output of DMS (3.9 versus 7.6 ppb). Group differences were not significant for ethane and the remaining substances. It was concluded that chemical breath analysis for volatile organic compounds is feasible and may hold potential for the noninvasive diagnosis and follow-up of inflammatory processes in cystic fibrosis lung disease.
    - **summary**: In this context, acetone and cystic fibrosis are connected through the study of exhaled breath analysis as a noninvasive method for monitoring disease markers. Acetone, along with other volatile organic compounds (VOCs), was measured in the breath samples of cystic fibrosis patients and healthy controls to explore potential biomarkers for inflammation associated with cystic fibrosis. However, while acetone is one of the VOCs analyzed, it is not highlighted as having a significant difference between cystic fibrosis patients and controls, unlike other compounds like pentane and dimethyl sulfide (DMS).
    - **score reason**: The score of 3 reflects a moderate relevance, because while acetone is part of the broader VOC analysis relevant to cystic fibrosis, it is not specifically linked to the disease's inflammatory processes in the same way as other VOCs in the study.

    ### Score 4 example
    - **term_A**: CYP2E1
    - **term_B**: toluene
    - **context**: CYP2E1, an inducible enzyme present in different human tissues, metabolizes several potentially toxic substances including many volatile organic compounds (VOCs). One indirect way to monitor exposure to VOCs may be, therefore, the assessment of CYP2E1 activity in vivo using the chlorzoxazone (CHZ) test. Goal: To compare CYP2E1 activity in two groups of workers: one with a known occupational exposure to VOCs (exposed group) and the other employed in administrative tasks at two universities (control group) from the city of León, Guanajuato, México. Material and methods: (1) Passive diffusion monitors were used to evaluate individual levels of exposure to toluene, benzene and ethylbenzene in 48 persons (24 tannery workers and 24 administrative controls) during a 8 h work shift; (2) after 12 h fasting 500 mg CHZ, a selective probe for assessing CYP2E1 activity, was orally administered and, after 2 h, a venous blood sample was collected for HPLC plasmatic quantitative determination of CHZ and its mean metabolite 6-hydroxychlorzoxazone. Results: Toluene mean exposure levels were higher in the exposed group (2.86 ± 2 ppm vs. 0.05 ± 0.005 ppm; p < 0.001). Also, in this group CYP2E1 activity was lower (p < 0.05) and it decreased as the accumulated months of labor exposure increased (negative correlation, p < 0.05). These results are in line with previous findings obtained from shoemakers exposed to various solvents but, interestingly, they are partly in contrast with those of another study in printers. Conclusion: In spite of the relatively low levels of toluene exposure found for tannery workers, an effect on CYP2E1 activity was evident. Although the mechanism of this interaction is still unknown, the decrease in CYP2E1 activity per se might represent a health risk, considering that these workers may be less protected against other CYP2E1 substrates present in the labor setting or derived from an intentional exposure.
    - **summary**: In this context, the relationship between CYP2E1 and toluene is mentioned in the experiment methods, revealing that tannery workers with higher toluene exposure had significantly reduced CYP2E1 enzyme activity compared to controls. This decrease in activity correlated negatively with cumulative exposure duration, suggesting long-term exposure weakens CYP2E1's metabolic function. The lowered CYP2E1 activity may reduce metabolic defense against other toxic VOCs, potentially increasing health risks for these workers despite the relatively low exposure levels.
    - **score reason**: The score of 4 reflects a moderate to high relevance between toluene exposure and CYP2E1 enzyme activity. The study provides quantitative data supporting this association, indicating both a statistically significant reduction in enzyme activity and a potential occupational health risk. However, the uncertainty about the exact mechanisms prevents a higher score.

    ### Score 5 example
    - **term_A**: uric acid
    - **term_B**: metabolic syndrome
    - **context**: They breathed 100% O2 between 60th and 90thmin of the 4-h study protocol. Pulse wave augmentation index (AIx) at brachial and radial arteries, plasma antioxidant capacity (AOC), thiobarbituric acid-reactive substances (TBARS), lipid hydroperoxides (LOOH) assessed by xylenol orange method, UA and blood ethanol concentrations were determined before and 60, 90, 120, 150 and 240min after beverage consumption. Consumption of the beverages did not affect the AIx, TBARS or LOOH values during 60min before exposure to hyperoxia, while AOC and plasma UA increased except in the water group. Significant increase of AIx, plasma TBARS and LOOH, which occurred during 30min of hyperoxia in the water group, was largely prevented in the groups that consumed red wine, glycerol+ethanol or fructose. In contrast to chronic hyperuricemia, generally considered as a risk factor for cardiovascular diseases and metabolic syndrome, acute increase of UA acts protectively against hyperoxia-induced oxidative stress and related increase of arterial stiffness in large peripheral arteries.
    - **summary**: In this context, the study investigates the relationship between acute, food-induced increases in plasma uric acid (UA) and markers of arterial stiffness and oxidative damage. Temporary UA elevation, achieved by consuming red wine, ethanol + glycerol, or fructose, provided a protective effect against oxidative stress and arterial stiffness during hyperoxia exposure. This suggests a beneficial effect of short-term UA increase in reducing oxidative damage and arterial stiffness, contrasting with chronic hyperuricemia, which is typically linked to higher risks of cardiovascular disease and metabolic syndrome.
    - **score reason**: The score of 5 reflects a very strong relevance, as the context mentioned that chronic hyperuricemia, generally considered as a risk factor for metabolic syndrome. 'Chronic hyperuricemia' refers to a state of persistently high concentrations of uric acid in the body, so the word 'risk factor' means there are strong relationship between uric acid and metabolic syndrome.

    **Evaluation Target:**
    term_A: {term_a}
    term_B: {term_b}
    Context: "{context}"

    Output in JSON format:
    {{ 
        "summary": "<summarize the relationship between {term_a} and {term_b}>",
        "reason":"<score reason>",
        "score": <1-5>
    }}
    """
    # Use OpenAI's API to send the prompt to GPT-4o-mini
    completion = client.chat.completions.create(
        model="gpt-4o-mini", 
        response_format = {"type": "json_object"},
        messages=[ 
            {"role": "system", "content": """
            You are an expert assistant in chemistry and biology. Your primary skills include:
            - Analyzing relationships between chemical and biological terms.
            - Summarizing complex interactions succinctly.
            - Providing relevance scores based on contextual analysis.
            """},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        max_tokens=256
    )

    # Extract and return the response text
    llm_response = completion.choices[0].message.content.strip()
    print("Generating summary and score......")
    return llm_response