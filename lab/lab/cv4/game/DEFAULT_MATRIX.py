from lab.cv4.game.RectState import RectState


DEFAULT_MATRIX = [
    [RectState.EMPTY, RectState.EMPTY, RectState.EMPTY, RectState.EMPTY, RectState.EMPTY],
    [RectState.EMPTY, RectState.TRAP, RectState.EMPTY, RectState.EMPTY, RectState.EMPTY],
    [RectState.EMPTY, RectState.EMPTY, RectState.EMPTY, RectState.TRAP, RectState.EMPTY],
    [RectState.EMPTY, RectState.EMPTY, RectState.EMPTY, RectState.CHEESE, RectState.EMPTY],
    [RectState.EMPTY, RectState.EMPTY, RectState.EMPTY, RectState.EMPTY, RectState.EMPTY],
]
