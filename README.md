# plex-updater

Dead simple updating for Plex channels, powered by GitHub.

## Usage

Copy `Contents/Code/updater.py` to your channel's `Contents/Code/`, and
in your `Contents/Code/__init__.py` add:

```python
PLUGIN_PREFIX = '/video/my-channel'
import updater
updater.init(repo = 'owner/repo', branch = 'branch') # branch defaults to master

def MainMenu():
    container = ObjectContainer()
    # ...
    updater.add_button_to(container)
```

The update button will only appear when there is newer code in the
target branch on GitHub. When the user presses the button, the archive
will be downloaded and extracted to the expected `Plex Media
Server/Plug-ins` folder.

Note that you need to `import updater` *after* you have set `PLUGIN_PREFIX`. This is due to current framework limitations.

Should you want to add a discrete button to check for updates, just add
something that calls back to `updater.PerformUpdate`:

```python
PLUGIN_PREFIX = '/video/my-channel'
import updater
updater.init(repo = 'owner/repo')

def MainMenu():
    container = ObjectContainer()
    # ...
    container.add(DirectoryObject(
        title = L('Check for updates'),
        key   = Callback(updater.PerformUpdate)
    ))
```
