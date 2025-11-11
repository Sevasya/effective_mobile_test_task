from users.models import AccessRoleRule, BusinessElement


def has_permission(user, element_name, action, own_object=False):
    """
    Проверяет, есть ли у пользователя доступ к действию на объекте
    action: 'read', 'create', 'update', 'delete'
    own_object: True если проверка на свои объекты
    """
    if not user or not user.is_active or not user.role:
        return False

    try:
        element = BusinessElement.objects.get(name=element_name)
        rule = AccessRoleRule.objects.get(role=user.role, element=element)
    except (BusinessElement.DoesNotExist, AccessRoleRule.DoesNotExist):
        return False

    if own_object:
        return getattr(rule, f"{action}_permission", False)
    return getattr(rule, f"{action}_all_permission", False)