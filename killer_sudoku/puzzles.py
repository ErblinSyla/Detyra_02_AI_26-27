"""Puzzle-t Killer Sudoku. layout: 9 rreshta, secili shkronjë/shifër është id-ja e kafazit të asaj qelize.
sums: shuma e secilit kafaz. Për të shtuar një puzzle nga sudoku.com: shëno kafazet me ID dhe shkruaj shumat
(shuma e të gjitha kafazeve duhet të jetë 405)."""
PUZZLES = {
    "Easy": (
        ['TULLFJKKK', 'TUPLFJhAA', 'ddPLSJNHa', 'CiBBDNNHH', 'CCBODDDII', 'GGbOQEEEI', 'gGbQQZEVV', 'WWWMXYeRc', 'ffWMXXeRR'],
        {'A': 13, 'B': 21, 'C': 11, 'D': 23, 'E': 26, 'F': 11, 'G': 16, 'H': 15, 'I': 14, 'J': 13, 'K': 14, 'L': 16,
         'M': 11, 'N': 9, 'O': 6, 'P': 9, 'Q': 14, 'R': 7, 'S': 9, 'T': 14, 'U': 4, 'V': 15, 'W': 22, 'X': 12, 'Y': 8,
         'Z': 1, 'a': 4, 'b': 9, 'c': 3, 'd': 14, 'e': 15, 'f': 12, 'g': 2, 'h': 8, 'i': 4}),
    "Hard": (
        ['RQQFFIJJJ', 'CQQFFIAAA', 'CXBKKMMHH', 'CCBKMMTHH', 'GSBNDDTHW', 'GSBNDEEEW', 'GSNNDOOOW', 'GVVVDUUUW', 'YYLLLUPPP'],
        {'A': 21, 'B': 27, 'C': 27, 'D': 25, 'E': 21, 'F': 20, 'G': 10, 'H': 22, 'I': 11, 'J': 14, 'K': 19, 'L': 16,
         'M': 12, 'N': 18, 'O': 13, 'P': 14, 'Q': 10, 'R': 5, 'S': 15, 'T': 9, 'U': 19, 'V': 15, 'W': 22, 'X': 8, 'Y': 12}),
}