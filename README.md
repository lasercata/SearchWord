# SearchWord
Search for a word in multiple files with a command line interface (python3 argparse).

## Installing
Download the script `SearchWord.py` ;

Make it executable : 

```bash
$ chmod +x SearchWord.py
```

If your are on Linux, you can copy that script to the `/bin` folder to be able to run it from anywhere :
```bash
$ sudo cp SearchWord.py /bin/SearchWord
```

## Usage
```
$./SearchWord.py -h
usage: SearchWord [-h] [-v] [-p PATH] [-e EXTENSION] [-x EXCLUDE] [-sn] [-sl] [-w] [-s] word

Search for a word in multiple files.

positional arguments:
  word                  Word to search for

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Show SearchWord version and exit
  -p PATH, --path PATH  Path where to search. If not provided, search in current (".").
  -e EXTENSION, --extension EXTENSION
                        Format of the filenames extensions. Read only in the files with one of these
                        extensions. "," (comma, without spaces) between them.
  -x EXCLUDE, --exclude EXCLUDE
                        Patterns to exclude. "," (comma, without spaces) between them.
  -sn, --show_line_nb   Show line numbers where WORD was found in each file.
  -sl, --show_lines     Show the lines' content where WORD was found for each file.
  -w, --whole_word      Search only for complete word.
  -s, --silent          Hide files errors.

Examples :
        SearchWord word
        SearchWord "example of string" -e .py;.txt
        SearchWord someword -x .pyc -sn
```
