from transactions.models import InstitutionQuotesTypeRegister


class ShoppingCartManager:

    @staticmethod
    def get_quota_balance(type_registries_id, institution_id):
        try:
            return InstitutionQuotesTypeRegister.objects.get(
                institution_id=institution_id,
                type_register_id=type_registries_id
            ).quotas_balance
        except:
            return 0

    @staticmethod
    def get_quota_sum(shopping_cart: dict or None):
        try:
            quotas = 0

            if shopping_cart is None:
                return 0

            for k, v in shopping_cart.items():
                quotas += int(v)

            return quotas

        except:
            return 0