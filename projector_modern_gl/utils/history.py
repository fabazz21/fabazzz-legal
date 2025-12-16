"""
History / Undo-Redo System
"""

import copy


class Action:
    """Base class for undo/redo actions"""

    def __init__(self, action_type, data=None):
        """Initialize action"""
        self.action_type = action_type
        self.data = data or {}

    def execute(self):
        """Execute action (override in subclass)"""
        raise NotImplementedError

    def undo(self):
        """Undo action (override in subclass)"""
        raise NotImplementedError

    def __repr__(self):
        return f"<Action {self.action_type}>"


class TransformAction(Action):
    """Transform action (position, rotation, scale change)"""

    def __init__(self, obj, old_state, new_state):
        super().__init__('transform')
        self.obj = obj
        self.old_state = old_state
        self.new_state = new_state

    def execute(self):
        """Apply new state"""
        self.obj.position = copy.deepcopy(self.new_state['position'])
        self.obj.rotation = copy.deepcopy(self.new_state['rotation'])
        if 'scale' in self.new_state:
            self.obj.scale = copy.deepcopy(self.new_state['scale'])

    def undo(self):
        """Restore old state"""
        self.obj.position = copy.deepcopy(self.old_state['position'])
        self.obj.rotation = copy.deepcopy(self.old_state['rotation'])
        if 'scale' in self.old_state:
            self.obj.scale = copy.deepcopy(self.old_state['scale'])


class CreateObjectAction(Action):
    """Create object action"""

    def __init__(self, scene, obj):
        super().__init__('create_object')
        self.scene = scene
        self.obj = obj

    def execute(self):
        """Add object to scene"""
        self.scene.add_object(self.obj)

    def undo(self):
        """Remove object from scene"""
        self.scene.remove_object(self.obj)


class DeleteObjectAction(Action):
    """Delete object action"""

    def __init__(self, scene, obj):
        super().__init__('delete_object')
        self.scene = scene
        self.obj = obj

    def execute(self):
        """Remove object from scene"""
        self.scene.remove_object(self.obj)

    def undo(self):
        """Restore object to scene"""
        self.scene.add_object(self.obj)


class History:
    """History manager for undo/redo"""

    def __init__(self, max_size=50):
        """Initialize history"""
        self.max_size = max_size
        self.undo_stack = []
        self.redo_stack = []

    def push(self, action):
        """Add action to undo stack"""
        self.undo_stack.append(action)

        # Clear redo stack when new action is performed
        self.redo_stack.clear()

        # Limit undo stack size
        if len(self.undo_stack) > self.max_size:
            self.undo_stack.pop(0)

    def undo(self):
        """Undo last action"""
        if not self.can_undo():
            return False

        action = self.undo_stack.pop()
        action.undo()
        self.redo_stack.append(action)

        print(f"  ↶ Undone: {action.action_type}")
        return True

    def redo(self):
        """Redo last undone action"""
        if not self.can_redo():
            return False

        action = self.redo_stack.pop()
        action.execute()
        self.undo_stack.append(action)

        print(f"  ↷ Redone: {action.action_type}")
        return True

    def can_undo(self):
        """Check if undo is available"""
        return len(self.undo_stack) > 0

    def can_redo(self):
        """Check if redo is available"""
        return len(self.redo_stack) > 0

    def clear(self):
        """Clear all history"""
        self.undo_stack.clear()
        self.redo_stack.clear()

    def get_undo_count(self):
        """Get number of undo actions available"""
        return len(self.undo_stack)

    def get_redo_count(self):
        """Get number of redo actions available"""
        return len(self.redo_stack)
