# Fluffy Snips

CLI tools that I find useful

## Installation

```bash
pip install fluffysnips
```

## Commands

### mvscreenshot

Move your most recent screenshot to a destination

```bash
Usage: mvscreenshot [OPTIONS] DESTINATION

Arguments:
  DESTINATION  [required]

Options:
  -m      Print markdown to use image  [default: False]
  --help  Show this message and exit.
```

Example
```bash
$ mvscreenshot pictures/example_1
Screenshot from 18 hours ago
Move to: /home/user/current/directory/pictures/example_1.png
Confirm [Y/n]: y
```
