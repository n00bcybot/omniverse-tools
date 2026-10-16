# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

# Below - a simple extension for adding Xform as a parent to selected meshes

import omni.usd
import omni.ext
import omni.ui as ui
from pxr import Sdf, UsdGeom


# Any class derived from `omni.ext.IExt` in the top level module (defined in
# `python.modules` of `extension.toml`) will be instantiated when the extension
# gets enabled, and `on_startup(ext_id)` will be called. Later when the
# extension gets disabled on_shutdown() is called.

class MyExtension(omni.ext.IExt):

    # ext_id is the current extension id. It can be used with the extension
    # manager to query additional information, like where this extension is
    # located on the filesystem.
    def on_startup(self, _ext_id):
        """This is called every time the extension is activated."""
        print("[my_company.my_python_ui_extension] Extension startup")

        self._count = 0
        self._window = ui.Window("Add Xform", width=300, height=300)

        with self._window.frame:
            with ui.VStack():
                def print_selection():

                    # Get the current USD Context
                    usd_context = omni.usd.get_context()
                    stage = usd_context.get_stage()

                    # Get the paths of all currently selected prims
                    selected_paths = usd_context.get_selection().get_selected_prim_paths()

                    try:
                        # If selected_paths is empty or None, raise an IndexError or ValueError.
                        if not selected_paths:
                            raise ValueError("Nothing selected")

                        for path in selected_paths:

                            # Prepare paths
                            prim_path = Sdf.Path(path)
                            prim = stage.GetPrimAtPath(path)

                            if not prim.IsValid():
                                print(f"Prim at path {prim_path} NOT valid!")
                                continue
                            else:
                                print(f"Prim at path {prim_path} is valid!")

                            xform_path = prim_path.GetParentPath().AppendChild(prim_path.name + "_Xform")
                            dest_path = xform_path.AppendChild(prim_path.name)

                            # Create Xforms
                            UsdGeom.Xform.Define(stage, Sdf.Path(xform_path))

                            # Move prims under the Xforms
                            omni.kit.commands.execute("MovePrimCommand", path_from=path, path_to=dest_path)

                    except ValueError:
                        print("Nothing selected")

                    # for path in paths_list:

                with ui.HStack():
                    ui.Button("Add Xform", clicked_fn=print_selection)
