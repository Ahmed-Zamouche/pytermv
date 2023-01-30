 # pytermv

A terminal iptv player written in python

`pytermv` is a small python script that allows you to select an iptv stream using `fzf` and play it using `mpv`.

The list of channels is obtained from [https://iptv-org.github.io/](https://iptv-org.github.io/).


## Dependencies

- [`mpv`](https://mpv.io)
- [`fzf`](https://github.com/junegunn/fzf)
- [`pyfzf`](https://github.com/nk412/pyfzf)
- `git` (optional, for installation by cloning the repository)
- [`python 3`](https://www.python.org/downloads)
- `xdo` (optional, for `-s` flag)

## Usage

```console
usage: pytermv [-h] [-c CACHE_DIR] [-f] [-s] [-u]

What the program does

optional arguments:
  -h, --help            show this help message and exit
  -c CACHE_DIR, --cache-dir CACHE_DIR
                        path to cache directory
  -f, --full_screen     run in full-screen mode
  -s, --term_swallow    hide controlling terminal while playing
  -u, --update          update the channels database

Text at the bottom of help
```

## Installation

### Using installer

```sh
curl -sLf https://raw.githubusercontent.com/Ahmed-Zamouche/pytermv/main/install.sh | bash -s -- -install

```

### Cloning the repository

```sh
git clone https://github.com/Ahmed-Zamouche/pytermv.git "$HOME"/.pytermv
echo "PATH=\"\$HOME/.pytermv:\$PATH\"" >> "$HOME"/.bashrc
source "$HOME"/.bashrc 
```

## Uninstallation

### Using installer

```sh
curl -sLf https://raw.githubusercontent.com/Ahmed-Zamouche/pytermv/main/install.sh | bash -s -- --uinstall

```

### Manualy 

```sh
rm -rf "$HOME"/.pytermv
sed -i '/pytermv/d' "$HOME"/.bashrc
```

## Credits

A big thank you to all the [`contributors`](https://github.com/Ahmed-Zamouche/pytermv/graphs/contributors)

Thanks to [`termv`](https://github.com/Roshan-R/termv) for player
