knowledge_bases = {

    "tenant_a": [
        "Employee Policy",
        "Leave Rules",
        "Payroll Guide"
    ],

    "tenant_b": [
        "Python Coding Standards",
        "System Design",
        "Microservices"
    ],

    "tenant_c": [
        "Refund Policy",
        "Customer FAQ",
        "Support Handbook"
    ]

}


def get_documents(tenant_id):

    return knowledge_bases.get(
        tenant_id,
        []
    )