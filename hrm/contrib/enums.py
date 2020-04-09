from hrm.collaborator.enums import StatusCollaboratorEnums
from hrm.payroll.enums import StatusPayrollEnums


class TypePayrollEnums:
    biweekly = 'Quincenal'


class StatusEnums:
    collaborator = StatusCollaboratorEnums()
    payroll = StatusPayrollEnums()