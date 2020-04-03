from django.db.models import Q


class StatusCollaboratorEnums:
    active = 'Activo'
    out = 'Dado de baja'

    @property
    def limit_choices_to(self):
        return Q(name=self.active) | Q(name=self.out)