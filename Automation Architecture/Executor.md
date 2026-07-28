Executor transforms source per [[Work Order]], applying [[Smart Library]] transforms against the [[Reference Source]] oracle and using the [[Asset Converter]] for non-code artifacts.

It keeps its own memory of prior [[Flag]]s so it never re-ships a rejected fix, and sends output to [[AST_LSP]].
