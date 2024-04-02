import bpy


class Repository():
    def __init__(self, name, remote_path):
        self.name = name
        self.remote_path = remote_path

REPOSITORIES = [
    Repository("BlenderKit.com", "https://blenderkit.com"),
]

def load_repositories():
    preferences = bpy.context.preferences    
    remote_paths = [repo.remote_path for repo in preferences.filepaths.extension_repos]
    names = [repo.name for repo in preferences.filepaths.extension_repos]
    for repo in REPOSITORIES:
        if repo.name in names:
                continue # already added
        if repo.remote_path in remote_paths:
                continue # already added
        bpy.ops.preferences.extension_repo_add(name=repo.name, remote_path=repo.remote_path, type='REMOTE')

    return


def register():
    bpy.app.timers.register(load_repositories, first_interval=0.1)


def unregister():
    if bpy.app.timers.is_registered(load_repositories):
        bpy.app.timers.unregister(load_repositories)
