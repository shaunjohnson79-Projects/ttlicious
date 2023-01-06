class ClassSettings():
    def __init__(self) -> None:

        self.columnNamesDictionary = {
            cfg.statusLabels.date: cfg.statusLabels.date,
            cfg.statusLabels.status: cfg.statusLabels.status,
            "search": cfg.statusLabels.search,
        }
        return
