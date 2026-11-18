# Retis

Interactive generator of Cisco IOS configuration scripts for routers and switches.

## Usage

```bash
poetry install
poetry run retis        # or: poetry run python -m retis
```

Pick a device, choose an output file (`output/<name>.txt|.cfg`) and add sections
(basic, interfaces, routing, VLAN, security). Each section is validated as you
type; the file is rewritten as one script:

```
configure terminal
...sections...
end
copy running-config startup-config
```

Press `U` in the device menu to undo the last section.

Note: scripts contain the passwords you enter in plain text (they are meant to be
pasted into a device), so `output/` is git-ignored.

## Layout

- `retis/generators/` – one class per section, filling `retis/templates/*.cfg`
- `retis/core/` – engine (registry and script assembly) and CLI
- `retis/utils/` – input validators and file handling