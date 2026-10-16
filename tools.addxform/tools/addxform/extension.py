# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
import omni.ext
import omni.ui as ui
import omni.kit.ui

# Any class derived from 'omni.ext.IExt' in top level module (defined in 'python.modules' of 'extension.toml') will be instantiated when Extension gets enabled and 'on_startup(ext_id)' will be called. Later when Extension gets disabled 'on_shutdown()' is called.
class MyExtension(omni.ext.IExt):
    # ext_id is current Extension id. It can be used with Extension manager to query additional information, like where this Extension is located on filesystem.
    def on_startup(self, ext_id):
        # Initialize some properties
        self._count = 0
        self._window = None
        self._menu = None
        # Create a menu item inside the already existing "Window" menu.
        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            self._menu = editor_menu.add_item("Window/Add Xform", self.show_window, toggle=True, value=False)
    def on_shutdown(self):
        self._window = None
        self._menu = None
    def show_window(self, menu_path: str, visible: bool):
        if visible:
            # Create window
            self._window = ui.Window("Add Xform", width=300, height=300)
            with self._window.frame:
                with ui.VStack():
                    label = ui.Label("")
                    def on_click():
                        self._count += 1
                        label.text = f"count: {self._count}"
                    def on_reset():
                        self._count = 0
                        label.text = "not empty"
                    on_reset()
                    with ui.HStack():
                        ui.Button("Increase", clicked_fn=on_click)
                        ui.Button("Reset", clicked_fn=on_reset)
            self._window.set_visibility_changed_fn(self._visiblity_changed_fn)
        elif self._window:
            # Remove window
            self._window = None
            self._count = 0
        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            editor_menu.set_value("Window/Add Xform", visible)
    def _visiblity_changed_fn(self, visible):
        editor_menu = omni.kit.ui.get_editor_menu()
        if editor_menu:
            # Toggle the checked state of the menu item
            editor_menu.set_value("Window/Add Xform", visible)

