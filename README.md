# plex-updater

Dead simple updating for Plex channels, powered by GitHub.

## Usage

Copy `Contents/Code/updater.py` to your channel's `Contents/Code/`, and
in your `Contents/Code/__init__.py` add:

```python
import updater
updater.init(repo = 'owner/repo', branch = 'branch') # branch defaults to master

def PerformUpdate():
    return updater.PerformUpdate()

def MainMenu():
    container = ObjectContainer()
    # ...
    updater.add_button_to(container, PerformUpdate)
```

The update button will only appear when there is newer code in the
target branch on GitHub. When the user presses the button, the archive
will be downloaded and extracted to the expected `Plex Media
Server/Plug-ins` folder.

Should you want to add a discrete button to check for updates, just add
something that calls back to `updater.PerformUpdate`:

```python
import updater
updater.init(repo = 'owner/repo')

def PerformUpdate():
    return updater.PerformUpdate()

def MainMenu():
    container = ObjectContainer()
    # ...
    container.add(DirectoryObject(
        title = L('Check for updates'),
        key   = Callback(PerformUpdate)
    ))
```
