from . import structures as structs


class ProcessMixin(object):
    """Mixin class which provides model specific logic to data structures."""
    pass


class FlatProcess(ProcessMixin, structs.FlatNode):
    pass


class ListProcess(ProcessMixin, structs.ListNode):
    pass


class NestedProcess(ProcessMixin, structs.NestedNode):
    pass


class Strategy(object):
    """Class which defines params by which algorithm
    can choose which way is the best.
    """
    flat_priority = None
    nested_priority = None
