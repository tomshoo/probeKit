from commands import (
    run, banner, clear, show,
    doc, set, unset, use,
    help
)

Commands: dict = {
    'run': run.run,
    'banner': banner.run,
    'clear': clear.run,
    'show': show.run,
    'doc': doc.Docs,
    'set': set.Set,
    'unset': unset.unset_val,
    'use': use.use,
    'help': help.run
}