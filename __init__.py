import bpy
from bpy.types import AddonPreferences, PropertyGroup
from bpy.props import BoolProperty, StringProperty, CollectionProperty

REPOSITORIES = [
    {"name": "BlenderKit.com", "remote_url": "https://blenderkit.com/api/v1/extensions", "enabled": False, "description": "BlenderKit's official and community repository"},
    {"name": "Polygoniq.com", "remote_url": "https://extensions.polygoniq.com/api/v1/extensions", "enabled": False, "description": "Polygoniq's official repository"}
]


def repository_enabled_update(self, context):
    preferences = bpy.context.preferences
    remote_urls = [repo.remote_url for repo in preferences.extensions.repos]
    names = [repo.name for repo in preferences.extensions.repos]
    if self.enabled == True:
        if self.remote_url in remote_urls:
            return
        if self.name in names:
            return
        bpy.ops.preferences.extension_repo_add(name=self.name, remote_url=self.remote_url, type='REMOTE', use_sync_on_startup=self.use_sync_on_startup)
        return

    if self.remote_url in remote_urls:
        index = remote_urls.index(self.remote_url)
        bpy.ops.preferences.extension_repo_remove(index=index)
        return
    if self.name in names:
        index = names.index(self.name)
        bpy.ops.preferences.extension_repo_remove(index=index)
        return


def repository_sync_update(self, context):
    for repo in bpy.context.preferences.extensions.repos:
        if repo.name != self.name or repo.remote_url != self.remote_url:
            repo.use_sync_on_startup = self.use_sync_on_startup


class Repository(PropertyGroup):
    enabled: BoolProperty(name="Enabled", default=True, update=repository_enabled_update)
    name: StringProperty(name="Name")
    remote_url: StringProperty(name="URL")
    description: StringProperty(name="Description")
    use_sync_on_startup: BoolProperty(name="Sync", update=repository_sync_update)


class AwesomeReposPreferences(AddonPreferences):
    bl_idname = __name__
    repositories: CollectionProperty(type=Repository)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Enable remote repositories:")
        row.label(text="Sync on startup")
        for repo in self.repositories:
            row = layout.row()
            row.prop(repo, "enabled", text=f"{repo.name}: {repo.description}")
            row.prop(repo, "use_sync_on_startup")


def init_timer():
    prefs = bpy.context.preferences.addons[__name__].preferences
    pref_names = [pref.name for pref in prefs.repositories]
    pref_remote_urls = [pref.remote_url for pref in prefs.repositories]
    for REPO in REPOSITORIES:
        if REPO["name"] in pref_names or REPO["remote_url"] in pref_remote_urls:
            continue
        repo_item = prefs.repositories.add()
        repo_item.name = REPO["name"]
        repo_item.remote_url = REPO["remote_url"]
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
