from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .models import Tender, Requirement
from django.http import JsonResponse
from .serializers import TenderSerializer,RequirementSerializer
from django.views.decorators.csrf import csrf_exempt
import requests
import json


# Create your views here.
seller_certificate = [{
    "submitter": "Raksa Oy",
    "verification_status": True,
    "verification_details": "All data submitted verified and qualification criteria met.",
    "documents": [
        {
            "issuer": "PRH, Finland",
            "issuer_logo_url": "https://media-exp1.licdn.com/dms/image/C4D0BAQFiNcu9oQtTuQ/company-logo_200_200/0/1619676514255?e=2147483647&v=beta&t=_XxpFjPOQHqnm2WumeH8HNA1B2iZPxa3sp6b6ep6xvk",
            "presentation_record": {
                "data_agreement_template_id": "974c628b-83c4-4a22-a8c0-7b42169248ef",
                "presentation_request": {
                    "name": "Verify Certificate Of Registration",
                    "version": "1.0.0",
                    "requested_attributes": {
                            "additionalProp1": {
                                "name": "name",
                                "restrictions": [
                                    {
                                        "schema_id": "GsMTo44BktRxUFjRVxR1nL:2:Certificate Of Registration:2.0.0",
                                        "cred_def_id": "GsMTo44BktRxUFjRVxR1nL:3:CL:3878:default"
                                    }
                                ]
                            },
                        "additionalProp2": {
                                "name": "legalForm",
                                "restrictions": [
                                    {
                                        "schema_id": "GsMTo44BktRxUFjRVxR1nL:2:Certificate Of Registration:2.0.0",
                                        "cred_def_id": "GsMTo44BktRxUFjRVxR1nL:3:CL:3878:default"
                                    }
                                ]
                            },
                        "additionalProp3": {
                                "name": "activity",
                                "restrictions": [
                                    {
                                        "schema_id": "GsMTo44BktRxUFjRVxR1nL:2:Certificate Of Registration:2.0.0",
                                        "cred_def_id": "GsMTo44BktRxUFjRVxR1nL:3:CL:3878:default"
                                    }
                                ]
                            },
                        "additionalProp4": {
                                "name": "registrationDate",
                                "restrictions": [
                                    {
                                        "schema_id": "GsMTo44BktRxUFjRVxR1nL:2:Certificate Of Registration:2.0.0",
                                        "cred_def_id": "GsMTo44BktRxUFjRVxR1nL:3:CL:3878:default"
                                    }
                                ]
                            },
                        "additionalProp5": {
                                "name": "legalStatus",
                                "restrictions": [
                                    {
                                        "schema_id": "GsMTo44BktRxUFjRVxR1nL:2:Certificate Of Registration:2.0.0",
                                        "cred_def_id": "GsMTo44BktRxUFjRVxR1nL:3:CL:3878:default"
                                    }
                                ]
                            },
                        "additionalProp6": {
                                "name": "registeredAddress.fullAddress",
                                "restrictions": [
                                    {
                                        "schema_id": "GsMTo44BktRxUFjRVxR1nL:2:Certificate Of Registration:2.0.0",
                                        "cred_def_id": "GsMTo44BktRxUFjRVxR1nL:3:CL:3878:default"
                                    }
                                ]
                            },
                        "additionalProp7": {
                                "name": "registeredAddress.thoroughFare",
                                "restrictions": [
                                    {
                                        "schema_id": "GsMTo44BktRxUFjRVxR1nL:2:Certificate Of Registration:2.0.0",
                                        "cred_def_id": "GsMTo44BktRxUFjRVxR1nL:3:CL:3878:default"
                                    }
                                ]
                            },
                        "additionalProp8": {
                                "name": "registeredAddress.locatorDesignator",
                                "restrictions": [
                                    {
                                        "schema_id": "GsMTo44BktRxUFjRVxR1nL:2:Certificate Of Registration:2.0.0",
                                        "cred_def_id": "GsMTo44BktRxUFjRVxR1nL:3:CL:3878:default"
                                    }
                                ]
                            },
                        "additionalProp9": {
                                "name": "registeredAddress.postCode",
                                "restrictions": [
                                    {
                                        "schema_id": "GsMTo44BktRxUFjRVxR1nL:2:Certificate Of Registration:2.0.0",
                                        "cred_def_id": "GsMTo44BktRxUFjRVxR1nL:3:CL:3878:default"
                                    }
                                ]
                            },
                        "additionalProp10": {
                                "name": "registeredAddress.postName",
                                "restrictions": [
                                    {
                                        "schema_id": "GsMTo44BktRxUFjRVxR1nL:2:Certificate Of Registration:2.0.0",
                                        "cred_def_id": "GsMTo44BktRxUFjRVxR1nL:3:CL:3878:default"
                                    }
                                ]
                            },
                        "additionalProp11": {
                                "name": "registeredAddress.adminUnitLevel1",
                                "restrictions": [
                                    {
                                        "schema_id": "GsMTo44BktRxUFjRVxR1nL:2:Certificate Of Registration:2.0.0",
                                        "cred_def_id": "GsMTo44BktRxUFjRVxR1nL:3:CL:3878:default"
                                    }
                                ]
                            }
                    },
                    "requested_predicates": {

                    },
                    "nonce": "874945343276784245290789"
                },
                "updated_at": "2022-11-04 12:40:39.961960Z",
                "state": "verified",
                "thread_id": "8e3c0a44-7a13-45ae-ab6f-79afac6972b6",
                "auto_present": False,
                "presentation_request_dict": {
                    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0/request-presentation",
                    "@id": "8e3c0a44-7a13-45ae-ab6f-79afac6972b6",
                    "~data-agreement-context": {
                        "message_type": "protocol",
                        "message": {
                            "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/data-agreement-negotiation/1.0/offer",
                            "@id": "54029602-b670-41e3-8fac-848a4c7c0289",
                            "body": {
                                "@context": [
                                        "https://raw.githubusercontent.com/decentralised-dataexchange/automated-data-agreements/main/interface-specs/data-agreement-schema/v1/data-agreement-schema-context.jsonld",
                                        "https://w3id.org/security/v2"
                                ],
                                "id": "c550b259-4e0e-45f4-b9b0-821cbe847e2b",
                                "version": 1,
                                "template_id": "974c628b-83c4-4a22-a8c0-7b42169248ef",
                                "template_version": 1,
                                "data_controller_name": "Procurement Portal",
                                "data_controller_url": "https://procurementportal.se/policy.html",
                                "purpose": "Verify Certificate Of Registration",
                                "purpose_description": "To verify Certificate Of Registration credentials shared by Organisations.",
                                "lawful_basis": "consent",
                                "method_of_use": "data-using-service",
                                "data_policy": {
                                    "data_retention_period": 3,
                                    "policy_URL": "https://igrant.io/policy_default.html",
                                    "jurisdiction": "Stockholm, SE",
                                    "industry_sector": "Government",
                                    "geographic_restriction": "Europe",
                                    "storage_location": "Europe"
                                },
                                "personal_data": [
                                    {
                                        "attribute_id": "9ad4b55e-c827-4c49-824e-d8381423d5ac",
                                        "attribute_name": "name",
                                        "attribute_description": "Name"
                                    },
                                    {
                                        "attribute_id": "b9828584-59eb-4864-a715-421513156d22",
                                        "attribute_name": "legalForm",
                                        "attribute_description": "Legal Form"
                                    },
                                    {
                                        "attribute_id": "0d7ee295-4b2d-447e-9db9-487c348d93ba",
                                        "attribute_name": "activity",
                                        "attribute_description": "Activity"
                                    },
                                    {
                                        "attribute_id": "327541fa-f1a2-411c-84af-29ad5c30248b",
                                        "attribute_name": "registrationDate",
                                        "attribute_description": "Registration Date"
                                    },
                                    {
                                        "attribute_id": "d32da262-348e-4c1b-b01f-e34f9ea4ffeb",
                                        "attribute_name": "legalStatus",
                                        "attribute_description": "Legal status"
                                    },
                                    {
                                        "attribute_id": "a1f9d56c-7425-4985-bcc8-d6765148d266",
                                        "attribute_name": "registeredAddress.fullAddress",
                                        "attribute_description": "Full address"
                                    },
                                    {
                                        "attribute_id": "5f988913-aac8-4fa8-a1a1-51cb7f041c8d",
                                        "attribute_name": "registeredAddress.thoroughFare",
                                        "attribute_description": "Thorough fare"
                                    },
                                    {
                                        "attribute_id": "f9d58c6e-f1f7-437c-90c1-96017aebeb7b",
                                        "attribute_name": "registeredAddress.locatorDesignator",
                                        "attribute_description": "Locator designator"
                                    },
                                    {
                                        "attribute_id": "5facba7c-42be-4772-a686-1a0bd6cca796",
                                        "attribute_name": "registeredAddress.postCode",
                                        "attribute_description": "Postal code"
                                    },
                                    {
                                        "attribute_id": "0d40e6c2-3345-4548-8f6b-f69195783aaa",
                                        "attribute_name": "registeredAddress.postName",
                                        "attribute_description": "Postal name"
                                    },
                                    {
                                        "attribute_id": "0a93c771-584b-4a4e-b23e-0a4418bfb432",
                                        "attribute_name": "registeredAddress.adminUnitLevel1",
                                        "attribute_description": "Admin unit level 1"
                                    }
                                ],
                                "dpia": {
                                    "dpia_date": "2022-11-04T12:15:01.941+00:00",
                                    "dpia_summary_url": "https://privacyant.se/dpia_results.html"
                                },
                                "event": [
                                    {
                                        "id": "did:mydata:z6MkrFjtXE3R1U9hXibRWB9sZoqtgL8JTsU8nm1GP6TdcV5D#1",
                                        "time_stamp": "2022-11-04T12:40:36.629257+00:00",
                                        "did": "did:mydata:z6MkrFjtXE3R1U9hXibRWB9sZoqtgL8JTsU8nm1GP6TdcV5D",
                                        "state": "offer"
                                    }
                                ],
                                "proof": {
                                    "id": "did:mydata:z6MkrFjtXE3R1U9hXibRWB9sZoqtgL8JTsU8nm1GP6TdcV5D#1",
                                    "type": "Ed25519Signature2018",
                                    "created": "2022-11-04T12:40:36.635004+00:00",
                                    "verificationMethod": "did:mydata:z6MkrFjtXE3R1U9hXibRWB9sZoqtgL8JTsU8nm1GP6TdcV5D",
                                    "proofPurpose": "contractAgreement",
                                    "proofValue": "eyJhbGciOiAiRWREU0EiLCAiYjY0IjogZmFsc2UsICJjcml0IjogWyJiNjQiXX0..g33AH5sPCmgLIXFrhDKol5o1D5q6AB98AFFLgLNXipitGHsuS5bZqav0c27Io5KL3HDdS930GWQdKNUOhmchAQ"
                                },
                                "data_subject_did": "did:mydata:zAqA16eMvFjkdjwuu26nopLcgW"
                            },
                            "from": "did:mydata:z6MkrFjtXE3R1U9hXibRWB9sZoqtgL8JTsU8nm1GP6TdcV5D",
                            "to": "did:mydata:zAqA16eMvFjkdjwuu26nopLcgW",
                            "created_time": "1667565636660"
                        }
                    },
                    "request_presentations~attach": [
                        {
                            "@id": "libindy-request-presentation-0",
                            "mime-type": "application/json",
                            "data": {
                                "base64": "eyJuYW1lIjogIlZlcmlmeSBDZXJ0aWZpY2F0ZSBPZiBSZWdpc3RyYXRpb24iLCAidmVyc2lvbiI6ICIxLjAuMCIsICJyZXF1ZXN0ZWRfYXR0cmlidXRlcyI6IHsiYWRkaXRpb25hbFByb3AxIjogeyJuYW1lIjogIm5hbWUiLCAicmVzdHJpY3Rpb25zIjogW3sic2NoZW1hX2lkIjogIkdzTVRvNDRCa3RSeFVGalJWeFIxbkw6MjpDZXJ0aWZpY2F0ZSBPZiBSZWdpc3RyYXRpb246Mi4wLjAiLCAiY3JlZF9kZWZfaWQiOiAiR3NNVG80NEJrdFJ4VUZqUlZ4UjFuTDozOkNMOjM4Nzg6ZGVmYXVsdCJ9XX0sICJhZGRpdGlvbmFsUHJvcDIiOiB7Im5hbWUiOiAibGVnYWxGb3JtIiwgInJlc3RyaWN0aW9ucyI6IFt7InNjaGVtYV9pZCI6ICJHc01UbzQ0Qmt0UnhVRmpSVnhSMW5MOjI6Q2VydGlmaWNhdGUgT2YgUmVnaXN0cmF0aW9uOjIuMC4wIiwgImNyZWRfZGVmX2lkIjogIkdzTVRvNDRCa3RSeFVGalJWeFIxbkw6MzpDTDozODc4OmRlZmF1bHQifV19LCAiYWRkaXRpb25hbFByb3AzIjogeyJuYW1lIjogImFjdGl2aXR5IiwgInJlc3RyaWN0aW9ucyI6IFt7InNjaGVtYV9pZCI6ICJHc01UbzQ0Qmt0UnhVRmpSVnhSMW5MOjI6Q2VydGlmaWNhdGUgT2YgUmVnaXN0cmF0aW9uOjIuMC4wIiwgImNyZWRfZGVmX2lkIjogIkdzTVRvNDRCa3RSeFVGalJWeFIxbkw6MzpDTDozODc4OmRlZmF1bHQifV19LCAiYWRkaXRpb25hbFByb3A0IjogeyJuYW1lIjogInJlZ2lzdHJhdGlvbkRhdGUiLCAicmVzdHJpY3Rpb25zIjogW3sic2NoZW1hX2lkIjogIkdzTVRvNDRCa3RSeFVGalJWeFIxbkw6MjpDZXJ0aWZpY2F0ZSBPZiBSZWdpc3RyYXRpb246Mi4wLjAiLCAiY3JlZF9kZWZfaWQiOiAiR3NNVG80NEJrdFJ4VUZqUlZ4UjFuTDozOkNMOjM4Nzg6ZGVmYXVsdCJ9XX0sICJhZGRpdGlvbmFsUHJvcDUiOiB7Im5hbWUiOiAibGVnYWxTdGF0dXMiLCAicmVzdHJpY3Rpb25zIjogW3sic2NoZW1hX2lkIjogIkdzTVRvNDRCa3RSeFVGalJWeFIxbkw6MjpDZXJ0aWZpY2F0ZSBPZiBSZWdpc3RyYXRpb246Mi4wLjAiLCAiY3JlZF9kZWZfaWQiOiAiR3NNVG80NEJrdFJ4VUZqUlZ4UjFuTDozOkNMOjM4Nzg6ZGVmYXVsdCJ9XX0sICJhZGRpdGlvbmFsUHJvcDYiOiB7Im5hbWUiOiAicmVnaXN0ZXJlZEFkZHJlc3MuZnVsbEFkZHJlc3MiLCAicmVzdHJpY3Rpb25zIjogW3sic2NoZW1hX2lkIjogIkdzTVRvNDRCa3RSeFVGalJWeFIxbkw6MjpDZXJ0aWZpY2F0ZSBPZiBSZWdpc3RyYXRpb246Mi4wLjAiLCAiY3JlZF9kZWZfaWQiOiAiR3NNVG80NEJrdFJ4VUZqUlZ4UjFuTDozOkNMOjM4Nzg6ZGVmYXVsdCJ9XX0sICJhZGRpdGlvbmFsUHJvcDciOiB7Im5hbWUiOiAicmVnaXN0ZXJlZEFkZHJlc3MudGhvcm91Z2hGYXJlIiwgInJlc3RyaWN0aW9ucyI6IFt7InNjaGVtYV9pZCI6ICJHc01UbzQ0Qmt0UnhVRmpSVnhSMW5MOjI6Q2VydGlmaWNhdGUgT2YgUmVnaXN0cmF0aW9uOjIuMC4wIiwgImNyZWRfZGVmX2lkIjogIkdzTVRvNDRCa3RSeFVGalJWeFIxbkw6MzpDTDozODc4OmRlZmF1bHQifV19LCAiYWRkaXRpb25hbFByb3A4IjogeyJuYW1lIjogInJlZ2lzdGVyZWRBZGRyZXNzLmxvY2F0b3JEZXNpZ25hdG9yIiwgInJlc3RyaWN0aW9ucyI6IFt7InNjaGVtYV9pZCI6ICJHc01UbzQ0Qmt0UnhVRmpSVnhSMW5MOjI6Q2VydGlmaWNhdGUgT2YgUmVnaXN0cmF0aW9uOjIuMC4wIiwgImNyZWRfZGVmX2lkIjogIkdzTVRvNDRCa3RSeFVGalJWeFIxbkw6MzpDTDozODc4OmRlZmF1bHQifV19LCAiYWRkaXRpb25hbFByb3A5IjogeyJuYW1lIjogInJlZ2lzdGVyZWRBZGRyZXNzLnBvc3RDb2RlIiwgInJlc3RyaWN0aW9ucyI6IFt7InNjaGVtYV9pZCI6ICJHc01UbzQ0Qmt0UnhVRmpSVnhSMW5MOjI6Q2VydGlmaWNhdGUgT2YgUmVnaXN0cmF0aW9uOjIuMC4wIiwgImNyZWRfZGVmX2lkIjogIkdzTVRvNDRCa3RSeFVGalJWeFIxbkw6MzpDTDozODc4OmRlZmF1bHQifV19LCAiYWRkaXRpb25hbFByb3AxMCI6IHsibmFtZSI6ICJyZWdpc3RlcmVkQWRkcmVzcy5wb3N0TmFtZSIsICJyZXN0cmljdGlvbnMiOiBbeyJzY2hlbWFfaWQiOiAiR3NNVG80NEJrdFJ4VUZqUlZ4UjFuTDoyOkNlcnRpZmljYXRlIE9mIFJlZ2lzdHJhdGlvbjoyLjAuMCIsICJjcmVkX2RlZl9pZCI6ICJHc01UbzQ0Qmt0UnhVRmpSVnhSMW5MOjM6Q0w6Mzg3ODpkZWZhdWx0In1dfSwgImFkZGl0aW9uYWxQcm9wMTEiOiB7Im5hbWUiOiAicmVnaXN0ZXJlZEFkZHJlc3MuYWRtaW5Vbml0TGV2ZWwxIiwgInJlc3RyaWN0aW9ucyI6IFt7InNjaGVtYV9pZCI6ICJHc01UbzQ0Qmt0UnhVRmpSVnhSMW5MOjI6Q2VydGlmaWNhdGUgT2YgUmVnaXN0cmF0aW9uOjIuMC4wIiwgImNyZWRfZGVmX2lkIjogIkdzTVRvNDRCa3RSeFVGalJWeFIxbkw6MzpDTDozODc4OmRlZmF1bHQifV19fSwgInJlcXVlc3RlZF9wcmVkaWNhdGVzIjoge30sICJub25jZSI6ICI4NzQ5NDUzNDMyNzY3ODQyNDUyOTA3ODkifQ=="
                            }
                        }
                    ],
                    "comment": "To verify Certificate Of Registration credentials shared by Organisations."
                },
                "presentation": {
                    "proof": {
                        "proofs": [
                                {
                                    "primary_proof": {
                                        "eq_proof": {
                                            "revealed_attrs": {
                                                "activity": "36156805201336898515197930177279554392133345123455282686660289260173216831534",
                                                "legalform": "36156805201336898515197930177279554392133345123455282686660289260173216831534",
                                                "legalstatus": "36156805201336898515197930177279554392133345123455282686660289260173216831534",
                                                "name": "36156805201336898515197930177279554392133345123455282686660289260173216831534",
                                                "registeredaddress.adminunitlevel1": "36156805201336898515197930177279554392133345123455282686660289260173216831534",
                                                "registeredaddress.fulladdress": "36156805201336898515197930177279554392133345123455282686660289260173216831534",
                                                "registeredaddress.locatordesignator": "36156805201336898515197930177279554392133345123455282686660289260173216831534",
                                                "registeredaddress.postcode": "36156805201336898515197930177279554392133345123455282686660289260173216831534",
                                                "registeredaddress.postname": "36156805201336898515197930177279554392133345123455282686660289260173216831534",
                                                "registeredaddress.thoroughfare": "36156805201336898515197930177279554392133345123455282686660289260173216831534",
                                                "registrationdate": "36156805201336898515197930177279554392133345123455282686660289260173216831534"
                                            },
                                            "a_prime": "87940026864126185534291289478624114639606233297418477959668596980996717318282378998532385721737373400644564526160528467155713195755125346682889359111743608752113500516014704515144361034494883910576807987188708109055373840229298235790410695382857000243049956178892664420128885455102984694231586161460903371328823237533729275565662825908265910221081135143739141652898356790262916033339501654330518871153254629137080699372802650922556462846877418236504208063274767839817353766968446445856209634030648146210806018686239758327365128212505118725252776482175091822670910008630821863277713677015044547950729822344317152265422",
                                            "e": "112856210774359060033326391517620987955440984705400725176779981903246773580138151964927288656886731493913167045978502042940051231742616928",
                                            "v": "6122021912939951970380540962130775686017370578352318814894136371635588028094046457882772919277116054940179694142260513829076154744433927907637017325791483799394158190552285038236674344229110249727209396350800160490676881337378817293761926824536649874400336797864453104499136114510969507160547265657397631680407683707938589784654845994756125743123496680977847368958011219770344120121134963079953595061526994905890384638713177108365866314727401160918678914985626356581897814296805413324655526809763773912053702228111843799564093580263942508390162239862691496002537463733598346910095114983040763596144624556323747091989815737861460701512233403669089113342877437812633249740748708872454158039494202560077774915760132620145665302743595744461066785686857687019597257224673769654136004938555623860865508596865894111690733054939109465259711809131374130104493820163665643528383801130295648968165356609786128162189471147359816484",
                                            "m": {
                                                "master_secret": "2158399458160642007218434345803578597134368186799704341677573310966655466325751011689622951174405250065081782379739897167758961131444790492606408575060247718874878229410867688568"
                                            },
                                            "m2": "12428084018414822422921135335261996521961398530602062794240143402920665045272056606178811735901460138088505137749596739796310111869203714938041177844028356188052807122287701779182"
                                        },
                                        "ge_proofs": [

                                        ]
                                    },
                                    "non_revoc_proof": 'null'
                                }
                        ],
                        "aggregated_proof": {
                            "c_hash": "87803085415164662994439070917382043034643281662479849655046354718250116816812",
                            "c_list": [
                                [
                                    2,
                                    184,
                                    158,
                                    131,
                                    208,
                                    30,
                                    243,
                                    253,
                                    67,
                                    186,
                                    167,
                                    85,
                                    184,
                                    165,
                                    10,
                                    0,
                                    63,
                                    152,
                                    146,
                                    129,
                                    157,
                                    184,
                                    83,
                                    197,
                                    2,
                                    111,
                                    198,
                                    113,
                                    247,
                                    13,
                                    234,
                                    223,
                                    34,
                                    179,
                                    233,
                                    137,
                                    0,
                                    75,
                                    89,
                                    70,
                                    251,
                                    155,
                                    67,
                                    94,
                                    142,
                                    37,
                                    182,
                                    13,
                                    12,
                                    175,
                                    248,
                                    32,
                                    126,
                                    210,
                                    105,
                                    44,
                                    147,
                                    109,
                                    66,
                                    95,
                                    204,
                                    191,
                                    52,
                                    45,
                                    87,
                                    134,
                                    163,
                                    136,
                                    124,
                                    2,
                                    124,
                                    13,
                                    112,
                                    177,
                                    90,
                                    111,
                                    174,
                                    134,
                                    73,
                                    177,
                                    144,
                                    177,
                                    44,
                                    185,
                                    63,
                                    127,
                                    196,
                                    192,
                                    243,
                                    15,
                                    62,
                                    136,
                                    207,
                                    238,
                                    217,
                                    238,
                                    63,
                                    207,
                                    241,
                                    115,
                                    192,
                                    121,
                                    91,
                                    0,
                                    147,
                                    219,
                                    54,
                                    55,
                                    135,
                                    32,
                                    170,
                                    126,
                                    236,
                                    100,
                                    116,
                                    184,
                                    240,
                                    36,
                                    152,
                                    38,
                                    32,
                                    65,
                                    4,
                                    214,
                                    13,
                                    255,
                                    12,
                                    67,
                                    181,
                                    125,
                                    61,
                                    40,
                                    82,
                                    244,
                                    63,
                                    141,
                                    62,
                                    24,
                                    93,
                                    84,
                                    102,
                                    234,
                                    109,
                                    207,
                                    51,
                                    121,
                                    240,
                                    140,
                                    87,
                                    118,
                                    119,
                                    234,
                                    210,
                                    108,
                                    68,
                                    234,
                                    70,
                                    67,
                                    17,
                                    112,
                                    33,
                                    84,
                                    75,
                                    27,
                                    12,
                                    156,
                                    202,
                                    143,
                                    84,
                                    118,
                                    31,
                                    186,
                                    64,
                                    103,
                                    137,
                                    239,
                                    24,
                                    107,
                                    248,
                                    75,
                                    220,
                                    137,
                                    116,
                                    244,
                                    222,
                                    95,
                                    73,
                                    70,
                                    185,
                                    64,
                                    9,
                                    191,
                                    176,
                                    253,
                                    159,
                                    87,
                                    132,
                                    169,
                                    126,
                                    173,
                                    122,
                                    217,
                                    3,
                                    137,
                                    40,
                                    55,
                                    111,
                                    79,
                                    243,
                                    72,
                                    247,
                                    74,
                                    63,
                                    13,
                                    42,
                                    56,
                                    104,
                                    57,
                                    199,
                                    172,
                                    35,
                                    193,
                                    215,
                                    204,
                                    150,
                                    108,
                                    77,
                                    232,
                                    154,
                                    32,
                                    26,
                                    3,
                                    117,
                                    190,
                                    49,
                                    99,
                                    36,
                                    132,
                                    139,
                                    203,
                                    155,
                                    231,
                                    109,
                                    13,
                                    140,
                                    162,
                                    45,
                                    245,
                                    159,
                                    50,
                                    47,
                                    164,
                                    31,
                                    31,
                                    112,
                                    4,
                                    206
                                ]
                            ]
                        }
                    },
                    "requested_proof": {
                        "revealed_attrs": {
                            "additionalProp5": {
                                "sub_proof_index": 0,
                                "raw": "DEMO",
                                "encoded": "36156805201336898515197930177279554392133345123455282686660289260173216831534"
                            },
                            "additionalProp4": {
                                "sub_proof_index": 0,
                                "raw": "DEMO",
                                "encoded": "36156805201336898515197930177279554392133345123455282686660289260173216831534"
                            },
                            "additionalProp10": {
                                "sub_proof_index": 0,
                                "raw": "DEMO",
                                "encoded": "36156805201336898515197930177279554392133345123455282686660289260173216831534"
                            },
                            "additionalProp6": {
                                "sub_proof_index": 0,
                                "raw": "DEMO",
                                "encoded": "36156805201336898515197930177279554392133345123455282686660289260173216831534"
                            },
                            "additionalProp1": {
                                "sub_proof_index": 0,
                                "raw": "DEMO",
                                "encoded": "36156805201336898515197930177279554392133345123455282686660289260173216831534"
                            },
                            "additionalProp11": {
                                "sub_proof_index": 0,
                                "raw": "DEMO",
                                "encoded": "36156805201336898515197930177279554392133345123455282686660289260173216831534"
                            },
                            "additionalProp3": {
                                "sub_proof_index": 0,
                                "raw": "DEMO",
                                "encoded": "36156805201336898515197930177279554392133345123455282686660289260173216831534"
                            },
                            "additionalProp7": {
                                "sub_proof_index": 0,
                                "raw": "DEMO",
                                "encoded": "36156805201336898515197930177279554392133345123455282686660289260173216831534"
                            },
                            "additionalProp8": {
                                "sub_proof_index": 0,
                                "raw": "DEMO",
                                "encoded": "36156805201336898515197930177279554392133345123455282686660289260173216831534"
                            },
                            "additionalProp2": {
                                "sub_proof_index": 0,
                                "raw": "DEMO",
                                "encoded": "36156805201336898515197930177279554392133345123455282686660289260173216831534"
                            },
                            "additionalProp9": {
                                "sub_proof_index": 0,
                                "raw": "DEMO",
                                "encoded": "36156805201336898515197930177279554392133345123455282686660289260173216831534"
                            }
                        },
                        "self_attested_attrs": {

                        },
                        "unrevealed_attrs": {

                        },
                        "predicates": {

                        }
                    },
                    "identifiers": [
                        {
                            "schema_id": "GsMTo44BktRxUFjRVxR1nL:2:Certificate Of Registration:2.0.0",
                            "cred_def_id": "GsMTo44BktRxUFjRVxR1nL:3:CL:3878:default",
                            "rev_reg_id": 'null',
                            "timestamp": 'null'
                        }
                    ]
                },
                "data_agreement_id": "c550b259-4e0e-45f4-b9b0-821cbe847e2b",
                "initiator": "self",
                "trace": False,
                "created_at": "2022-11-04 12:40:36.594131Z",
                "verified": "true",
                "data_agreement_status": "accept",
                "connection_id": "baff5114-4a7b-47dc-8baa-7b5a8178a731",
                "presentation_exchange_id": "6d37d1ec-db85-4319-80ee-47178a8c452d",
                "data_agreement": {
                    "@context": [
                            "https://raw.githubusercontent.com/decentralised-dataexchange/automated-data-agreements/main/interface-specs/data-agreement-schema/v1/data-agreement-schema-context.jsonld",
                            "https://w3id.org/security/v2"
                    ],
                    "id": "c550b259-4e0e-45f4-b9b0-821cbe847e2b",
                    "version": 1,
                    "template_id": "974c628b-83c4-4a22-a8c0-7b42169248ef",
                    "template_version": 1,
                    "data_controller_name": "Procurement Portal",
                    "data_controller_url": "https://procurementportal.se/policy.html",
                    "purpose": "Verify Certificate Of Registration",
                    "purpose_description": "To verify Certificate Of Registration credentials shared by Organisations.",
                    "lawful_basis": "consent",
                    "method_of_use": "data-using-service",
                    "data_policy": {
                        "data_retention_period": 3,
                        "policy_URL": "https://igrant.io/policy_default.html",
                        "jurisdiction": "Stockholm, SE",
                        "industry_sector": "Government",
                        "geographic_restriction": "Europe",
                        "storage_location": "Europe"
                    },
                    "personal_data": [
                        {
                            "attribute_id": "9ad4b55e-c827-4c49-824e-d8381423d5ac",
                            "attribute_name": "name",
                            "attribute_description": "Name"
                        },
                        {
                            "attribute_id": "b9828584-59eb-4864-a715-421513156d22",
                            "attribute_name": "legalForm",
                            "attribute_description": "Legal Form"
                        },
                        {
                            "attribute_id": "0d7ee295-4b2d-447e-9db9-487c348d93ba",
                            "attribute_name": "activity",
                            "attribute_description": "Activity"
                        },
                        {
                            "attribute_id": "327541fa-f1a2-411c-84af-29ad5c30248b",
                            "attribute_name": "registrationDate",
                            "attribute_description": "Registration Date"
                        },
                        {
                            "attribute_id": "d32da262-348e-4c1b-b01f-e34f9ea4ffeb",
                            "attribute_name": "legalStatus",
                            "attribute_description": "Legal status"
                        },
                        {
                            "attribute_id": "a1f9d56c-7425-4985-bcc8-d6765148d266",
                            "attribute_name": "registeredAddress.fullAddress",
                            "attribute_description": "Full address"
                        },
                        {
                            "attribute_id": "5f988913-aac8-4fa8-a1a1-51cb7f041c8d",
                            "attribute_name": "registeredAddress.thoroughFare",
                            "attribute_description": "Thorough fare"
                        },
                        {
                            "attribute_id": "f9d58c6e-f1f7-437c-90c1-96017aebeb7b",
                            "attribute_name": "registeredAddress.locatorDesignator",
                            "attribute_description": "Locator designator"
                        },
                        {
                            "attribute_id": "5facba7c-42be-4772-a686-1a0bd6cca796",
                            "attribute_name": "registeredAddress.postCode",
                            "attribute_description": "Postal code"
                        },
                        {
                            "attribute_id": "0d40e6c2-3345-4548-8f6b-f69195783aaa",
                            "attribute_name": "registeredAddress.postName",
                            "attribute_description": "Postal name"
                        },
                        {
                            "attribute_id": "0a93c771-584b-4a4e-b23e-0a4418bfb432",
                            "attribute_name": "registeredAddress.adminUnitLevel1",
                            "attribute_description": "Admin unit level 1"
                        }
                    ],
                    "dpia": {
                        "dpia_date": "2022-11-04T12:15:01.941+00:00",
                        "dpia_summary_url": "https://privacyant.se/dpia_results.html"
                    },
                    "event": [
                        {
                            "id": "did:mydata:z6MkrFjtXE3R1U9hXibRWB9sZoqtgL8JTsU8nm1GP6TdcV5D#1",
                            "time_stamp": "2022-11-04T12:40:36.629257+00:00",
                            "did": "did:mydata:z6MkrFjtXE3R1U9hXibRWB9sZoqtgL8JTsU8nm1GP6TdcV5D",
                            "state": "offer"
                        },
                        {
                            "id": "did:mydata:z6MkjLRLkTiC5mgMVHWuwHgtQVhB2kdmLVyFgD11txLAu5w2#2",
                            "time_stamp": "2022-11-04T12:40:38.410518+00:00",
                            "did": "did:mydata:z6MkjLRLkTiC5mgMVHWuwHgtQVhB2kdmLVyFgD11txLAu5w2",
                            "state": "accept"
                        }
                    ],
                    "proofChain": [
                        {
                            "id": "did:mydata:z6MkrFjtXE3R1U9hXibRWB9sZoqtgL8JTsU8nm1GP6TdcV5D#1",
                            "type": "Ed25519Signature2018",
                            "created": "2022-11-04T12:40:36.635004+00:00",
                            "verificationMethod": "did:mydata:z6MkrFjtXE3R1U9hXibRWB9sZoqtgL8JTsU8nm1GP6TdcV5D",
                            "proofPurpose": "contractAgreement",
                            "proofValue": "eyJhbGciOiAiRWREU0EiLCAiYjY0IjogZmFsc2UsICJjcml0IjogWyJiNjQiXX0..g33AH5sPCmgLIXFrhDKol5o1D5q6AB98AFFLgLNXipitGHsuS5bZqav0c27Io5KL3HDdS930GWQdKNUOhmchAQ"
                        },
                        {
                            "id": "did:mydata:z6MkjLRLkTiC5mgMVHWuwHgtQVhB2kdmLVyFgD11txLAu5w2#2",
                            "type": "Ed25519Signature2018",
                            "created": "2022-11-04T12:40:38.413218+00:00",
                            "verificationMethod": "did:mydata:z6MkjLRLkTiC5mgMVHWuwHgtQVhB2kdmLVyFgD11txLAu5w2",
                            "proofPurpose": "contractAgreement",
                            "proofValue": "eyJhbGciOiAiRWREU0EiLCAiYjY0IjogZmFsc2UsICJjcml0IjogWyJiNjQiXX0..oN8AV-PU8UyIovIt6s7kGMyQS3bJuUiSjRq53Ampf17U3KWV-uJVdySCL4296R03sbIYwEsa7puCve9rP-zJCA"
                        }
                    ],
                    "data_subject_did": "did:mydata:zAqA16eMvFjkdjwuu26nopLcgW"
                },
                "role": "verifier"
            }
        }
    ]
}]


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def list_tenders(request):
    tenders = Tender.objects.all()
    response = []
    for tender in tenders:
        serializer = TenderSerializer(tender)
        tenderData = serializer.data
        requirement = Requirement.objects.filter(tender_id=tender.id)
        serializer = RequirementSerializer(requirement,many=True)
        requirementData = serializer.data
        tenderData['requirement'] = requirementData 
        tenderData['responses'] = seller_certificate 
        response.append(tenderData)

    return JsonResponse(response,safe=False)


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def get_tender(request, tender_id):
    tender = get_object_or_404(Tender, pk=tender_id)
    serializer = TenderSerializer(tender)
    tenderData = serializer.data
    requirement = Requirement.objects.filter(tender_id=tender.id)
    serializer = RequirementSerializer(requirement, many=True)
    requirementData = serializer.data
    tenderData['requirement'] = requirementData
    tenderData['responses'] = seller_certificate 
    return JsonResponse(tenderData)


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["POST"])
def publish_tender(request, tender_id):
    tender = get_object_or_404(Tender, pk=tender_id)
    tender.status = "PUBLISHED"
    tender.save()
    serializer = TenderSerializer(tender)
    tenderData = serializer.data
    requirement = Requirement.objects.filter(tender_id=tender.id)
    serializer = RequirementSerializer(requirement,many=True)
    requirementData = serializer.data
    tenderData['requirement'] = requirementData 
 
    return JsonResponse(tenderData)


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(["GET"])
def get_qualification_documents(request):
    response = {
        "qualification_documents": [
            {
                "schema_id": "GsMTo44BktRxUFjRVxR1nL:2:Certificate Of Registration:2.0.0",
                "cred_def_id": "GsMTo44BktRxUFjRVxR1nL:3:CL:3878:default",
                "issuer_label": "Bolagsverket, Sweden",
                "data_agreement_id": "974c628b-83c4-4a22-a8c0-7b42169248ef"
            }
        ]
    }
    return JsonResponse(response)



