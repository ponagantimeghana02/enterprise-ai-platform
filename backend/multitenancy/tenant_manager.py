from .tenant_config import TENANTS

class TenantManager:

    @staticmethod
    def get_tenant(tenant_id):

        if tenant_id not in TENANTS:
            raise Exception("Invalid Tenant")

        return TENANTS[tenant_id]