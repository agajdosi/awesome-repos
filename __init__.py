import bpy
from bpy.types import AddonPreferences, PropertyGroup
from bpy.props import BoolProperty, StringProperty, CollectionProperty

REPOSITORIES = [
    {"name": "BlenderKit.com", "remote_path": "https://blenderkit.com/api/v1/extensions", "enabled": False, "description": "Production repository"},
    {"name": "devel.BlenderKit.com", "remote_path": "https://devel.blenderkit.com/api/v1/extensions", "enabled": True, "description": "Development repository"},
    {"name": "staging.BlenderKit.org", "remote_path": "https://staging.blenderkit.com/api/v1/extensions", "enabled": False, "description": "Staging repository"},
]

def repository_enabled_update(self, context):
    preferences = bpy.context.preferences    
    remote_paths = [repo.remote_path for repo in preferences.filepaths.extension_repos]
    names = [repo.name for repo in preferences.filepaths.extension_repos]
    if self.enabled == True:
        if self.remote_path in remote_paths or self.name in names:
            return
        bpy.ops.preferences.extension_repo_add(name=self.name, remote_path=self.remote_path, type='REMOTE')
        return

    if self.remote_path in remote_paths:
        index = remote_paths.index(self.remote_path)
        bpy.ops.preferences.extension_repo_remove(index=index)
        return
    if self.name in names:
        index = names.index(self.name)
        bpy.ops.preferences.extension_repo_remove(index=index)
        return

class Repository(PropertyGroup):
    enabled: BoolProperty(name="Enabled", default=True, update=repository_enabled_update)
    name: StringProperty(name="Name")
    remote_path: StringProperty(name="URL")
    description: StringProperty(name="Description")

class AwesomeReposPreferences(AddonPreferences):
    bl_idname = __name__
    repositories: CollectionProperty(type=Repository)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Enable remote repositories:")
        for repo in self.repositories:
            row = layout.row()
            row.prop(repo, "enabled", text=f"{repo.name}: {repo.description}")

def init_timer():
    prefs = bpy.context.preferences.addons[__name__].preferences
    pref_names = [pref.name for pref in prefs.repositories]
    pref_remote_paths = [pref.remote_path for pref in prefs.repositories]
    for REPO in REPOSITORIES:
        if REPO["name"] in pref_names or REPO["remote_path"] in pref_remote_paths:
            continue
        repo_item = prefs.repositories.add()
        repo_item.name = REPO["name"]
        repo_item.remote_path = REPO["remote_path"]
        repo_item.description = REPO["description"]
        repo_item.enabled = REPO.get("enabled", True)
    
    return None 


def register():
    bpy.utils.register_class(Repository)
    bpy.utils.register_class(AwesomeReposPreferences)
    bpy.app.timers.register(init_timer, first_interval=0.1)

def unregister():
    bpy.utils.unregister_class(AwesomeReposPreferences)
    bpy.utils.unregister_class(Repository)
    if bpy.app.timers.is_registered(init_timer):
        bpy.app.timers.unregister(init_timer)
