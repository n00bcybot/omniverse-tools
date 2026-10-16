# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import omni.usd
import omni.ext
import omni.ui as ui
from pxr import Sdf, UsdGeom


# Functions and vars are available to other extensions as usual in python:
# `my_company.my_python_ui_extension.some_public_function(x)`
def some_public_function(x: int):
    """This is a public function that can be called from other extensions."""
    print(f"[my_company.my_python_ui_extension] some_public_function was called with {x}")
    return x ** x


# Any class derived from `omni.ext.IExt` in the top level module (defined in
# `python.modules` of `extension.toml`) will be instantiated when the extension
# gets enabled, and `on_startup(ext_id)` will be called. Later when the
# extension gets disabled on_shutdown() is called.
def on_shutdown():
    """This is called every time the extension is deactivated. It is used
    to clean up the extension state."""
    print("[my_company.my_python_ui_extension] Extension shutdown")


class MyExtension(omni.ext.IExt):
    """This extension manages a simple counter UI."""

    # ext_id is the current extension id. It can be used with the extension
    # manager to query additional information, like where this extension is
    # located on the filesystem.
    def on_startup(self, _ext_id):
        """This is called every time the extension is activated."""
        print("[my_company.my_python_ui_extension] Extension startup")

        self._count = 0
        self._window = ui.Window(
            "Add Xform", width=300, height=300
        )
        with self._window.frame:
            with ui.VStack():
                def print_selection():

                    # Get the current USD Context
                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()

                    # Get the paths of all currently selected prims
                    selected_paths = usd_context.get_selection().get_selected_prim_paths()

                    paths_list = []
                    prims_names = []
                    parent_paths = []

                    try:
                        # If selected_paths is empty or None, raise an IndexError or ValueError.
                        if not selected_paths:
                            raise ValueError("Nothing selected")

                        for path in selected_paths:

                            path = str(path)
                            paths_list.append(path)

                            prim = stage.GetPrimAtPath(path)
                            parent_path = prim.GetPath().GetParentPath()
                            parent_paths.append(parent_path)

                            if prim.IsValid():
                                prim_name = prim.GetName()
                                prims_names.append(prim_name)

                    except ValueError:
                        print("Nothing selected")

                    for path, j, z in zip(paths_list, parent_paths, prims_names):
                        xform_path = path + "_Xform"
                        UsdGeom.Xform.Define(stage, Sdf.Path(xform_path))
                        dest_path = xform_path + "/" + z
                        omni.kit.commands.execute('MovePrimCommand',
                                                  path_from=path,
                                                  path_to=dest_path,
                                                  keep_world_transform=True,
                                                  destructive=True
                                                  )

                with ui.HStack():
                    ui.Button("Add Xform", clicked_fn=print_selection)
