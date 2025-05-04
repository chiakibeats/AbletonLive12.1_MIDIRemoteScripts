# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\live\detail_view_controller.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

class DetailViewController:
    pass

    def __init__(self, application, show_clip=True, *a, **k):
        super().__init__(*a, **k)
        self._did_show = False
        self._app_view = application.view
        self._detail_was_visible = False
        self._sub_view_was_visible = False
        self._sub_view_name = 'Detail/{}'.format('Clip' if show_clip else 'DeviceChain')

    def show(self):
        pass
        self._detail_was_visible = self._app_view.is_view_visible('Detail')
        self._sub_view_was_visible = self._app_view.is_view_visible(self._sub_view_name, False)
        if not self._sub_view_was_visible:
            self._app_view.show_view(self._sub_view_name)
        self._did_show = True

    def restore(self):
        pass
        if self._did_show:
            if not self._detail_was_visible:
                self._app_view.hide_view('Detail')
            elif not self._sub_view_was_visible:
                self._app_view.hide_view(self._sub_view_name)
        self._did_show = False