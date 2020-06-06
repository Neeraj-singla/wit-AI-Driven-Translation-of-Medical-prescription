from ibm_whcs_sdk import annotator_for_clinical_data as acd
from ibm_cloud_sdk_core.authenticators.iam_authenticator import IAMAuthenticator
import sys


def medical_annotators(text):
    api_key_annotator = '{api-key}'
    url_annotator = 'url-annotator'
    service = acd.AnnotatorForClinicalDataV1(
    authenticator=IAMAuthenticator(apikey=api_key_annotator), version='2020-06-03')
    service.set_service_url(url_annotator)
    flowId = "wh_acd.ibm_clinical_insights_v1.0_standard_flow"
    try:
        output_dict = {}
        response = service.analyze_with_flow(flowId, text)
        concepts = response.concepts
        for concept in concepts:
            print("Type: ", concept.type, "- Name: ", concept.preferred_name)
            output_dict[concept.type] = concept.preferred_name
        return output_dict

    except acd.ACDException as ex:
        print("Error Occurred: Code ", ex.code, " Message ", ex.message, " CorrelationId ", ex.correlation_id)


if __name__ == '__main__':
    text = """Patient notes no changes from last visit. Patient reports pain in their neck; lower back pain 5/10 and cewical pain 3-4/10. Patient denies any headahe or numbness/tingling. Exam procedures are not performed each visit unless otherwise stated. Discussed with the patient about taking Vitamin D 2000UI each day.
Past Medical History:
Anxiety, Arthritis, Bunions (distorted foot problem), High Blood Pressure, Insomnia, Sleep apnea
Current Medictions:
cyclobenzaprine 15 mg oral capsule 30 Capsule 2122/2017
traMADol 200 mg/24 hours oral capsule 30 Capsule 2/2212017
hydrochlorothiazide-losartan 12.5 mg-50 mg oral tablet 90 Tablet 1212912016
In Office Procedures:
G0283 Physical Therarpy Electrical stimulation for Medicare - reason: reduce muscle spasm, tissue perfusion, pain relief;
98941 CHIROPRACTIC MANIPULATION;
97035 Ultrasound therapy - Reason: reduce muscle spasm. tissue perfusion. pain relief;
97012 Mechanical Traction Therapy
97010 Hot or Cold Packs therapy - Reason: reduce muscle spasm, tissue perfusion, pain relief.
Family History:
Father had colon cancer, mother had COPD
ALLERGIES:
Compazine and Allegra.
Impressions:
Patient had an MRI of the back.
M99.03 Segmental and somatic dysfunction of lumbar region PoC - treat 3xlweek for 2 weeks.
M99.05 Segmental and somatic dysfunction of pelvic region PoC - treat 3x/week for 2 weeks.
S13.4XXA Sprain of ligaments of cervical spine. initial encounter PoC - treat 3x/week for 2 weeks.
S39.012A Strain of muscle, fascia and tendon of lower back, initial encounter PoC - treat 3x/week for 2 weeks."""
    output = medical_annotators(text)
    print(output)
