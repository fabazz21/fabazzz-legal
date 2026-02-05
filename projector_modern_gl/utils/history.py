"""
Undo/Redo History System
"""

import copy


class HistoryAction:
    """Single action in history"""

    def __init__(self, name, undo_func, redo_func, undo_data=None, redo_data=None):
        """
        Initialize history action

        Args:
            name: Human-readable action name
            undo_func: Function to call for undo
            redo_func: Function to call for redo
            undo_data: Data to pass to undo function
            redo_data: Data to pass to redo function
        """
        self.name = name
        self.undo_func = undo_func
        self.redo_func = redo_func
        self.undo_data = undo_data
        self.redo_data = redo_data

    def undo(self):
        """Execute undo"""
        if self.undo_func:
            if self.undo_data is not None:
                self.undo_func(self.undo_data)
            else:
                self.undo_func()

    def redo(self):
        """Execute redo"""
        if self.redo_func:
            if self.redo_data is not None:
                self.redo_func(self.redo_data)
            else:
                self.redo_func()

    def __repr__(self):
        return f"<HistoryAction '{self.name}'>"


class History:
    """Undo/Redo history manager"""

    def __init__(self, max_history=100):
        """Initialize history"""
        self.actions = []
        self.current_index = -1
        self.max_history = max_history

    def add_action(self, action):
        """Add action to history"""
        # Remove any actions after current index
        if self.current_index < len(self.actions) - 1:
            self.actions = self.actions[:self.current_index + 1]

        # Add new action
        self.actions.append(action)
        self.current_index += 1

        # Limit history size
        if len(self.actions) > self.max_history:
            self.actions = self.actions[-self.max_history:]
            self.current_index = len(self.actions) - 1

        print(f"  ✅ Action added: {action.name}")

    def undo(self):
        """Undo last action"""
        if self.can_undo():
            action = self.actions[self.current_index]
            action.undo()
            self.current_index -= 1
            print(f"  ↶ Undo: {action.name}")
            return True
        else:
            print("  ⚠️ Nothing to undo")
            return False

    def redo(self):
        """Redo next action"""
        if self.can_redo():
            self.current_index += 1
            action = self.actions[self.current_index]
            action.redo()
            print(f"  ↷ Redo: {action.name}")
            return True
        else:
            print("  ⚠️ Nothing to redo")
            return False

    def can_undo(self):
        """Check if undo is possible"""
        return self.current_index >= 0

    def can_redo(self):
        """Check if redo is possible"""
        return self.current_index < len(self.actions) - 1

    def clear(self):
        """Clear all history"""
        self.actions.clear()
        self.current_index = -1
        print("  🗑️ History cleared")

    def get_undo_name(self):
        """Get name of action that would be undone"""
        if self.can_undo():
            return self.actions[self.current_index].name
        return None

    def get_redo_name(self):
        """Get name of action that would be redone"""
        if self.can_redo():
            return self.actions[self.current_index + 1].name
        return None

    def __repr__(self):
        return f"<History actions={len(self.actions)} index={self.current_index}>"


def create_property_change_action(obj, property_name, old_value, new_value):
    """
    Create a property change action for history

    Args:
        obj: Object whose property changed
        property_name: Name of the property
        old_value: Old value
        new_value: New value

    Returns:
        HistoryAction
    """
    def set_property(value):
        setattr(obj, property_name, copy.deepcopy(value))

    return HistoryAction(
        name=f"Change {property_name}",
        undo_func=set_property,
        redo_func=set_property,
        undo_data=old_value,
        redo_data=new_value
    )
