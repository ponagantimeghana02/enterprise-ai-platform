from datetime import datetime

audit_logs = []


def log_action(

        tenant_id,
        user,
        action

):

    audit_logs.append({

        "tenant": tenant_id,

        "user": user,

        "action": action,

        "time": datetime.now().isoformat()

    })


def get_logs():

    return audit_logs