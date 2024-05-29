(module
	(import "console" "log" (func (param i64)))
    (func (export "main")
		i64.const 43
		i64.const 54
		i64.add
		call 0)
)