#!/bin/python3
# -*- coding: utf-8 -*-

'''This script allow you to search for a word in several files'''

auth = 'Lasercata'
last_update = '2021.04.05'
version = '1.0'


##-import
from os import system, walk, stat
from os import chdir, mkdir, getcwd
from os.path import exists, abspath

import argparse


##-ini
alf = 'abcdefghijklmnopqrstuvwxyz'


##-Useful function
def set_prompt(lst):
    '''
    Return a str organized correctly to print.
    'lst' should be a list, a tuple, or a set.
    '''

    ret = ''
    for k in lst:
        ret += str(k)

        if k != lst[-1]:
            ret += ', '

    return ret

def ind(s, word):
    '''Return the indexes of word in s.'''
    
    nb = s.count(word)
    idx = [s.find(word)]
    
    for k in range(1, nb):
        idx.append(s[idx[k - 1] + 1:].find(word))
    
    return idx


##-main
class SearchWord:
    '''Class which help to search for a word in multiple files.'''
    
    def __init__(self, word, path='.', ext=[], exclude=[], whole_word=False, hide_err=False):
        '''
        Initiate SearchWord.
        
        - word : The word to search for ;
        - path : The path where to search ;
        - ext : The list of extensions of the files (search only in these ones) ;
        - exclude : The list of filenames' patterns to exclude ;
        - whole_word : If True, search only for whole words ;
        - hide_err : A bool indicating if hide files errors.
        '''
        
        if not exists(path):
            raise ValueError('SearchWord: Path "{}" not found'.format(path))
        
        elif True in [type(k) not in (list, tuple, set) for k in (ext, exclude)]:
            raise ValueError('`ext` and `exclude` should be lists, tuple, or sets, but different found (ext: {}, exclude: {})'.format(type(ext), type(exclude)))
        
        self.word = word
        self.path = path
        self.ext = ext
        self.exclude = exclude
        self.whole_word = whole_word
        self.hide_err = hide_err
        
    
    def search(self):
        '''Search for word `word` in the files in the path.'''

        ret = {} #dict of the form : {'filename1': [(l_nb1, line1), (l_nb2, line2), ...], ...}
        cond = True

        for r, d, f in walk(self.path):
            for fn in f:
                #print(fn)
                
                if ((True in [fn[-len(k):] == k for k in self.ext]) or (self.ext == [])) and (True not in [k in fn for k in self.exclude]):
                    #print(fn)
                    
                    try:
                        with open(r + '/' + fn, 'r') as file_:
                            for l_nb, line in enumerate(file_):                                
                                if self.word in line:
                                    if self.whole_word:
                                        idx = ind(line, self.word)
                                        cond = True in [not(line[k - 1] in alf or line[k + len(self.word) + 1] in alf) for k in idx]
                                    
                                    if cond:
                                        try:
                                            ret[r + '/' + fn].append((l_nb, line.strip('\n')))
                                        except KeyError:
                                            ret[r + '/' + fn] = [(l_nb, line.strip('\n'))]
                    
                    except Exception as err:
                        if not self.hide_err:
                            print('SearchWord: file "{}": {}'.format(fn, err))

        return ret


    def gsearch(self, show_l_nb=True, show_lines=False):
        '''
        Use self.search and print the result to stdout.
        
        - show_l_nb : A bool indicating if show the line number where the word was found.
        - show_lines : A bool indicating if show the line in which the word was found.
        '''
        
        d = self.search()
        
        if len(d) == 0:
            print('The word "{}" was not found in "{}"'.format(self.word, abspath(self.path)))
            return None #Stop.
        
        else:
            print('Word "{}" found in these files :\n'.format(self.word))
        
        for fn in d:
            if not(show_l_nb or show_lines):
                print('\t' + fn)
            
            elif show_l_nb and (not show_lines):
                print('\t- ' + fn)
                print('\t\tLines # {}.\n'.format(set_prompt([d[fn][k][0] for k in range(len(d[fn]))])))
            
            else:
                print('\t- ' + fn)
                for k in d[fn]:
                    print('\t\tLine #{} : "{}"'.format(k[0], k[1]))
                
                print('')


##-Using interface
class Parser:
    '''Class which allow to use SearchWord in command-line.'''

    def __init__(self):
        '''Initiate Parser'''

        self.parser = argparse.ArgumentParser(
            prog='SearchWord',
            description='Search for a word in multiple files.',
            epilog='Examples :\n\tSearchWord word\n\tSearchWord "example of string" -e .py;.txt\n\tSearchWord someword -x .pyc -sn',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        self.parser.add_argument(
            'word',
            help='Word to search for'
        )

        self.parser.add_argument(
            '-v', '--version',
            help='Show SearchWord version and exit',
            nargs=0,
            action=self.Version
        )

        self.parser.add_argument(
            '-p', '--path',
            help='Path where to search. If not provided, search in current (".").'
        )

        self.parser.add_argument(
            '-e', '--extension',
            help='Format of the filenames extensions. Read only in the files with one of these extensions. "," (comma, without spaces) between them.'
        )

        self.parser.add_argument(
            '-x', '--exclude',
            help='Patterns to exclude. "," (comma, without spaces) between them.'
        )

        self.parser.add_argument(
            '-sn', '--show_line_nb',
            help='Show line numbers where WORD was found in each file.',
            action='store_true'
        )

        self.parser.add_argument(
            '-sl', '--show_lines',
            help="Show the lines' content where WORD was found for each file.",
            action='store_true'
        )

        self.parser.add_argument(
            '-w', '--whole_word',
            help="Search only for complete word.",
            action='store_true'
        )

        self.parser.add_argument(
            '-s', '--silent',
            help="Hide files errors.",
            action='store_true'
        )


    def parse(self):
        '''Parse the args'''

        #------Get arguments
        args = self.parser.parse_args()

        #---ext, exclude, path
        if args.extension == None:
            ext = []
        else:
            ext = args.extension.split(',')
        
        if args.exclude == None:
            exclude = []
        else:
            exclude = args.exclude.split(',')
        
        path = (args.path, '.')[args.path == None]

        #------Search
        Searcher = SearchWord(args.word, path, ext, exclude, args.whole_word, args.silent)
        
        Searcher.gsearch(args.show_line_nb, args.show_lines)


    class Version(argparse.Action):
        '''Class used to show Synk version.'''

        def __call__(self, parser, namespace, values, option_string):

            print(f'SearchWord v{version}')
            parser.exit()




##-run
if __name__ == '__main__':
    app = Parser()
    app.parse()

