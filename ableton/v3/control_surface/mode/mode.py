# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\mode\mode.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ...base import depends, nop, task
from ...live import DetailViewController
from . import LayerModeBase, Mode
from .modes import ModesComponent

class EnablingAddLayerMode(LayerModeBase):
    pass

    @depends(parent_task_group=None)
    def __init__(self, parent_task_group=None, *a, **k):
        super().__init__(*a, **k)
        self._should_track_layers = not isinstance(self._component, ModesComponent) and (not hasattr(self._component, 'disable_layer_tracking')) and hasattr(self._component, 'num_layers')
        if self._should_track_layers:
            self._possibly_disable_component_task = parent_task_group.add(task.run(self._possibly_disable_component))
            self._possibly_disable_component_task.kill()

    def enter_mode(self):
        component = self._get_component()
        self._layer.grab(component)
        if not component.is_enabled():
            component.set_enabled(True)

    def leave_mode(self):
        component = self._get_component()
        self._layer.release(component)
        if self._should_track_layers:
            self._possibly_disable_component_task.restart()

    def _possibly_disable_component(self):
        component = self._get_component()
        if not component.num_layers:
            component.set_enabled(False)
            return

class CallFunctionMode(Mode):
    pass

    def __init__(self, on_enter_fn=nop, on_exit_fn=nop, *a, **k):
        super().__init__(*a, **k)
        self._on_enter_fn = on_enter_fn
        self._on_exit_fn = on_exit_fn

    def enter_mode(self):
        self._on_enter_fn()

    def leave_mode(self):
        self._on_exit_fn()

class ShowDetailClipMode(Mode):
    pass

    def __init__(self, application, *a, **k):
        super().__init__(*a, **k)
        detail_view_controller = DetailViewController(application)
        self.enter_mode = detail_view_controller.show
        self.leave_mode = detail_view_controller.restore